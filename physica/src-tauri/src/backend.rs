use crate::{
    corpus,
    model::{Problem, Settings},
    scheduler,
    store::{now, Result, Store},
};
use rand::SeedableRng;
use rand_chacha::ChaCha8Rng;
use rusqlite::params;
use serde_json::{json, Value};
use std::{
    collections::HashMap,
    path::{Path, PathBuf},
};

fn refresh_availability(problems: &mut [Problem], mut is_file: impl FnMut(&str) -> bool) {
    // Several problems share each source PDF. Stat each distinct path once per refresh,
    // while still detecting deleted/restored files when the screening DB is unchanged.
    let mut files = HashMap::new();
    for problem in problems {
        problem.available = problem.pdf_path.as_deref().is_some_and(|path| {
            *files
                .entry(path.to_owned())
                .or_insert_with(|| is_file(path))
        });
    }
}

#[cfg(test)]
mod startup_tests {
    use super::*;

    fn problem(id: &str, path: Option<&Path>) -> Problem {
        serde_json::from_value(json!({
            "problem_id": id, "title": "test", "competition": "test",
            "secondary_topics": [], "pdf_path": path.map(|p| p.to_string_lossy()),
            "page_start": 1, "available": true, "decision": "KEEP", "location": {}
        }))
        .unwrap()
    }

    #[test]
    fn availability_checks_shared_pdfs_once_and_detects_removal_and_restore() {
        let dir = tempfile::tempdir().unwrap();
        let present = dir.path().join("present.pdf");
        let missing = dir.path().join("missing.pdf");
        std::fs::write(&present, b"test").unwrap();
        let mut problems = vec![
            problem("1", Some(&present)),
            problem("2", Some(&present)),
            problem("3", Some(&missing)),
            problem("4", Some(&missing)),
            problem("5", None),
        ];
        let mut calls = 0;
        refresh_availability(&mut problems, |path| {
            calls += 1;
            Path::new(path).is_file()
        });
        assert_eq!(calls, 2);
        assert_eq!(
            problems.iter().map(|p| p.available).collect::<Vec<_>>(),
            [true, true, false, false, false]
        );
        std::fs::remove_file(&present).unwrap();
        std::fs::write(&missing, b"test").unwrap();
        refresh_availability(&mut problems, |path| Path::new(path).is_file());
        assert_eq!(
            problems.iter().map(|p| p.available).collect::<Vec<_>>(),
            [false, false, true, true, false]
        );
    }
}

pub struct Backend {
    pub store: Store,
    pub problems: Vec<Problem>,
    pub root: Option<PathBuf>,
    pub state_path: PathBuf,
    rng: ChaCha8Rng,
}
impl Backend {
    pub fn new(state_path: PathBuf) -> Result<Self> {
        let store = Store::open(&state_path)?;
        let mut b = Self {
            store,
            problems: vec![],
            root: None,
            state_path,
            rng: ChaCha8Rng::from_os_rng(),
        };
        let settings = b.store.settings()?;
        let configured = settings
            .corpus_root
            .map(PathBuf::from)
            .filter(|p| p.join(corpus::DB_REL).is_file());
        let detected = std::env::current_dir()
            .ok()
            .and_then(|p| {
                p.ancestors()
                    .find(|p| p.join(corpus::DB_REL).is_file())
                    .map(Path::to_path_buf)
            })
            .or_else(|| {
                std::env::current_exe().ok().and_then(|p| {
                    p.ancestors()
                        .find(|p| p.join(corpus::DB_REL).is_file())
                        .map(Path::to_path_buf)
                })
            });
        b.root = configured.or(detected);
        #[cfg(debug_assertions)]
        if b.root.is_none() {
            let p = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
            if p.join(corpus::DB_REL).is_file() {
                b.root = p.canonicalize().ok();
            }
        }
        Ok(b)
    }
    pub fn index(&mut self, force: bool) -> Result<()> {
        let Some(root) = self.root.as_ref() else {
            return Ok(());
        };
        let fp = format!(
            "{}:adapter1",
            corpus::fingerprint(&root.join(corpus::DB_REL))?
        );
        if !force && self.store.meta("source_fingerprint")?.as_deref() == Some(&fp) {
            let mut q = self
                .store
                .db
                .prepare("SELECT json FROM problem_index ORDER BY problem_id")
                .map_err(|e| e.to_string())?;
            let rows = q
                .query_map([], |r| r.get::<_, String>(0))
                .map_err(|e| e.to_string())?;
            self.problems = rows
                .map(|r| {
                    r.map_err(|e| e.to_string())
                        .and_then(|s| serde_json::from_str(&s).map_err(|e| e.to_string()))
                })
                .collect::<Result<_>>()?;
            refresh_availability(&mut self.problems, |path| Path::new(path).is_file());
            if !self.problems.is_empty() {
                return Ok(());
            }
        }
        let problems = corpus::load(root)?;
        if !problems.iter().any(|p| p.available) {
            return Err("Corpus folder contains the database but no usable source PDFs.".into());
        }
        let tx = self.store.db.transaction().map_err(|e| e.to_string())?;
        tx.execute("DELETE FROM problem_index", [])
            .map_err(|e| e.to_string())?;
        {
            let mut q = tx
                .prepare("INSERT INTO problem_index VALUES (?,?)")
                .map_err(|e| e.to_string())?;
            for p in &problems {
                q.execute(params![
                    p.problem_id,
                    serde_json::to_string(p).map_err(|e| e.to_string())?
                ])
                .map_err(|e| e.to_string())?;
            }
        }
        for (key, value) in [
            ("source_fingerprint", fp),
            ("last_indexed", now().to_string()),
        ] {
            tx.execute("INSERT INTO app_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",params![key,value]).map_err(|e|e.to_string())?;
        }
        tx.commit().map_err(|e| e.to_string())?;
        self.problems = problems;
        Ok(())
    }
    pub fn diagnostics(&self) -> Result<Value> {
        let keep: Vec<_> = self
            .problems
            .iter()
            .filter(|p| p.decision.as_deref() == Some("KEEP"))
            .collect();
        let mut formats = serde_json::Map::new();
        for f in ["Theory", "MCQ", "Experimental"] {
            formats.insert(
                f.into(),
                json!(keep
                    .iter()
                    .filter(|p| p.format.as_deref() == Some(f))
                    .count()),
            );
        }
        let topics: Vec<_> = (0..6)
            .map(|t| keep.iter().filter(|p| p.topic == Some(t)).count())
            .collect();
        Ok(
            json!({"source_db":self.root.as_ref().map(|p|p.join(corpus::DB_REL).to_string_lossy().to_string()),"state_db":self.state_path.to_string_lossy(),"total":self.problems.len(),"keep":keep.len(),"formats":formats,"topics":topics,
            "missing_pdf":self.problems.iter().filter(|p|!p.available).count(),"keep_missing_pdf":keep.iter().filter(|p|!p.available).count(),"unresolved_format":keep.iter().filter(|p|p.format.is_none()).count(),"unresolved_topic":keep.iter().filter(|p|p.topic.is_none()).count(),"solution_linked":keep.iter().filter(|p|p.solution.is_some()).count(),"aliases":keep.iter().filter(|p|p.canonical_id.is_some()).count(),"skipped":self.store.states()?.values().filter(|s|s.skipped).count(),"last_indexed":self.store.meta("last_indexed")?,"fingerprint":self.store.meta("source_fingerprint")?}),
        )
    }
    pub fn snapshot(&self) -> Result<Value> {
        Ok(
            json!({"states":self.store.states()?,"history":self.store.history()?,"active":self.store.active()?,"settings":self.store.settings()?,"diagnostics":self.diagnostics()?}),
        )
    }
    fn problem(&self, id: &str) -> Result<&Problem> {
        self.problems
            .iter()
            .find(|p| p.problem_id == id)
            .ok_or_else(|| "Problem is not in the current corpus.".into())
    }
    pub fn document(&self, id: &str, solution: bool) -> Result<Value> {
        let p = self.problem(id)?;
        let (path, start, end, note) = if solution {
            let s = p
                .solution
                .as_ref()
                .ok_or("No official solution linked for this problem.")?;
            (s.path.clone(), s.page, s.page_end, Some(s.note.clone()))
        } else {
            (
                p.pdf_path
                    .clone()
                    .ok_or("The original PDF is unavailable.")?,
                p.page_start,
                p.page_end,
                None,
            )
        };
        let actual = Path::new(&path)
            .canonicalize()
            .map_err(|e| format!("PDF unavailable: {e}"))?;
        let root = self
            .root
            .as_ref()
            .ok_or("Select a corpus folder first.")?
            .canonicalize()
            .map_err(|e| e.to_string())?;
        if !actual.starts_with(root)
            || !actual
                .extension()
                .is_some_and(|s| s.eq_ignore_ascii_case("pdf"))
        {
            return Err("PDF path is outside the corpus.".into());
        }
        let fp = corpus::fingerprint(&actual)?;
        let anchor = self
            .store
            .db
            .query_row(
                "SELECT page,y_ratio FROM pdf_anchor_cache WHERE problem_id=? AND fingerprint=?",
                params![id, fp],
                |r| Ok(json!({"page":r.get::<_,u32>(0)?,"y_ratio":r.get::<_,f64>(1)?})),
            )
            .ok();
        Ok(
            json!({"path":actual.to_string_lossy(),"page_start":start,"page_end":end,"fingerprint":fp,"anchor":if solution {None}else{anchor},"note":note}),
        )
    }
    pub fn dispatch(&mut self, command: &str, payload: Value) -> Result<Value> {
        let id = payload
            .get("problem_id")
            .and_then(Value::as_str)
            .unwrap_or("");
        match command {
            "bootstrap" => {
                self.index(false)?;
                let mut data = self.snapshot()?;
                data["problems"] = json!(self.problems);
                data["corpus_root"] = json!(self.root.as_ref().map(|p| p.to_string_lossy()));
                Ok(data)
            }
            "snapshot" => self.snapshot(),
            "refresh" => {
                self.index(true)?;
                self.dispatch("bootstrap", json!({}))
            }
            "draw" => {
                let settings = self.store.settings()?;
                let p = scheduler::draw(&self.problems, &self.store.states()?, &self.store.recent()?, &settings, &mut self.rng)
                    .ok_or_else(|| match scheduler::format_lock(&settings.mode) {
                        Some(format) => format!("No eligible {format} problems. Restore skipped items or disable Exclude solved problems. Choose another mode to draw a different format."),
                        None => "No eligible problems. Adjust filters, weights, or restore skipped items. Unresolved formats are available in Library.".into(),
                    })?;
                Ok(json!(p))
            }
            "open" => {
                if !self.problem(id)?.available {
                    return Err("The original PDF is unavailable.".into());
                }
                Ok(json!(self.store.open_attempt(id)?))
            }
            "checkpoint" => {
                self.store.checkpoint(
                    payload["attempt_id"].as_i64().ok_or("Missing attempt")?,
                    payload["elapsed"].as_u64().ok_or("Missing elapsed time")?,
                )?;
                Ok(json!(true))
            }
            "outcome" => Ok(json!(self.store.outcome(
                payload["attempt_id"].as_i64().ok_or("Missing attempt")?,
                payload["action"].as_str().ok_or("Missing action")?,
                payload["elapsed"].as_u64().ok_or("Missing elapsed time")?
            )?)),
            "restore" => {
                self.store.restore(id)?;
                self.snapshot()
            }
            "settings" => {
                let mut s: Settings = serde_json::from_value(payload).map_err(|e| e.to_string())?;
                s.corpus_root = self.root.as_ref().map(|p| p.to_string_lossy().into());
                self.store.save_settings(&s)?;
                self.snapshot()
            }
            "document" => self.document(id, payload["solution"].as_bool().unwrap_or(false)),
            "anchor" => {
                let d = self.document(id, false)?;
                let fp = payload["fingerprint"]
                    .as_str()
                    .ok_or("Missing fingerprint")?;
                if d["fingerprint"].as_str() != Some(fp) {
                    return Err("PDF changed; reopen it before caching an anchor.".into());
                }
                let page = payload["page"]
                    .as_u64()
                    .filter(|p| *p > 0)
                    .ok_or("Invalid page")?;
                let y = payload["y_ratio"]
                    .as_f64()
                    .filter(|y| y.is_finite() && *y >= 0. && *y <= 1.)
                    .ok_or("Invalid anchor")?;
                self.store
                    .db
                    .execute(
                        "DELETE FROM pdf_anchor_cache WHERE problem_id=? AND fingerprint<>?",
                        params![id, fp],
                    )
                    .map_err(|e| e.to_string())?;
                self.store.db.execute("INSERT INTO pdf_anchor_cache VALUES (?,?,?,?) ON CONFLICT(problem_id,fingerprint) DO UPDATE SET page=excluded.page,y_ratio=excluded.y_ratio",params![id,fp,page,y]).map_err(|e|e.to_string())?;
                Ok(json!(true))
            }
            _ => Err("Unknown Physica command".into()),
        }
    }
    pub fn choose_root(&mut self, path: PathBuf) -> Result<Value> {
        let root = path.canonicalize().map_err(|e| e.to_string())?;
        let ps = corpus::load(&root)?;
        if !ps
            .iter()
            .any(|p| p.available && p.decision.as_deref() == Some("KEEP"))
        {
            return Err("Select the repository folder containing screening.sqlite and olimpicos_physics_corpus.".into());
        }
        self.root = Some(root);
        let mut s = self.store.settings()?;
        s.corpus_root = self.root.as_ref().map(|p| p.to_string_lossy().into());
        self.store.save_settings(&s)?;
        self.index(true)?;
        self.dispatch("bootstrap", json!({}))
    }
}

use crate::model::{Attempt, ProblemState, Settings};
use rusqlite::{params, Connection, OptionalExtension};
use std::{
    collections::HashMap,
    path::Path,
    time::{SystemTime, UNIX_EPOCH},
};
pub fn now() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs() as i64
}
pub type Result<T> = std::result::Result<T, String>;
pub struct Store {
    pub db: Connection,
}
impl Store {
    pub fn open(path: &Path) -> Result<Self> {
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
        }
        let mut db = Connection::open(path).map_err(|e| e.to_string())?;
        db.busy_timeout(std::time::Duration::from_secs(5))
            .map_err(|e| e.to_string())?;
        db.execute_batch("PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL;")
            .map_err(|e| e.to_string())?;
        let version: i32 = db
            .query_row("PRAGMA user_version", [], |r| r.get(0))
            .map_err(|e| e.to_string())?;
        if version > 1 {
            return Err("This state database needs a newer Physica version.".into());
        }
        if version == 0 {
            let tx = db.transaction().map_err(|e| e.to_string())?;
            tx.execute_batch("CREATE TABLE app_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
              CREATE TABLE problem_index(problem_id TEXT PRIMARY KEY,json TEXT NOT NULL);
              CREATE TABLE problem_state(problem_id TEXT PRIMARY KEY,opened INTEGER NOT NULL DEFAULT 0,solved INTEGER NOT NULL DEFAULT 0,failed INTEGER NOT NULL DEFAULT 0,skipped INTEGER NOT NULL DEFAULT 0,last_opened INTEGER,last_result TEXT);
              CREATE TABLE attempts(id INTEGER PRIMARY KEY,problem_id TEXT NOT NULL,started_at INTEGER NOT NULL,finished_at INTEGER,result TEXT,elapsed INTEGER NOT NULL DEFAULT 0,answer_viewed INTEGER NOT NULL DEFAULT 0);
              CREATE INDEX attempt_problem ON attempts(problem_id,started_at);
              CREATE INDEX attempt_finished ON attempts(finished_at DESC);
              CREATE INDEX state_skip ON problem_state(skipped);
              CREATE TABLE settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
              CREATE TABLE recent_draws(id INTEGER PRIMARY KEY,problem_id TEXT NOT NULL,opened_at INTEGER NOT NULL);
              CREATE TABLE pdf_anchor_cache(problem_id TEXT NOT NULL,fingerprint TEXT NOT NULL,page INTEGER NOT NULL,y_ratio REAL NOT NULL,PRIMARY KEY(problem_id,fingerprint));
              PRAGMA user_version=1;").map_err(|e|e.to_string())?;
            tx.commit().map_err(|e| e.to_string())?;
        }
        Ok(Self { db })
    }
    pub fn meta(&self, key: &str) -> Result<Option<String>> {
        self.db
            .query_row("SELECT value FROM app_meta WHERE key=?", [key], |r| {
                r.get(0)
            })
            .optional()
            .map_err(|e| e.to_string())
    }
    pub fn set_meta(&self, key: &str, value: &str) -> Result<()> {
        self.db.execute("INSERT INTO app_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",params![key,value]).map_err(|e|e.to_string())?;
        Ok(())
    }
    pub fn settings(&self) -> Result<Settings> {
        let json: Option<String> = self
            .db
            .query_row("SELECT value FROM settings WHERE key='practice'", [], |r| {
                r.get(0)
            })
            .optional()
            .map_err(|e| e.to_string())?;
        match json {
            Some(s) => serde_json::from_str(&s).map_err(|e| e.to_string()),
            None => Ok(Settings::default()),
        }
    }
    pub fn save_settings(&self, settings: &Settings) -> Result<()> {
        if !matches!(
            settings.mode.as_str(),
            "Balanced" | "Theory" | "MCQ" | "Experimental" | "Topic Focus" | "Unseen"
        ) || settings.topics.iter().any(|t| *t > 5)
            || settings
                .weights
                .iter()
                .any(|w| !w.is_finite() || *w < 0. || *w > 100.)
            || settings.weights.iter().sum::<f64>() <= 0.
        {
            return Err("Choose a valid mode and at least one positive format weight.".into());
        }
        let value = serde_json::to_string(settings).map_err(|e| e.to_string())?;
        self.db.execute("INSERT INTO settings VALUES ('practice',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",[value]).map_err(|e|e.to_string())?;
        Ok(())
    }
    pub fn states(&self) -> Result<HashMap<String, ProblemState>> {
        let mut q=self.db.prepare("SELECT problem_id,opened,solved,failed,skipped,last_opened,last_result FROM problem_state").map_err(|e|e.to_string())?;
        let result = q
            .query_map([], |r| {
                Ok(ProblemState {
                    problem_id: r.get(0)?,
                    opened: r.get(1)?,
                    solved: r.get(2)?,
                    failed: r.get(3)?,
                    skipped: r.get(4)?,
                    last_opened: r.get(5)?,
                    last_result: r.get(6)?,
                })
            })
            .map_err(|e| e.to_string())?
            .map(|r| {
                r.map(|s| (s.problem_id.clone(), s))
                    .map_err(|e| e.to_string())
            })
            .collect();
        result
    }
    pub fn history(&self) -> Result<Vec<Attempt>> {
        let mut q=self.db.prepare("SELECT id,problem_id,started_at,finished_at,result,elapsed,answer_viewed FROM attempts ORDER BY id DESC LIMIT 2000").map_err(|e|e.to_string())?;
        let result = q
            .query_map([], |r| {
                Ok(Attempt {
                    id: r.get(0)?,
                    problem_id: r.get(1)?,
                    started_at: r.get(2)?,
                    finished_at: r.get(3)?,
                    result: r.get(4)?,
                    elapsed: r.get(5)?,
                    answer_viewed: r.get(6)?,
                })
            })
            .map_err(|e| e.to_string())?
            .map(|r| r.map_err(|e| e.to_string()))
            .collect();
        result
    }
    pub fn attempt(&self, id: i64) -> Result<Attempt> {
        self.db.query_row("SELECT id,problem_id,started_at,finished_at,result,elapsed,answer_viewed FROM attempts WHERE id=?",[id],|r|Ok(Attempt {id:r.get(0)?,problem_id:r.get(1)?,started_at:r.get(2)?,finished_at:r.get(3)?,result:r.get(4)?,elapsed:r.get(5)?,answer_viewed:r.get(6)?})).map_err(|e|e.to_string())
    }
    pub fn active(&self) -> Result<Option<Attempt>> {
        if let Some(id) = self.meta("active_attempt")? {
            if let Ok(a) = self.attempt(id.parse().unwrap_or(0)) {
                if a.finished_at.is_none() {
                    return Ok(Some(a));
                }
            }
        }
        Ok(None)
    }
    pub fn open_attempt(&mut self, id: &str) -> Result<Attempt> {
        if let Some(a) = self.active()? {
            if a.problem_id == id {
                return Ok(a);
            }
        }
        let t = now();
        let tx = self.db.transaction().map_err(|e| e.to_string())?;
        // An abandoned attempt stays in history, with no fabricated outcome.
        tx.execute(
            "UPDATE attempts SET finished_at=? WHERE finished_at IS NULL",
            [t],
        )
        .map_err(|e| e.to_string())?;
        tx.execute(
            "INSERT INTO attempts(problem_id,started_at) VALUES (?,?)",
            params![id, t],
        )
        .map_err(|e| e.to_string())?;
        let attempt_id = tx.last_insert_rowid();
        tx.execute("INSERT INTO app_meta VALUES ('active_attempt',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",[attempt_id.to_string()]).map_err(|e|e.to_string())?;
        tx.execute("INSERT INTO problem_state(problem_id,opened,last_opened) VALUES (?,1,?) ON CONFLICT(problem_id) DO UPDATE SET opened=opened+1,last_opened=excluded.last_opened",params![id,t]).map_err(|e|e.to_string())?;
        tx.execute(
            "INSERT INTO recent_draws(problem_id,opened_at) VALUES (?,?)",
            params![id, t],
        )
        .map_err(|e| e.to_string())?;
        tx.execute("DELETE FROM recent_draws WHERE id NOT IN (SELECT id FROM recent_draws ORDER BY id DESC LIMIT 100)",[]).map_err(|e|e.to_string())?;
        tx.commit().map_err(|e| e.to_string())?;
        self.attempt(attempt_id)
    }
    pub fn recent(&self) -> Result<Vec<String>> {
        let mut q = self
            .db
            .prepare("SELECT problem_id FROM recent_draws ORDER BY id DESC LIMIT 100")
            .map_err(|e| e.to_string())?;
        let result = q
            .query_map([], |r| r.get::<_, String>(0))
            .map_err(|e| e.to_string())?
            .map(|r| r.map_err(|e| e.to_string()))
            .collect();
        result
    }
    pub fn checkpoint(&self, id: i64, elapsed: u64) -> Result<()> {
        self.db
            .execute(
                "UPDATE attempts SET elapsed=? WHERE id=? AND finished_at IS NULL",
                params![elapsed.min(31_536_000), id],
            )
            .map_err(|e| e.to_string())?;
        Ok(())
    }
    pub fn outcome(&mut self, id: i64, action: &str, elapsed: u64) -> Result<Attempt> {
        if !matches!(action, "Answer" | "Solved" | "Failed" | "SKIP") {
            return Err("Invalid outcome".into());
        }
        let a = self.attempt(id)?;
        if a.finished_at.is_some() {
            return Err("This attempt is already complete.".into());
        }
        let tx = self.db.transaction().map_err(|e| e.to_string())?;
        if action == "Answer" {
            tx.execute(
                "UPDATE attempts SET answer_viewed=1,elapsed=? WHERE id=?",
                params![elapsed, id],
            )
            .map_err(|e| e.to_string())?;
        } else {
            tx.execute(
                "UPDATE attempts SET result=?,elapsed=?,finished_at=? WHERE id=?",
                params![action, elapsed, now(), id],
            )
            .map_err(|e| e.to_string())?;
            tx.execute("UPDATE problem_state SET last_result=?,solved=solved+?,failed=failed+?,skipped=CASE WHEN ?='SKIP' THEN 1 ELSE skipped END WHERE problem_id=?",params![action,(action=="Solved") as i32,(action=="Failed") as i32,action,a.problem_id]).map_err(|e|e.to_string())?;
            tx.execute("DELETE FROM app_meta WHERE key='active_attempt'", [])
                .map_err(|e| e.to_string())?;
        }
        tx.commit().map_err(|e| e.to_string())?;
        self.attempt(id)
    }
    pub fn restore(&mut self, id: &str) -> Result<()> {
        let tx = self.db.transaction().map_err(|e| e.to_string())?;
        tx.execute(
            "UPDATE problem_state SET skipped=0 WHERE problem_id=?",
            [id],
        )
        .map_err(|e| e.to_string())?;
        tx.commit().map_err(|e| e.to_string())?;
        Ok(())
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn practice_modes_persist_without_schema_change() {
        let t = tempfile::tempdir().unwrap();
        let path = t.path().join("state.sqlite");
        for mode in [
            "Balanced",
            "Theory",
            "MCQ",
            "Experimental",
            "Topic Focus",
            "Unseen",
        ] {
            let s = Store::open(&path).unwrap();
            let settings = Settings {
                mode: mode.into(),
                ..Settings::default()
            };
            s.save_settings(&settings).unwrap();
            drop(s);
            let s = Store::open(&path).unwrap();
            assert_eq!(s.settings().unwrap().mode, mode);
            assert_eq!(s.settings().unwrap().weights, [2., 1., 1.]);
            assert_eq!(
                s.db.query_row("PRAGMA user_version", [], |r| r.get::<_, i32>(0))
                    .unwrap(),
                1
            );
        }
    }
    #[test]
    fn migration_outcomes_restore_and_restart() {
        let t = tempfile::tempdir().unwrap();
        let p = t.path().join("state.sqlite");
        let mut s = Store::open(&p).unwrap();
        let a = s.open_attempt("p").unwrap();
        s.checkpoint(a.id, 74).unwrap();
        s.outcome(a.id, "Answer", 75).unwrap();
        assert!(s.active().unwrap().unwrap().answer_viewed);
        assert_eq!(s.states().unwrap()["p"].failed, 0);
        s.outcome(a.id, "Solved", 90).unwrap();
        let a = s.open_attempt("p").unwrap();
        s.outcome(a.id, "Failed", 30).unwrap();
        let a = s.open_attempt("p").unwrap();
        s.outcome(a.id, "SKIP", 12).unwrap();
        drop(s);
        let mut s = Store::open(&p).unwrap();
        assert!(s.states().unwrap()["p"].skipped);
        assert_eq!(s.states().unwrap()["p"].solved, 1);
        assert_eq!(s.states().unwrap()["p"].failed, 1);
        s.restore("p").unwrap();
        assert!(!s.states().unwrap()["p"].skipped);
        assert_eq!(s.history().unwrap().len(), 3);
        assert_eq!(s.history().unwrap()[2].elapsed, 90);
        let a = s.open_attempt("p").unwrap();
        s.checkpoint(a.id, 43).unwrap();
        drop(s);
        let s = Store::open(&p).unwrap();
        assert_eq!(s.active().unwrap().unwrap().elapsed, 43);
        assert_eq!(
            s.db.query_row("PRAGMA user_version", [], |r| r.get::<_, i32>(0))
                .unwrap(),
            1
        );
    }
}

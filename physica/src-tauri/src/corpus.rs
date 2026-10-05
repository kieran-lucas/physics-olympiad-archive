//! The only module aware of the screening schema. No source writes, OCR or topic inference.
use crate::model::{Problem, Solution};
use rusqlite::{Connection, OpenFlags};
use std::{
    collections::HashMap,
    path::{Path, PathBuf},
};

pub const DB_REL: &str = "syllabus_screening/spho_2026/screening.sqlite";
pub fn source_connection(root: &Path) -> Result<Connection, String> {
    let c = Connection::open_with_flags(root.join(DB_REL), OpenFlags::SQLITE_OPEN_READ_ONLY)
        .map_err(|e| e.to_string())?;
    c.execute_batch("PRAGMA query_only=ON;")
        .map_err(|e| e.to_string())?;
    Ok(c)
}
pub fn fingerprint(path: &Path) -> Result<String, String> {
    let m = path.metadata().map_err(|e| e.to_string())?;
    Ok(format!(
        "{}:{}:{}",
        path.display(),
        m.len(),
        m.modified()
            .map_err(|e| e.to_string())?
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos()
    ))
}
pub fn resolve(root: &Path, relative: &str) -> Option<PathBuf> {
    // Historical paths are relative to the acquisition corpus. Never allow traversal or paths outside the selected root.
    let base = root.canonicalize().ok()?;
    let candidates = [
        root.join("olimpicos_physics_corpus").join(relative),
        root.join(relative),
    ];
    candidates
        .into_iter()
        .filter_map(|p| p.canonicalize().ok())
        .find(|p| p.starts_with(&base) && p.is_file())
}
pub fn topic_blocks(raw: &str) -> Vec<usize> {
    let mut result = vec![];
    for token in raw.split([';', ',', '|']) {
        let roman = token.trim().split('_').next().unwrap_or("");
        let block = match roman {
            "I" | "II" => Some(0),
            "III" | "IV" | "V" => Some(1),
            "VI" => Some(2),
            "VII" | "VIII" => Some(3),
            "IX" | "X" => Some(4),
            "XI" | "XII" => Some(5),
            _ => None,
        };
        if let Some(b) = block {
            if !result.contains(&b) {
                result.push(b);
            }
        }
    }
    result
}
/// Explicit format first. Data-analysis is experimental; numerical/short-answer are theory.
/// F=ma is an MCQ paper (including mixed records). FYKOS team contests and OPhO Open use written/numerical problems.
/// Ambiguous general national 'Problems' sections and mixed records remain unresolved.
pub fn format_mapping(raw: &str, source_type: &str, slug: &str, section: &str) -> Option<String> {
    fn explicit(v: &str) -> Option<&'static str> {
        match v.to_lowercase().as_str() {
            "theory" | "numerical" | "short_answer" => Some("Theory"),
            "mcq" | "multiple_choice" => Some("MCQ"),
            "experimental" | "data_analysis" => Some("Experimental"),
            _ => None,
        }
    }
    if let Some(v) = explicit(raw) {
        return Some(v.into());
    }
    let s = section.to_lowercase();
    if slug == "usapho" && (s.contains("f=ma") || s.contains("quarterfinal")) {
        return Some("MCQ".into());
    }
    if let Some(v) = explicit(source_type) {
        return Some(v.into());
    }
    if s.contains("experimental") || s.contains("data analysis") || s == "experiencia" {
        return Some("Experimental".into());
    }
    if s.contains("theory") || s == "short problems" || s == "long problems" {
        return Some("Theory".into());
    }
    if matches!(slug, "fyziklani" | "physicsbrawl") || (slug == "opho" && s.starts_with("open")) {
        return Some("Theory".into());
    }
    None
}
pub fn load(root: &Path) -> Result<Vec<Problem>, String> {
    let c = source_connection(root)?;
    c.execute_batch("BEGIN DEFERRED;")
        .map_err(|e| e.to_string())?;
    let mut solutions: HashMap<String, Vec<Solution>> = HashMap::new();
    let mut q=c.prepare("SELECT uf.screening_unit_id,f.local_path,uf.file_id,uf.document_id,uf.role,COALESCE(d.document_scope,'') FROM unit_files uf JOIN source_files f ON f.id=uf.file_id LEFT JOIN source_documents d ON d.id=uf.document_id WHERE uf.role IN ('solution','marking_scheme','combined') ORDER BY CASE uf.role WHEN 'solution' THEN 0 WHEN 'marking_scheme' THEN 1 ELSE 2 END,uf.document_id").map_err(|e|e.to_string())?;
    let rows = q
        .query_map([], |r| {
            Ok((
                r.get::<_, String>(0)?,
                r.get::<_, String>(1)?,
                r.get::<_, i64>(2)?,
                r.get::<_, i64>(3)?,
                r.get::<_, String>(4)?,
                r.get::<_, String>(5)?,
            ))
        })
        .map_err(|e| e.to_string())?;
    for row in rows {
        let (id, relative, file_id, document_id, role, scope) = row.map_err(|e| e.to_string())?;
        if let Some(path) = resolve(root, &relative) {
            if path
                .extension()
                .is_some_and(|e| e.eq_ignore_ascii_case("pdf"))
            {
                let note = if role == "combined" {
                    "Combined statement/solution document; exact solution page is not recorded."
                } else if scope != "problem" {
                    "Linked official document may cover the whole paper; exact solution page is not recorded."
                } else {
                    "Linked official solution; exact page is not recorded."
                };
                solutions.entry(id).or_default().push(Solution {
                    path: path.to_string_lossy().into(),
                    file_id,
                    document_id,
                    role,
                    page: 1,
                    page_end: None,
                    note: note.into(),
                });
            }
        }
    }
    let mut q=c.prepare("SELECT u.screening_unit_id,u.problem_title,u.problem_number,u.competition,u.year,u.round_or_section,u.format,u.primary_spho_domains,COALESCE(u.source_file,f.local_path),u.page_start,u.page_end,u.source_file_id,u.source_problem_id,u.decision,u.location_json,e.canonical_unit_id,sp.problem_type,u.competition_slug,u.source_quality_notes,sdoc.document_id FROM units u LEFT JOIN source_files f ON f.id=u.source_file_id LEFT JOIN unit_equivalences e ON e.alias_unit_id=u.screening_unit_id LEFT JOIN source_problems sp ON sp.id=u.source_problem_id LEFT JOIN (SELECT screening_unit_id,file_id,MIN(document_id) document_id FROM unit_files WHERE role IN ('problem','combined') GROUP BY screening_unit_id,file_id) sdoc ON sdoc.screening_unit_id=u.screening_unit_id AND sdoc.file_id=u.source_file_id ORDER BY u.screening_unit_id").map_err(|e|e.to_string())?;
    let rows = q
        .query_map([], |r| {
            let id: String = r.get(0)?;
            let label: Option<String> = r.get(2)?;
            let title: Option<String> = r.get(1)?;
            let section: Option<String> = r.get(5)?;
            let domains: Option<String> = r.get(7)?;
            let blocks = topic_blocks(domains.as_deref().unwrap_or(""));
            let relative: Option<String> = r.get(8)?;
            let path = relative.as_deref().and_then(|p| resolve(root, p));
            let location: Option<String> = r.get(14)?;
            let location = serde_json::from_str(location.as_deref().unwrap_or("{}"))
                .unwrap_or(serde_json::json!({}));
            let raw: Option<String> = r.get(6)?;
            let source_type: Option<String> = r.get(16)?;
            let slug: Option<String> = r.get(17)?;
            let solution = solutions.get(&id).and_then(|ss| ss.first()).cloned();
            Ok(Problem {
                problem_id: id,
                title: title
                    .filter(|s| !s.trim().is_empty())
                    .unwrap_or_else(|| format!("Problem {}", label.as_deref().unwrap_or("—"))),
                label,
                competition: r
                    .get::<_, Option<String>>(3)?
                    .unwrap_or_else(|| "Unknown source".into()),
                year: r.get(4)?,
                section: section.clone(),
                format: format_mapping(
                    raw.as_deref().unwrap_or(""),
                    source_type.as_deref().unwrap_or(""),
                    slug.as_deref().unwrap_or(""),
                    section.as_deref().unwrap_or(""),
                ),
                topic: blocks.first().copied(),
                secondary_topics: blocks.into_iter().skip(1).collect(),
                available: path.is_some(),
                pdf_path: path.map(|p| p.to_string_lossy().into()),
                page_start: r.get::<_, Option<u32>>(9)?.unwrap_or(1).max(1),
                page_end: r.get(10)?,
                file_id: r.get(11)?,
                source_problem_id: r.get(12)?,
                decision: r.get(13)?,
                location,
                canonical_id: r.get(15)?,
                solution,
                source_quality_notes: r.get(18)?,
                document_id: r.get(19)?,
            })
        })
        .map_err(|e| e.to_string())?;
    rows.collect::<Result<Vec<_>, _>>()
        .map_err(|e| e.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn six_blocks_and_primary_order() {
        assert_eq!(
            topic_blocks(
                "XI_quantum_light;I_force_motion;II_oscillations_waves;XII_atomic_nuclear"
            ),
            vec![5, 0]
        );
        assert_eq!(topic_blocks("III_ideal_gas;IV_thermodynamics;V_real_gas;VI_electric_field;VII_magnetic_field;VIII_induction;IX_em;X_optics"),vec![1,2,3,4]);
        assert!(topic_blocks("").is_empty());
    }
    #[test]
    fn deterministic_formats() {
        assert_eq!(
            format_mapping("multiple_choice", "", "", ""),
            Some("MCQ".into())
        );
        assert_eq!(
            format_mapping("unknown", "Theory", "ipho", ""),
            Some("Theory".into())
        );
        assert_eq!(
            format_mapping("unknown", "", "ipho", "Experimental"),
            Some("Experimental".into())
        );
        assert_eq!(format_mapping("unknown", "", "unknown", "Problems"), None);
        assert_eq!(
            format_mapping("data_analysis", "", "", ""),
            Some("Experimental".into())
        );
    }
    #[test]
    fn missing_and_traversal() {
        let t = tempfile::tempdir().unwrap();
        assert!(resolve(t.path(), "absent.pdf").is_none());
        assert!(resolve(t.path(), "../../Cargo.toml").is_none());
    }
    #[test]
    fn real_corpus_readonly_and_boundaries() {
        let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        if !root.join(DB_REL).exists() {
            return;
        }
        let c = source_connection(&root).unwrap();
        assert!(c
            .execute("CREATE TABLE physica_must_never_exist(x)", [])
            .is_err());
        let raw: i64 = c
            .query_row(
                "SELECT count(*) FROM units WHERE decision='KEEP'",
                [],
                |r| r.get(0),
            )
            .unwrap();
        let ps = load(&root).unwrap();
        assert_eq!(
            ps.iter()
                .filter(|p| p.decision.as_deref() == Some("KEEP"))
                .count(),
            raw as usize
        );
        let p = ps.iter().find(|p| p.problem_id == "raw::5").unwrap();
        assert_eq!(p.page_start, 1);
        assert_eq!(p.page_end, Some(6));
        assert!(p.available);
        assert!(p
            .pdf_path
            .as_ref()
            .unwrap()
            .ends_with("IPhO_2025_Q1__866d34e6f1c5469c.pdf"));
        assert!(p.solution.is_some());
    }
}

use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Problem {
    pub problem_id: String,
    pub title: String,
    pub label: Option<String>,
    pub competition: String,
    pub year: Option<String>,
    pub section: Option<String>,
    pub format: Option<String>,
    pub topic: Option<usize>,
    pub secondary_topics: Vec<usize>,
    pub pdf_path: Option<String>,
    pub page_start: u32,
    pub page_end: Option<u32>,
    pub file_id: Option<i64>,
    pub document_id: Option<i64>,
    pub source_problem_id: Option<i64>,
    pub solution: Option<Solution>,
    pub available: bool,
    pub canonical_id: Option<String>,
    pub decision: Option<String>,
    pub location: serde_json::Value,
    pub source_quality_notes: Option<String>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Solution {
    pub path: String,
    pub file_id: i64,
    pub document_id: i64,
    pub role: String,
    pub page: u32,
    pub page_end: Option<u32>,
    pub note: String,
}
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct ProblemState {
    pub problem_id: String,
    pub opened: u32,
    pub solved: u32,
    pub failed: u32,
    pub skipped: bool,
    pub last_opened: Option<i64>,
    pub last_result: Option<String>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Attempt {
    pub id: i64,
    pub problem_id: String,
    pub started_at: i64,
    pub finished_at: Option<i64>,
    pub result: Option<String>,
    pub elapsed: u64,
    pub answer_viewed: bool,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(default)]
pub struct Settings {
    pub mode: String,
    pub weights: [f64; 3],
    pub topics: Vec<usize>,
    pub exclude_solved: bool,
    pub corpus_root: Option<String>,
}
impl Default for Settings {
    fn default() -> Self {
        Self {
            mode: "Balanced".into(),
            weights: [2., 1., 1.],
            topics: vec![],
            exclude_solved: false,
            corpus_root: None,
        }
    }
}

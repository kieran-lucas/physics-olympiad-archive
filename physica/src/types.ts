export const TOPICS = ['Mechanics & Mechanical Waves', 'Thermal & Statistical Physics', 'Electrostatics', 'Magnetism & Electromagnetic Induction', 'Electromagnetic Waves & Wave Optics', 'Quantum, Atomic & Nuclear Physics'];
export const FORMATS = ['Theory', 'MCQ', 'Experimental'];
export type Problem = {
  problem_id: string; title: string; label: string | null; competition: string; year: string | null; section: string | null;
  format: string | null; topic: number | null; secondary_topics: number[]; pdf_path: string | null; page_start: number; page_end: number | null;
  file_id: number | null; document_id: number | null; source_problem_id: number | null; solution: { path: string; file_id: number; document_id: number; role: string; page: number; page_end: number | null; note: string } | null;
  available: boolean; canonical_id: string | null; decision: string | null; location: Record<string, unknown>; source_quality_notes: string | null;
};
export type ProblemState = { problem_id: string; opened: number; solved: number; failed: number; skipped: boolean; last_opened: number | null; last_result: string | null };
export type Attempt = { id: number; problem_id: string; started_at: number; finished_at: number | null; result: string | null; elapsed: number; answer_viewed: boolean };
export type Settings = { mode: string; weights: [number, number, number]; topics: number[]; exclude_solved: boolean; corpus_root: string | null };
export type Diagnostics = { source_db: string | null; state_db: string; total: number; keep: number; formats: Record<string, number>; topics: number[]; missing_pdf: number; keep_missing_pdf: number; unresolved_format: number; unresolved_topic: number; solution_linked: number; aliases: number; skipped: number; last_indexed: string | null; fingerprint: string | null };
export type Snapshot = { states: Record<string, ProblemState>; history: Attempt[]; active: Attempt | null; settings: Settings; diagnostics: Diagnostics };
export type Bootstrap = Snapshot & { problems: Problem[]; corpus_root: string | null };
export type DocumentInfo = { path: string; page_start: number; page_end: number | null; fingerprint: string; anchor: { page: number; y_ratio: number } | null; note: string | null };
export const source = (p: Problem) => [p.competition, p.year, p.section].filter(Boolean).join(' · ');
export const time = (seconds: number) => [Math.floor(seconds / 3600), Math.floor(seconds / 60) % 60, Math.floor(seconds) % 60].map(x => String(x).padStart(2, '0')).join(':');

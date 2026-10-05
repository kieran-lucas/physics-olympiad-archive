# FAST SCOPE PASS state

User instruction of 2026-10-04 overrides the earlier forensic workflow. Screening.sqlite is authoritative; never replay completed work.

8568 registered units; 8558 decisions ({'BORDERLINE': 92, 'KEEP': 8019, 'REJECT': 447}); 0 workable pending and 10 explicit unavailable sources. 0 physical-paper audits and 0 required focused reviews remain.

Fast scope classification and complete physical-paper inventory audit are finished for available sources. No active content, boundary or focused-review queue remains. Keep source-unavailable records explicit in remaining.csv; do not guess decisions or replay committed batches. Archival enrichment and documented source-PDF structure issues remain separate deferred work. See final_checkpoint.json.

Use actual statement text first, renders only when necessary, solutions only for consequential prerequisite ambiguity. Existing rubric and whole-problem rule remain unchanged.

Materialization: current KEEP selection materialized; archival validation status recorded separately. Latest strict archival validation issues: ['PDF repair required 2680', 'PDF repair required 2682', 'PDF repair required 2683', 'PDF repair required 2686', 'PDF repair required 2688']. The strict assertion remains enabled; do not claim the full archival phase is validated while issues remain.

Lightweight checkpoint: python syllabus_screening/spho_2026/_scripts/fast_scope.py checkpoint
Major checkpoint: existing checkpoint.py for materialization/full validation, then fast_scope.py checkpoint to restore fast-mode cursor. Deep archival validation timestamp is recorded separately. Remaining.csv retains explicit unavailable sources.

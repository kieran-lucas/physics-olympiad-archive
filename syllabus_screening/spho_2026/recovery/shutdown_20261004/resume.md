# Resume the incomplete SPhO content screening

Canonical state: `screening.sqlite`. Original 205 decisions are preserved and
verified against their saved review records. Do not restart, regenerate the raw
baseline, re-extract all PDFs, re-expand containers, or rescreen reviewed units.

Current checkpoint (2026-10-04):

- 8,472 registered units: 6,159 direct + 2,313 derived.
- Inventory is PROVISIONAL: 1,140 complete physical-paper boundary audits
  remain. 50 independently printed tasks omitted from raw logical rows have
  been discovered inside indexed shared papers and added without raw changes.
- All 233 whole-paper containers expanded; the 222 pending at resume are resolved.
- 807 units have actual-content decisions: 780 KEEP, 8 BORDERLINE,
  19 REJECT. One additional source row has an explicit withdrawal notice.
- Exactly 7,664 units await content review; 1 unavailable-source residual.
- Zero pending focused reviews; zero low-confidence decisions.
- 780 selected KEEP units, 369 unique files, all verified hardlinks.
- 2,984 PDF extraction caches and inspected page renders remain available.

`remaining.csv` is the exact residual queue for currently registered work. Its
`stage=paper_boundary_audit` rows also identify files that can contain additional
unregistered questions. `remaining_paper_boundaries.csv` gives the same file queue
separately. Filter `stage=content_review` for
workable pending content; `stage=source_unavailable` is OPhO 2025 Open Q24,
explicitly removed in the paper. Do not invent a scope decision for it.

Use the fixed `scope_calibration.md` rubric. Process each unique statement file
once from its cache, inspect figures/scans when needed, refine inclusive page
locations, and decide every printed top-level question. Keep internal subparts
together. MCQ, numerical and experimental material are first-class.

One careful content inspection finishes clear high-confidence KEEP/REJECT.
Second review applies to BORDERLINE, medium/low confidence, suspicious supplied
models and random QC samples. Record actual evidence, not title/tag guesses.
Use new explicit JSON batches with `save_batch.py` or `workflow.py decisions`.
Do not rerun old record_*.py batches: they are historical acquisition/review
evidence, not automatic classifiers. `record_second_pass.py` is tied to the
historical 205 and must not be rerun unchanged.

Whole-paper locations may conservatively share a page; `location_json` records
translation ranges and session distinctions. Taiwan camp container 4002 contains
five exams and 15 units, including two experiments. Its repeated numbers are
separated by source session and deterministic IDs. Do not collapse them.

After each substantive batch:

```powershell
python syllabus_screening/spho_2026/_scripts/workflow.py export
python syllabus_screening/spho_2026/_scripts/workflow.py materialize
python syllabus_screening/spho_2026/_scripts/validate_outputs.py
python syllabus_screening/spho_2026/_scripts/workflow.py check_raw
python syllabus_screening/spho_2026/_scripts/update_resume_checkpoint.py
```

Materialization is incremental and now prunes obsolete selection membership if
a focused audit changes a new decision. It preserves all still-used shared files;
raw files must never be renamed, deleted or written. All 3,312 raw snapshot hashes
matched at this checkpoint. Never call `workflow.py snapshot` again.

Check essential round/year supplements against actual statements. Existing
verified simulator/marking/instruction associations remain in the database.
Source-quality notes flag the unavailable US 2022 experiment executable,
separate IZho 2023 writing sheets, and OPhO 2025 Q34's conflicting solution.

This is an INCOMPLETE reviewed subset. Do not interpret NULL decisions as
BORDERLINE or assume the remaining archives share the selected-set KEEP rate.
Detailed current statistics: `validation.json`, `competition_coverage.csv`,
`format_statistics.csv`, `domain_statistics.csv`, `resume_checkpoint.json`.

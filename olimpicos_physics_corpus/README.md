# Olimpicos Physics corpus

Start with `ai_manifest.csv`; paths are relative to this directory. `manifest.sqlite` is canonical. `audit.md` explains scope, counts, validation and source errors. `reports/competition_coverage.csv` gives per-series coverage. Original downloaded bytes live under `originals/`.

Important: source rows marked not_published usually have a shared paper. The manifest preserves every logical row and all source relationships. Aggregate rows represent whole-paper source entries rather than invented internal questions. Source row numbers can differ from PDF problem numbers; use raw titles, source keys, sessions and source_band_index when inspecting.

Five source-labelled solution links return statement-only material. They are recorded in errors.csv and metadata/residual_issues.csv. No acquisitions remain pending; metadata/residual_queue.csv is empty apart from its header.

To resume interrupted transfers from this database, run `python _scripts/corpus.py download` and then `python _scripts/corpus.py export`. Already acquired records are skipped. Install `_scripts/requirements.txt` first.

For a fresh reconstruction, use a separate empty corpus directory and follow the saved fetch_pages, corpus discover, metadata_review, corpus download, mixed_evidence, content_review, repair_bands, moscow_rounds, aggregate_review, finalize, spot_checks, paper_structure_check, verify_pdfs, recheck_scope and write_audit scripts. Content corrections preserve source labels and supplied bytes; visual verification of scanned round labels is described in the audit. Do not replace the saved pre-download snapshot when resuming.

No OCR, translation, syllabus classification, physics solving or question splitting was performed. ZIP experimental resources are preserved as received; the acquisition did not execute archived programs.

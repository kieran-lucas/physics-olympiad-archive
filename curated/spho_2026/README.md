# SPhO 2026 KEEP selection — fast scope pass complete

8,019 reviewed KEEP records (8,010 distinct verified problems) are selected by
`selected_problems.csv` and `manifest.sqlite`. They reference 2,926 unique
physical files: 2,908 immutable acquisition files and 18 source-linked reference
files. All available registered statements have scope decisions; all 1,396
physical statement papers and 235 acquisition containers have completed
boundary checks. Ten unavailable or withdrawn statements remain explicitly
accounted for outside the selection. BORDERLINE and REJECT are excluded.

`source_file` paths are relative to `../../olimpicos_physics_corpus/`.
Curated file paths are relative to this directory. Page bounds are one-based.
Shared PDFs can contain nonselected questions: only selected manifest rows are
KEEP selections. Papers have not been physically split.

All 2,926 physical files are verified NTFS hardlinks. Do not edit their bytes
in place; create a separate working copy for later extraction or typesetting.
Raw-corpus hashes are unchanged, with zero known curated hash mismatches.
Source document relationships and source-linked supplements are preserved;
simulator executables were not executed.

Strict archival validation still reports original PDF structure repair required
for source file IDs 2680, 2682, 2683, 2686 and 2688. These PDFs open and all pages
load; their original hashes match. No raw file was rewritten and no assertion
was suppressed. Full archival validation and optional enrichment are separate
from the completed fast scope pass. See
`../../syllabus_screening/spho_2026/final_checkpoint.json` and `validation.json`.

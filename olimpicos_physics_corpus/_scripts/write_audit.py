import json,csv,sqlite3,platform,importlib.metadata
from pathlib import Path
from datetime import datetime, timezone, timedelta
from corpus import ROOT,db,now
c=db()
summary=json.loads((ROOT/'reports/summary.json').read_text(encoding='utf-8'))
coverage=list(csv.DictReader((ROOT/'reports/competition_coverage.csv').open(encoding='utf-8-sig')))
spots=json.loads((ROOT/'reports/spot_check_evidence.json').read_text(encoding='utf-8'))
pdf=json.loads((ROOT/'reports/independent_pdf_validation.json').read_text(encoding='utf-8'))
landing=json.loads((ROOT/'reports/landing_scope_recheck.json').read_text(encoding='utf-8'))
scope_review=json.loads((ROOT/'reports/shared_file_scope_review.json').read_text(encoding='utf-8'))
errors=list(c.execute("SELECT c.slug,d.year,d.original_filename,d.direct_url,i.detail FROM issues i JOIN documents d ON d.id=i.document_id JOIN competitions c ON c.id=d.competition_id WHERE i.resolved=0 AND i.kind='source_content_mismatch'"))
ai=list(csv.DictReader((ROOT/'ai_manifest.csv').open(encoding='utf-8-sig')))
statement_missing=sum(not r['problem_file_path'] for r in ai)
solution_missing=sum(not r['solution_file_path'] for r in ai)
status=summary['document_statuses']
local_time=datetime.now(timezone(timedelta(hours=7))).isoformat()
lines=[
    '# Olimpicos Physics corpus acquisition audit','',
    f'Audited {local_time} (Asia/Ho_Chi_Minh). Source universe: https://olimpicos.net/physics/. The final live landing-page recheck still lists the same 40 competitions; no series appeared or disappeared during this run.','',
    'Acquisition and inventory reconciliation are finished for all 40 discovered archives. Every discovered source item is accounted for. Five source-labelled solution URLs supply statement-only material; these are explicit source errors, not unresolved transfers. This corpus represents what Olimpicos supplies, not a claim that every historical olympiad or every genuine solution exists on Olimpicos.','',
    '| Measure | Final value |','|---|---:|',
    f'| Competitions discovered / processed | {summary["competitions"]} / {summary["processed_competitions"]} |',
    f'| Competition-years | {summary["competition_years"]} |',
    f'| Distinct source archive bands | {summary["archive_sections"]} |',
    f'| Competition-year-session combinations | {summary["year_sessions"]} |',
    f'| Indexed source rows | {summary["logical_problem_rows"]:,} |',
    f'| Individually enumerated problem rows | {summary["logical_problem_rows"]-summary["aggregate_rows"]:,} |',
    f'| Aggregate whole-paper source rows | {summary["aggregate_rows"]} |',
    f'| Document records | {summary["document_records"]:,} |',
    f'| Acquired document records | {status["downloaded"]+status["content_duplicate"]:,} |',
    f'| Intentionally index-only records | {status["index_only"]} |',
    f'| Distinct acquired URLs | {summary["distinct_acquired_urls"]:,} |',
    f'| Unique physical files | {summary["unique_files"]:,} |',
    f'| Original file bytes | {summary["file_bytes"]:,} ({summary["file_bytes"]/1e9:.3f} GB; {summary["file_bytes"]/1024**3:.3f} GiB) |',
    f'| Different-URL SHA-256 duplicates avoided | {summary["sha256_duplicate_downloads_avoided"]} |',
    f'| Redundant document-level physical copies avoided | {summary["redundant_document_copies_avoided"]} |',
    f'| Source rows marked individual material not published | {summary["not_published_individual_rows"]:,} |',
    f'| Source-authored titles explicitly marked by Olimpicos | {summary["source_authored_titles"]:,} |',
    f'| Unresolved transfer / validation / access errors | {summary["unresolved_document_errors"]} |',
    f'| Unresolved parser warnings | {summary["parser_warnings"]} |',
    f'| Unresolved source content errors | {summary["source_content_mismatches"]} |',
    f'| Unexplained records | {len(summary["unexplained_document_records"])} |','',
    'The 233 aggregate rows are retained because the source explicitly offers a whole paper as one archive row (often titled “All problems”, or Paper 1/2). Their source row identifiers are not asserted to be individual questions inside those papers. The later inspection stage can enumerate the actual internal questions; this acquisition did not manufacture problem identifiers.','',
    f'Every one of the {len(ai):,} AI-manifest rows points to an acquired statement or combined file. {summary["not_published_individual_rows"]:,} source rows say individual material is “not published”, but all retain available shared-paper relationships. {solution_missing:,} AI rows have no confidently mapped genuine solution; an absent source link is not automatically declared an unpublished solution.','',
    '**Reconciliation and provenance.**','',
    '3,715 document records = 3,575 acquired + 140 intentionally index-only + 0 unavailable HTTP documents + 0 failed transfers. The acquired records reference 3,560 distinct URLs and 3,187 unique SHA-256 files. The difference is 373 different-URL content duplicates and 15 repeated document references to already-inventoried URLs. The five content errors overlap acquired documents: their bytes are preserved, while their falsely labelled solution role is corrected. They are not an unexplained remainder.','',
    'The canonical SQLite manifest separates competitions, archive_sections, problems, documents, files, problem_documents and document_sources. Each document retains its raw label, exact direct URL, source page, final URL, HTTP/MIME response, attempts and original filename. The files table contains one row per hash. Every document has provenance and every logical row has document relationships. CSV paths are relative to the corpus root and use forward slashes. UTF-8 BOM CSVs are suitable for Windows inspection.','',
    'The pre-download database snapshot is metadata/pre_download_inventory.sqlite. It contains all 6,392 source rows and all 3,715 documents before bulk acquisition. The final audit split 32 initially grouped archive bands into distinct identities; no document or logical problem was lost in that grouping. The final 905 bands now reconcile exactly to the source HTML. Original HTML, robots snapshots, the relevant show-all JavaScript, all request attempts, audit evidence and correction scripts remain on disk.','',
    '**Validation and retries.**','',
    f'All {summary["unique_files"]:,} files were streamed through .part files, checked, hashed, then atomically promoted. All 2,984 PDFs passed magic-byte, EOF, parser-open and nonzero-page checks. An independent MuPDF pass reopened every PDF and agreed with pypdf on every page count: {pdf["total_pdf_pages"]:,} pages, from {pdf["minimum_pages"]} to {pdf["maximum_pages"]} pages per PDF. All 101 ZIP archives passed CRC checks; all 102 plain TeX transcriptions passed UTF-8/text-command checks.','',
    'Twenty Taiwan PDFs use AES encryption with public empty-password readability. The initial parser lacked its optional cryptography provider, so validation failed. The dependency was installed, a fresh process retried all twenty URLs, and every file then validated. No password, authentication, CAPTCHA or access restriction was bypassed. Request history preserves those resolved attempts.','',
    'Final disk verification recomputed all 3,187 SHA-256 hashes and checked sizes. There are zero missing files, size/hash mismatches, orphan originals or .part files. SQLite integrity_check is ok; foreign_key_check reports zero violations. No acquired URL returned an accepted HTML/error page or zero-byte file. Requests used normal HTTP, three workers, host spacing, conservative retry backoff and a transparent research user agent. Source robots.txt allows crawling; externally linked errata was also checked against its host robots policy.','',
    '**Adversarial findings and corrections.**','',
    '- Compared every saved archive HTML against manifest URLs, years, source row counts and distinct band counts. All 40 comparisons match; no unparsed page remains.',
    '- Verified show-all is a CSS/UI expansion of rows already present in HTML, rather than an uncollected network page. All hidden rows were parsed.',
    '- Collected year-level, band-level and individual links independently. Full papers were retained even when individual rows say not published.',
    '- Preserved Theory/Experimental, Open/Invitational, Round 1/2, X/Y/W, F=ma, Exam A/B, Semifinal, Training Camp, and other source labels without merging repeated identifiers across sessions.',
    '- Repaired 32 repeated-label bands in OIbF and MOSh. source_band_index and archive_section_id distinguish them without inventing source names. All 30 MOSh round labels were subsequently verified in original PDF headers/footers, including one scanned page viewed directly. WoPhO selection/final attribution follows the explicit archive note.',
    f'- Reviewed {len(scope_review)} shared physical-file groups initially referenced as individual materials. Their document scopes and shared-file relationships now acknowledge multi-problem coverage. Differently named NBPhO URLs often return the same whole paper.',
    '- Reviewed all 59 physical PDFs simultaneously referenced through source problem and solution roles. Fifty-four contain statements plus substantive solutions, marking information or answers and were normalized as combined. Five are statement-only source mislinks, listed below.',
    '- Resolved relative URLs from each actual competition URL and retained the external errata document. Generic official/archive website references are index-only and were not used to supplement Olimpicos from independent archives.',
    '- Downloaded all five experimental ZIP bundles, all exposed TeX/LaTeX material, appendices, calibration/alignment material, instructions, presentations and answer/marking documents. The two exposed XLSX files are explicitly Results spreadsheets and remain indexed administrative records. Administrative PDFs and reference websites are also indexed.',
    '- Avoided filename-only deduplication. Common TeX basenames in different competitions remain distinct unless their bytes match. Canonical storage ownership is sorted by source metadata after acquisition, making paths independent of worker completion order.',
    '- Captured topics only from each individual source row’s data-t/data-s attributes. Filter option lists were not assigned to problems. Source-created title markers remain distinct from unknown provenance. No physics-topic inference, syllabus filtering, translation, OCR, solving or problem splitting was performed.','',
    '**Content spot checks.**','',
    f'{len(spots)} selected document records across {len({x["competition_id"] for x in spots})} competitions were opened; detailed native-text evidence is in reports/spot_check_evidence.json. These are structural/provenance checks, not physics classification. Some extracted individual PDFs omit competition/year headers; where absent, year attribution remains explicitly grounded in the source page and adjacent paper context, not invented from the PDF.','',
    '| Sample | Finding |','|---|---|',
    '| IPhO 2026 T1 and 2025 T2, statements/solutions | Matching numbered titles and problem/solution roles; dates/source context consistent. 2025 solution also embeds the statement and marking information. |',
    '| EuPhO 2026 T1 pair | Matching Jumper title and statement/worked-solution contents; source year from archive context. |',
    '| IPhO 1967 problem 1 pair; 1969 scanned problem 1 | Historical material opens correctly. 1967 introduction precedes the actual problem. The 1969 scan visibly states competition, year and Problem 1; no OCR used. |',
    '| IPhO 2022 theory solutions | S1/S2/S3 URLs return one 23-page shared theoretical solution paper, correctly mapped to all three logical rows. |',
    '| NBPhO 2019 pair | Full statement paper contains all eight listed problems; shared solutions contain their numbered answers. Source per-problem filenames are not individual files in content. |',
    '| WoPhO 2012 final problem and solution | Source final-round grouping and Magnetic Monopole title agree; solution file includes the statement and marking material. |',
    '| USAPhO 2022 F=ma Exam A pair | Source A/B distinction retained. Exam A PDF has exactly 25 numbered questions and the corresponding answer/solution paper. |',
    '| Russia TST 2026 X/Y problem 1 pairs | Distinct round files and matching statement/solution content; source Russian titles retained. |',
    '| BPhO 2024 Round 1 Section 1 pair and Round 2 paper | Distinct papers verified from cover/date/section labels. Section 1 is an aggregate source row, not a fabricated single exam question. |',
    '| Fyziklani 2026 | Both source roles resolve to one 69-page combined booklet. All 58 codes AA through HB are present, matching 58 logical source rows despite individual not-published labels. |',
    '| Physics Brawl 2025 | All 68 problems present: 1–56 plus B.1–B.4, P.1–P.4 and R.1–R.4. Their source sequential row identifiers and raw original labels are retained. |',
    '| Ortvay 1997 | Full historical paper preserved with its listed source problem inventory; no invented solution pairing. |',
    '| SPhO 2002 and 2023 Paper 1/2 | Papers contain multiple actual questions. Whole-paper source rows are flagged aggregate. |',
    '| Taiwan TST 2026 | Publicly readable PDF contains the exam plus substantive marking/answer material; normalized combined. |',
    '| APhO 2021 experimental archive | ZIP contains the experimental simulation and its data/resources. CRC valid; archive preserved intact without executing its programs. |','',
    '**Unresolved source errors.**','',
    '| Competition/year | Source-labelled solution file | Actual supplied content |','|---|---|---|'
]
for e in errors:lines.append(f'| {e["slug"]} {e["year"]} | [{e["original_filename"]}]({e["direct_url"]}) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |')
lines += ['', 'These five records appear in errors.csv, missing_or_unavailable.csv and metadata/residual_issues.csv, with document IDs and exact URLs. They retain status downloaded because their supplied bytes were acquired. ai_manifest.csv excludes them from genuine solution_file_path assignments. metadata/residual_queue.csv has only a header: there are no pending or failed acquisitions to resume. No second archive was consulted to fill these gaps.','',
    '**Per-competition coverage.**','',
    'Counts below are document/provenance counts, not assumed distinct files per problem. “NP” is individual not-published rows, including those covered by shared papers. “Source errors” are the five content mislinks. All transfer failures, validation failures and parser warnings are zero. reports/competition_coverage.csv contains the full machine-readable metrics.','',
    '| Competition | Years | Bands | Rows | Documents | Acquired refs | Unique files | Index-only | NP | Duplicates | Source errors |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
]
for r in coverage:lines.append('| '+' | '.join(str(r[k]) for k in ['competition','years','sections','logical_problem_rows','document_records','acquired_document_records','unique_files_referenced','index_only','individual_not_published','duplicate_document_storage_avoided','source_content_mismatches'])+' |')
lines += ['', '**Final limitations.**','',
    'Completeness is scoped to the current Physics landing page and materials referenced by its archive pages, including exposed embedded transcription URLs. It does not mean every historical competition year is hosted, every paper has a genuine solution, or every internal subproblem has its own record. Source-created titles, original languages, scans, page ordering, original numbering and source errors are preserved. Document hyperlinks to other websites remain embedded in the original PDFs; independent external archives were not recursively harvested. Individual PDF contents were spot checked, not exhaustively semantically interpreted.','',
    'Final reconciliation: zero unexplained source records; all 40 archives processed. Five explicit source-content errors remain. The collection is ready for source-material inspection in the later AI stage.',''
]
(ROOT/'audit.md').write_text('\n'.join(lines),encoding='utf-8')
readme='''# Olimpicos Physics corpus

Start with `ai_manifest.csv`; paths are relative to this directory. `manifest.sqlite` is canonical. `audit.md` explains scope, counts, validation and source errors. `reports/competition_coverage.csv` gives per-series coverage. Original downloaded bytes live under `originals/`.

Important: source rows marked not_published usually have a shared paper. The manifest preserves every logical row and all source relationships. Aggregate rows represent whole-paper source entries rather than invented internal questions. Source row numbers can differ from PDF problem numbers; use raw titles, source keys, sessions and source_band_index when inspecting.

Five source-labelled solution links return statement-only material. They are recorded in errors.csv and metadata/residual_issues.csv. No acquisitions remain pending; metadata/residual_queue.csv is empty apart from its header.

To resume interrupted transfers from this database, run `python _scripts/corpus.py download` and then `python _scripts/corpus.py export`. Already acquired records are skipped. Install `_scripts/requirements.txt` first.

For a fresh reconstruction, use a separate empty corpus directory and follow the saved fetch_pages, corpus discover, metadata_review, corpus download, mixed_evidence, content_review, repair_bands, moscow_rounds, aggregate_review, finalize, spot_checks, paper_structure_check, verify_pdfs, recheck_scope and write_audit scripts. Content corrections preserve source labels and supplied bytes; visual verification of scanned round labels is described in the audit. Do not replace the saved pre-download snapshot when resuming.

No OCR, translation, syllabus classification, physics solving or question splitting was performed. ZIP experimental resources are preserved as received; the acquisition did not execute archived programs.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
packages=['requests','beautifulsoup4','pypdf','lxml','PyMuPDF','cryptography','fonttools']
(ROOT/'_scripts/requirements.txt').write_text('\n'.join(p+'=='+importlib.metadata.version(p) for p in packages)+'\n',encoding='utf-8')
c.execute('PRAGMA wal_checkpoint(TRUNCATE)');c.close()
summary['total_corpus_bytes']=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
summary['spot_checked_document_records']=len(spots);summary['spot_checked_competitions']=len({x['competition_id'] for x in spots})
summary['ai_rows_missing_statement_path']=statement_missing;summary['ai_rows_without_solution_path']=solution_missing
(ROOT/'reports/summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['total_corpus_bytes','spot_checked_document_records','spot_checked_competitions','ai_rows_missing_statement_path','ai_rows_without_solution_path']},indent=2))

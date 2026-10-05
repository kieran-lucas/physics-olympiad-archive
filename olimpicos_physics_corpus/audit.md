# Olimpicos Physics corpus acquisition audit

Audited 2026-10-04T03:36:31.759549+07:00 (Asia/Ho_Chi_Minh). Source universe: https://olimpicos.net/physics/. The final live landing-page recheck still lists the same 40 competitions; no series appeared or disappeared during this run.

Acquisition and inventory reconciliation are finished for all 40 discovered archives. Every discovered source item is accounted for. Five source-labelled solution URLs supply statement-only material; these are explicit source errors, not unresolved transfers. This corpus represents what Olimpicos supplies, not a claim that every historical olympiad or every genuine solution exists on Olimpicos.

| Measure | Final value |
|---|---:|
| Competitions discovered / processed | 40 / 40 |
| Competition-years | 598 |
| Distinct source archive bands | 905 |
| Competition-year-session combinations | 683 |
| Indexed source rows | 6,392 |
| Individually enumerated problem rows | 6,159 |
| Aggregate whole-paper source rows | 233 |
| Document records | 3,715 |
| Acquired document records | 3,575 |
| Intentionally index-only records | 140 |
| Distinct acquired URLs | 3,560 |
| Unique physical files | 3,187 |
| Original file bytes | 1,909,799,341 (1.910 GB; 1.779 GiB) |
| Different-URL SHA-256 duplicates avoided | 373 |
| Redundant document-level physical copies avoided | 388 |
| Source rows marked individual material not published | 5,119 |
| Source-authored titles explicitly marked by Olimpicos | 2,491 |
| Unresolved transfer / validation / access errors | 0 |
| Unresolved parser warnings | 0 |
| Unresolved source content errors | 5 |
| Unexplained records | 0 |

The 233 aggregate rows are retained because the source explicitly offers a whole paper as one archive row (often titled “All problems”, or Paper 1/2). Their source row identifiers are not asserted to be individual questions inside those papers. The later inspection stage can enumerate the actual internal questions; this acquisition did not manufacture problem identifiers.

Every one of the 6,392 AI-manifest rows points to an acquired statement or combined file. 5,119 source rows say individual material is “not published”, but all retain available shared-paper relationships. 1,538 AI rows have no confidently mapped genuine solution; an absent source link is not automatically declared an unpublished solution.

**Reconciliation and provenance.**

3,715 document records = 3,575 acquired + 140 intentionally index-only + 0 unavailable HTTP documents + 0 failed transfers. The acquired records reference 3,560 distinct URLs and 3,187 unique SHA-256 files. The difference is 373 different-URL content duplicates and 15 repeated document references to already-inventoried URLs. The five content errors overlap acquired documents: their bytes are preserved, while their falsely labelled solution role is corrected. They are not an unexplained remainder.

The canonical SQLite manifest separates competitions, archive_sections, problems, documents, files, problem_documents and document_sources. Each document retains its raw label, exact direct URL, source page, final URL, HTTP/MIME response, attempts and original filename. The files table contains one row per hash. Every document has provenance and every logical row has document relationships. CSV paths are relative to the corpus root and use forward slashes. UTF-8 BOM CSVs are suitable for Windows inspection.

The pre-download database snapshot is metadata/pre_download_inventory.sqlite. It contains all 6,392 source rows and all 3,715 documents before bulk acquisition. The final audit split 32 initially grouped archive bands into distinct identities; no document or logical problem was lost in that grouping. The final 905 bands now reconcile exactly to the source HTML. Original HTML, robots snapshots, the relevant show-all JavaScript, all request attempts, audit evidence and correction scripts remain on disk.

**Validation and retries.**

All 3,187 files were streamed through .part files, checked, hashed, then atomically promoted. All 2,984 PDFs passed magic-byte, EOF, parser-open and nonzero-page checks. An independent MuPDF pass reopened every PDF and agreed with pypdf on every page count: 20,729 pages, from 1 to 104 pages per PDF. All 101 ZIP archives passed CRC checks; all 102 plain TeX transcriptions passed UTF-8/text-command checks.

Twenty Taiwan PDFs use AES encryption with public empty-password readability. The initial parser lacked its optional cryptography provider, so validation failed. The dependency was installed, a fresh process retried all twenty URLs, and every file then validated. No password, authentication, CAPTCHA or access restriction was bypassed. Request history preserves those resolved attempts.

Final disk verification recomputed all 3,187 SHA-256 hashes and checked sizes. There are zero missing files, size/hash mismatches, orphan originals or .part files. SQLite integrity_check is ok; foreign_key_check reports zero violations. No acquired URL returned an accepted HTML/error page or zero-byte file. Requests used normal HTTP, three workers, host spacing, conservative retry backoff and a transparent research user agent. Source robots.txt allows crawling; externally linked errata was also checked against its host robots policy.

**Adversarial findings and corrections.**

- Compared every saved archive HTML against manifest URLs, years, source row counts and distinct band counts. All 40 comparisons match; no unparsed page remains.
- Verified show-all is a CSS/UI expansion of rows already present in HTML, rather than an uncollected network page. All hidden rows were parsed.
- Collected year-level, band-level and individual links independently. Full papers were retained even when individual rows say not published.
- Preserved Theory/Experimental, Open/Invitational, Round 1/2, X/Y/W, F=ma, Exam A/B, Semifinal, Training Camp, and other source labels without merging repeated identifiers across sessions.
- Repaired 32 repeated-label bands in OIbF and MOSh. source_band_index and archive_section_id distinguish them without inventing source names. All 30 MOSh round labels were subsequently verified in original PDF headers/footers, including one scanned page viewed directly. WoPhO selection/final attribution follows the explicit archive note.
- Reviewed 47 shared physical-file groups initially referenced as individual materials. Their document scopes and shared-file relationships now acknowledge multi-problem coverage. Differently named NBPhO URLs often return the same whole paper.
- Reviewed all 59 physical PDFs simultaneously referenced through source problem and solution roles. Fifty-four contain statements plus substantive solutions, marking information or answers and were normalized as combined. Five are statement-only source mislinks, listed below.
- Resolved relative URLs from each actual competition URL and retained the external errata document. Generic official/archive website references are index-only and were not used to supplement Olimpicos from independent archives.
- Downloaded all five experimental ZIP bundles, all exposed TeX/LaTeX material, appendices, calibration/alignment material, instructions, presentations and answer/marking documents. The two exposed XLSX files are explicitly Results spreadsheets and remain indexed administrative records. Administrative PDFs and reference websites are also indexed.
- Avoided filename-only deduplication. Common TeX basenames in different competitions remain distinct unless their bytes match. Canonical storage ownership is sorted by source metadata after acquisition, making paths independent of worker completion order.
- Captured topics only from each individual source row’s data-t/data-s attributes. Filter option lists were not assigned to problems. Source-created title markers remain distinct from unknown provenance. No physics-topic inference, syllabus filtering, translation, OCR, solving or problem splitting was performed.

**Content spot checks.**

31 selected document records across 13 competitions were opened; detailed native-text evidence is in reports/spot_check_evidence.json. These are structural/provenance checks, not physics classification. Some extracted individual PDFs omit competition/year headers; where absent, year attribution remains explicitly grounded in the source page and adjacent paper context, not invented from the PDF.

| Sample | Finding |
|---|---|
| IPhO 2026 T1 and 2025 T2, statements/solutions | Matching numbered titles and problem/solution roles; dates/source context consistent. 2025 solution also embeds the statement and marking information. |
| EuPhO 2026 T1 pair | Matching Jumper title and statement/worked-solution contents; source year from archive context. |
| IPhO 1967 problem 1 pair; 1969 scanned problem 1 | Historical material opens correctly. 1967 introduction precedes the actual problem. The 1969 scan visibly states competition, year and Problem 1; no OCR used. |
| IPhO 2022 theory solutions | S1/S2/S3 URLs return one 23-page shared theoretical solution paper, correctly mapped to all three logical rows. |
| NBPhO 2019 pair | Full statement paper contains all eight listed problems; shared solutions contain their numbered answers. Source per-problem filenames are not individual files in content. |
| WoPhO 2012 final problem and solution | Source final-round grouping and Magnetic Monopole title agree; solution file includes the statement and marking material. |
| USAPhO 2022 F=ma Exam A pair | Source A/B distinction retained. Exam A PDF has exactly 25 numbered questions and the corresponding answer/solution paper. |
| Russia TST 2026 X/Y problem 1 pairs | Distinct round files and matching statement/solution content; source Russian titles retained. |
| BPhO 2024 Round 1 Section 1 pair and Round 2 paper | Distinct papers verified from cover/date/section labels. Section 1 is an aggregate source row, not a fabricated single exam question. |
| Fyziklani 2026 | Both source roles resolve to one 69-page combined booklet. All 58 codes AA through HB are present, matching 58 logical source rows despite individual not-published labels. |
| Physics Brawl 2025 | All 68 problems present: 1–56 plus B.1–B.4, P.1–P.4 and R.1–R.4. Their source sequential row identifiers and raw original labels are retained. |
| Ortvay 1997 | Full historical paper preserved with its listed source problem inventory; no invented solution pairing. |
| SPhO 2002 and 2023 Paper 1/2 | Papers contain multiple actual questions. Whole-paper source rows are flagged aggregate. |
| Taiwan TST 2026 | Publicly readable PDF contains the exam plus substantive marking/answer material; normalized combined. |
| APhO 2021 experimental archive | ZIP contains the experimental simulation and its data/resources. CRC valid; archive preserved intact without executing its programs. |

**Unresolved source errors.**

| Competition/year | Source-labelled solution file | Actual supplied content |
|---|---|---|
| oibf 2015 | [OIbF_2015_S1.pdf](https://olimpicos.net/files/oibf/OIbF_2015_S1.pdf) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |
| oibf 2015 | [OIbF_2015_S2.pdf](https://olimpicos.net/files/oibf/OIbF_2015_S2.pdf) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |
| oibf 2015 | [OIbF_2015_S3.pdf](https://olimpicos.net/files/oibf/OIbF_2015_S3.pdf) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |
| oibf 2014 | [OIbF_2014_S1-3.pdf](https://olimpicos.net/files/oibf/OIbF_2014_S1-3.pdf) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |
| rmph 2021 | [RMPh_2021_S4.pdf](https://olimpicos.net/files/rmph/RMPh_2021_S4.pdf) | Statement-only PDF, identical to problem link; no genuine solution supplied at this URL. |

These five records appear in errors.csv, missing_or_unavailable.csv and metadata/residual_issues.csv, with document IDs and exact URLs. They retain status downloaded because their supplied bytes were acquired. ai_manifest.csv excludes them from genuine solution_file_path assignments. metadata/residual_queue.csv has only a header: there are no pending or failed acquisitions to resume. No second archive was consulted to fill these gaps.

**Per-competition coverage.**

Counts below are document/provenance counts, not assumed distinct files per problem. “NP” is individual not-published rows, including those covered by shared papers. “Source errors” are the five content mislinks. All transfer failures, validation failures and parser warnings are zero. reports/competition_coverage.csv contains the full machine-readable metrics.

| Competition | Years | Bands | Rows | Documents | Acquired refs | Unique files | Index-only | NP | Duplicates | Source errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| IPhO | 57 | 112 | 260 | 742 | 706 | 703 | 36 | 0 | 3 | 0 |
| EuPhO | 10 | 20 | 44 | 256 | 245 | 239 | 11 | 0 | 6 | 0 |
| APhO | 26 | 52 | 120 | 420 | 397 | 397 | 23 | 4 | 0 | 0 |
| NBPhO | 24 | 24 | 215 | 540 | 515 | 217 | 25 | 0 | 298 | 0 |
| OIbF | 28 | 46 | 152 | 109 | 108 | 103 | 1 | 100 | 5 | 4 |
| RMPh | 9 | 15 | 39 | 79 | 77 | 75 | 2 | 0 | 2 | 1 |
| WoPhO | 3 | 3 | 36 | 57 | 56 | 56 | 1 | 0 | 0 | 0 |
| GPhO | 4 | 8 | 17 | 26 | 22 | 22 | 4 | 14 | 0 | 0 |
| IZhO | 17 | 32 | 32 | 65 | 64 | 64 | 1 | 0 | 0 | 0 |
| ISPhO | 4 | 7 | 15 | 34 | 33 | 33 | 1 | 0 | 0 | 0 |
| USAPhO | 20 | 49 | 748 | 100 | 98 | 98 | 2 | 747 | 0 | 0 |
| USA TST | 2 | 3 | 3 | 7 | 6 | 6 | 1 | 0 | 5 | 0 |
| CPhO | 23 | 23 | 23 | 37 | 36 | 36 | 1 | 0 | 0 | 0 |
| PanPhO | 22 | 33 | 165 | 79 | 77 | 77 | 2 | 161 | 0 | 0 |
| VsOSh | 15 | 15 | 75 | 31 | 30 | 30 | 1 | 75 | 0 | 0 |
| Russia TST | 14 | 62 | 225 | 424 | 423 | 422 | 1 | 0 | 1 | 0 |
| MOSh | 15 | 30 | 150 | 61 | 60 | 58 | 1 | 150 | 2 | 0 |
| InPhO | 18 | 18 | 103 | 39 | 38 | 34 | 1 | 102 | 4 | 0 |
| OBF | 12 | 12 | 96 | 15 | 14 | 14 | 1 | 96 | 0 | 0 |
| SOIF | 5 | 5 | 26 | 11 | 10 | 10 | 1 | 26 | 0 | 0 |
| BPhO | 25 | 62 | 62 | 111 | 110 | 95 | 1 | 0 | 15 | 0 |
| ONF | 21 | 21 | 63 | 42 | 41 | 41 | 1 | 63 | 0 | 0 |
| UPhO | 1 | 1 | 5 | 2 | 1 | 1 | 1 | 5 | 0 | 0 |
| Eötvös | 12 | 12 | 36 | 14 | 12 | 12 | 2 | 36 | 0 | 0 |
| Fyziklani | 20 | 20 | 969 | 42 | 40 | 20 | 2 | 969 | 20 | 0 |
| EFO | 25 | 25 | 250 | 51 | 50 | 50 | 1 | 250 | 0 | 0 |
| TwPhO TST | 17 | 17 | 72 | 29 | 28 | 17 | 1 | 66 | 11 | 0 |
| TwPhO Camp | 7 | 18 | 18 | 19 | 18 | 18 | 1 | 0 | 0 | 0 |
| SPhO | 21 | 26 | 26 | 28 | 27 | 27 | 1 | 0 | 0 | 0 |
| SPhO TST | 9 | 9 | 9 | 20 | 19 | 19 | 1 | 0 | 0 | 0 |
| SJPO | 17 | 17 | 17 | 33 | 32 | 32 | 1 | 0 | 0 | 0 |
| KPhC | 8 | 10 | 10 | 11 | 10 | 10 | 1 | 0 | 0 | 0 |
| AuPhO | 18 | 18 | 19 | 44 | 43 | 43 | 1 | 0 | 0 | 0 |
| OSN Fisika | 4 | 4 | 95 | 6 | 5 | 4 | 1 | 95 | 1 | 0 |
| AzPhO | 3 | 3 | 55 | 4 | 3 | 3 | 1 | 55 | 0 | 0 |
| OPhO | 6 | 17 | 265 | 31 | 30 | 29 | 1 | 252 | 1 | 0 |
| Physics Brawl | 14 | 14 | 858 | 30 | 28 | 14 | 2 | 858 | 14 | 0 |
| Ortvay | 29 | 29 | 995 | 30 | 29 | 29 | 1 | 995 | 0 | 0 |
| Physics Cup | 3 | 3 | 14 | 15 | 14 | 14 | 1 | 0 | 0 | 0 |
| BAUPC | 10 | 10 | 10 | 21 | 20 | 20 | 1 | 0 | 0 | 0 |

**Final limitations.**

Completeness is scoped to the current Physics landing page and materials referenced by its archive pages, including exposed embedded transcription URLs. It does not mean every historical competition year is hosted, every paper has a genuine solution, or every internal subproblem has its own record. Source-created titles, original languages, scans, page ordering, original numbering and source errors are preserved. Document hyperlinks to other websites remain embedded in the original PDFs; independent external archives were not recursively harvested. Individual PDF contents were spot checked, not exhaustively semantically interpreted.

Final reconciliation: zero unexplained source records; all 40 archives processed. Five explicit source-content errors remain. The collection is ready for source-material inspection in the later AI stage.

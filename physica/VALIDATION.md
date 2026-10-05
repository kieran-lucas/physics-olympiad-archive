# Delivered validation

Validated 2026-10-04T15:26:03+00:00 against the real repository and production Windows executable.

- `npm test`: 12 UI/heading tests and 9 Rust tests passed.
- `npm run tauri:build`: x64 executable and NSIS installer built successfully.
- Production WebView2 smoke: 24 real-PDF openings; no JavaScript page errors. External network requests were blocked.
- Heading results across those openings: {'Problem heading': 16, 'Page fallback': 5, 'Cached heading': 3}. A scanned/textless statement (`raw::131`) rendered with a clean page fallback.
- Real official solution for IPhO 2025 Q1 opened in the same viewer.
- Zoom/page navigation, timer pinned on page 8, all confirmations, both Solved choices, Topic Focus/Unseen/Exclude solved, SKIP/Restore and restart persistence passed.
- Unfinished stopwatch resumed paused with saved elapsed time after a second restart.

## Current normalized checkpoint

- Registered: **8,567**. KEEP: **8,018**.
- KEEP formats: Theory **4,364**, MCQ **1,931**, Experimental **358**, unresolved **1,365**.
- KEEP with linked official solution/marking/combined PDF: **6,035**. Known KEEP aliases: **9**.
- Missing PDFs: **0** overall, **0** KEEP.
- Unclassified KEEP primary topics: **5,511**.

| Explicit primary block | KEEP |
| --- | ---: |
| Mechanics & Mechanical Waves | 1,748 |
| Thermal & Statistical Physics | 185 |
| Electrostatics | 257 |
| Magnetism & Electromagnetic Induction | 92 |
| Electromagnetic Waves & Wave Optics | 189 |
| Quantum, Atomic & Nuclear Physics | 36 |

## Input integrity

- All **3,312** acquisition files retained their start-of-task sizes and mtimes; no additions/deletions. Physica only reads PDFs.
- Source SQLite is enforced read-only, including an automated attempted-write rejection. Every mutable table is in the Physica-owned state DB.
- An independent workflow updated screening exports/database and curated outputs while implementation ran. The checkpoint advanced from 8,486 registered / 7,907 KEEP to the counts above; those updates were preserved.
- Source SHA-256 at final smoke start: `199b77ca8a80d74841d40dad126de9f3dbb9b70018bcb9861c01365002b9f4b9`.
- Source SHA-256 after final smoke: `834c1b3391a5ff2672bb5a691bceac93c630f328e2734aebb154a8ef61cf0e6f`. Unchanged during final smoke: **False**.

## Source limitations

- 1,365 KEEP records have no trustworthy format mapping and are browsable but excluded from weighted draws.
- 5,511 KEEP records lack an explicit topic. Balanced/Unseen retain unknown-topic supply; Topic Focus uses explicit primary blocks only.
- Some official links identify a whole paper or combined statement/solution; exact solution pages are not recorded. The viewer discloses this and opens the best linked PDF at page 1.
- Missing/unreliable text headings fall back to recorded pages. No OCR, source repairs, reclassification or Round 2 curation was performed.
- Source notes already flag some PDFs as requiring repair; the app leaves original bytes intact and reports render failures instead of rewriting them.
- Challenge and Mock are absent from v1; no reliable difficulty dataset or coherent mock composition was added.

Evidence: `tests/artifacts/desktop-smoke.json`, `input-integrity.json`, `tests-final.log`, `windows-build.log`, and screenshot PNGs. These local validation artifacts are ignored by Git.

The production adapter was run again using `cargo run --manifest-path src-tauri/Cargo.toml --example corpus-diagnostics`; it independently reproduced the registered/KEEP, format and topic counts above after the final external metadata update. It uses a temporary state database that is removed after the check.

# Physica

Offline Windows physics-olympiad practice using the repository's screened corpus. Tauri 2, React/TypeScript, Rust/rusqlite, PDF.js, and bundled Lexend. The approved root v12 reference supplies the visual baseline; production screens use live metadata and original PDFs.

## Run and build

From `physica/`, with Node, Rust/MSVC Windows build tools, and Microsoft Edge WebView2 installed:

```powershell
npm ci
npm run dev          # frontend development server; native data requires Tauri
npm run tauri:dev    # complete desktop app
npm run typecheck
npm test            # focused UI/heading tests and native tests, including the real local corpus
npm run build       # frontend production bundle
npm run tauri:build # Windows executable and NSIS installer
cargo run --manifest-path src-tauri/Cargo.toml --example corpus-diagnostics # read-only native check
```

Artifacts: `src-tauri/target/release/physica.exe` and `src-tauri/target/release/bundle/nsis/Physica_1.0.0_x64-setup.exe`. The installer uses the existing WebView2 runtime; it does not download a runtime or bundle the corpus. Dependencies require internet during initial installation; normal app use is offline.

## Corpus and persistence

Development detects the repository from the current directory/executable ancestors. Installed copies offer **Select corpus folder**: select the repository root containing `syllabus_screening/spho_2026/screening.sqlite` and `olimpicos_physics_corpus/`. The selection is remembered. **Refresh index** rechecks metadata and paths without changing source data.

The source adapter opens SQLite with `SQLITE_OPEN_READ_ONLY` and `PRAGMA query_only=ON`; it reads a consistent snapshot. All training state, versioned migrations, index cache and heading anchors belong to `%APPDATA%\local.physica.desktop\physica_state.sqlite` (the normal Tauri app-data directory). Diagnostics shows exact paths. `PHYSICA_STATE_DIR` can choose a separate local profile for testing. Back up that directory to preserve progress. No account, network backend, telemetry, source migrations or PDF modifications.

Only current KEEP, available PDFs and resolved formats enter random rotation. Library defaults to KEEP and exposes other decisions through Advanced filters. Unknown formats remain browsable. Source explicit classifications take priority; `primary_spho_domains` tokens map to the six blocks, with the first distinct block primary and the remaining blocks secondary. Missing classifications remain unknown.

Deterministic format mapping: theory/numerical/short_answer â†’ Theory; MCQ/multiple_choice â†’ MCQ; experimental/data_analysis â†’ Experimental. Missing formats use explicit source problem types and clear Theory/Experimental/Data Analysis sections. F=ma/USAPhO Quarterfinal â†’ MCQ; FYKOS Fyziklani/Physics Brawl and OPhO Open â†’ written Theory. Ambiguous national `Problems` sections and unsupported mixed formats remain unresolved. These are broad practice formats, not new screening decisions.

## Scheduler and practice

Choose format first using independent 2:1:1 weights, renormalized over available formats; pool size cannot overwhelm those weights. Theory/MCQ known topics use inverse smoothed exposure over the last 100 openings. Experimental uses `eligible bucket supply / (recent bucket exposure + 4)`. Unknown topics receive their actual share within the chosen format; Topic Focus selects explicit primary classifications only. Within a bucket, unseen items receive a modest bonus and repeated exposure reduces weight. The most recent problem is excluded if its format has an alternative, and the previous twelve are avoided within a bucket when possible.

SKIP always excludes a problem; Restore changes only that exclusion. Solved remains eligible unless **Exclude solved problems** is enabled. Failed remains eligible. Known aliases share skip/solved/unseen eligibility and collapse to an eligible canonical candidate. A seeded RNG makes these rules testable.

All four actions require confirmation. Answer records viewing without implying failure and opens a linked official PDF; no generated solution is supplied. Solved saves before the second **Solve another / Back to home** modal. The stopwatch starts manually, stays pinned inside the workspace and saves every five seconds, on pause/navigation, and on confirmed outcomes. Resume restores an unfinished attempt paused; an abrupt power loss may lose up to five seconds. Opening a different problem preserves the abandoned attempt without inventing a result.

PDF pages render only near the visible viewport, with distant canvases released. Text selection works when available; scans render as images. Opening targets recorded pages/heading coordinates or searches PDF text for a reliable label/title. Precise anchors cache normalized page/Y with the file size/mtime fingerprint; missing text falls back to the recorded page. Zoom, fit width and page navigation sit in a small floating bottom control. The removed context bar remains absent.

## Validation

`npm test` covers read-only source access, KEEP/path/page normalization, mappings, missing sources, seeded scheduler behavior, migrations, results/restores/timer persistence, all action confirmations, both Solved choices and text heading fallback.

For actual desktop automation, start `npm run dev` and build the debug binary (`cargo build --manifest-path src-tauri/Cargo.toml`), then:

```powershell
npm run test:desktop
# Or exercise the production bundle without a dev server:
$env:PHYSICA_EXE = (Resolve-Path src-tauri/target/release/physica.exe)
npm run test:desktop
Remove-Item Env:PHYSICA_EXE
```

The smoke runner opens the actual WebView2 process with remote debugging only for the test, uses a fresh temporary state profile, drives real PDF/solution and confirmation flows, restarts the process, and writes screenshots plus `tests/artifacts/desktop-smoke.json`. No debug server is enabled by normal app launches. See [VALIDATION.md](VALIDATION.md) for the delivered corpus checkpoint and known source limitations.

Implementation references: [Tauri local asset scope](https://v2.tauri.app/security/asset-protocol/) and [PDF.js API](https://mozilla.github.io/pdf.js/api/).

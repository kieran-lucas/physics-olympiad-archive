# Physics Olympiad Archive

Original physics olympiad materials, an SPhO 2026 scope selection, and the
Physica offline Windows practice app.

- [Original corpus](olimpicos_physics_corpus/README.md): acquisition scripts,
  source metadata, manifests, and original downloaded files.
- [SPhO 2026 selection](curated/spho_2026/README.md): selected problems and
  preserved source files.
- [Screening checkpoint](syllabus_screening/spho_2026/resume.md): decisions,
  review evidence, workflow scripts, and remaining source limitations.
- [Physica](physica/README.md): setup, desktop builds, practice features, and
  validation instructions.
- [Visual reference](physica_horizon_vibe_v12_no_hero.html): the app's original
  HTML design reference.

Corpus and selection paths retain their repository-relative layout. Git keeps
file bytes unchanged; a checkout stores curated copies as regular files rather
than recreating the local NTFS hardlinks. Treat original and curated source
files as immutable.

Local environments, dependency directories, generated app assets, build outputs,
and Python bytecode are excluded. Screening text caches and rendered review
evidence are retained alongside the decisions they support.

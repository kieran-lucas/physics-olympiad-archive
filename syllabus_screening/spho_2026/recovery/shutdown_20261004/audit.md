# SPhO 2026 screening audit — INCOMPLETE CHECKPOINT

<!-- RESUMED_CHECKPOINT_START -->
## Current resumed checkpoint — 2026-10-04

**INCOMPLETE content screening; complete container expansion.** Historical tables
below describe the original pilot and are retained as audit history. Current
canonical counts supersede them:

| Item | Count |
|---|---:|
| Registered units | 8,472 |
| Direct / derived | 6,159 / 2,313 |
| Unindexed embedded units discovered / physical-paper audits pending | 50 / 1,140 |
| Whole-paper containers expanded / pending | 233 / 0 |
| Content-decided units | 807 |
| KEEP / BORDERLINE / REJECT | 780 / 8 / 19 |
| Awaiting actual content review | 7,664 |
| Explicit source withdrawal / unavailable statement | 1 |
| New focused or random second-review units | 61 |
| Low-confidence decisions / required second reviews pending | 0 / 0 |
| Curated physical files / hardlinks / copies | 369 / 369 / 0 |
| Curated payload bytes | 183,949,734 |
| Raw snapshot files / hash mismatches | 3,312 / 0 |

Registered accounting: **8,472 = 780 + 8 + 19 + 7664 pending
+ 1 explicit source-unavailable item**. This is zero *unexplained* remainder,
not zero unfinished work. The withdrawn Q24 is a retained source logical row,
not a fabricated physical question. All 6,392 acquisition rows reconcile as
6,159 direct source rows plus 233 containers. Current source-row/container counts
are proved by SQLite and `validate_outputs.py`; direct content locations still
require inspection for the pending units.

**Additional boundary finding:** full-page reading of indexed Estonian papers
revealed independently printed E1/E2 experiments omitted from their ten acquired
theory rows. 50 such units are now registered with deterministic SHA-based
embedded IDs, NULL raw problem IDs, exact printed labels/titles/pages and full-exam
document provenance. Matching solution E1/E2 labels/content were inspected before
pairing. The acquisition corpus remains immutable. A separate physical-paper
boundary ledger and residual queue now prevent claiming that expanded containers
alone prove the final problem universe. There are 1,140 remaining paper
audits; the final total can increase. Registered-unit reconciliation is exact,
but the full-corpus top-level total is not yet established.

The resumed run resolved every one of the 222 pending containers. Source-specific
checks included all MCQ labels, parallel Korean columns, scanned papers,
multilingual repetitions, whole-paper problem-plus-solution PDFs, British printed
competition year versus exam date, and Taiwan session resets. A 31-page Taiwan
camp file contains five exams: 5+5+3 theory units and two experiments. Shared page
ranges remain inclusive until individual content inspection refines their bounds.
Explicit source grand questions such as British General Q1 and US Take Five are
kept together, without independently screening their internal parts.

New actual-content reviews include old British scans, Singapore MCQs and written
papers, Chinese finals, US selection theory/experiment, Fourier spectrometry and
the 2025 OPhO open numerical paper. These decisions use full statements; caches
and page renders are saved. The original 205 decisions match their saved JSON
records (`original_205_preservation.json`); none was changed.

Quality control after the 48-unit calibration used focused checks and seeded
random sampling, not universal second review. The new second-review total is
61, including 12 seeded random cases and focused boundary/model cases. Two
new decisions changed to BORDERLINE after inspecting supplied target equations
and equally weighted internal tasks. A mistaken heat-capacity/lens description
was corrected while its KEEP decision remained valid. Full-size scans confirmed
classical two-charge magnetic motion rather than inferred quantum theory.

OPhO solution evidence establishes two clear rejections: unsupplied WKB tunneling
controls fusion rate, and unsupplied relativistic hidden momentum controls loop
motion. Hubble motion, monopole laws and gravitational-radiation scaling supplied
by their statements remain KEEP when ordinary mechanics/fields suffice.
Q24's withdrawal is separately recorded. Q34's official solution has inconsistent
methane labels/constants and starting temperature; this is flagged for later
training use rather than silently trusted or rewritten. US simulation executables
and IZho writing sheets absent from the acquired document inventory are explicitly
not claimed present; statements and associated solutions are retained.

Validation: both SQLite integrity checks, foreign keys, source/page/provenance
relationships, curated selection equality, SHA-256, hardlink identity, PDF opening
and ZIP CRC checks passed with zero issues. A transient SQLite lock during contact
rendering was fixed by closing the parent read cursor before subprocess writes;
the render batch resumed successfully. No unresolved operational failure remains.

The full screening request is still unfinished. `7,664` pending content
items and one unavailable-source item are exactly enumerated in `remaining.csv`.
Current distributions and complete per-competition pending coverage are exported
alongside this audit. No classification is fabricated to claim completion.
<!-- RESUMED_CHECKPOINT_END -->

The reviewed subset is materialized; the complete Olimpicos corpus is **not yet
screened**. No title/keyword classifier assigned decisions to uninspected content.
The content-review capacity of this execution was insufficient to finish the
remaining thousands of units. All completed decisions, full PDF text caches,
rendered inspection pages and the exact remaining source queue are persisted.

## Reconciliation and coverage

| Item | Count |
|---|---:|
| Original acquisition problem rows preserved | 6,392 |
| Source individual rows registered as direct candidates | 6,159 |
| Original whole-paper containers | 233 |
| Containers expanded after actual boundary inspection | 11 |
| Derived top-level units | 110 |
| Currently registered direct + derived units | 6,269 |
| Content-verified, screened and second-reviewed units | 205 |
| Reviewed direct units | 95 |
| Reviewed derived units | 110 |
| KEEP | 203 |
| BORDERLINE | 1 |
| REJECT | 1 |
| Registered units still awaiting actual content/location review | 6,064 |
| Containers still awaiting top-level boundary inspection | 222 |

The full number of top-level problems is **unknown until those 222 containers
are expanded**. Pending direct candidates also require boundary/location
verification when their actual shared papers are read. Counts above are not a
claim that the complete top-level inventory has been verified.

Identified-unit accounting: **6,269 = 203 + 1 + 1 + 6,064**. Raw-row accounting:
**6,392 = 6,159 direct rows + 233 containers**. Container accounting:
**233 = 11 expanded + 222 pending**. There is no unexplained inventory remainder,
but there is a substantial explicitly unresolved review queue. Complete-corpus
screening reconciliation has not been achieved.

`decision` remains NULL for unreviewed content. SQLite `unit_accounting` and CSV
`accounting_status` identify it as `UNRESOLVED_ERROR`, without inventing a physics
judgement. `screening_errors.csv` has 6,286 pending-review entries: 6,064 known
units plus 222 containers. There are zero additional extraction, database,
materialization or validation failures. Pending review is an execution residual,
not evidence that a problem is outside the syllabus.

`remaining.csv` contains the source IDs, file IDs, SHA-256, relative source paths
and stages needed to resume. `competition_coverage.csv` accounts for all 40
competitions. Two source archives have complete content coverage in this
checkpoint: EuPhO and BAUPC.

| Competition | Reviewed | KEEP | BORDERLINE | REJECT | Content coverage |
|---|---:|---:|---:|---:|---|
| EuPhO | 44 | 42 | 1 | 1 | All listed 2017–2026 material |
| BAUPC | 60 | 60 | 0 | 0 | All ten 1995–2004 papers; six top-level questions each |
| IPhO | 16 | 16 | 0 | 0 | 1969, 2010, 2025 incl. backup; 2015 T-1 |
| APhO | 4 | 4 | 0 | 0 | 2025 three theory problems and one complete experiment |
| USAPhO | 31 | 31 | 0 | 0 | All 2025 F=ma MCQs and six USAPhO written problems |
| SJPO | 50 | 50 | 0 | 0 | All numbered items in the supplied 2026 transcription; older papers pending |

The other 34 competition archives have been registered and cached where PDFs
exist, but have not received physics decisions in this checkpoint.

## Calibration and evidence

`scope_calibration.md` fixes the user's twelve-domain operational scope and
general-physics/mathematical/experimental foundations before screening. The
Vietnamese 2025 organizer's public official syllabus was read and preserved in
`references/official_scope_2025.pdf`. The detailed Vietnamese 2025 written and
experimental papers were not present locally or obtained; their calibration
examples are explicitly attributed to the user's descriptions, not claimed as
independently inspected documents. Olimpicos's SPhO and SPhO TST series are
Singapore competitions, not the Vietnamese target competition.

All 2,984 source PDFs were opened and embedded text cached by physical SHA-256:
20,729 pages, 60,324,037 extracted characters, zero fatal extraction errors.
Extraction is a reusable acquisition aid, **not a screening decision**.
Scans/font failures, diagrams, graph options, apparatus and important equations
were inspected as rendered pages. All 205 completed units have visual inspection
recorded; solutions informed scope checks for 13. Not every page of every
solution was read, and no thousands-of-problems solution bank was generated.

Each decision has individual required physics, a concise reason and actual
statement evidence in `units` and saved review JSON. A second conceptual pass
by the same reviewing AI reconsidered every completed unit. This is not an
independent second reviewer. The genuine BORDERLINE case, medium-confidence
KEEP and supplied/external-model cases received focused statement/solution
review. No low-confidence KEEP is materialized. One KEEP, EuPhO 2026 T3, retains
medium confidence after review; its solution explicitly allows dimensional
estimates without the advanced lubrication PDE.

## Boundaries and mappings checked

All eleven expanded containers have verified top-level counts. The SJPO 2026
paper contributes 50 separate MCQs, with heading coordinates and shared-stem
page locations. Its transcription explicitly reorders the original questions;
the stored numbering belongs to this physical transcription. The FIZIKA
companion solutions use the same order and are unofficial. BAUPC contributes
60 units from ten papers. Lettered parts, including unrelated short-answer
parts grouped under one numbered BAUPC question, were not independently screened.

All 25 F=ma MCQs map directly to source logical rows, although they share one
statement paper and one solution paper. USAPhO A1–A3/B1–B3 are six additional
whole problems. Shared context for F=ma Q13/Q14 and the USAPhO constants page is
recorded in location metadata.

APhO 2025 Experiment Q1 is one 20-point problem: its three internal experiments
measure the same cooker/coil system and remain together. IPhO 2010 explicitly
separates Experimental Problems 1 and 2 despite shared press apparatus. All
parts of each IPhO theory problem, including its backup problem, stay together.

Actual printed question labels were distinguished from sequential archive
catalogue numbers, particularly IPhO/APhO theory versus experiment, and EuPhO
experimental E1/E2. Unnumbered EuPhO 2018/2019 experiments retain a NULL printed
number. Original source rows and catalogue identifiers remain preserved.
Source-authored F=ma titles were not treated as official titles or as evidence
of physics content. Q17's statement supplies a quadratic potential despite its
misleading navigation title.

Shared papers are not split. In particular, the selected EuPhO 2024 shared
theory sheet necessarily contains the rejected spaceship problem as well;
**only T1 and T3 appear in selected_problems.csv**. Selection metadata, not the
presence of every page in a retained physical paper, defines the curated set.

## Adversarial findings and corrections

| Failure mode challenged | Content finding and disposition |
|---|---|
| Literal syllabus matching | Hydrostatics, surface tension, ordinary ray optics/DC circuits, center of mass and uncertainty were accepted as conventional foundations, with required physics explicitly recorded. |
| Exotic-context rejection | USAPhO 2025 Black Tides explicitly ignores relativity and supplies the radius comparison. Newtonian tidal/orbital work is KEEP. Galaxy, champagne, atmospheric and neural-network contexts were similarly evaluated by their equations. |
| Given-model rejection | EuPhO acoustic levitation, piezo response, waveguide dispersion, Rutherford scattering and diffusion models are given. APhO skin depth/NTC/load models and IPhO Fermi occupation/scaling rules were checked for sufficient operational definitions. |
| Theory/MCQ/experiment bias | All 75 reviewed MCQs and all 19 experiments received actual-content review. Apparatus operation, fitting, uncertainty and graphing were not rejection criteria. |
| Subproblem fragmentation | IPhO T1 sections, APhO Q1 experimental stages, and BAUPC lettered parts remain inside their parent unit. |
| Whole-paper under-fragmentation | Fifty SJPO MCQs and six questions in each BAUPC paper were explicitly derived; 222 uninspected containers remain queued rather than falsely classified as single problems. |
| Mathematical difficulty bias | Infinite collision sequences, resistor networks, gyroscopic geometry and variational/optimization tasks were kept when the underlying physics is ordinary. |
| Guessed-solution bias | EuPhO dry-ice solution explicitly says its detailed PDE is unnecessary. Nuclear recoil solution admits nonrelativistic reaction kinematics. Official solutions clarified two missing circuit drawings. |
| Metadata substitution | Decisions cite statement models and dependencies. No competition name, source tag, title or reputation generated a decision. |
| Visual omission | BAUPC font-garbled pages and IPhO 1969 scans were read visually. IPhO 2010 chimney's Bernoulli equation and IPhO 2015 T-1 equations disappear from embedded extraction and were checked in images. |
| Borderline inflation | Two initial missing-drawing BORDERLINE cases became KEEP after their solutions established ordinary circuit methods; quality warnings remain. Unreviewed content never became BORDERLINE. |
| Over-permissiveness | EuPhO 2024 spaceships is REJECT because unsupplied Lorentz/simultaneity/velocity addition controls the whole problem. EuPhO 2017 superconducting mesh remains BORDERLINE because necessary unsupplied local flux locking sits at an uncertain prerequisite boundary. |
| Lost year-level supporting material | Found and fixed: EuPhO 2020/2021 experiment-data ZIPs, 2018/2019 marking schemes and substantive IPhO instruction/data sheets were outside direct problem-document links. Verified explicit round/year associations now supplement unit_files, preserving source document_scope=year. |

Whole-problem majority remains semantic. IPhO 2015 T-1 is KEEP: independent
solar-cell/radiation/gravity work, nuclear flux and ordinary thermal Doppler form
the meaningful majority; unsupplied relativistic electron energy is confined to
one independent Cherenkov task. IPhO 2010 T3's exact laboratory gamma-Doppler
extension is peripheral to the nuclear binding/fission/reaction problem. The
entire original problem is retained in both cases, without selecting subparts.

The 99.024% KEEP rate among completed decisions triggered a permissiveness
review. Most reviewed material consists of classical undergraduate mechanics,
electrostatics, broad general physics or explicitly supplied models. No quota
was imposed. This high rate **cannot be extrapolated** to unreviewed archives
such as Ortvay, TSTs or other potentially different material. It is a checkpoint
distribution, not a statistical estimate of the whole corpus.

## Deep spot checks

Purposeful statement/solution checks included EuPhO 2017 mesh (files 931/933),
EuPhO 2026 dry-ice scaling (704/717), APhO 2025 spin chains (965/966), IPhO
2010 nuclear reactions (317/319), IPhO 2015 particles (250/251), BAUPC 1995
LC ladder (3177/3176), BAUPC 1996 cube network (3174/3175), and F=ma 2025
slip/rolling Q13–Q14 (1914/1915). These confirm competition/year, top-level
scope, statement-versus-solution role and the relevant physical method.

Six additional high-confidence KEEP draws used deterministic random seed
20261004, from sorted reviewed units by competition category and format. Each
statement page was reopened as text and image:

| Stratum | Unit | Physical file/page | Finding |
|---|---|---|---|
| International | raw::268 | 742 / 1 | EuPhO neuron experiment is ordinary circuits with supplied sigmoid, not ML prerequisite. |
| National | derived::d086c64af4c00eac::4055::15 | 2980 / 11 | Two in-phase coupled pendulums; independent MCQ with complete options. |
| Open | derived::e4d6f3dca986b3ee::6384::1 | 3160 / 1 | Folded rope support force; diagram confirms variable-mass geometry. |
| Theory | derived::a4f633140fd3956b::6387::4 | 3166 / 2 | Garbled extraction replaced by visual inspection; elastic semicircle collisions, one question with (a),(b). |
| MCQ | raw::962 | 1914 / 2 | Position-graph shapes and axes inspected; ordinary speed-component test. |
| Experimental | raw::287 | 842 / 2 | Supplied conduction/convection/radiation models, parameter fitting; simulator ZIP now retained. |

The single BORDERLINE and single REJECT were also deeply reconsidered; neither
enters selected_problems.csv. No independent correctness guarantee is made for
every unofficial answer. SJPO Q34's unofficial solution reports an options
inconsistency; this is retained as a source-quality warning rather than silently
repaired. BAUPC's missing original drawings remain explicitly flagged.

## Materialization and validation

Curated root: `../../curated/spho_2026/`. Screening and curation metadata live
entirely outside the immutable raw acquisition root.

| Verified result | Value |
|---|---:|
| Selected KEEP units | 203 |
| Distinct selected primary statement files | 62 |
| Total unique selected physical files incl. supporting material | 253 |
| Source-file payload bytes | 119,472,783 |
| Curated directory bytes including manifests/README | 121,005,570 |
| Hardlinks | 253 |
| Copies | 0 |
| PDFs structurally opened, without repair | 151 |
| Pages in those PDFs | 876 |
| ZIPs checked with CRC validation | 52 |
| Plain TeX sources retained | 50 |
| SHA-256 or size mismatches | 0 |
| SQLite integrity/foreign-key/page-range/provenance check failures | 0 |

All selected files match the original source SHA-256; paths are deterministic,
Windows-compatible and collision-resistant. A shared source file is stored
once. Provenance preserves source document records and every document_sources
relationship. Supplementary associations specify round/year scope and their
inspection evidence rather than pretending a year-level ZIP is problem-specific.
Experiment simulator binaries were inventoried and preserved inside their ZIPs;
they were not executed. No raw PDF was split, translated or rewritten.

All 3,312 files present in the raw baseline were rehashed after screening and
materialization, with zero changed, missing or additional raw files. See
`raw_immutability_check.json`. NTFS hardlinks share file contents; the curated
sources must be treated as immutable too. Future editing must operate on a new
working copy, not either hardlinked path.

## Decision distributions

Percentages refer to the **205 completed reviews**, not pending content:
KEEP 203 (99.024%), BORDERLINE 1 (0.488%), REJECT 1 (0.488%).

| Format | Reviewed | KEEP | BORDERLINE | REJECT |
|---|---:|---:|---:|---:|
| Theory | 110 | 108 | 1 | 1 |
| Multiple choice | 75 | 75 | 0 | 0 |
| Experimental | 19 | 19 | 0 | 0 |
| Mixed short-answer top-level problem | 1 | 1 | 0 | 0 |

No separately labelled numerical, short-answer or data-analysis unit was added
by splitting internal tasks. Such tasks occur inside the reviewed mixed/theory/
experimental units. This is not a claim that the remaining corpus lacks them.

KEEP domain counts overlap when a problem requires several domains:

| User domain | KEEP units |
|---|---:|
| I Force and motion | 140 |
| II Oscillations and waves | 32 |
| III Ideal gas | 15 |
| IV Thermodynamics | 31 |
| V Real gas | 0 |
| VI Electric field and foundational circuits | 28 |
| VII Magnetic field | 24 |
| VIII Induction | 8 |
| IX EM oscillations and waves | 11 |
| X Wave optics and foundational ray optics | 21 |
| XI Quantum light | 12 |
| XII Atomic/nuclear | 3 |

The foundational vector-algebra MCQ has no forced physical-domain assignment.
Zero real-gas selections in this partial checkpoint is not a rejection policy.
Machine-readable distributions are in `format_statistics.csv`,
`domain_statistics.csv`, `competition_coverage.csv` and `validation.json`.

## Remaining limitations

Complete screening and top-level boundary discovery remain unfinished. Full
Vietnamese 2025 papers were not independently inspected. Some source diagrams
are absent and some companion solutions are unofficial. These limitations are
recorded; none is hidden behind a completion claim. `progress.json` and curated
`materialization.json` explicitly state that the run/selection is incomplete.
Use `resume.md` and `remaining.csv` to continue without re-extracting PDFs or
re-screening completed units.


## Resumed calibration sanity audit — 2026-10-04

Inspected 48 previously pending top-level units: all 24 Ortvay 2026 problems,
all 14 Physics Cup archive problems, all five All-Ukrainian 2025 problems,
three World Physics Olympiad 2013 problems and two Russian TST 2026 problems.
The purposive sample spans five additional archives and includes relativity,
quantum measurement, many-body quantum theory, classical fluid models,
magnetization, optical response and simulation/data reasoning.
Complete statements were read from existing physical-file caches; diagrams,
ambiguous photographs, potential laws and the graphene plot were visually
inspected. LED solution 1751 was consulted to distinguish Carnot/Planck
reasoning from a semiconductor theory prerequisite.

Results: 36 KEEP, four BORDERLINE, eight REJECT (75% KEEP). This is a targeted
boundary sample, not an estimate of corpus-wide proportions. Canonical
Hamiltonian dynamics, unsupplied Heisenberg exchange, relativistic scalar
coupling, quantum operator measurement, Friedmann cosmology, Hubbard path
integrals, quantum wavepacket optimization and relativistic interception were
rejected for central unsupplied prerequisites. Explicit Drude/graphene models,
the supplied magnetic-moment invariant, Carnot LED model and classical
pair-potential simulation were kept. Mathematical difficulty, exotic context,
ordinary surface tension and hydrostatics did not cause rejection.

No systematic calibration error requiring a rubric change was identified.
All 205 historical decisions are preserved; none was overwritten or rescreened.
Their high KEEP rate cannot be extrapolated to unreviewed archives. Four new
borderline cases remain outside curated selection: snow/branch model ambiguity,
distributed-water normal modes, balanced relativistic/Newtonian alien-disk
sections and synchrotron orbit/phase-oscillation dependence.

Twelve focused reviews and six seeded random QC checks are recorded in
reviews/resume_calibration_focused_qc.json and review_events. No systematic
correction resulted. Clear high-confidence records now finish after one careful
inspection; flagged/uncertain cases require a second pass. This supersedes the
earlier universal-second-review workflow requirement.

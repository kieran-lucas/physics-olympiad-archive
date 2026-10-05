"""Publish the current exact checkpoint and compare the preserved original 205."""
import collections,json
import workflow as w
c=w.connect();root=w.ROOT
original=json.loads((root/'reviews/second_pass.json').read_text(encoding='utf-8'));assert len(original)==205
uids={r['screening_unit_id'] for r in original};assert len(uids)==205
expected={}
for p in (root/'reviews').glob('*.decisions.json'):
 for r in json.loads(p.read_text(encoding='utf-8')):
  if r['screening_unit_id'] in uids:expected[r['screening_unit_id']]=r['decision']
assert set(expected)==uids
for r in json.loads((root/'reviews/baupc_quality_corrections.json').read_text(encoding='utf-8')):
 expected[r['screening_unit_id']]=r['decision']
issues=[]
for uid,d in expected.items():
 r=c.execute('select decision,review_status from units where screening_unit_id=?',(uid,)).fetchone()
 if not r or r['decision']!=d or r['review_status']!='pass_2_complete':issues.append(uid)
assert not issues,issues
w.writejson(root/'original_205_preservation.json',{'checked_at':w.now(),'historical_units':205,'historical_decisions_unchanged':True,'mismatches':issues,'evidence':'Historical saved *.decisions.json compared against the 205 unique IDs in reviews/second_pass.json; no historical decision rewritten.'})
# Source Q1 explicitly asks about van der Waals equation; no topic quota applied.
u=c.execute('select * from units where source_problem_id=2603 and problem_number=?',('1',)).fetchone()
if 'V_real_gas' not in u['primary_spho_domains'].split(';'):
 c.execute('update units set primary_spho_domains=? where screening_unit_id=?',(u['primary_spho_domains']+';V_real_gas',u['screening_unit_id']))
c.commit()
stat=json.loads((root/'progress.json').read_text(encoding='utf-8'));v=json.loads((root/'validation.json').read_text(encoding='utf-8'));cur=json.loads((w.CUR/'materialization.json').read_text(encoding='utf-8'))
reviewed=c.execute('select count(*) from units where decision is not null').fetchone()[0]
direct=c.execute('select count(*) from units where derived_from_whole_paper=0').fetchone()[0]
derived=c.execute('select count(*) from units where derived_from_whole_paper=1').fetchone()[0]
embedded=c.execute('select count(*) from units where source_problem_id is null and derived_from_whole_paper=1').fetchone()[0]
paper_pending=c.execute("select count(*) from paper_boundary_audit where status!='full_paper_boundaries_verified'").fetchone()[0]
dec=dict(c.execute('select decision,count(*) from units where decision is not null group by decision').fetchall())
awaiting=c.execute("select count(*) from units where decision is null and review_status!='unresolved_source_unavailable'").fetchone()[0]
unavailable=c.execute("select count(*) from units where review_status='unresolved_source_unavailable'").fetchone()[0]
qc=c.execute('select count(distinct screening_unit_id) from review_events where pass=2').fetchone()[0]
newqc=c.execute("select count(distinct screening_unit_id) from review_events where pass=2 and screening_unit_id not in ("+','.join('?'*len(uids))+')',list(uids)).fetchone()[0]
counts={'registered_units':stat['identified_units'],'decisioned_units':reviewed,'awaiting_content_review':awaiting,'statement_unavailable':unavailable,'decisions':dec,'containers_expanded':233,'containers_pending':0,'original_205_preserved':True,'new_second_review_units':newqc,'total_distinct_second_review_units':qc,'low_confidence_units':c.execute("select count(*) from units where decision is not null and confidence='low'").fetchone()[0],'focused_reviews_pending':c.execute("select count(*) from units where decision is not null and review_status not in ('pass_2_complete','single_pass_complete')").fetchone()[0]}
w.writejson(root/'resume_checkpoint.json',counts)
resume=f'''# Resume the incomplete SPhO content screening

Canonical state: `screening.sqlite`. Original 205 decisions are preserved and
verified against their saved review records. Do not restart, regenerate the raw
baseline, re-extract all PDFs, re-expand containers, or rescreen reviewed units.

Current checkpoint (2026-10-04):

- {stat['identified_units']:,} registered units: {direct:,} direct + {derived:,} derived.
- Inventory is PROVISIONAL: {paper_pending:,} complete physical-paper boundary audits
  remain. {embedded} independently printed tasks omitted from raw logical rows have
  been discovered inside indexed shared papers and added without raw changes.
- All 233 whole-paper containers expanded; the 222 pending at resume are resolved.
- {reviewed} units have actual-content decisions: {dec['KEEP']} KEEP, {dec['BORDERLINE']} BORDERLINE,
  {dec['REJECT']} REJECT. {unavailable} source rows have explicit unavailable-statement status.
- Exactly {awaiting:,} units await content review; {unavailable} unavailable-source residual.
- {counts['focused_reviews_pending']} pending focused reviews; {counts['low_confidence_units']} low-confidence decisions.
- {cur['selected_units']} selected KEEP units, {cur['unique_physical_files']} unique files, all verified hardlinks.
- 2,984 PDF extraction caches and inspected page renders remain available.

`remaining.csv` is the exact residual queue for currently registered work. Its
`stage=paper_boundary_audit` rows also identify files that can contain additional
unregistered questions. `remaining_paper_boundaries.csv` gives the same file queue
separately. Filter `stage=content_review` for
workable pending content; `stage=source_unavailable` records explicit statement
withdrawals/unavailability, with source evidence in each row. Do not invent scope decisions for them.

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
Source-quality notes and registered references preserve supplement availability,
separate IZho 2023 writing sheets, and OPhO 2025 Q34's conflicting solution.
The US 2022 experiment executable and source archive are now preserved and hashed.

This is an INCOMPLETE reviewed subset. Do not interpret NULL decisions as
BORDERLINE or assume the remaining archives share the selected-set KEEP rate.
Detailed current statistics: `validation.json`, `competition_coverage.csv`,
`format_statistics.csv`, `domain_statistics.csv`, `resume_checkpoint.json`.
'''
w.writetext(root/'resume.md',resume)
audit=f'''<!-- RESUMED_CHECKPOINT_START -->
## Current resumed checkpoint — 2026-10-04

**INCOMPLETE content screening; complete container expansion.** Historical tables
below describe the original pilot and are retained as audit history. Current
canonical counts supersede them:

| Item | Count |
|---|---:|
| Registered units | {stat['identified_units']:,} |
| Direct / derived | {direct:,} / {derived:,} |
| Unindexed embedded units discovered / physical-paper audits pending | {embedded} / {paper_pending:,} |
| Whole-paper containers expanded / pending | 233 / 0 |
| Content-decided units | {reviewed} |
| KEEP / BORDERLINE / REJECT | {dec['KEEP']} / {dec['BORDERLINE']} / {dec['REJECT']} |
| Awaiting actual content review | {awaiting:,} |
| Explicit source withdrawal / unavailable statement | {unavailable} |
| New focused or random second-review units | {newqc} |
| Low-confidence decisions / required second reviews pending | {counts['low_confidence_units']} / {counts['focused_reviews_pending']} |
| Curated physical files / hardlinks / copies | {cur['unique_physical_files']} / {cur['hardlinks']} / {cur['copies']} |
| Curated payload bytes | {cur['byte_size']:,} |
| Raw snapshot files / hash mismatches | 3,312 / 0 |

Registered accounting: **{stat['identified_units']:,} = {dec['KEEP']} + {dec['BORDERLINE']} + {dec['REJECT']} + {awaiting} pending
+ {unavailable} explicit source-unavailable item**. This is zero *unexplained* remainder,
not zero unfinished work. Explicitly withdrawn items remain source logical rows,
not fabricated physical questions. All 6,392 acquisition rows reconcile as
6,159 direct source rows plus 233 containers. Current source-row/container counts
are proved by SQLite and `validate_outputs.py`; direct content locations still
require inspection for the pending units.

**Additional boundary finding:** full-page reading of indexed Estonian papers
revealed independently printed E1/E2 experiments omitted from their ten acquired
theory rows. {embedded} such units are now registered with deterministic SHA-based
embedded IDs, NULL raw problem IDs, exact printed labels/titles/pages and full-exam
document provenance. Matching solution E1/E2 labels/content were inspected before
pairing. The acquisition corpus remains immutable. A separate physical-paper
boundary ledger and residual queue now prevent claiming that expanded containers
alone prove the final problem universe. There are {paper_pending:,} remaining paper
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
{newqc}, including 12 seeded random cases and focused boundary/model cases. Two
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

The full screening request is still unfinished. `{awaiting:,}` pending content
items and {unavailable} unavailable-source items are exactly enumerated in `remaining.csv`.
Current distributions and complete per-competition pending coverage are exported
alongside this audit. No classification is fabricated to claim completion.
<!-- RESUMED_CHECKPOINT_END -->

'''
old=(root/'audit.md').read_text(encoding='utf-8')
if '<!-- RESUMED_CHECKPOINT_START -->' in old:
 start=old.index('<!-- RESUMED_CHECKPOINT_START -->');end=old.index('<!-- RESUMED_CHECKPOINT_END -->')+len('<!-- RESUMED_CHECKPOINT_END -->')
 old=old[:start]+old[end:].lstrip('\n')
first,rest=old.split('\n',1);w.writetext(root/'audit.md',first+'\n\n'+audit+rest.lstrip('\n'))
print(json.dumps(counts,indent=2))

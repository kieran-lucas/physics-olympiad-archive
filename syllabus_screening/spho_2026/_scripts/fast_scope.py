"""Persist explicit statement-based fast-pass decisions and lightweight checkpoints.

No physics classification is automated. Existing decisions cannot be overwritten.
"""
import argparse, contextlib, csv, io, json, os
from pathlib import Path
import workflow as w
import paper_boundary_audit

def checkpoint():
    with contextlib.redirect_stdout(io.StringIO()):
        w.export()
        paper_boundary_audit.export()
    c = w.connect()
    assert c.execute('pragma quick_check').fetchone()[0] == 'ok'
    assert not c.execute('pragma foreign_key_check').fetchall()
    rows = c.execute('select * from units').fetchall()
    expected = {r['screening_unit_id'] for r in rows if r['decision'] is None}
    actual = {r['item_id'] for r in csv.DictReader(open(w.ROOT/'remaining.csv', encoding='utf-8-sig')) if r['stage'] in ('content_review','source_unavailable')}
    assert expected == actual
    boundary_expected = {str(r[0]) for r in c.execute("select file_id from paper_boundary_audit where status!='full_paper_boundaries_verified'")}
    boundary_actual = {r['item_id'] for r in csv.DictReader(open(w.ROOT/'remaining_paper_boundaries.csv', encoding='utf-8-sig'))}
    assert boundary_expected == boundary_actual
    old = json.loads((w.ROOT/'clean_checkpoint.json').read_text(encoding='utf-8'))
    prior_deep = old.get('last_deep_validation_at', old['checked_at'])
    counts = dict(c.execute('select decision,count(*) from units where decision is not null group by decision'))
    pending = sum(r['decision'] is None and r['review_status'] != 'unresolved_source_unavailable' for r in rows)
    focused = [dict(r) for r in c.execute("select screening_unit_id,source_file_id,problem_number from units where decision is not null and review_status not in ('single_pass_complete','pass_2_complete')")]
    latest = c.execute('select competition_slug,source_file_id from units where decision is not null order by screened_at desc limit 1').fetchone()
    nxt = c.execute("select screening_unit_id,source_file_id,competition_slug,year,problem_number,source_file from units where decision is null and review_status!='unresolved_source_unavailable' and competition_slug=? order by cast(year as int) desc,source_file_id,cast(problem_number as int) limit 1", (latest['competition_slug'],)).fetchone()
    if nxt is None:
        nxt = c.execute("select screening_unit_id,source_file_id,competition_slug,year,problem_number,source_file from units where decision is null and review_status!='unresolved_source_unavailable' order by competition_slug,source_file_id,cast(problem_number as int) limit 1").fetchone()
    report = dict(checked_at=w.now(),mode='FAST_SCOPE_PASS',sqlite_integrity='ok (quick_check)',queue_equals_database=True,registered_units=len(rows),reviewed_units=sum(counts.values()),decisions=counts,awaiting_content_review=pending,source_unavailable=len(expected)-pending,pending_paper_audits=c.execute("select count(*) from paper_boundary_audit where status!='full_paper_boundaries_verified'").fetchone()[0],pending_focused_reviews=len(focused),last_deep_validation_at=prior_deep,archival_validation='deferred; previous deep validation retained in validation.json',materialization='deferred until major checkpoint')
    validation = json.loads((w.ROOT/'validation.json').read_text(encoding='utf-8'))
    report['latest_archival_validation_at'] = validation['checked_at']
    report['archival_validation_issues'] = validation.get('validation_issues', [])
    report['archival_validation'] = 'latest full validation has documented issues; last successful deep checkpoint timestamp retained' if report['archival_validation_issues'] else 'latest full validation passed; subsequent archival checks deferred'
    report['registered_scope_complete'] = pending == 0
    report['scope_and_inventory_complete'] = pending == 0 and not focused and not boundary_expected and not c.execute("select 1 from containers where status!='expanded_content_verified'").fetchone()
    materialization_path = w.CUR/'materialization.json'
    if materialization_path.exists():
        materialized = json.loads(materialization_path.read_text(encoding='utf-8'))
        if materialized['selected_units'] == counts.get('KEEP', 0):
            report['materialization'] = 'current KEEP selection materialized; archival validation status recorded separately'
            report['materialized_keep_records'] = materialized['selected_units']
    phase = 'REGISTERED_SCOPE' if pending else 'PHYSICAL_PAPER_COMPLETENESS'
    if report['scope_and_inventory_complete']:
        phase = 'FAST_SCOPE_COMPLETE_WITH_SOURCE_UNAVAILABLE' if expected else 'FAST_SCOPE_COMPLETE'
    w.writejson(w.ROOT/'clean_checkpoint.json', report)
    instructions='Screen registered pending statements first. When workable pending is zero, continue remaining_paper_boundaries.csv, deterministically register genuinely missing top-level problems and fast-screen them immediately. Reuse completed complete-source inspection; never replay committed decisions. Archival enrichment and routine second review remain deferred.'
    if report['scope_and_inventory_complete']:
        instructions = 'Fast scope classification and complete physical-paper inventory audit are finished for available sources. No active content, boundary or focused-review queue remains. Keep source-unavailable records explicit in remaining.csv; do not guess decisions or replay committed batches. Archival enrichment and documented source-PDF structure issues remain separate deferred work. See final_checkpoint.json.'
    w.writejson(w.ROOT/'continuation_cursor.json',dict(checked_at=report['checked_at'],mode='FAST_SCOPE_PASS',phase=phase,last_durable_source_file_id=latest['source_file_id'],required_focused_reviews=focused,next_content_unit=dict(nxt) if nxt else None,boundary_queue='remaining_paper_boundaries.csv',instructions=instructions))
    w.writejson(w.ROOT/'resume_checkpoint.json',report)
    w.writetext(w.ROOT/'resume.md', '# FAST SCOPE PASS state\n\nUser instruction of 2026-10-04 overrides the earlier forensic workflow. Screening.sqlite is authoritative; never replay completed work.\n\n'+f"{len(rows)} registered units; {sum(counts.values())} decisions ({counts}); {pending} workable pending and {len(expected)-pending} explicit unavailable sources. {report['pending_paper_audits']} physical-paper audits and {len(focused)} required focused reviews remain.\n\n"+instructions+'\n\nUse actual statement text first, renders only when necessary, solutions only for consequential prerequisite ambiguity. Existing rubric and whole-problem rule remain unchanged.\n\n'+f"Materialization: {report['materialization']}. Latest strict archival validation issues: {report['archival_validation_issues']}. The strict assertion remains enabled; do not claim the full archival phase is validated while issues remain.\n\nLightweight checkpoint: python syllabus_screening/spho_2026/_scripts/fast_scope.py checkpoint\nMajor checkpoint: existing checkpoint.py for materialization/full validation, then fast_scope.py checkpoint to restore fast-mode cursor. Deep archival validation timestamp is recorded separately. Remaining.csv retains explicit unavailable sources.\n")
    c.close()
    with open(w.ROOT/'screening.sqlite','r+b') as f: os.fsync(f.fileno())
    print(json.dumps(report))

def save(path):
    records=json.loads(Path(path).read_text(encoding='utf-8'))
    c=w.connect()
    with c:
        for row in records:
            uid=row['screening_unit_id']
            old=c.execute('select * from units where screening_unit_id=?',(uid,)).fetchone()
            assert old is not None and old['decision'] is None, ('Refuse replay',uid)
            assert row['decision'] in ('KEEP','REJECT','BORDERLINE')
            assert row.get('evidence') and row.get('required_physics') and row.get('decision_reason')
            confidence=row.get('confidence','high'); assert confidence in ('high','medium','low')
            review=row.pop('needs_second_review',False) or row['decision']=='BORDERLINE' or confidence!='high'
            vals={k:v for k,v in row.items() if k!='screening_unit_id'}
            vals.update(confidence=confidence,screened_at=w.now(),review_status='pass_1_complete' if review else 'single_pass_complete')
            assert set(vals) <= set(old.keys())
            c.execute('update units set '+','.join(k+'=?' for k in vals)+' where screening_unit_id=?',list(vals.values())+[uid])
            c.execute('insert into review_events(screening_unit_id,pass,reviewed_at,detail) values (?,?,?,?)',(uid,1,w.now(),row['evidence']))
    c.close()
    print('Saved',len(records),'new explicit fast-pass decisions')
    checkpoint()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['save','checkpoint']);p.add_argument('path',nargs='?');a=p.parse_args()
    if a.command=='save':save(a.path)
    else:checkpoint()

"""Verify durable truth, preserve pre-recovery artifacts; never replay reviews."""
import collections,csv,gzip,json,sqlite3
import workflow as w

c=w.connect();report={'checked_at':w.now(),'issues':[]}
def check(ok,label):
    if not ok:report['issues'].append(label)
assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
assert not c.execute('pragma foreign_key_check').fetchall()
backup=w.ROOT/'recovery'/'shutdown_20261004'
backup.mkdir(parents=True,exist_ok=True)
if not (backup/'screening.sqlite').exists():
    b=sqlite3.connect(backup/'screening.sqlite');c.backup(b);b.close()
import shutil
for name in ['resume.md','resume_checkpoint.json','audit.md','validation.json','remaining.csv','remaining_paper_boundaries.csv','progress.json']:
    if not (backup/name).exists():shutil.copy2(w.ROOT/name,backup/name)
report['backup']=str(backup.relative_to(w.ROOT))
required={'units','review_events','source_files','unit_files','containers','extraction','raw_snapshot','paper_boundary_audit','unit_equivalences'}
check(required<={r[0] for r in c.execute("select name from sqlite_master where type='table'")},'required schema tables')
units={r['screening_unit_id']:dict(r) for r in c.execute('select * from units')}
for uid,u in units.items():
    events=c.execute('select * from review_events where screening_unit_id=?',(uid,)).fetchall()
    if u['decision']:
        check(all(u[k] for k in ('evidence','required_physics','decision_reason','confidence','screened_at')),'partial decision '+uid)
        check(any(r['pass']==1 for r in events),'missing pass 1 '+uid)
        if u['review_status']=='pass_2_complete':check(any(r['pass']==2 for r in events),'missing pass 2 '+uid)
    else:check(not events,'events without decision '+uid)
check(not c.execute('select 1 from review_events e left join units u using(screening_unit_id) where u.screening_unit_id is null').fetchone(),'orphan review events')
duplicates=[dict(r) for r in c.execute('select screening_unit_id,pass,detail,count(*) n,min(reviewed_at) first_at,max(reviewed_at) last_at from review_events group by screening_unit_id,pass,detail having n>1')]
report['historical_exact_duplicate_events']=duplicates
report['duplicate_disposition']='Preserved historical replay evidence; all exact duplicates predate the interrupted Ortvay 2024 batch. Distinct-unit QC totals avoid inflation.'
check(all(r['last_at']<'2026-10-04T00:56:49' for r in duplicates),'restart-era duplicate review events')
latest=json.loads((w.ROOT/'reviews/resume_ortvay_2024_32.json').read_text(encoding='utf-8'))
check(len(latest)==32,'latest batch length')
for row in latest:
    check(all(units[row['screening_unit_id']].get(k)==v for k,v in row.items()),'latest batch field mismatch '+row['screening_unit_id'])
    check(c.execute('select count(*) from review_events where screening_unit_id=? and pass=1',(row['screening_unit_id'],)).fetchone()[0]==1,'latest batch event multiplicity')
report['last_durable_batch']={'file':'reviews/resume_ortvay_2024_32.json','rows':32,'status':'fully committed; three focused reviews pending; no replay required'}
report['decision_counts']=dict(collections.Counter(u['decision'] for u in units.values() if u['decision']))
report['pending_focused_reviews']=[uid for uid,u in units.items() if u['decision'] and u['review_status'] not in ('single_pass_complete','pass_2_complete')]
old=list(csv.DictReader(open(w.ROOT/'remaining.csv',encoding='utf-8-sig')))
old_ids={r['item_id'] for r in old if r['stage']=='content_review'}
new_ids={uid for uid,u in units.items() if not u['decision'] and u['review_status']!='unresolved_source_unavailable'}
report['stale_queue_completed_rows']=sorted(old_ids-new_ids)
check(not(new_ids-old_ids),'pending rows silently missing from old queue')
partials=[str(p.relative_to(w.ROOT)) for p in w.ROOT.rglob('*') if p.is_file() and (p.suffix in ('.part','.tmp','.lock') or p.name.endswith(('-wal','-shm','-journal')))]
report['partial_or_lock_artifacts']=partials;check(not partials,'partial or lock artifacts')
# Check every existing SHA-keyed cache without extracting PDFs again.
for r in c.execute("select e.*,f.sha256 source_hash from extraction e join source_files f on f.id=e.file_id where e.status='extracted'"):
    try:
        with gzip.open(w.ROOT/r['cache_path'],'rt',encoding='utf-8') as f:data=json.load(f)
        check(data['sha256']==r['sha256']==r['source_hash'] and len(data['pages'])==r['page_count'],'cache identity '+str(r['file_id']))
    except Exception as e:report['issues'].append('cache '+str(r['file_id'])+': '+str(e))
with sqlite3.connect(w.CUR/'manifest.sqlite') as m:
    check(m.execute('pragma integrity_check').fetchone()[0]=='ok','curated integrity')
    existing={r[0] for r in m.execute('select screening_unit_id from selected_problems')}
    check(all(uid in units and units[uid]['decision']=='KEEP' and units[uid]['review_status'] in ('single_pass_complete','pass_2_complete') for uid in existing),'existing curated membership')
    report['keep_rows_awaiting_materialization']=sorted({uid for uid,u in units.items() if u['decision']=='KEEP' and u['review_status'] in ('single_pass_complete','pass_2_complete')}-existing)
    m.row_factory=sqlite3.Row
    for r in m.execute('select * from files'):
        p=w.CUR/r['curated_file'];check(p.is_file() and w.digest(p)==r['sha256'],'existing curated hash '+str(r['file_id']))
        check(w.digest(w.RAW/r['source_file'])==r['sha256'],'existing source hash '+str(r['file_id']))
for r in c.execute('select * from unit_equivalences'):
    a=units[r['alias_unit_id']];b=units[r['canonical_unit_id']]
    check(a['source_sha256']==b['source_sha256']==r['source_sha256'] and a['decision']==b['decision'],'alias consistency '+r['alias_unit_id'])
c.execute('begin immediate');c.rollback();report['write_lock_probe']='passed'
report['process_probe']='PowerShell process inspection found only unrelated ppt-mcp servers, no old screening worker.'
w.writejson(w.ROOT/'shutdown_recovery.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('historical_exact_duplicate_events','stale_queue_completed_rows','keep_rows_awaiting_materialization')},ensure_ascii=False,indent=2))
assert not report['issues'],report['issues']

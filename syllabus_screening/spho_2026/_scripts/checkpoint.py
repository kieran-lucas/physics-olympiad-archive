"""Refresh and validate a small durable review checkpoint, without replaying it."""
import contextlib,csv,json,os,re,subprocess,sys
import workflow as w
import paper_boundary_audit as p

log=w.ROOT/'reviews'/('checkpoint_'+w.now().replace(':','').replace('+','_')+'.log')
with open(log,'w',encoding='utf-8') as output,contextlib.redirect_stdout(output):
    p.export();w.export();w.materialize()
    for name in ('validate_outputs.py','update_resume_checkpoint.py'):
        result=subprocess.run([sys.executable,str(w.ROOT/'_scripts'/name)],capture_output=True,text=True,encoding='utf-8')
        output.write(result.stdout);output.write(result.stderr);output.flush()
        if result.returncode:
            raise RuntimeError(name+' failed; see '+str(log)+'\n'+result.stderr)
    w.snapshot(check=True)
    output.flush();os.fsync(output.fileno())
c=w.connect()
expected=set()
for u in c.execute('select * from units'):
    if not u['decision']:
        expected.add(('source_unavailable' if u['review_status']=='unresolved_source_unavailable' else 'content_review',u['screening_unit_id']))
    elif u['review_status'] not in ('single_pass_complete','pass_2_complete'):expected.add(('second_review',u['screening_unit_id']))
for r in c.execute("select file_id from paper_boundary_audit where status!='full_paper_boundaries_verified'"):
    expected.add(('paper_boundary_audit',str(r[0])))
for r in c.execute("select source_problem_id from containers where status!='expanded_content_verified'"):
    expected.add(('top_level_boundary_review',str(r[0])))
actual={(r['stage'],r['item_id']) for r in csv.DictReader(open(w.ROOT/'remaining.csv',encoding='utf-8-sig'))}
assert actual==expected,(expected-actual,actual-expected)
boundaries={r['item_id'] for r in csv.DictReader(open(w.ROOT/'remaining_paper_boundaries.csv',encoding='utf-8-sig'))}
assert boundaries=={uid for stage,uid in expected if stage=='paper_boundary_audit'}
v=json.loads((w.ROOT/'validation.json').read_text(encoding='utf-8'))
raw=json.loads((w.ROOT/'raw_immutability_check.json').read_text(encoding='utf-8'));assert raw['unchanged']
report={'checked_at':w.now(),'sqlite_integrity':c.execute('pragma integrity_check').fetchone()[0],
        'queue_equals_database':True,'boundary_queue_equals_database':True,'raw_unchanged':True,
        'validation_issues':v['validation_issues'],'registered_units':v['identified_top_level_units'],
        'reviewed_units':v['reviewed_units'],'awaiting_content_review':v['awaiting_content_review'],
        'pending_paper_audits':len(boundaries),'pending_focused_reviews':sum(s=='second_review' for s,u in expected)}
w.writejson(w.ROOT/'clean_checkpoint.json',report)
# Keep the curated entrance text in sync with its authoritative selection manifest.
cur=json.loads((w.CUR/'materialization.json').read_text(encoding='utf-8'))
readme=w.CUR/'README.md';text=readme.read_text(encoding='utf-8')
text=re.sub(r'\d+ reviewed KEEP (?:problems|records \(\d+ distinct verified questions\))',str(cur['selected_units'])+' reviewed KEEP records ('+str(cur['verified_distinct_selected_questions'])+' distinct verified questions)',text)
text=re.sub(r'\d+ unique original physical files',str(cur['unique_physical_files'])+' unique original physical files',text)
w.writetext(readme,text)
# Persist the ongoing competition cursor from actual pending rows, never infer decisions.
latest=c.execute('select competition_slug,source_file_id from units where decision is not null order by screened_at desc limit 1').fetchone()
focused=[dict(r) for r in c.execute("select screening_unit_id,source_file_id,problem_number from units where decision is not null and review_status not in ('single_pass_complete','pass_2_complete') order by source_file_id,cast(problem_number as int)")]
next_unit=c.execute("select screening_unit_id,source_file_id,competition_slug,year,problem_number,source_file from units where decision is null and review_status!='unresolved_source_unavailable' and competition_slug=? order by cast(year as int) desc,source_file_id,cast(problem_number as int) limit 1",(latest['competition_slug'],)).fetchone()
if next_unit is None:
    next_unit=c.execute("select screening_unit_id,source_file_id,competition_slug,year,problem_number,source_file from units where decision is null and review_status!='unresolved_source_unavailable' order by competition_slug,source_file_id,cast(problem_number as int) limit 1").fetchone()
w.writejson(w.ROOT/'continuation_cursor.json',{'checked_at':report['checked_at'],'last_durable_source_file_id':latest['source_file_id'],'required_focused_reviews':focused,'next_content_unit':dict(next_unit) if next_unit else None,'boundary_queue':'remaining_paper_boundaries.csv','instructions':'Finish required focused checks, then inspect the next physical source completely using existing cache and renders. Decisions, aliases and boundaries remain authoritative in screening.sqlite. Never replay historical record scripts.'})
c.close()
for path in (w.ROOT/'screening.sqlite',w.CUR/'manifest.sqlite',w.ROOT/'clean_checkpoint.json'):
    with open(path,'r+b') as f:os.fsync(f.fileno())
print(json.dumps(report,indent=2))

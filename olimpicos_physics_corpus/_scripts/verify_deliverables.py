import sqlite3,csv,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
r=Path('olimpicos_physics_corpus').resolve();c=sqlite3.connect(r/'manifest.sqlite')
required=['manifest.sqlite','competitions.csv','problems.csv','documents.csv','files.csv','ai_manifest.csv','missing_or_unavailable.csv','errors.csv','audit.md']
assert all((r/f).is_file() and (r/f).stat().st_size for f in required)
for name in ['competitions','problems','documents','files']:
 rows=list(csv.DictReader((r/(name+'.csv')).open(encoding='utf-8-sig')));expected=c.execute('select count(*) from '+name).fetchone()[0];assert len(rows)==expected,(name,len(rows),expected)
ai=list(csv.DictReader((r/'ai_manifest.csv').open(encoding='utf-8-sig')));assert len(ai)==c.execute('select count(*) from problems').fetchone()[0]
paths=set()
for row in ai:
 assert row['problem_file_path'],row['source_problem_key']
 paths.update(p for p in [row['problem_file_path'],row['solution_file_path']] if p)
 paths.update(json.loads(row['other_relevant_files']))
assert all((r/p).is_file() for p in paths)
err=list(csv.DictReader((r/'errors.csv').open(encoding='utf-8-sig')));assert len(err)==5 and all(x['status']=='source_content_mismatch' and x['entity']=='source' for x in err)
assert len(list(csv.DictReader((r/'missing_or_unavailable.csv').open(encoding='utf-8-sig'))))==5124
assert not list(csv.DictReader((r/'metadata/residual_queue.csv').open(encoding='utf-8-sig')))
assert len(list(csv.DictReader((r/'metadata/residual_issues.csv').open(encoding='utf-8-sig'))))==5
recon=json.loads((r/'reports/discovery_reconciliation.json').read_text(encoding='utf-8'))
expected_competitions=len(json.loads((r/'metadata/competitions_discovered.json').read_text(encoding='utf-8')))
assert len(recon)==expected_competitions and all(not x['missing_urls'] and not x['extra_urls'] and not x['year_difference'] and x['logical_rows_match'] and x['bands_match'] for x in recon)
assert c.execute('pragma integrity_check').fetchone()[0]=='ok' and not c.execute('pragma foreign_key_check').fetchall()
assert c.execute("select count(*) from competitions where discovery_status='processed'").fetchone()[0]==expected_competitions
sizes=sum(p.stat().st_size for p in r.rglob('*') if p.is_file())
report=dict(required_deliverables_present=True,csv_counts_match_database=True,ai_rows=len(ai),referenced_ai_paths_verified=len(paths),unresolved_source_errors=5,unavailable_record_rows=5124,remaining_acquisitions=0,all_competition_reconciliations_match=True,total_corpus_bytes=sizes)
(r/'reports/deliverable_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))

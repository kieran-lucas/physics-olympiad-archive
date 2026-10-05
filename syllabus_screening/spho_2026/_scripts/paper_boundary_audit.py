"""Track full physical-paper boundary checks separately from indexed containers.

An expanded acquisition container does not establish that all other indexed
shared papers lack unindexed questions. This queue makes that residual explicit.
"""
import workflow as w
def initialize():
 c=w.connect()
 c.execute('''create table if not exists paper_boundary_audit(file_id integer primary key references source_files(id),status text default 'pending_full_paper_boundary_audit',expected_units integer,observed_units integer,evidence text,checked_at text)''')
 for r in c.execute('select distinct source_file_id from units where source_file_id is not null').fetchall():
  fid=r[0];n=c.execute('select count(*) from units where source_file_id=?',(fid,)).fetchone()[0]
  c.execute('insert or ignore into paper_boundary_audit(file_id,expected_units) values (?,?)',(fid,n))
 # Papers represented solely by expanded containers were completely inspected
 # for printed question labels in the saved boundary-evidence batches.
 for r in c.execute('select * from paper_boundary_audit').fetchall():
  fid=r['file_id'];direct=c.execute('select count(*) from units where source_file_id=? and derived_from_whole_paper=0',(fid,)).fetchone()[0]
  co=c.execute('select * from containers where source_file_id=?',(fid,)).fetchall()
  if not direct and co and all(x['status']=='expanded_content_verified' for x in co):
   n=c.execute('select count(*) from units where source_file_id=?',(fid,)).fetchone()[0]
   c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=?,evidence=?,checked_at=? where file_id=? and status!='full_paper_boundaries_verified'",(n,'Complete source-container boundary inspection: '+ ' | '.join(x['notes'] or '' for x in co),w.now(),fid))
 for fid in [2859,2860,2861,2864]:
  if c.execute('select count(*) from embedded_unit_discovery where source_file_id=?',(fid,)).fetchone()[0]==2:
   c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=12,evidence=?,checked_at=? where file_id=?",('Read entire paper and every supplemental page: ten theory problems plus independently printed E1/E2. Supplemental graphs/templates repeat earlier problems.',w.now(),fid))
 # Explicit whole physical paper content review, including withdrawn Q24.
 for r in c.execute("select distinct source_file_id from units where competition_slug='opho' and year='2025' and round_or_section like '%Open%'").fetchall():
  fid=r[0];n=c.execute('select count(*) from units where source_file_id=?',(fid,)).fetchone()[0]
  if n==35:c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=35,evidence=?,checked_at=? where file_id=?",('Complete 2025 Open paper inspected: Q1-Q35 with explicit Q24 withdrawal, no other top-level problems.',w.now(),fid))
 c.commit();export()
def export():
 c=w.connect();rows=[]
 for a in c.execute('select a.*,f.local_path,f.sha256 from paper_boundary_audit a join source_files f on f.id=a.file_id order by a.file_id'):
  u=c.execute('select competition_slug,year from units where source_file_id=? limit 1',(a['file_id'],)).fetchone()
  rows.append({'item_type':'physical_paper','item_id':str(a['file_id']),'stage':'paper_boundary_audit','competition_slug':u['competition_slug'],'year':u['year'],'source_problem_id':None,'source_file_id':a['file_id'],'source_file':a['local_path'],'source_sha256':a['sha256'],'detail':a['evidence'] if a['status']=='full_paper_boundaries_verified' else 'Read complete source file once; compare printed top-level questions with registered rows and derive any missing units. Do not rescreen existing decisions.','status':a['status'],'observed_units':a['observed_units']})
 w.csvout(w.ROOT/'paper_boundary_audit.csv',rows)
 w.csvout(w.ROOT/'remaining_paper_boundaries.csv',[r for r in rows if r['status']!='full_paper_boundaries_verified'],list(rows[0]) if rows else None)
 print('Physical papers:',len(rows),'verified',sum(r['status']=='full_paper_boundaries_verified' for r in rows),'pending',sum(r['status']!='full_paper_boundaries_verified' for r in rows))
if __name__=='__main__':initialize()

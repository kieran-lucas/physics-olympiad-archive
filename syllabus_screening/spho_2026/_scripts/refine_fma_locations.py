"""Source-inspected inclusive MCQ page locations; no decision changes."""
import workflow as w
c=w.connect()
groups={2:range(1,4),3:range(4,7),4:range(7,10),5:range(10,13),6:range(13,15),7:range(15,18),8:range(18,20),9:range(20,24),10:range(24,26)}
for fid in [1909,1918]:
 for u in c.execute('select * from units where source_file_id=?',(fid,)).fetchall():
  assert u['decision']=='KEEP';n=int(u['problem_number'])
  page=n+1 if fid==1909 else next(p for p,ns in groups.items() if n in ns)
  c.execute('update units set page_start=?,page_end=? where screening_unit_id=?',(page,page,u['screening_unit_id']))
c.commit();print('Refined 50 MCQ page locations from inspected source papers.')

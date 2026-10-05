"""Explicit source-verified maps for the last 25 containers."""
import workflow as w
c=w.connect();out=[]
maps={
1695:([1,1,1,1,2,2,2,3],[1,1,1,1,2,2,3,3]),
1703:([1,1,1,2,3,4],[1,1,2,2,4,4]),
1704:([1,1,1,1,2,2],[1,1,1,2,2,3]),
4003:([2,3,4,5,6],None),4004:([2,3,5,6,7],[2,4,5,6,8]),4005:([2,3,4,5,6],None),
4006:([2,4,5,6,8],[3,4,5,7,8]),4007:([2,4,6],[3,5,7]),4008:([2,3,4,6,7],[2,3,5,6,7]),
4009:([2,4,5,7,9],[3,4,6,8,10]),4010:([2,5,7],[4,6,7]),4011:([2,3,4,5,6],None),
4012:([2,4,5,6,7],[3,4,5,6,8]),4013:([2,4,5],[4,5,8]),4014:([2,2,4,4,5],[2,4,4,5,6]),
4015:([2,2,4,6,6],[2,4,6,6,7]),4016:([2,3,4],[3,4,5]),4017:([2,3,5,6,7],[2,4,5,6,7]),
4018:([2,3,4,6,7],[3,4,6,6,7]),4019:([1,2,3],[2,3,4]),
3998:([2,2,3,5,6,6],[2,3,4,5,6,7]),3999:([2,2,3,4,5,6],[2,3,4,5,6,7]),
4000:([2,2,3,4,4,5],[2,3,4,4,5,5]),4001:([2,2,4,5,5,6],[2,4,4,5,6,6])}
for pid,(starts,ends) in maps.items():
 r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone();assert r['status']=='pending_boundary_review'
 ends=ends or starts
 nums=list('一二三四五六七八')[:len(starts)] if pid in (1695,1703,1704) else [str(n) for n in range(1,len(starts)+1)]
 loc={'boundary_note':'All rendered statement pages inspected for source grand-question headings. Internal lettered/numbered parts kept; conservative inclusive page ranges retain shared pages.','page_range_precision':'conservative_until_content_review'}
 if pid in (1695,1703,1704):loc['combined_source_solution_section']=[max(ends)+1,len(w.cache(r['source_file_id'])['pages'])]
 out.append(dict(source_problem_id=pid,boundary_evidence='Source cover counts and printed first-level question labels verified visually. Repeated bold versions of a Chinese question and reference solutions are not additional units.',units=[dict(number=n,page_start=s,page_end=e,format='theory',location=loc) for n,s,e in zip(nums,starts,ends)]))
# This one physical document contains five distinct examinations, not only the first cover's five questions.
pid=4002;r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone();assert r['status']=='pending_boundary_review'
us=[]
for session,prefix,starts,ends,fmt,date in [
 ('筆試(一)','W1',[2,3,4,5,7],[2,3,4,6,7],'theory','2024-03-30'),
 ('筆試(二)','W2',[9,10,11,12,13],[9,10,11,12,13],'theory','2024-04-02'),
 ('理論模擬','T',[15,16,18],[16,17,20],'theory','2024-04-03'),
 ('實驗模擬(一)','E1',[22],[24],'experimental','2024-04-01'),
 ('實驗模擬(二)','E2',[26],[31],'experimental','2024-04-01')]:
 for n,(s,e) in enumerate(zip(starts,ends),1):
  number=prefix+'P'+str(n) if fmt=='theory' else prefix
  us.append(dict(number=number,page_start=s,page_end=e,format=fmt,location={'source_session':session,'source_date':date,'printed_problem_number':str(n) if fmt=='theory' else prefix[-1],'page_range_precision':'conservative_until_content_review','boundary_note':'Separate exam cover verified. Experimental Q1-1/Q1-2 and Q2-1/Q2-2 labels are pages of one experiment, not separate tasks.'}))
out.append(dict(source_problem_id=pid,boundary_evidence='All 31 rendered pages inspected: five distinct exam covers, five plus five written problems, three theory-simulation problems, and two experiments. Repeated page labels within each experiment retained as one top-level experiment.',units=us))
p=w.ROOT/'reviews/resume_final_25_boundaries.json';w.writejson(p,out);w.derive(p)
for r in out:c.execute("update units set boundary_status='top_level_count_verified_location_pending' where source_problem_id=? and decision is null",(r['source_problem_id'],))
for u in c.execute('select * from units where source_problem_id=4002').fetchall():
 import json
 loc=json.loads(u['location_json']);c.execute('update units set problem_number=?,round_or_section=? where screening_unit_id=?',(loc['printed_problem_number'],(u['round_or_section']+' / '+loc['source_session']+' / '+loc['source_date']).strip(' /'),u['screening_unit_id']))
c.commit();print('New top-level units:',sum(len(r['units']) for r in out));print('All containers:',c.execute('select status,count(*) from containers group by status').fetchall());print('Total registered:',c.execute('select count(*) from units').fetchone()[0])

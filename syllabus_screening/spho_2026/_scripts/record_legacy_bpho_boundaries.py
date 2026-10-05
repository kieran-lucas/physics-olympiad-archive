"""Explicit legacy British paper boundary inventory; no content classification."""
import json
import workflow as w
c=w.connect();out=[]
accepted={2573:[1],2574:[2,3,4,5,6],2576:[1],2577:list(range(2,10)),2578:list(range(1,7)),2580:list(range(1,7)),2581:list(range(1,6)),2582:[1],2583:list(range(2,9)),2584:list(range(1,6)),2585:[1],2586:list(range(2,10)),2587:[1,2,3],2588:[1],2589:list(range(2,10)),2590:[1,2],2591:[1],2592:list(range(2,10)),2594:[1,2,3,4],2596:[1,2,3,4],2598:[1,2,3,4,5],2600:[1,2,3,4],2602:[1,2,3,4],2604:[1,2,3,4],2606:[1,2,3,4,5,6]}
for r in json.loads((w.ROOT/'reviews/bpho_legacy_boundary_candidates.json').read_text(encoding='utf-8')):
 pid=r['pid']
 if pid not in accepted:continue
 hits=[];seen=set()
 for h in r['hits']:
  if int(h['number']) not in accepted[pid] or h['number'] in seen:continue
  seen.add(h['number']);hits.append(h)
 assert [int(h['number']) for h in hits]==accepted[pid],pid
 units=[]
 for i,h in enumerate(hits):
  units.append({'number':h['number'],'page_start':h['page'],'page_end':hits[i+1]['page'] if i+1<len(hits) else r['page_count'],'format':'theory',
   'location':{'heading_text':h['heading'],'heading_bbox':h['bbox'],'boundary_note':'Retain all lettered/decimal internal parts; repeated Q1.a/Q1.b markers are the same problem. Conservative end page, to refine during physics content review.','page_range_precision':'conservative_until_content_review'}})
 out.append({'source_problem_id':pid,'boundary_evidence':'Reviewed cached original Q-number headings across the paper. Repeated subpart markers, footer page numbers and numerical data excluded. 2010 cover explicitly confirms only two questions. Physics content remains pending.','units':units})
out.append({'source_problem_id':2579,'boundary_evidence':'Source begins Section 1 on page 3, followed only by lettered parts (a)...; retain this entire source section as one unnumbered top-level unit.','units':[{'number':'Section1','page_start':3,'page_end':7,'format':'theory','title':'Section 1','location':{'source_label_present':False,'heading_text':'Section 1','boundary_note':'All lettered parts retained; no question number invented.'}}]})
path=w.ROOT/'reviews/resume_legacy_bpho_boundaries.json';w.writejson(path,out);w.derive(path)
for r in out:c.execute("update units set boundary_status='top_level_count_verified_location_pending' where source_problem_id=? and decision is null",(r['source_problem_id'],))
c.execute('update units set problem_number=NULL where source_problem_id=2579 and derived_from_whole_paper=1');c.commit()
print('New legacy British units',sum(len(r['units']) for r in out))

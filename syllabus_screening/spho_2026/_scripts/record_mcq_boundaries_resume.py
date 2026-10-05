"""Explicitly accepted numbered MCQ inventories, including visually verified gaps."""
import json
import workflow as w
c=w.connect();candidates=json.loads((w.ROOT/'reviews/mcq_boundary_candidates.json').read_text(encoding='utf-8'));out=[]
# These labels/pages were verified on rendered source pages, not inferred from gaps.
fixes={4058:{28:17},4059:{1:3,2:3},4064:{45:21,50:23},4067:{25:11},4069:{17:8,28:12},4070:{19:9}}
accepted_sjpo=[4056,4057,4058,4059,4061,4062,4063,4064,4065,4066,4067,4068,4069,4070,4071]
accepted_kphc={4072:15,4073:15,4076:30,4077:30,4078:30,4080:20,4081:20}
for r in candidates:
 pid=r['pid']
 if pid not in accepted_sjpo and pid not in accepted_kphc:continue
 count=50 if pid in accepted_sjpo else accepted_kphc[pid]
 hits=[h for h in r['hits'] if 1<=int(h['number'])<=count]
 if pid==4071:hits=[h for h in hits if not (h['number']=='12' and h['page']==11)] # resistance value 120 ohm, not question 12
 for n,p in fixes.get(pid,{}).items():hits.append({'number':str(n),'page':p,'heading':f'{n}. [source label verified visually]','bbox':None})
 hits.sort(key=lambda h:int(h['number']))
 assert [int(h['number']) for h in hits]==list(range(1,count+1)),pid
 units=[]
 for i,h in enumerate(hits):
  units.append({'number':h['number'],'page_start':h['page'],
   'page_end':hits[i+1]['page'] if i+1<len(hits) else r['page_count'],'format':'multiple_choice',
   'location':{'heading_text':h['heading'],'heading_bbox':h['bbox'],
     'boundary_note':'One numbered MCQ, not its options. Conservative inclusive end page; refine end/shared-stem start during content inspection.',
     'page_range_precision':'conservative_until_content_review','visual_boundary_verification':int(h['bbox'] is None)}})
 out.append({'source_problem_id':pid,'boundary_evidence':f'Reviewed full source numbering 1-{count}; cover instructions excluded. Visual gap repairs are recorded explicitly. Physics decisions remain pending; shared stems must be retained during content inspection.','units':units})
path=w.ROOT/'reviews/resume_mcq_boundaries.json';w.writejson(path,out);w.derive(path)
for r in out:c.execute("update units set boundary_status='top_level_count_verified_location_pending' where source_problem_id=? and decision is null",(r['source_problem_id'],))
c.commit();print('New numbered MCQ units',sum(len(r['units']) for r in out))

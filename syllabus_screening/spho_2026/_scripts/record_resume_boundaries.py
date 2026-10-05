"""Commit explicit paper-boundary acceptances after cached source-heading review.

This derives inventory only. No KEEP/BORDERLINE/REJECT decisions are generated.
"""
import re,json
import workflow as w
c=w.connect();out=[]
pattern=re.compile(r'^\s*(?:Problem|Question|Qu)\s*(\d+)(?:\.(?!\d))?(?:\s|$)')
def headers(pid,expected,last_page=None):
 r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone()
 assert r and r['status']=='pending_boundary_review'
 d=w.cache(r['source_file_id']); hits=[]
 for p in d['pages']:
  if last_page and p['page']>last_page:break
  for block in p['blocks']:
   for line in block[4].splitlines():
    m=pattern.match(line)
    if not m:continue
    if line.strip().startswith('Qu 6 if'):continue
    hits.append((m.group(1),p['page'],line.strip(),block[:4]))
 assert [h[0] for h in hits]==[str(n) for n in expected],(pid,hits,expected)
 units=[]
 for i,(num,page,heading,bbox) in enumerate(hits):
  end=last_page or len(d['pages'])
  if i+1<len(hits):
   following=hits[i+1]
   # Retain a shared boundary page when the next heading follows earlier content.
   end=max(page,following[1]-(following[3][1]<110))
  units.append({'number':num,'page_start':page,'page_end':end,'format':'theory',
   'location':{'heading_text':heading,'heading_bbox':bbox,'next_heading_text':hits[i+1][2] if i+1<len(hits) else None,
    'boundary_note':'Source top-level numbered heading; all internal decimal/lettered parts remain grouped. Shared-page heading anchors delimit neighboring problems.'}})
 if pid==888:
  for u in units:u['location']['additional_language_versions']={'Kazakh_offset_pages':6,'Russian_offset_pages':12}
 if pid==890:
  alternate=[{'Kazakh':[8,9],'Russian':[16,16]},{'Kazakh':[10,12],'Russian':[17,18]},{'Kazakh':[13,14],'Russian':[19,20]}]
  for u,v in zip(units,alternate):u['location']['additional_language_versions']=v
 out.append({'source_problem_id':pid,'boundary_evidence':'Reviewed cached top-level source headings, sequential numbering and cover instructions; decimal and lettered subparts excluded. Only boundary inventory reviewed, physics remains pending.','units':units})

# Complete heading lists were inspected for these English Chinese-final transcriptions.
for pid,count in {1682:7,1683:6,1684:7,1685:6,1686:5,1687:7,1688:6,1689:8,1690:8,1691:8,1692:8,1693:8,1694:8}.items():headers(pid,range(1,count+1))
# British papers: Section 1's lettered general questions remain ONE source question.
bpho={2545:[1,2,3,4],2546:[1],2547:[2,3,4,5],2548:[1,2,3,4],2549:[1],2550:[2,3,4,5],2551:[1,2,3,4],2552:[1],2553:[2,3,4,5],2554:[1,2,3,4],2555:[1],2556:[2,3,4,5],2557:[1,2,3,4],2558:[1],2559:[2,3,4,5,6],2560:[1,2,3,4],2561:[1],2562:[2,3,4,5,6],2563:[1,2,3,4],2564:[1],2565:[2,3,4,5,6],2566:[1,2,3,4,5],2567:[1],2568:[2,3,4,5,6],2569:[1,2,3,4,5],2570:[1],2571:[2,3,4,5,6,7,8],2572:[1,2,3,4,5],2575:[1,2,3,4,5]}
for pid,nums in bpho.items():headers(pid,nums)
# Zhautykov theory has three top-level tasks, even when task 1 has unrelated parts.
for pid in [884,886,888,890,892,894,896,898,900,901,903,905,907,909,910,912,914]:
 headers(pid,[1,2,3],6 if pid in (888,890) else None)

def experiment(pid,start,end,title,note,number='E',extra=None):
 u={'number':number,'page_start':start,'page_end':end,'format':'experimental','title':title,
    'location':{'source_label_present':number!='E','boundary_note':note,**(extra or {})}}
 out.append({'source_problem_id':pid,'boundary_evidence':note+' Boundary inventory only; scope decision remains pending.','units':[u]})
experiment(885,2,4,'Torsion: Construction of the Potential Curve','Cover explicitly states one experimental problem; Parts 1-4 are internal stages.')
experiment(887,2,5,'Galvanic cells','Cover explicitly states one experimental problem; industrial and homemade cells are stages of the one experiment.')
experiment(889,2,4,'Superposition of oscillations','Cover states one problem. Physical PDF includes the same experiment in three languages; no duplicate screening units.',extra={'additional_language_versions':{'Kazakh':[6,8],'Russian':[10,12]}})
experiment(895,1,3,'A mathematical pendulum or what angle can be considered rather small ...','One titled computer experiment with numbered internal modeling/measurement steps.')
experiment(897,2,3,'Maxwell’s Disc','Cover explicitly states one experimental problem; motion down/up are internal stages.')
experiment(899,2,4,'Absorption of light','Cover explicitly states one experimental problem; photodetector calibration and absorption measurement remain grouped.')
experiment(902,2,3,'Torsion pendulum','Cover explicitly states one experimental problem; small/large twists are internal stages.')
experiment(904,2,2,'Coal tablet','Cover explicitly states one experimental problem.')
experiment(906,2,3,'Resistance of graphite','Cover explicitly states one experimental problem; temperature dependence and cooling remain grouped.')
experiment(908,2,3,'Magnetic interactions','Cover explicitly states one experimental problem; interaction measurements are internal stages.')
experiment(911,2,4,'Electric currents in volume','Cover explicitly states one experimental problem; geometry and electrode-distance investigations remain grouped.')
experiment(913,2,4,'Deformation, Hysteresis, and Bistability','Cover explicitly states one experimental problem; internal theoretical and measured stages remain grouped.')
experiment(915,2,3,'Slow motion','Cover explicitly states one experimental problem; different rod-diameter tests remain grouped.')
# The 2022 experimental cover instead explicitly states TWO experiments.
out.append({'source_problem_id':893,'boundary_evidence':'Cover explicitly states two problems; Experiment 1 precedes Experiment 2: Rolling friction on page 3. Internal numbered steps are not separate problems.','units':[
 {'number':'1','page_start':1,'page_end':2,'format':'experimental','location':{'heading_text':'Experiment 1','boundary_note':'Includes experiment introduction and table on page 2.'}},
 {'number':'2','page_start':3,'page_end':4,'format':'experimental','title':'Rolling friction','location':{'heading_text':'Experiment 2: Rolling friction'}}]})
path=w.ROOT/'reviews/resume_boundaries_1.json';w.writejson(path,out);w.derive(path)
# E is a deterministic internal unit suffix, not an invented printed question number.
for r in out:
 for u in r['units']:
  if u['number']=='E':c.execute('update units set problem_number=NULL where source_problem_id=? and derived_from_whole_paper=1',(r['source_problem_id'],))
c.commit()
print('Newly identified units:',sum(len(r['units']) for r in out))

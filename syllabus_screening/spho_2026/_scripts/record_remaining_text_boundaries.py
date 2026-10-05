"""Source-grounded explicit remaining text and initial scan boundary maps."""
import workflow as w
c=w.connect();out=[]
def add(pid,starts,ends=None,nums=None,fmt='theory',note='',titles=None):
 r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone();assert r['status']=='pending_boundary_review'
 d=w.cache(r['source_file_id']);nums=nums or list(range(1,len(starts)+1));ends=ends or starts[1:]+[len(d['pages'])]
 assert len(nums)==len(starts)==len(ends)
 units=[]
 for i,(num,start,end) in enumerate(zip(nums,starts,ends)):
  assert 1<=start<=end<=len(d['pages'])
  units.append({'number':str(num),'page_start':start,'page_end':end,'format':fmt,'title':titles[i] if titles else None,
   'location':{'source_label_present':str(num)!='E','boundary_note':note,'page_range_precision':'conservative_until_content_review'}})
 out.append({'source_problem_id':pid,'boundary_evidence':note+' This is a boundary inventory, not a physics decision.','units':units})

add(1679,[2,4,5],[3,4,6],note='2022 theoretical cover states three problems. Titled Take Five, Chain Reaction and Lego Movie are the top-level units; explicitly unrelated numbered parts remain internal.',titles=['Take Five','Chain Reaction','Lego Movie'])
add(1680,[1],[4],nums=['E'],fmt='experimental',note='Cover explicitly says single simulation-based lab. Disk-wall and disk-disk measurements are internal stages.',titles=['The Future Circular Collider'])
add(1681,[2,5,8],[4,7,10],note='2021 USAPhO+ Question 1, Question 2 and Question 3 source headings verified.')
add(891,[2],[4],nums=['E'],fmt='experimental',note='Rendered 2023 experimental cover says one problem. Fourier spectrometer stages 1-4 are internal.',titles=['Fourier spectrometer'])
add(2593,[2,5,6,7,8,9,10,11],[4,5,6,7,8,9,10,11],note='All scanned pages visually inspected for Q1-Q8. Page 12 is blank; Q1 general lettered parts remain one problem.')
add(2595,[2,5,6,7,8,9,10,11],[4,5,6,7,8,9,10,11],note='Scanned cover explicitly says eight questions; all Q1-Q8 headings visually verified. Archive 2007 exam date and printed 2008 competition label both retained in provenance.')
add(3996,[3,4,4,5,5,6],[3,4,5,5,6,7],nums=list('一二三四五六'),note='Rendered Taiwan 2015 cover states six grand questions; Chinese labels 一 through 六 verified. Prefatory formula list excluded; all internal lettered parts retained.')
add(3997,[3,4,5,6,7,8],[3,4,5,6,7,9],nums=list('一二三四五六'),note='Chinese first-level headings 一 through 六 verified in embedded text; internal numbered tasks remain grouped.')
# Older Chinese originals often combine statements followed by numbered solutions.
for pid,starts,last,nums in [
 (1696,[1,1,1,1,2,2,3,3],4,list('一二三四五六七八')),
 (1697,[1,1,2,3,3,4,5,6],6,list('一二三四五六七八')),
 (1698,[1,2,3,4,5,6,7],7,list('一二三四五六七')),
 (1699,[1,1,2,3,5,5,6],6,list('一二三四五六七')),
 (1700,[1,1,1,2,3,4,4],4,list('一二三四五六七')),
 (1701,[1,1,1,2,3,4],4,list('一二三四五六')),
 (1702,[2,2,3,4,5,6,7],7,list(range(1,8)))]:
 add(pid,starts,starts[1:]+[last],nums=nums,note='Reviewed first-level source question headings across the statement section. Subsequent reference-solution headings are not new units. The source grand fill-in problem retains its internal numbered parts, consistently with British general-question bundles.')
 if pid in [1697,1698,1699,1700]:
  for u in out[-1]['units']:u['location']['combined_source_solution_section']=[last+1,len(w.cache(c.execute('select source_file_id from containers where source_problem_id=?',(pid,)).fetchone()[0])['pages'])]
 if pid in [1697,1698]:out[-1]['units'][0]['format']='short_answer'
# Korean 2021/2020 layout is two independent questions in parallel columns per page.
for pid in [4074,4075]:
 starts=[2+(n-1)//2 for n in range(1,31)]
 add(pid,starts,starts,fmt='multiple_choice',note='Reviewed two-column source numbering: questions 1-30, two per physical page 2-16. Parallel text-column reading order does not change question numbers; parameters/figures still require visual physics review.')
starts=[2,2,3,3,4,5,5,6,7,7,8,9,9,10,10,11,12,12,13,13,14,14,15,16,16,17,17,18,19,20]
add(4079,starts,starts,fmt='multiple_choice',note='Korean 2016 original explicitly has 【문제1 】 through 【문제30 】; spaces before closing brackets are source formatting, not missing questions.')
path=w.ROOT/'reviews/resume_remaining_text_boundaries.json';w.writejson(path,out);w.derive(path)
for r in out:
 c.execute("update units set boundary_status='top_level_count_verified_location_pending' where source_problem_id=? and decision is null",(r['source_problem_id'],))
 for u in r['units']:
  if u['number']=='E':c.execute('update units set problem_number=NULL where source_problem_id=? and derived_from_whole_paper=1',(r['source_problem_id'],))
c.commit();print('Additional units:',sum(len(r['units']) for r in out))

"""Explicit source-heading/page maps reviewed in the resumed boundary pass."""
import json
import workflow as w
c=w.connect();out=[]
def paper(pid,starts,fmt='theory',last=None,numbers=None,context=''):
 r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone();assert r['status']=='pending_boundary_review'
 d=w.cache(r['source_file_id']);units=[];numbers=numbers or list(range(1,len(starts)+1))
 for i,(number,start) in enumerate(zip(numbers,starts)):
  units.append({'number':str(number),'page_start':start,'page_end':starts[i+1] if i+1<len(starts) else (last or len(d['pages'])),'format':fmt,
   'location':{'source_top_level_label':str(number),'boundary_note':context+' Inclusive page ranges are conservative until actual physics content review; lettered/decimal internal parts remain grouped.','page_range_precision':'conservative_until_content_review'}})
 out.append({'source_problem_id':pid,'boundary_evidence':'Inspected source cover counts and actual top-level question/section headings and page transitions. '+context+' Physics content remains pending.','units':units})

# Singapore national papers (distinct from Vietnamese SPhO calibration).
for pid,starts in {
4020:[1,1,2,3,4,5,5,6,6],4021:[3,6,8,11,13,16,19,23,26,27],4022:[3,6,9,11,13],4023:[3,5,7,9,11],4024:[3,4,5,6,7],4025:[3,4,5,6,7],4026:[2,4,6,8,10,12,14,17,20,24],4027:[2,3,5,6,7,10,12,14,16],4028:[2,4,6,8,10],4029:[2,4,8,11,13],4030:[2,4,6,7,8],4031:[2,7,9,15],4032:[2,4,6,8],4034:[3,4,5,6,7,8,9,10,11],4040:[1,1,1,2,2,2,2,3,3,3],4041:[2,2,2,2,2,2,3,3,4,4],4042:[2,2,2,2,3,3,3,3],4043:[2,3,4],4044:[2,3,3,4],4045:[2,3,3,4]
}.items():
 paper(pid,starts,last=3 if pid==4040 else None,context='Repeated same-number (a)/(b) headers are continuations, not new units.'+(' File also includes solutions on pages 4-11.' if pid==4040 else ''))
paper(4033,[2,6,10],last=15,numbers=[5,6,7],context='Cover says three questions; printed question labels are 5, 6 and 7, preserved without renumbering.')
# Singapore team-selection tests: all top-level numeric roots, not internal sections.
for pid,starts in {4046:[2,2,3,4,5,7,8,9,9,11],4047:[2,2,3,3,5,6,9,10,12],4048:[3,3,4,4,5,7,8,9,10],4049:[3,3,4,4,5,6,6,7],4050:[3,3,3,4,5,6,8,9,9],4051:[3,3,4,5,5,6,7,7,8,9],4052:[3,3,4,5,5,5],4053:[3,5,6,6,7,9,9],4054:[3,4,5,5,6,7,9,11]}.items():paper(pid,starts,context='Cover/contents counts reconciled to source numeric or Question headings; contents entries not duplicated.')
# Australian older mixed papers explicitly enumerate ten MCQs followed by long questions.
au={4088:[2,2,2,3,3,4,4,5,5,5,6,8,10,11],4089:[2,2,3,3,3,4,4,4,4,5,6,8,9,10],4090:[2,2,2,3,3,3,4,4,5,5,6,8,9,10],4091:[2,2,3,3,4,4,4,5,5,6,7,8,10,11],4092:[2,2,2,3,3,4,4,5,5,5,6,7,9,10],4093:[2,2,2,3,3,3,4,4,4,4,5,7,8,9],4095:[2,2,3,3,4,4,5,5,5,6,7,8,9,10],4096:[2,2,3,3,3,4,4,5,5,6,7,8,10,11],4097:[2,2,3,3,3,4,4,5,6,6,7,8,9,10,12],4100:[2,2,3,3,3,4,4,4,5,5,6,8,9,10,11,12]}
for pid,starts in au.items():
 paper(pid,starts,context='Cover specifies ten multiple-choice items followed by numbered written questions. Question 11 continued in 2007 is not a new problem. Australian 2013 Q9/Q10 share a printed line.')
 for i,u in enumerate(out[-1]['units']):u['format']='multiple_choice' if i<10 else 'theory'
paper(4082,[3,7,12,16],context='Four explicitly numbered long problems, retain all stages and lettered questions.')
paper(4083,[3,4,6,9,10],numbers=['A','B','C','D','E'],context='Five independently titled source sections with reset internal numbering; internal dependent questions are subparts of the section problem.')
paper(4084,[3,5,13,18,22],numbers=['A','B','C','D','E'],context='Five independently titled source sections; internal numbered tasks remain grouped.')
def modern_au(pid,mcstarts,longstarts,letters,extra=None):
 starts=mcstarts+longstarts;nums=['A'+str(i) for i in range(1,11)]+letters
 paper(pid,starts,numbers=nums,context='Section A contains ten independent MCQs. Named long sections remain whole problems; explicitly independent questions in Unusual Physics are distinct units.')
 for i,u in enumerate(out[-1]['units']):
  if i<10:u['format']='multiple_choice';u['location']['source_top_level_label']=str(i+1);u['location']['section']='A'
  elif extra and u['number'] in extra:u['location']['source_top_level_label']=extra[u['number']];u['location']['section']='E'
modern_au(4085,[3,3,3,3,4,4,4,5,5,5],[6,13,17,20,20,21],['B','C','D','E1','E2','E3'],{'E1':'1','E2':'2','E3':'3'})
modern_au(4086,[3,3,4,5,5,6,7,7,8,9],[10,11,13,18,20],['B','C','D','E','F'])
modern_au(4087,[3,3,4,4,5,5,6,6,7,8],[9,12,16,17],['B','C','D','E'])
path=w.ROOT/'reviews/resume_english_boundaries.json';w.writejson(path,out);w.derive(path)
for r in out:
 c.execute("update units set boundary_status='top_level_count_verified_location_pending' where source_problem_id=? and decision is null",(r['source_problem_id'],))
 for u in r['units']:
  if 'section' in u['location']:
   internal=w.connect().execute('select source_sha256 from containers where source_problem_id=?',(r['source_problem_id'],)).fetchone()[0][:16]
   uid='derived::'+internal+'::'+str(r['source_problem_id'])+'::'+u['number']
   c.execute("update units set problem_number=?,round_or_section=round_or_section||' / Section '||? where screening_unit_id=?",(u['location']['source_top_level_label'],u['location']['section'],uid))
c.commit();print('New English-paper units:',sum(len(r['units']) for r in out))

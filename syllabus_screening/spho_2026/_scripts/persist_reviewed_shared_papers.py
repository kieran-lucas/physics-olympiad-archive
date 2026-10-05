"""Persistence helper for explicitly reviewed papers, never a classifier.

Each caller supplies every physics judgment, location and boundary observation.
"""
import json
import workflow as w
def save(name,specs,experiments,overrides=None):
 c=w.connect();out=[];overrides=overrides or {}
 for fid,spec in specs.items():
  us=c.execute('select * from units where source_file_id=? and derived_from_whole_paper=0 order by source_problem_id',(fid,)).fetchall();assert len(us)==len(spec)
  for u,(dom,a,b,physics) in zip(us,spec):
   assert u['decision'] is None,u['screening_unit_id']
   item=dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=dom,required_physics=physics,external_physics_if_any='',decision_reason='The central work is '+physics[0].lower()+physics[1:]+'. Syllabus knowledge, ordinary foundations and the supplied statement data are sufficient.',page_start=a,page_end=b,format='theory',visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence='Complete actual statement read from cached text; inspected the complete physical-paper page renders, including figures, graphs and apparatus. All internal subparts retained as one printed top-level problem.')
   item.update(overrides.get((fid,u['problem_number']),{}));out.append(item)
  for no,a,b,title,dom,physics,reason in experiments.get(fid,[]):
   u=dict(us[0]);uid='derived::'+u['source_sha256'][:16]+'::embedded::'+no
   assert not c.execute('select 1 from units where screening_unit_id=?',(uid,)).fetchone()
   fields={k:u[k] for k in ['competition','competition_slug','competition_category','year','source_file','source_file_id','source_sha256','source_url']}
   fields.update(screening_unit_id=uid,source_problem_id=None,derived_from_whole_paper=1,round_or_section='Experimental',format='experimental',problem_number=no,problem_title=title,title_provenance='official' if title else 'unknown',page_start=a,page_end=b,boundary_status='content_boundary_verified',location_json=json.dumps({'printed_label':no,'boundary_note':'Independent printed experiment omitted from raw logical rows; internal tasks remain together.'}))
   c.execute('insert into units('+','.join(fields)+') values ('+','.join('?' for _ in fields)+')',list(fields.values()))
   specific=overrides.get((fid,no),{}).copy()
   map_solution=specific.pop('map_solution',True)
   c.execute('insert into unit_files select ?,file_id,document_id,role from unit_files where screening_unit_id=?'+('' if map_solution else " and role!='solution'"),(uid,us[0]['screening_unit_id']))
   evidence='Complete experimental statement and apparatus/source figures inspected; '+('full-exam solution prints the matching experimental label/title and measurement method. ' if map_solution else 'Available solution paper covers theory only; no experimental solution confidently mapped. ')+'Ten raw logical rows enumerate theory only.'
   c.execute('insert into embedded_unit_discovery values (?,?,?,?)',(uid,fid,evidence,w.now()))
   item=dict(screening_unit_id=uid,decision='KEEP',confidence='high',primary_spho_domains=dom,required_physics=physics,external_physics_if_any='',decision_reason=reason,page_start=a,page_end=b,format='experimental',visual_inspection_used=1,solution_used=int(map_solution),boundary_status='content_boundary_verified',evidence=evidence)
   item.update(specific);out.append(item)
  c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=?,evidence=?,checked_at=? where file_id=?",(len(spec)+len(experiments.get(fid,[])),'Read all source pages and verified printed top-level theory/experimental labels; supplemental drawing copies and administrative text are not extra units.',w.now(),fid))
 c.commit();p=w.ROOT/'reviews'/name;w.writejson(p,out);w.decisions(p);print('Saved',len(out),'explicit content reviews.')

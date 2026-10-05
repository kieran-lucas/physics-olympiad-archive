"""Explicit seeded/focused QC after re-reading actual statements and solutions."""
import json
import workflow as w
c=w.connect()
# Evidence flags reflect actually displayed page images, not mere rendering.
sets={2839:{'AH','BA','CE','CF','DC','DF','DH','EA','ED','EE','GA','GD','GE','GH','HB'},2840:{'BA','BF','BG','CC','DB','DC','EC','EG','EH','FD','FE','FF','FG','GB','GC','GE','GF','GG','GH'}}
for fid,labels in sets.items():
 for u in c.execute('select screening_unit_id,problem_number from units where source_file_id=?',(fid,)).fetchall():
  c.execute('update units set visual_inspection_used=? where screening_unit_id=?',(int(u['problem_number'] in labels),u['screening_unit_id']))
queue=json.loads((w.ROOT/'reviews/resume_fma_fyziklani_seeded_qc_queue.json').read_text(encoding='utf-8'))
details=[
 'Wakeboard force is expressly normal and static buoyancy is specified; ordinary component balance suffices. KEEP confirmed.',
 'The penetration-depth relation is supplied in the statement. Scaling impact work with kinetic energy requires no material-impact theory. KEEP confirmed.',
 'The source yo-yo figure and changing string radius specify the kinematic constraint; ordinary rotational energy determines acceleration. KEEP confirmed.',
 'The thin spherical shell asks only the Newtonian gravitational field jump. It does not invoke relativistic gravity. KEEP confirmed.',
 'The uniform coating assumption makes nacho coverage an area-ratio model. It is foundational geometry practice, with no invented SPhO domain assigned. KEEP confirmed under the core prerequisite test.',
 'Supplied cutting energy and two Coulomb friction forces leave a gravitational-work balance. KEEP confirmed.',
 'Spring length and fixed rope geometry determine pulley loading by Hooke law and static balance. KEEP confirmed.',
 'The bubble volume stays fixed in the rigid filled tube; hydrostatic head and the isothermal trapped gas are general physics. KEEP confirmed.'
]
events=[{'screening_unit_id':r['screening_unit_id'],'detail':'Seed 2026100402 content QC: '+detail} for r,detail in zip(queue,details,strict=True)]
u=c.execute("select * from units where source_file_id=2839 and problem_number='EA'").fetchone()
events.append({'screening_unit_id':u['screening_unit_id'],'detail':'Focused kaon check: source/solution p32 explicitly gives relativistic dispersion in the statement. Equal pion energies plus energy/vector-momentum conservation determine the angle. This supplied-model KEEP is consistent with rejecting unsupplied chocolate-relativity in 2025.'})
u=c.execute("select * from units where source_file_id=2839 and problem_number='HB'").fetchone()
events.append({'screening_unit_id':u['screening_unit_id'],'detail':'Focused source/solution pp67-68 check: conducting-sphere enhancement follows equipotential boundary conditions and dipole superposition. Mathematical construction is demanding but all physical laws are ordinary electrostatics. KEEP confirmed.'})
c.commit();p=w.ROOT/'reviews/resume_fma_fyziklani_qc_10.json';w.writejson(p,events);w.review(p)
print('Saved 8 seeded random and 2 focused actual-content reviews; corrected image-use flags.')

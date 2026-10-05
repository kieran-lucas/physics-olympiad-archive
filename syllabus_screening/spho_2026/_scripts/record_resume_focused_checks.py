"""Focused and sampled QC; revise only new affected records, preserve original 205."""
import json
import workflow as w
c=w.connect();events=[]
def unit(pid,n):
 r=c.execute('select * from units where source_problem_id=? and problem_number=?',(pid,str(n))).fetchone();assert r and r['decision'];return r
def qc(pid,n,detail):events.append(dict(screening_unit_id=unit(pid,n)['screening_unit_id'],detail=detail))
# Full-size source pages exposed a mistaken subpart description; eligibility stays KEEP.
u=unit(4035,7)
c.execute('update units set required_physics=?,primary_spho_domains=?,decision_reason=? where screening_unit_id=?',('Heat capacity inferred from supplied temperature-time heating law; refractive-index profile of a thin graded-index lens','IV_thermodynamics;X_wave_optics','Both internal tasks use ordinary thermal energy balance and ray-optics optical-path reasoning; the empirical heating relation is supplied.',u['screening_unit_id']))
qc(4035,7,'Full-size page 4 correction: the source says a supplied heating power law and an impurity-made graded-index lens, not a two-level relaxation model. KEEP unchanged; physics description/domains corrected.')
# Exactly balanced 5+5 source marks, unlike the rough thumbnail interpretation.
u=unit(4035,8)
c.execute('update units set decision=?,confidence=?,decision_reason=?,review_status=? where screening_unit_id=?',('BORDERLINE','medium','The thermal dimensional-analysis task and meson momentum-transfer task have equal source marks. The latter may require unsupplied relativistic energy/momentum laws, although beta=0.1 permits a conventional approximation; the whole question sits near the scope boundary.','pass_1_complete',u['screening_unit_id']))
qc(4035,8,'Re-read full-size pages 4-5. Each internal part is explicitly 5 marks. Revised this new KEEP to BORDERLINE because conceptual usefulness is balanced and the slow-meson approximation is not stated. No original pilot record changed.')
u=unit(4036,5)
c.execute('update units set decision=?,confidence=?,decision_reason=?,review_status=? where screening_unit_id=?',('BORDERLINE','medium','The photon rocket needs unsupplied relativistic energy and momentum laws for its central setup, but a displayed target conservation equation makes several later algebraic parts self-contained. Neither clear rejection nor clear suitability is warranted for the whole task.','pass_1_complete',u['screening_unit_id']))
qc(4036,5,'Full-size page 3 review recognizes the displayed gamma*f+v*gamma*f=1 relation. Revised new REJECT to BORDERLINE: the hint supplies much of later algebra while initial physical justification still needs unsupplied relativity.')
qc(4064,48,'Reconsidered statement and official answer key file 2996 (Q48=E). The key asserts all listed device groups depend on quantum operation but supplies no explanation of semiconductor/device physics. Genuine prerequisite ambiguity remains BORDERLINE.')
c.execute('update units set solution_used=1 where screening_unit_id=?',(unit(4064,48)['screening_unit_id'],))
qc(1679,3,'Focused supplied-model audit with solution file 1932 pp12-17: escape energy, Newtonian orbits, dimensional radiation scaling, energy-loss differentiation and graph frequency suffice. The source explicitly ignores relativity; KEEP confirmed.')
c.execute('update units set solution_used=1 where screening_unit_id=?',(unit(1679,3)['screening_unit_id'],))
qc(2595,8,'Rechecked classical crossed-field majority and later explicitly supplied m(v). The extension is self-contained and does not displace the main Lorentz-force task. KEEP confirmed.')
# Random-seeded candidate selection is recorded; these chosen source pages were
# re-read in full during this audit (not automatically reviewed by this script).
qc(2601,7,'Full-size Q7 page 10: Compton scattering is explicitly in SPhO and the energy-momentum relation is supplied. No unsupplied frame-transformation theory needed. KEEP confirmed.')
qc(2605,8,'Full-size Q8 page 10: diffraction and radio interference dominate; pulsar extension uses rotation and propagation delay in a changed refractive medium. Exotic context does not require neutron-star microphysics. KEEP confirmed.')
qc(2597,4,'Full-size Q4 page 7 confirms the indentation power law is explicitly supplied. Graph validity, restitution and uncertainty are ordinary experiment/data reasoning. KEEP confirmed.')
qc(4037,6,'Full-size Q6 page 3 requires fields, charge densities and stream velocities in another relativistically moving frame. Those transformations are not supplied; REJECT confirmed.')
qc(4037,8,'Full-size Q8 page 3 actually specifies classical two-particle magnetic/Coulomb circular motion. No quantum filling or quantization is requested. KEEP confirmed, guarding against garbled thumbnail inference.')
qc(1695,'六','Full-size page 2 supplies dissociation fraction versus temperature, dissociation energy and internal-energy law. Thermodynamic energy balance needs no chemical-equilibrium theory. KEEP confirmed.')
qc(1704,'六','Full-size page 2 and continuation page 3: dynamic mass is merely named, not supplied as a function of velocity. Composite rest mass after absorption needs relativistic dynamics, central throughout. REJECT confirmed.')
c.execute('update units set source_quality_notes=? where source_problem_id=1680',('The simulation executable referenced inside the statement is not a document record in the acquired archive. Statement and official solution retained; performing the simulation requires the referenced program.',))
c.execute('update units set source_quality_notes=? where source_problem_id=891',('Statement refers to separate writing-sheet numerical graphs/tables not independently inventoried in acquisition. Associated solution retains worked numerical tables/graphs; standalone writing sheets not claimed present.',))
c.commit();p=w.ROOT/'reviews/resume_focused_visual_qc_13.json';w.writejson(p,events);w.review(p)
print('Reviewed',len(events),'focused/QC cases; 2 new decisions revised, original 205 untouched')

"""Persist actual seeded random page re-inspections and supplied-model checks."""
import json
import workflow as w
c=w.connect();events=[]
details={
'derived::48dc659e9e1bc1b2::2599::6':'Full-size page 10 re-read: annular particle flux, Coulomb closest approach and nucleus recoil require energy/momentum conservation. KEEP confirmed.',
'derived::13f583f4157c7811::4067::25':'Full-size page 11 MCQ and all options re-read: ordinary ice/steam latent-heat calorimetry. KEEP confirmed.',
'derived::68a927f32a6a8f22::4037::2':'Full-size page 2 re-read with block diagram and both internal cases: Newtonian tensions and friction. Source speed/acceleration wording conflict does not introduce external physics. KEEP confirmed.',
'raw::4264':'Cached complete cable-car statement re-read on physical page 7. Constraint geometry, work/energy and time integration suffice; no elastic/continuum cable theory is required. KEEP confirmed.',
'derived::aef53bc89bff7e1e::4038::10':'Full-size page 6 re-read: moving observer reverses apparent superluminal arrival order, then transforms rod length/orientation. Unsupplied Lorentz transformations are central; REJECT confirmed.',
'raw::4282':'Statement re-read alongside official solution pp33-34: WKB probability is introduced only in the solution, not supplied in the problem. Tunneling controls the fusion rate; REJECT confirmed.'}
selected=json.loads((w.ROOT/'reviews/resume_random_qc_candidates.json').read_text(encoding='utf-8'))
assert set(x['screening_unit_id'] for x in selected)==set(details)
events.extend(dict(screening_unit_id=x['screening_unit_id'],detail='Seed 20261004 random QC: '+details[x['screening_unit_id']]) for x in selected)
for uid,detail in [
('raw::4255','Supplied Hubble velocity law plus ordinary light-travel kinematics in official solution p6: cosmological context is self-contained, KEEP confirmed.'),
('raw::4265','Statement and solution p14 supply both hypothetical monopole relations. Faraday/Ohm/Biot-Savart and mechanical motion use in-scope physics; KEEP confirmed.'),
('raw::4279','Magnetization is explicitly in the SPhO syllabus; official solution p30 uses surface magnetization charges and elementary magnetic-force/stress balance. KEEP confirmed.'),
('raw::4281','Official solution pp31-33 explicitly identifies relativistic hidden momentum and imports a specialized prior result. This coupling is not in the statement; REJECT confirmed.'),
('raw::4284','Statement and official solution pp35-36 reviewed: hydrostatics, ideal gas, latent heat and saturation thermodynamics can generate the model. KEEP scope confirmed, while conflicting methane labels/constants are explicitly flagged as source-quality defects.')]:
 events.append(dict(screening_unit_id=uid,detail='Focused model review: '+detail))
p=w.ROOT/'reviews/resume_random_and_model_qc_11.json';w.writejson(p,events);w.review(p)
print('Recorded six random and five focused reviews')

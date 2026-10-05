"""Persist only the seeded and suspicious-case content checks actually performed."""
import json
import workflow as w
c=w.connect();out=[]
details={
'raw::5409':'Seeded QC: re-read complete printed Ortvay Q12 p4. The Morse interaction is explicit and the kinetic term is identifiable. Potential differentiation and Newtonian small vibrations give dispersion; no unsupplied quantum lattice theory is needed. KEEP confirmed.',
'raw::5422':'Seeded QC: re-read complete Ortvay Q25 pp11-12. The fitness model is supplied, but photon rocket acceleration, proper time and trajectory are not. Those relativistic laws control the entire interstellar distance. REJECT confirmed for prerequisites, not astronomy context.',
'raw::4535':'Seeded QC: re-read complete Brawl Q20 p18 and previously inspected apparatus. Rolling hoop inertia and spring energy give ordinary oscillations; the slope changes equilibrium but introduces no external theory. KEEP confirmed.',
'raw::4541':'Seeded QC: re-read complete Brawl Q26 p26. The square is symmetric around the straight wire, and vertical displacement leaves its magnetic flux unchanged. Ordinary induction symmetry and Newtonian fall suffice. KEEP confirmed.',
'raw::4536':'Seeded QC: re-read complete Brawl Q21 p19. The explicitly relativistic proton energy is given, but momentum as a function of energy is not. The official solution confirms relativistic momentum is essential to the requested B. REJECT confirmed.',
'raw::4563':'Focused supplied-model check: actual Brawl Q48 pp62-64 statement and solution use ideal-gas entropy and Boltzmann microstate counting, not quantum state evolution. The microstate-bin convention is recorded as a source quality note. KEEP confirmed.',
'raw::4566':'Focused supplied-model check: actual Brawl Q51 p71 gives torque proportional to rod curvature. Torque balance with that relation defines the deformation; elliptic integration is mathematics. No unsupplied beam constitutive law is required. KEEP confirmed.',
'raw::4567':'Focused supplied-model check: actual Brawl Q52 pp73-74 gives neutron cross-section, reaction energies, straight-track ranges and detection rule. Interaction probability and geometry suffice; detector semiconductor theory does not control the task. KEEP confirmed.'}
queue=json.loads((w.ROOT/'reviews/resume_ortvay_brawl_random_qc_queue.json').read_text(encoding='utf-8'))
assert {q['screening_unit_id'] for q in queue}==set(list(details)[:5])
for uid,detail in details.items():
 assert c.execute('select decision from units where screening_unit_id=?',(uid,)).fetchone()[0]
 out.append(dict(screening_unit_id=uid,detail=detail))
p=w.ROOT/'reviews/resume_ortvay_brawl_qc_8.json';w.writejson(p,out);w.review(p)
print('Saved five seeded QC checks plus three focused supplied-model checks; no decision changes.')

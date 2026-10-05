"""Second reading of one seeded high-confidence item from each of six papers."""
import json
import workflow as w
queue=json.loads((w.ROOT/'reviews/resume_fma_2020_2023_random_qc_queue.json').read_text(encoding='utf-8'))
details={
'raw::1040':'Seeded QC: complete 2023 Q17 re-read and actual pendulum diagram checked. Pivot-to-mass distances and uniform-rod integration determine inertia; KEEP confirmed without using competition reputation.',
'raw::1069':'Seeded QC: complete 2022 A Q15 re-read. Maximizing ballistic height at a fixed wall uses only projectile kinematics and differentiation. Mathematical optimization is not external physics; KEEP confirmed.',
'raw::1085':'Seeded QC: complete 2022 B printed Q6 re-read. Equal force work over a fixed distance and p^2/(2m) determine momentum scaling. Acquisition Q31 is correctly mapped to printed Q6; KEEP confirmed.',
'raw::1128':'Seeded QC: complete 2021 Q14 re-read. The force dependence is explicitly restricted to R, v and viscosity with units supplied, so dimensional analysis supplies scaling; no flagellar hydrodynamics is required. KEEP confirmed.',
'raw::1160':'Seeded QC: complete 2020 A Q12 re-read. The sole point mass and two pendulum lengths fix both periods, requiring no unsupplied rigid-body complication. KEEP confirmed.',
'raw::1175':'Seeded QC: complete 2020 B printed Q2 re-read. The rod inertia is supplied; rotating-axis geometry and ordinary mass integration determine the square-plate result. KEEP confirmed.'}
assert set(details)=={q['screening_unit_id'] for q in queue}
p=w.ROOT/'reviews/resume_fma_2020_2023_qc_6.json';w.writejson(p,[dict(screening_unit_id=uid,detail=detail) for uid,detail in details.items()]);w.review(p)
print('Six seeded MCQ QC readings confirmed; no changes.')

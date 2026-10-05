"""Persist source-inspected seeded and focused QC; no automatic classifications."""
import json
import workflow as w
c=w.connect(); events=[]
queue=json.loads((w.ROOT/'reviews/resume_efo_seeded_qc_queue.json').read_text(encoding='utf-8'))
details=[
 'Re-read E2: ping-pong ball oscillations and supplied apparatus dimensions permit buoyancy, restoring-force and frequency measurement reasoning; no specialized fluid theory is necessary.',
 'Re-read Q4 and rendered physical page 5: the supplied triangle, source A and focus F define a ray-optics lens construction. Both repeated diagrams are copies, not additional questions.',
 'Re-read Q8 including page 3 continuation: adding a concave lens to preserve camera field of view requires only thin-lens imaging and geometry.',
 'Re-read Q2: braking-distance geometry, frictional deceleration and initial kinetic energy are ordinary mechanics.',
 'Re-read Q6 and its graph: deep/shallow wave-speed laws are explicitly given; frequency, front spacing and limiting speed determine depth without unsupplied water-wave dispersion theory.',
 'Re-read Q10: the slider requires force balance, contact/friction constraints and mechanical energy; difficulty of the optimization is mathematical.',
 'Re-read Q1: blunt shears require torque and friction at contact; the familiar cutting context introduces no material-fracture theory.',
 'Re-read experiment E2: externally measured black-box capacitor/diode responses can be analyzed with basic circuit charge/current laws and qualitative rectification, without semiconductor band theory.',
 'Re-read Q10: proton motion in the supplied magnetic field follows Lorentz force, magnetic rigidity and induction; no relativistic or nuclear scattering model is asked.',
 'Re-read Q7 and supplied graph: bird-flight power is used as an empirical curve; work, power and energy determine the requested optimum without aerodynamics.',
 'Re-read Q9 including page 4: cylinder volumes, combustion assumptions and ideal-gas adiabatic exponent are supplied. Cycle energy/efficiency is ordinary thermodynamics.',
 'Re-read Q7 including circuit drawing on page 2: equivalent resistances and load power optimization require Kirchhoff/Ohm laws and algebra only.'
]
for row,detail in zip(queue,details,strict=True):
 events.append({'screening_unit_id':row['screening_unit_id'],'detail':'Seed 20261004 Estonian batch QC. '+detail+' KEEP confirmed.'})
focused=[
 (2872,'10',2874,'Official solution pp6-8 uses Kirchhoff load lines and the supplied thyristor I-V characteristic, including instability and branch jumps. Semiconductor microscopic theory is not required.'),
 (2876,'6',2877,'Official solution p5 uses the explicitly supplied deep/shallow wave laws and plotted front spacings. No derivation of hydrodynamic dispersion is required.'),
 (2861,'9',2863,'Official solution pp8-9 balances hemispheric forces, applies the explicitly supplied stress law and constant rubber volume, then ideal-gas reasoning. No unsupplied elastic continuum theory is required.'),
 (2880,'9',2881,'Official solution p5 analyzes the neuron as the statement-specified capacitor and two emf/resistance branches. Kirchhoff steady-state currents suffice; neurochemistry is unnecessary.'),
 (2901,'9',2902,'Official solution p6 derives equal coupling amplitudes by energy conservation and the phase relation by interference. No guided-mode or evanescent-field theory is required.'),
 (2899,'10',2900,'Official solution pp4-5 uses the given coupling intensity ratio, energy conservation and closed-ring optical phase resonance; the source supplies the device model.'),
 (2885,'E1',2886,'Official solution p6 derives wrap-friction force balance from ordinary Coulomb friction and differential geometry, then compares measured tensions. The mathematics does not constitute external specialized physics.'),
 (2884,'8',2875,'Official solution p5 treats displaced water mass, geometry and mechanical energy. No unsupplied fluid PDE or constitutive law controls the nested-cylinder motion.'),
]
for fid,num,solution,detail in focused:
 row=c.execute('select * from units where source_file_id=? and problem_number=?',(fid,num)).fetchone()
 assert row and row['decision']=='KEEP', (fid,num)
 assert c.execute("select 1 from unit_files where screening_unit_id=? and file_id=? and role='solution'",(row['screening_unit_id'],solution)).fetchone()
 c.execute('update units set solution_used=1 where screening_unit_id=?',(row['screening_unit_id'],))
 events.append({'screening_unit_id':row['screening_unit_id'],'detail':'Focused actual-statement/official-solution check. '+detail+' KEEP confirmed.'})
c.commit();p=w.ROOT/'reviews/resume_efo_qc_20.json';w.writejson(p,events);w.review(p)
print('Persisted',len(events),'actual QC events; decisions unchanged.')

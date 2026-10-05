"""Persist explicit reviews of all 56 printed statements; preserve raw inventory."""
import json
import workflow as w
c=w.connect();fid=2840
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
rows=[
('AA',[IV],'Water heat capacity and parallel heating power','Thermal energy balance and the two available powers determine the shortest heating time.'),
('AB',[I],'Escalator relative velocities and route times','Both travel alternatives follow ordinary velocity addition and distance/time reasoning.'),
('AC',[],'Dimensional consistency of fuel-consumption arithmetic','The supplied two cost estimates determine consumption by elementary unit-aware algebra; no external physics is necessary.'),
('AD',[I],'Constant deceleration and braking distance','The limiting acceleration is supplied; ordinary kinematics determines initial speed.'),
('AE',[II],'Dimensions of a stipulated gravity-wave dispersion form','The source gives the sole variables and power-law form. Dimensional analysis supplies the exponents without hydrodynamic wave theory.'),
('AF',[I],'Static friction versus hanging weight','Force balance and the static-friction threshold determine whether motion starts and the actual friction force.'),
('AG',[IV,XII],'Supplied fission and combustion energies per fuel mass','Energy conservation and molar particle counting compare fuel masses; reactor microphysics is not required.'),
('AH',[I,III],'Hydrostatic head and isothermal trapped gas','Rigid volume constraints, ordinary hydrostatics and ideal-gas reasoning determine the pressure change.'),
('BA',[VI],'Maximum electrical power density from a supplied graph','The polarization curve is explicitly plotted; maximizing voltage times current density requires no electrochemistry.'),
('BB',[IV],'Thermal expansion constrained by displacement accuracy','The STM is context only; linear expansion of the specified support is the entire physics.'),
('BC',[I],'Buoyant force and hydrostatic pressure in a density gradient','The bottom pressure supplies support force; the result follows force balance without unknown planetary or fluid theory.'),
('BD',[I,II],'Spring extension and pulley tension geometry','The prescribed rope length and Hooke-law spring determine the equilibrium force.'),
('BE',[VI],'Dimensional construction of conductance from universal constants','Only units of charge, action and conductance are needed; quantum tunneling is illustrative context rather than a prerequisite.'),
('BF',[I],'Near-surface circular orbit','Newtonian gravity and centripetal acceleration determine the projectile return time.'),
('BG',[I],'Volumetric transport in a specified peristaltic geometry','The drawing and negligible compressed volume specify the transport model; tube area and ring speed determine flow.'),
('BH',[I],'Projectile ranges and a landing interval','The three launch angles and pizza extent require ordinary ballistic kinematics.'),
('CA',[I],'Equal braking deceleration and residual speed','Kinematics or work-energy reasoning compares the two initial velocities over the same distance.'),
('CB',[II],'Doppler shift of periodic barking','Approaching and receding observed periods determine observer velocity with ordinary sound Doppler laws.'),
('CC',[I],'Connected blocks on three frictionless inclines','The rendered ropes, slopes and masses require Newton laws and common string acceleration.'),
('CD',[III,IV],'Ideal-gas fuel amount and ice warming/melting energy','All fuel heat, gas and ice properties are given; ordinary gas and phase-change calorimetry suffice.'),
('CE',[I],'Wheel torque and uphill force balance','No-slip wheel geometry and the available applied force determine the limiting slope.'),
('CF',[I],'Banked-track centripetal force','Gravity and circular acceleration determine the required rail-height difference.'),
('CG',[I],'Closest approach of two linearly moving points','Ordinary vector kinematics and mathematical minimization determine the time.'),
('CH',[I,II],'Spring-launch energy and spherical-Earth horizon geometry','Elastic energy and projectile height determine geometric visibility; the planetary story introduces no extra physics.'),
('DA',[I],'Inelastic collision, energy loss and projectile landing','Momentum conservation, the supplied loss fraction and falling time determine both launch speeds; retain the entire two-answer task.'),
('DB',[I],'Connected incline constraints and changed force balance','The different source slopes change the Newtonian common-acceleration condition; the diagram specifies the geometry.'),
('DC',[I],'Oblique cylinder rolling and rotational energy','Rigid-body kinetic energy and the no-slip geometrical constraint determine the acceleration component.'),
('DD',[I],'Planetary gravity and centrifugal change of weight','Uniform density and Newtonian gravity, with the measured pole/equator weight ratio, determine rotation period.'),
('DE',[I,II],'Spring centrifugal equilibrium and loss of finite radius','Hooke-law force balance gives the critical angular speed; no external nonlinear material law is required.'),
('DF',[IV],'Heating feedback and steady heat loss','Both thermostat and heat-loss laws are supplied; steady thermal energy balance determines the final temperature.'),
('DG',[III,IV],'Isothermal ideal-gas compression work','The slow thermal contact fixes the process; standard ideal-gas work integration suffices.'),
('DH',[I,II],'Spring-powered projectile and carousel timing','The two permitted spring stretches give projectile travel times and rotating-target phase constraints.'),
('EA',[I],'Rod-lifting torque and force minimization','The fixed pivot and hand position determine a purely static torque balance.'),
('EB',[I],'Sliding-to-rolling disk on a moving belt','Coulomb friction accelerates translation and rotation until the specified rolling condition is met.'),
('EC',[I],'Water projectile with changed nozzle geometry','The rendered apparatus and launch speed require geometry and gravity-driven flight, not fluid theory.'),
('ED',[I],'Direction of effective gravity on a rotating Earth','Newtonian gravity and centrifugal acceleration determine the angular deviation.'),
('EE',[VI],'Leakage resistance and capacitor discharge','Ordinary conductivity, parallel-plate capacitance and RC decay determine the time.'),
('EF',[I],'Free fall with explicitly supplied Coriolis acceleration','The noninertial acceleration law is given; first-order trajectory integration suffices.'),
('EG',[],'Relativistic moving mass and proper-time dilation','The entire shipment distance depends on unsupplied relativistic mass and time dilation. The official solution confirms those are central, not peripheral.'),
('EH',[I],'Four-pulley string constraints and Newton laws','The rendered nested pulley structure requires ordinary tension and acceleration constraints.'),
('FA',[I],'Moment-of-inertia redistribution and angular momentum','The source stipulates the original water distribution and final reservoir; rotational inertia and angular momentum suffice.'),
('FB',[VI,X,XI],'Electron acceleration, de Broglie diffraction and relativistic momentum','Diffraction and de Broglie waves are expressly in scope, but the official solution requires an unsupplied relativistic energy-momentum relation at 90 keV. The relativistic correction is intertwined with the single numerical answer, so suitability is borderline.'),
('FC',[I],'Acceleration-limited track shape and time optimization','Centripetal acceleration, path geometry and mathematical minimization determine the quickest orbit.'),
('FD',[I,II],'Hydrostatic restoring torque and rigid-body oscillations','The official solution integrates changing buoyancy and plate rotational inertia; it needs no advanced fluid PDE.'),
('FE',[X],'Eye-lens refraction and mirror image distance','The source gives refractive indices and dimensions; ordinary paraxial optics determines accommodation.'),
('FF',[I],'Centripetal normal force, friction and stopping time','Newtonian tangential deceleration and radial reaction lead to an ordinary differential equation.'),
('FG',[I],'Oblique elastic collision, constant drag and pocket geometry','The source specifies deceleration and neglects rotation; momentum transfer and work-energy determine minimum cue energy.'),
('FH',[I],'Impulse, rod rotation and immediate loss of contact','Linear/angular impulse and rigid-body endpoint velocities determine whether the whole pencil lifts.'),
('GA',[I],'Gravity of a homogeneous annular disk','Newtonian superposition and radial integration determine Saturn-ring force; no astronomical microphysics is required.'),
('GB',[I,II,VI],'Electrostatic-gravitational equilibrium and small oscillations','The charged square and bead define Coulomb forces; equilibrium and potential curvature determine oscillation frequency.'),
('GC',[X],'Ray refraction through a supplied index gradient','Layer-by-layer Snell law and the supplied integral determine the ray path; no specialized graded-medium theory is needed.'),
('GD',[I,III,VI],'Electrostatic plate attraction and isothermal gas pressure','Parallel-plate fields, force balance and the ideal-gas equation determine piston displacement.'),
('GE',[X],'Paraxial refraction and mirror reflection through a hemisphere','Tracing rays across ordinary refracting surfaces and the stated mirror determines the image; thick-element geometry is mathematical.'),
('GF',[VI],'Surface Ohm law, radial current spreading and superposition','The infinite sheet geometry reduces to current conservation and ordinary conductivity, not electronic band transport.'),
('GG',[I],'Variable-mass recoil from gravity-driven water outflow','The source explicitly stipulates the Torricelli outflow approximation; momentum conservation and mass integration determine recoil.'),
('GH',[II,VII,VIII],'Magnetic flux from supplied vector potential and Faraday induction','Both the vector potential and B=curl(A) are supplied; Stokes theorem and flux differentiation are ordinary Maxwell/induction tools.')]
f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
pack=json.loads((w.ROOT/'cache'/f'{f["sha256"]}.statement_pack.json').read_text(encoding='utf-8'))
assert not pack['warnings'];locs={r['number']:r for r in pack['statements']}
units={r['problem_title'].split('. ',1)[0].upper():r for r in c.execute('select * from units where source_file_id=?',(fid,))}
assert len(rows)==len(locs)==len(units)==56
visual={'BA','BF','BG','CC','DB','DC','EC','EG','EH','FD','FE','FF','FG','GB','GC','GE','GF','GG','GH'}
solutions={'BA','BF','BG','CC','DB','DC','EC','EG','EH','FB','FD','FE','FG','GB','GC','GE','GF','GG','GH','FA'}
out=[]
for number,domains,physics,reason in rows:
 u=units[number];p=locs[number];assert u['decision'] is None
 decision='REJECT' if number=='EG' else 'BORDERLINE' if number=='FB' else 'KEEP'
 out.append(dict(screening_unit_id=u['screening_unit_id'],decision=decision,confidence='medium' if decision=='BORDERLINE' else 'high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='Unsupplied relativistic mass and proper-time dilation' if number=='EG' else 'Unsupplied relativistic energy-momentum correction' if number=='FB' else '',decision_reason=reason,format='numerical',problem_number=number,page_start=p['page_start'],page_end=p['page_end'],location_json=json.dumps({'statement_locations':p['locations'],'acquisition_problem_number':u['problem_number'],'navigation_pack':f'{f["sha256"]}.statement_pack.json'}),visual_inspection_used=int(number in visual),solution_used=int(number in solutions),boundary_status='content_boundary_verified',evidence='Read all 56 actual slanted-font statements from combined source file 2840. Relevant figures and formulae visually inspected; official solution text used to establish stated external prerequisites where recorded.'))
c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=56,evidence=?,checked_at=? where file_id=?",('Complete 56-statement typography/navigation inventory AA-GH reconciled with source logical rows; no internal solution steps were promoted to questions.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fyziklani_2025_56.json';w.writejson(p,out);w.decisions(p)
events=[dict(screening_unit_id=units['FB']['screening_unit_id'],detail='Focused second review: re-read statement plus official solution physical pp39-40. The correct diffraction angle explicitly needs the unsupplied E^2=E0^2+p^2*c^2 relation. Electron diffraction itself is listed, and the correction is modest; balanced physics usefulness warrants BORDERLINE rather than automatic rejection or a low-precision KEEP.'),dict(screening_unit_id=units['GH']['screening_unit_id'],detail='Focused supplied-model check: solution pp61-62 obtains flux by Stokes theorem directly from the given A and uses Faraday law. Vector-calculus notation does not add external physics; KEEP confirmed.')]
p=w.ROOT/'reviews/resume_fyziklani_2025_focused_qc.json';w.writejson(p,events);w.review(p)
print('Saved 54 KEEP, 1 BORDERLINE, 1 REJECT and completed required borderline review.')

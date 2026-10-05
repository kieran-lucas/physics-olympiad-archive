"""Fifty explicit actual-content MCQ decisions; shared contexts retained."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1968:[
('River crossing with a current','Relative velocity vectors and river width determine travel time.'),
('Average speed over unequal journey segments','The given distances and speeds require only ordinary travel-time averaging.'),
('Aircraft power under a supplied drag law','The quadratic drag is explicitly given; force times speed determines power scaling.'),
('Acceleration-force graph across static and kinetic friction','Newton laws and the specified friction ratio determine the displayed threshold and slope.'),
('Gravity-induced projectile miss','The rendered target geometry and ordinary projectile equations determine the miss distance.'),
('Center-of-mass velocity after mixed collisions','Total momentum is conserved independently of the elastic/inelastic internal collisions.'),
('Three-cart completely inelastic collisions','Momentum conservation determines the final common speed.'),
('Three-cart elastic collision sequence','Momentum and kinetic-energy conservation determine the sequence; collision bookkeeping is mathematical.'),
('Two-dimensional collision with perpendicular final velocities','Vector momentum conservation and the stated right angle determine the final speed.'),
('Kinetic-energy change in the stated collision','The preceding measured velocities plus kinetic energy determine the sign/range of the change.'),
('Floating fraction in a different liquid','Ordinary buoyancy and the supplied liquid-density ratio determine the submerged fraction.'),
('Pendulum acceleration properties','Tangential gravity and centripetal acceleration determine which complete statement is true.'),
('Direction of a rising pendulum acceleration','The actual vector choices combine restoring tangential and inward radial acceleration.'),
('Rotating sliding-mass rope tension','Newtonian radial acceleration determines the initial tension.'),
('Work when the rotating masses are pulled inward','Angular momentum is conserved; the rotational-energy change equals the motor work.'),
('Force and energy from a potential-position graph','The actual potential graph and its slope determine force, equilibrium and accessible kinetic energy.'),
('Energy capacity of a strength-limited flywheel','Rotational kinetic energy and dimensional force-per-area strength scaling suffice; no advanced material constitutive theory is required.'),
('Relation represented on linear and logarithmic axes','The displayed data transformations require ordinary graph interpretation, not external physics.'),
('Small oscillations of liquid in a U-tube','Hydrostatic pressure imbalance supplies the restoring force for ordinary harmonic motion; viscosity is explicitly ignored.'),
('Two-liquid manometer equilibrium','Pressure equality and the specified densities/column lengths determine height difference.'),
('Total time of geometrically diminishing bounces','The restitution rule is explicitly defined; projectile times and a geometric series suffice.'),
('Kinetic-energy graph across rolling and sliding regimes','Newton laws, rotational energy and the stipulated friction determine angle dependence.'),
('Inelastic impact on a vertically supported spring','Momentum during impact, shifted equilibrium and harmonic energy determine maximum displacement.'),
('Frequency of strength-limited strings','The string-wave relation is supplied; tension per area and linear density determine the frequency ratio.'),
('Two-mass coupled-spring normal frequencies','The in-phase/out-of-phase forms are specified; Hooke forces and Newton laws determine both frequencies.')],
1972:[
('Vectors in a turning car','Angular momentum direction and centripetal acceleration follow their ordinary definitions.'),
('Reaction force of a rolling ball on a slope','The rendered vector choices follow normal force, static friction and Newton third law.'),
('Extra force needed to submerge a floating object','Ordinary buoyancy and the originally displaced fraction determine the object volume.'),
('Constraints on an exploding collection of particles','Vector momentum and total kinetic energy constrain particle directions and individual energies.'),
('Lean angle on a circular track','Centripetal force and torque balance determine the required lean.'),
('Dissipative collisions inside a freely sliding box','Center-of-mass motion and the explicitly defined restitution rule determine the eventual displacement.'),
('Balancing a uniform stick with an added mass','Static torque about the stated pivot determines the stick mass.'),
('Period of a half-spring on an incline','Uniform spring stiffness scaling and harmonic motion determine the period; gravity shifts equilibrium.'),
('Velocity from a force-time graph','The rendered graph area is impulse; Newton momentum theorem determines the final velocity.'),
('String break during angular acceleration','Rotational kinematics and the given centripetal-acceleration limit determine break time.'),
('Kinetic-versus-potential energy plot of an oscillator','Conserved mechanical energy determines the actual graph choice.'),
('Height exponent for terminal-speed helicopter descent','Once the stated terminal speed is reached, distance divided by constant speed fixes height scaling.'),
('Radius exponent in a dimensional helicopter model','The source specifies the dependencies. Dimensional analysis and identifiability suffice; rotor aerodynamics is unnecessary.'),
('Translational energy fraction of a pulled disk','Force and torque equations determine translational/rotational speeds and kinetic energies.'),
('Power-limited uphill vehicle speed','The source assumes a lossless adjustable transmission; work against gravity and constant power determine speed.'),
('Speed bound in an imperfect collision','Momentum conservation and nonincreasing kinetic energy bound the allowed speed.'),
('Gravity inside an expanded dust cloud','Newtonian spherical-shell superposition and conserved total mass determine interior gravity.'),
('Tensions of a box with two scales and a pulley','The actual rope attachments and static force balance determine both scale loads.'),
('Shape of a cable dragged through air','Uniform local gravity and drag per length admit ordinary segment force balance; no unsupplied fluid PDE is required.'),
('Rocket spin-up of a wheel space station','Torque, rim inertia and the desired centripetal acceleration determine firing duration.'),
('Acceleration with solid versus hollow pulleys','The actual removed disk changes rotational inertia; Newton laws and no slip determine acceleration.'),
('Binary orbit after an explicitly prescribed mass transfer','Newtonian two-body circular force balance determines orbital force, momentum and period changes.'),
('Impulse from a ball launcher','The specified relative ejection speed and momentum conservation determine recoil.'),
('Maximum steering angle from recoil','Galilean velocity addition and the fixed impulse magnitude reduce the optimization to geometry.'),
('Maximum rise on a frictional second ramp','Work-energy with the given friction and incline angle determines final height.')]
}
starts={1968:[2,2,3,3,4,4,5,5,5,6,6,6,7,7,8,8,9,9,10,10,10,11,11,12,12],1972:[2,2,3,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,11,11,12,12,13,13,13]}
ii={1968:{12,13,19,21,23,24,25},1972:{8,11}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==25
 for n,(u,(physics,reason)) in enumerate(zip(units,rows),1):
  assert u['decision'] is None;page=starts[fid][n-1];domains=[] if fid==1968 and n==18 else [I]+([II] if n in ii[fid] else [])
  shared=([5] if fid==1968 and n==10 else [6] if fid==1968 and n==13 else [7] if fid==1968 and n==15 else [])
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',page_start=page,page_end=page,location_json=json.dumps({'shared_intro_pages':shared}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Every actual statement/options and every question-page render inspected in source {fid}; exactly Q1-Q25. Shared introductions are context, not independent subproblems.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Complete printed statement/options and all figures inspected; 25 independent MCQs.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2014_2015_50.json';w.writejson(p,out);w.decisions(p)

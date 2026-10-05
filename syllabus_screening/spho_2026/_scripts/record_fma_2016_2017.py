"""Actual fifty statements/options/figures inspected; explicit semantic records."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1960:[
('Wall-riding motorcycle friction','Centripetal normal force and vertical force balance set the required friction.'),
('Freely falling box and internal spring mass','Coupled Newton equations and relative harmonic motion determine the frequency; uniform gravity drops out.'),
('Ball moving inside a freely sliding shell','Horizontal center-of-mass conservation determines the final shell displacement.'),
('Car spacing under delayed acceleration','Prescribed acceleration and reaction delays determine every displayed traffic pattern.'),
('Projectile range from a cliff','Ordinary ballistic motion and angle optimization determine the range maximum.'),
('Two-beam hanging mobile','The rendered attachment lengths and static torque/force balances determine the missing mass.'),
('Kinetic-energy growth of a snow-catching train','Specified mass arrival and constant speed determine the energy rate.'),
('Power for a snow-catching train','Momentum influx and engine work determine power; no external flow theory is needed.'),
('Pressure forces in differently shaped flasks','Water depth from the shown geometry and ordinary hydrostatic pressure determine bottom force.'),
('Gauge pressure in a plugged milk jug','The free surface and connected fluid determine bottom pressure despite trapped gas in the handle.'),
('Impact location giving a rod no spin','Angular momentum about the combined center of mass determines the impact condition.'),
('Impact mass giving a rod no spin','Linear/angular momentum conservation determines whether the no-spin condition depends on projectile mass.'),
('Extreme-mass Atwood tension','Newton laws for the two masses determine the finite limiting tension.'),
('Rolling-object acceleration','Rotational inertia and the no-slip constraint determine downhill acceleration.'),
('Speed of scaled rolling spheres','Gravitational energy and rotational kinetic energy determine mass/radius dependence.'),
('Rod sliding between two walls','Rigid-length differentiation and the actual contact geometry determine endpoint velocities.'),
('Downward launch from a building','Constant gravitational acceleration and the given last-segment travel time determine initial speed.'),
('Zero-acceleration point in a pulled rolling disk','Translation, angular acceleration and centripetal acceleration determine the point location.'),
('Incline friction inferred from a speed-time graph','The two rendered graph slopes and Newton law determine the friction coefficient.'),
('Maximum inelastic momentum transfer','Momentum conservation and mass-ratio limits control the requested fraction.'),
('Maximum elastic momentum transfer','Momentum and kinetic-energy conservation determine the transfer bound.'),
('Maximum elastic energy transfer','The ordinary two-body elastic collision formulas follow conservation and determine the optimum.'),
('Wave travel on a stretched spring','Hooke-law tension, changed linear density and standard string-wave speed determine the travel time.'),
('Spring compression in a free collision','Momentum conservation and spring/kinetic energy determine maximum compression.'),
('Speed on an eccentric planetary orbit','Newtonian central-force angular momentum and orbit geometry determine the speed ratio.')],
1964:[
('Wheel speed during a circular turn','No-slip rolling and the different radii of the actual left/right tracks determine angular speeds.'),
('Cylinder floating in two liquids','Ordinary buoyancy in the specified oil/water layers determines displaced fractions.'),
('Book stopped by a snow layer','Gravity and the stipulated constant stopping force enter the work-energy theorem.'),
('Bead acceleration on a uniform helix','Tangential gravity and growing centripetal acceleration determine the rendered time-graph choice.'),
('Projectile seen in an accelerating box','Relative acceleration under gravity determines the displayed paths; noninertial coordinates are foundational mechanics.'),
('Returning projectile in an accelerating box','The constant relative acceleration and initial velocity determine the return path; no advanced theory is needed.'),
('Transverse oscillation of a spring midpoint','Hooke force and changing spring geometry determine amplitude-dependent oscillation; nonlinear integration difficulty is mathematical.'),
('Kepler laws under a specified inverse-cube force','The force law is supplied. Central-force angular momentum and scaling determine which listed laws survive.'),
('Bead detachment from a sphere','Energy and the radial normal-force condition determine the loss-of-contact speed.'),
('Accelerations after cutting an elastic support','The unchanged initial string tensions and Newton laws determine both immediate accelerations.'),
('Power-limited car speed under a given drag law','Drag is explicitly proportional to area times speed squared; geometry, power and density scaling suffice.'),
('Buoyancy in an accelerating container','Effective gravitational acceleration multiplies weight and displaced-fluid force equally.'),
('Speed bounds for partially inelastic collisions','Momentum conservation and the allowed loss of kinetic energy bound the outgoing speed.'),
('Frequency after changing spring attachment on a rod','The actual lever arms, Hooke stiffness and rotational inertia determine small-oscillation frequency.'),
('Frequency of a prestressed longitudinal spring and rod','The shown geometry and Hooke-law restoring torque determine the frequency; no continuum constitutive machinery is required.'),
('Ball dropped from a moving truck','Relative horizontal velocity and ordinary free-fall time determine the landing separation.'),
('Stopping a spinning hollow sphere with friction','The shared frictional impulse changes linear and angular momentum according to its known inertia.'),
('Spin-up/coasting/spin-down time','Constant angular accelerations and total angular displacement determine elapsed time.'),
('Graph of launch geometry and projectile range','Energy on the semicircular track plus horizontal projectile motion determine the plotted relation.'),
('Toppling before sliding on an incline','The actual triangular cross-section, center of mass and Coulomb friction determine the threshold.'),
('Displacement of a collapsing two-mass rod','Horizontal center-of-mass conservation and rigid geometry determine the upper mass displacement.'),
('Speed of a collapsing two-mass rod','Conserved mechanical energy with the rigid-rod velocity constraint determines the impact speed.'),
('Rotating elastic ring radius','Hooke stiffness and Newtonian radial force on ring elements determine expansion; ordinary integration is sufficient.'),
('Hexagon inertia from a supplied triangle result','The source supplies the triangle inertia. Superposition and axis shifts determine the requested rigid-body inertia.'),
('Ranking length measurements with random errors','Independent uncertainties combine conventionally; experimental data reasoning is explicitly in scope.')]
}
starts={1960:[2,2,2,3,3,4,4,4,5,5,6,6,6,7,7,7,8,8,8,9,9,9,9,10,10],1964:[2,2,3,3,4,5,5,6,6,7,7,7,8,9,9,10,10,10,11,12,12,12,13,13,13]}
ii={1960:{2,23,24},1964:{7,14,15,23}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==25
 for n,(u,(physics,reason)) in enumerate(zip(units,rows),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  domains=[] if fid==1964 and n==25 else [I]+([II] if n in ii[fid] else [])
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',page_start=page,page_end=page,visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Complete actual file {fid}: all 25 numbered statements and answer options read and every question-page render inspected. Shared introductions preserved, distinct MCQ numbers remain separate; no internal subpart split.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('All pages inspected; exactly 25 separate printed MCQs.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2016_2017_50.json';w.writejson(p,out);w.decisions(p)

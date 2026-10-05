"""Seventy-five actual MCQ statements/graphs inspected, explicit scope reasons."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas'
data={1986:[
'Cyclist average speed: the known moving speed, stop time and average determine total travel distance.',
'Average acceleration from data: the rendered endpoint velocities and interval determine acceleration.',
'Maximum velocity from data: reading actual velocity-time extrema suffices.',
'Travel distance from data: integrating speed on the actual graphs determines distance.',
'Earth orbital acceleration: Newtonian circular motion with the ordinary orbital period determines acceleration.',
'Children sticking after collision: linear momentum conservation determines common velocity.',
'Skater kinetic-energy increase: conserved angular momentum and the specified frequency change determine rotational energy.',
'Floating wood fraction: the supplied full-submersion buoyancy and weight determine displaced volume.',
'Spring pulled at both ends: static force balance and Hooke law determine extension.',
'Pendulum period changes: gravity, length and finite-amplitude pendulum dynamics control the options.',
'Water-level graph as a cup fills and sinks: ordinary buoyancy, displacement volume and the constant incoming volume rate determine the stages.',
'Gravitationally compressed rod triangle: Newtonian pair forces resolved along the actual rods determine compression.',
'Pulled rolling spool direction: the actual winding radii, torque and no-slip constraint determine the critical angle.',
'Uniform rhythm of falling weights: free-fall times and the rendered spacing pattern determine the impact sequence.',
'Spring stiffness from speed and amplitude: harmonic energy determines the spring constant.',
'Rope held against a railing: the actual normal contact and static-friction bound support the hanging weight.',
'Sliding rope after a disturbance: the given kinetic/static friction ratio fixes net acceleration and impact speed.',
'Two frictional ramps: work-energy with the specified inclines and friction determines the final height.',
'Return time under a supplied central Hooke force: Newton equations reduce directly to harmonic motion.',
'Maximum distance under the same Hooke force: the initial speed and oscillator energy determine amplitude.',
'Gas capacity of a pressure vessel: stated radius independence and material-strength dimensions with ideal-gas variables determine the choice.',
'Maximum engine power from data: the actual torque-frequency graph and power equals torque times angular speed determine the optimum.',
'Projectile parabola versus bound ellipse: constant local gravity is an approximation to the ordinary Newtonian central-force orbit.',
'Frictional bearing power: ordinary friction force and torque arm determine the effects of bearing width and radius.',
'Rolling cylinder versus sliding block: rotational inertia, no slip and given equal arrival times determine kinetic friction.'
],1987:[
'Speed from a position-time plot: the slope of the actual graph determines maximum speed.',
'Speed from a velocity-time plot: the absolute ordinate of the actual graph determines maximum speed.',
'Speed from an acceleration-time plot: integrating the actual graph from rest determines velocity extrema.',
'Falling piano escape time: Newtonian free fall at the two specified heights determines remaining time.',
'Oppositely angled projectiles from a ledge: gravitational kinematics determines the difference in flight times.',
'Projectile height-to-range ratio: standard ballistic equations determine the angle dependence.',
'Angular momentum at a given radial acceleration: circular motion, mass and radius determine angular momentum; fictional context is irrelevant.',
'Maximum uphill traction: normal force, static friction and downhill gravity determine acceleration.',
'Pendulum tilt in an accelerating car: ordinary force components determine vehicle acceleration.',
'Slipping stacked blocks: the actual contact normals and given kinetic friction determine the lower block acceleration.',
'Three equal masses on pulleys: the rendered geometry and static tension balance determine the length ratio.',
'Kinetic-energy increase after horizontal launch: gravity adds vertical speed while horizontal speed remains constant.',
'Rolling-ball vertical launch: supplied inertia, rotational energy and the actual track shape determine center-of-mass rise.',
'Collision followed by frictional stopping: work-energy before/after and elastic-collision conservation determine stopping distance.',
'Block climbing a freely moving wedge: horizontal momentum and energy conservation determine height.',
'Block leaving the free wedge: the same two conservation laws determine outgoing speed.',
'Tetrahedron gravitational potential: summing ordinary Newtonian pair energies determines total energy.',
'Force corresponding to a potential graph: the negative slope of the actual piecewise-linear graph determines force.',
'Possible motion in the given potential: Newton law and force-free regions constrain the actual position-time graphs.',
'Total energy from position-time motion: turning points on the actual potential plot fix energy.',
'Gravitational self-energy radius scaling: Newtonian pair energies and uniform-density mass scaling determine the exponent.',
'Helium balloon in a turning car: effective body force in the enclosed air gives ordinary buoyancy opposite effective gravity.',
'Opposed U-tube water jets: steady momentum flux through the actual tube bends determines the net reaction; no external fluid PDE is necessary.',
'Inertia of an eccentrically perforated disk: supplied disk inertia and the parallel-axis theorem determine the removed contribution.',
'Thruster change from elliptic to circular orbit: Newtonian gravity, orbital energy and angular momentum determine circular speed.'
],1993:[
'Average impact pressure of an apple: gravitational speed, impulse over the given contact time and force per area determine pressure.',
'Three-block elastic sequence: momentum and energy conservation with the actual initial ordering determine the final center-block position.',
'Three-block inelastic sequence: conserved momentum and the specified sticking events determine the final position.',
'Accelerating astronaut support: Newton laws and reaction force determine the spacecraft load.',
'Orbital angular momentum ranking: the rendered circular/elliptical orbit geometry and Newtonian central-force motion determine the ordering.',
'Projectile speed at a fixed height: gravitational energy conservation makes the speed independent of launch angle.',
'Uniformly accelerating bird: constant-acceleration displacement and speed relation determine acceleration.',
'Angular acceleration from a spin graph: the slope of the actual angular-velocity graph gives acceleration.',
'Net angular displacement from a spin graph: the signed actual graph area gives displacement.',
'Separation of two oppositely thrown apples: equal gravitational acceleration cancels in relative motion.',
'Work from an acceleration-position graph: Newton force times displacement and the actual signed graph area determine work.',
'Work lifting two people: their gravitational potential-energy increases determine the total.',
'Balanced three-person seesaw: center of mass and each actual torque arm determine the largest torque.',
'Conservation over an entire ballistic-pendulum motion: external gravity and support impulses determine which listed quantities stay conserved; impact-only approximations are explicitly insufficient.',
'Constant-speed suitcase friction: normal/tangential force balance with the given pulling angle determines the coefficient.',
'Two masses joined by a spring: coupled Newton equations and relative harmonic motion determine frequency.',
'Calibration with kilogram and frequency references: standard oscillator dynamics gives stiffness in SI units without an independent length standard.',
'Pendulum striking a peg: the two effective lengths determine the combined small-angle period.',
'Maximum-range projectile height: ordinary ballistic equations at the optimal angle determine height.',
'Perpendicular inelastic space-goo collision: vector momentum conservation determines final speed.',
'Binary-star potential energy: ordinary Newtonian pair potential and the specified masses determine energy.',
'Binary-star orbital period: Newtonian mutual force and center-of-mass distances determine the common period.',
'Time of maximum spring power: harmonic displacement/velocity and Hooke force determine the product and its sign.',
'Toppling versus slipping rectangle: the center-of-mass line relative to the contact edge and Coulomb-friction limit determine the boundary.',
'Two frictional disks stopping together: the common tangential impulse and each disk inertia determine the required radius-frequency relation.'
]}
starts={1986:[2,2,2,2,3,3,3,3,3,4,4,5,5,6,6,7,7,7,8,8,8,9,9,10,10],1987:[2,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,6,7,8,8,9,9,9,10,10],1993:[2,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,6,7,7,7,8,8,8,9,9]}
ii={1986:{9,10,15,19,20},1987:set(),1993:{16,17,18,23}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==25
 for n,(u,reason) in enumerate(zip(units,rows),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  domains=[I]+([II] if n in ii[fid] else [])+([III] if fid==1986 and n==21 else [])
  shared=[7] if fid==1987 and n in (19,20) else []
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=reason.split(':',1)[0],external_physics_if_any='',decision_reason=reason,format='multiple_choice',page_start=page,page_end=page,location_json=json.dumps({'shared_intro_pages':shared}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'All actual Q1-25 statements and choices read in complete source {fid}; every question-page render inspected, including graphical answer options. Shared contexts retained as context, not split subparts.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Complete physical exam read with every graph and diagram; exactly 25 printed MCQs.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2009_2011_75.json';w.writejson(p,out);w.decisions(p)

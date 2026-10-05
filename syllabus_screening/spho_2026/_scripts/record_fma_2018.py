"""Explicit actual-content reviews of fifty MCQs; no topic/title classifier."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1955:[
('Velocity-time graph with resistive air force','Ordinary gravity and a resistive force opposite velocity determine the graph trend; a microscopic drag law is unnecessary.'),
('Center-of-mass velocity of colliding masses','Total momentum and total mass determine center-of-mass velocity independently of collision details.'),
('Conservation constraints of a collision without specified restitution','Momentum and center-of-mass motion remain conserved, while elasticity is not assumed; ordinary collision reasoning controls the options.'),
('Maximum orbital energy gain from a fixed impulse','Newtonian kinetic energy increment and the greater perigee speed determine the optimum.'),
('Recoil of a frictionless wedge with pulley-connected masses','The actual string/apparatus geometry and horizontal momentum balance determine wedge motion.'),
('Inclined-plane applied work and frictional loss','Force work, gravitational energy and the supplied friction determine final speed.'),
('Fastest acceleration-limited journey ending at rest','Constant acceleration/braking and distance constraints determine shortest time.'),
('No-slip disk motion within a fixed hoop','The actual contact geometry supplies center speed and instantaneous-axis velocity.'),
('Initial support reaction of a lifted uniform stick','Rigid-body torque, translation and endpoint contact determine the initial normal reaction.'),
('Acceleration-time graph with resistive air force','Newtonian gravity plus velocity-opposing resistance determines the graph including its change through the turning point.'),
('Halved uniform spring and parallel restoring stiffness','Ordinary Hooke-law stiffness scaling and harmonic oscillation determine the new frequency.'),
('Pendulum determination of g with Gaussian uncertainties','The ordinary pendulum law and independent uncertainty propagation determine the reported measurement.'),
('Cable elastic modulus from supplied stress/strain definition','The source defines Young modulus and supplies the stretched geometry; dimensional force/area and fractional extension suffice.'),
('Two-axis oscillations of a rigid three-mass pendulum','The actual mass arrangement and pivot require rotational inertia and gravitational restoring torque.'),
('Circular orbital kinetic energy after slow dissipation','Newtonian orbital energy and the circular-force condition determine how kinetic energy changes.'),
('Jump trajectory viewed from a rotating space station','Ordinary inertial straight-line motion and coordinate rotation determine relative acceleration and landing; no relativity is required.'),
('Sand-stream shape after a prescribed helicopter reversal','Each grain retains its launch velocity and falls under gravity; ordinary projectile geometry determines the displayed stream shape.'),
('Top-bottom rod tension in vertical circular motion','Mechanical energy and radial Newton law determine the tension difference.'),
('Pressure scaling from rain momentum flux','Drop mass, impact speed and arrival rate determine momentum transfer per area.'),
('Energy stored in two half-springs at equal fractional extension','Uniform Hooke-law spring scaling and energy determine the total.'),
('Sliding hollow sphere transition to rolling','Frictional translation and rotational acceleration with the no-slip condition determine transition time.'),
('Leak-rate graph for a floating rectangular boat','Hydrostatic buoyancy and equal displacement areas determine the pressure head as the boat fills; no unsupplied viscous-flow theory is needed.'),
('Angular-acceleration graph across rolling and slipping slopes','Newtonian torque and the supplied friction coefficient determine the two regimes and their transition.'),
('Pendulum period through oscillatory and rotating regimes','The entire motion follows ordinary gravitational potential and energy; large-amplitude integration difficulty is mathematical.'),
('Weighted combination of independent period measurements','The source supplies both measurement errors and weights; ordinary uncertainty aggregation determines the ranking.')],
1957:[
('Acceleration-time graph for falling and stopping clay','Gravity during flight and contact impulse while stopping determine the acceleration sequence; no clay constitutive law is needed.'),
('Frictional energy loss on an incline','The given friction coefficient, length and normal load determine work.'),
('Completely inelastic collision energy','Momentum conservation determines final velocity and kinetic energy.'),
('Energy and momentum of a bouncing ball considered alone','The external ground impulse and possible dissipative transfer determine which conservation statements apply.'),
('Angular acceleration from spin-up and coast-down rotations','Ordinary rotational kinematics with the stipulated constant accelerations determines their ratio.'),
('Beam-deflection dimensions under explicitly specified dependencies','The source supplies force linearity, inertia dependence and modulus units; dimensional analysis determines length scaling without beam theory.'),
('Vertically driven pendulum energy pumping','The actual modulation follows Newtonian pendulum dynamics; twice-frequency energy pumping is ordinary driven-oscillation reasoning, not an unsupplied field theory.'),
('Frictional spin-up graph before and after rolling','The given Coulomb friction and no-slip transition determine angular velocity over time.'),
('Allowed elastic collision velocities with zero total momentum','Momentum vectors and conserved kinetic energy constrain all options.'),
('Compressed balloon buoyancy at greater hydrostatic depth','Ordinary pressure compression and buoyancy determine the force trend; no specialized equation of state is required for the qualitative comparison.'),
('Transverse string-wave speed under centrifugal tension','Newtonian radial force determines string tension; the ordinary tension-wave relation determines speed scaling.'),
('Ball trajectory in a rotating frame','The source specifies the catch after half a rotation. Straight inertial motion transformed to the rotating frame determines the actual curve.'),
('Sliding onset of two stacked blocks','Newton laws and the supplied static-friction limit determine the applied-force threshold.'),
('Pulled spool with zero rotational acceleration','The actual winding/contact geometry and ordinary torque balance determine pull angle.'),
('Scale-response graph during a lift ending at rest','The force impulse needed to accelerate then decelerate the book determines the load pattern.'),
('Flight power and angle under supplied lift/drag laws','Both aerodynamic dependencies are given; relative air speed, force balance and work rate suffice without airfoil theory.'),
('Falling spring-mass system after the spring end sticks','The specified contact model and gravity-shifted harmonic energy determine maximum speed.'),
('Parallel springs with different natural lengths','Hooke-law force addition determines effective stiffness and equilibrium length.'),
('Sound-speed measurement uncertainty','Given distance/time measurements and Gaussian errors require ordinary propagation.'),
('Massive rope frictional stability after a displacement','Hanging weight imbalance and the supplied table friction determine the allowed displacement.'),
('Physical-pendulum period minimization by pivot placement','Rotational inertia, center of mass and gravity determine period; the optimization is mathematical.'),
('Pulley-coupled pendulum and vertical mass motion','The actual length constraint and Newtonian energy determine coupled motion and drift.'),
('Free two-mass rigid rod after a transverse impulse','Center-of-mass translation and rotation determine when the second endpoint returns to zero velocity.'),
('Gravity of a hemispherical shell at its center','Ordinary Newtonian superposition and angular integration determine force.'),
('Comparing instrument upgrades and repeated measurements','The supplied radius/length errors and independence assumption determine propagated surface-area uncertainty.')]
}
starts={1955:[2,2,3,3,3,4,4,4,5,6,7,7,8,8,9,9,10,10,11,11,11,12,13,13,14],1957:[2,2,3,3,3,3,4,4,5,5,5,6,7,7,8,9,9,10,10,10,11,11,11,12,12]}
ii={1955:{4,11,12,14,20,24,25},1957:{7,11,17,18,19,21,22}}
foundation_only={1955:{25},1957:{6,25}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(rows)==len(units)==25
 for n,((physics,reason),u) in enumerate(zip(rows,units),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  domains=[] if n in foundation_only[fid] else [I]+([II] if n in ii[fid] else [])
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',problem_number=str(n),page_start=page,page_end=page,location_json=json.dumps({'acquisition_problem_number':u['problem_number']}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'All actual statement/options and every question-page render inspected for complete file {fid}. Q1-25 are independent printed MCQs; all graphs and geometric apparatus retained.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Entire actual paper and all graph choices read; exactly 25 printed questions and no omitted experiment or extra task.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2018_50.json';w.writejson(p,out);w.decisions(p)
print('Saved 50 KEEP decisions after complete statement and visual inspection.')

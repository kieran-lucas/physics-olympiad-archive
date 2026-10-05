"""Explicit reviews after reading both complete papers and relevant diagrams."""
import workflow as w
c=w.connect();out=[]
I='I_force_motion';II='II_oscillations_waves'
data={1909:[
('Signal-travel delay and transverse jet geometry','The statement explicitly excludes special relativity; finite light-travel time and ordinary geometry suffice.'),
('Geometric scaling and gravitational falling times','Domino-wave scaling follows dimensional reasoning and Newtonian falling motion, without a specialized collective-wave model.'),
('Trajectory versus component velocity graphs','The rendered trajectory and options require only vector kinematics and graph interpretation.'),
('Relative projectile motion under common gravity','Both launch velocities and landing time are specified; ordinary projectile kinematics determines separation.'),
('Circular launch velocity and projectile fall time','Sand retains the helicopter tangential velocity; ordinary circular and projectile motion determine the landing radius.'),
('Work-energy scaling with supplied penetration law','The specialized impact-depth law is explicitly supplied; kinetic energy and work determine force scaling.'),
('Newtonian gravitational equilibrium and rotating-frame stability','L2 is defined by the statement. Perturbing gravitational and inertial forces requires ordinary mechanics, not relativistic astrophysics.'),
('Energy and relative velocity on a translating ramp','The moving heavy-ramp limit reduces to Galilean relative motion and mechanical energy conservation.'),
('Moving-wall elastic collisions and gravitational escape energy','Repeated elastic velocity increments and Newtonian escape energy supply the entire physical method.'),
('Gravity of extended uniform bodies','Newtonian gravitational superposition and integration determine the three accelerations; the integration difficulty is mathematical.'),
('Momentum and energy of a bead and freely moving hoop','The diagram specifies equal masses and the track angle; momentum and energy conservation determine center speed.'),
('Buoyancy and inclined reaction force balance','The buoyancy and normal-reaction model are supplied. Static vertical/horizontal balance suffices without fluid lift theory.'),
('Constant Coulomb friction and brief elastic rebounds','The spring interaction duration is stipulated negligible; total stopping time follows Newtonian deceleration and reversals.'),
('Constrained pendulum geometry and small oscillations','The rigid lengths and constraint are explicit; energy and linearized restoring acceleration determine the period.'),
('Sliding-to-rolling frictional dynamics','Translational and rotational friction impulses plus the rolling constraint determine final speed; no deformation theory is used.'),
('Elastic puck collisions and rack recoil','The triangle diagram and masses define ordinary elastic collisions and momentum conservation with moving boundaries.'),
('Sliding ladder rotational kinetic energy','Rigid-body kinematics, gravitational potential and rotational kinetic energy determine the endpoint speed.'),
('Pulley constraints and spring effective stiffness','The rendered pulley arrangement uses ordinary tension balance, Hooke law and oscillation energy.'),
('Coupled pendulum and sliding support oscillations','Conservation of horizontal momentum and small-angle mechanical energy determine the frequency.'),
('Motor torque and angular momentum balance','Internal motor torque can produce changing rod angular momentum; gravity and rotational dynamics control the answer.'),
('Repeated ballistic jumps off a rotating platform','The source stipulates instant reco-rotation and a massive platform; geometry and projectile flight determine the outward steps.'),
('Unequal wheel friction, torque and rotational inertia','Normal-force balance and the given radius-of-gyration definition determine angular acceleration; tire mechanics is not needed.'),
('Moment-of-inertia scaling and alternating geometric series','The self-similar mass pattern requires only rotational inertia and the supplied series identity.'),
('Centripetal force of a thin fluid sheet','The flow path, thickness and pressure limit are stipulated; a small mass element obeys Newtonian radial force balance without an unsupplied fluid constitutive theory.'),
('Gravity-driven drainage and vessel geometry','Inviscid outflow follows energy balance and volume continuity; the drawn cross sections determine emptying times without advanced fluid dynamics.')],
1918:[
('Projectile trajectory with two equal-height crossings','Ordinary constant-gravity kinematics controls the two crossing times.'),
('Centripetal acceleration and inclined normal force','Force resolution at the frictionless wall determines when floor support vanishes.'),
('Static force balance in a pinned bridge','The rendered truss geometry requires only tension/compression and equilibrium at vertices.'),
('Kinetic-energy graph of elastic vertical bounces','Projectile velocity and perfect restitution determine the plotted energy; all options were visually inspected.'),
('Normal reaction of a sliding block on a scale','Newtonian acceleration and force components determine the scale reading.'),
('Small pendulum motion and deposition density','The specified constant water leak samples the pendulum residence time; no specialized fluid model is required.'),
('Velocity-time versus velocity-position graphs','Kinematic integration and the plotted options establish the relationship.'),
('Rigid-rod endpoint and midpoint kinematics','Differentiating the wall/floor geometric constraint gives center velocity.'),
('Piecewise frictional braking work','Kinetic-energy loss on the dry and icy segments determines stopping distance.'),
('Spring force and circular equilibrium','The two given spring constants and centrifugal requirement determine the fixed position.'),
('Pressure force on hemispheres','Pressure difference integrated over projected area determines separation force; ordinary hydrostatics is foundational.'),
('Gravitational torque from point masses','The diagram and Newtonian gravitational forces determine torque about the indicated asteroid.'),
('Pulley tension with oblique string geometry','String constraints and Newton laws determine initial tension and its graph.'),
('Energy and recoil momentum of bead and movable hoop','Conserved horizontal momentum and mechanical energy determine the bead turning angle.'),
('Dimensions of viscosity and surface tension','The viscous force law is supplied. Defining surface tension as force per length is ordinary general physics; no Ohnesorge fluid theory is required.'),
('Pendulum release and projectile-range scaling','Mechanical energy and ballistic kinematics determine gravitational scaling without solving a specialized physical model.'),
('Static pulley and spring extension constraints','The rendered ropes and spring connections require Hooke law and ordinary tension balance.'),
('Orbital energy before and after rocket impulse','The elliptical-orbit energy relation is explicitly supplied; Newtonian circular motion and energy determine the impulse.'),
('Physical-pendulum inertia and center of mass','The unequal spoke masses determine gravitational restoring torque and ordinary small oscillation frequency.'),
('Constrained square motion and spring oscillations','Spring energies and hinge kinetic energy provide the linearized oscillation period.'),
('Incompressible continuity and syringe energy balance','Negligible viscosity and the areas are specified. Force work supplies water kinetic energy; no unsupplied viscous-flow theory is necessary.'),
('Newtonian gravity across a spherical shell','Gravitational superposition and the ordinary shell theorem determine the discontinuity.'),
('Restitution and moving-paddle collisions','The bounce-height condition supplies restitution; Galilean collision velocities and gravitational energy suffice.'),
('Supplied quadratic drag and terminal-motion scaling','The drag dependence is explicitly supplied; Newtonian motion and dimensional scaling determine displacement.'),
('Variable-radius yo-yo unwinding dynamics','The rendered winding geometry, rotational inertia and energy conservation determine changing acceleration.')]
}
for fid,rows in data.items():
 units={int(r['problem_number']):r for r in c.execute('select * from units where source_file_id=?',(fid,))}
 assert len(units)==len(rows)==25
 for n,(physics,reason) in enumerate(rows,1):
  u=units[n];assert u['decision'] is None
  domains=[I]+([II] if (fid==1909 and n in [14,18,19]) or (fid==1918 and n in [6,19,20]) else [])
  page=n+1 if fid==1909 else next(p for p,numbers in {2:range(1,4),3:range(4,7),4:range(7,10),5:range(10,13),6:range(13,15),7:range(15,18),8:range(18,20),9:range(20,24),10:range(24,26)}.items() if n in numbers)
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='Supplied impact model' if fid==1909 and n==6 else 'Supplied viscous force law; ordinary surface tension definition' if fid==1918 and n==15 else '',decision_reason=reason,format='multiple_choice',page_start=page,page_end=page,visual_inspection_used=1,solution_used=int((fid==1909 and n in [1,6,22,23]) or (fid==1918 and n in [12,13,15,16,17])),boundary_status='content_boundary_verified',evidence=f'Complete statement file {fid} inspected in cached text; equation/graph/apparatus diagrams inspected in saved page renders. Each printed numbered MCQ remains one unit. Relevant official solution pages checked as recorded.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Entire MCQ paper inspected: precisely questions 1-25 and no separate experiments or hidden appended questions.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2024_2026_50.json';w.writejson(p,out);w.decisions(p)
print('Saved 50 MCQ decisions from actual statement inspection.')

"""Explicit actual-content decisions for both complete 2019 MCQ papers."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1948:[
('Terminal-speed approach and net force','The stated approach to terminal velocity requires ordinary Newtonian force balance.'),
('Elastic versus sticking collision energy','Momentum conservation and the stipulated collision types determine the energy ratio.'),
('Recoil of a movable ramp and launch height','Conserved horizontal momentum and mechanical energy determine the launched block height.'),
('Spring release amplitude and oscillation period','Gravity and Hooke-law energy determine the equilibrium extension and period.'),
('Minimum torque to roll a cylinder over a step','The actual step geometry and optimal lever arm require only rigid-body torque balance.'),
('Elastic inclined bounces and successive flight intervals','Gravity components and specified restitution determine the spacing and timing trend.'),
('Pendulum-rod radial tension after release','Energy conservation gives speed; radial Newton law determines tension.'),
('Newtonian orbit classification from a tangential launch','Gravitational energy and turning-point geometry distinguish the supplied orbital choices.'),
('Ground-frame speed of a rolling-rim point','No-slip translation and rotation superpose to give the indicated point velocity.'),
('Rotational inertia of a half-annulus','Ordinary mass integration and axial symmetry determine the stated shape inertia.'),
('Speed uncertainty from a timed path','The known distance and stopwatch uncertainty require ordinary error propagation.'),
('Bounce-interval graph under supplied restitution','The velocity reduction is explicitly defined; ballistic timing and a geometric sequence determine the graph.'),
('Juggling power and ballistic time scaling','The specified minimum toss interval sets flight energy and rate; ordinary power reasoning determines the N dependence.'),
('Earth-rotation sideways deflection of a projectile','Newtonian rotating-frame kinematics or inertial velocity geometry determines the small deflection; no relativistic theory is required.'),
('Projectile rod translation and complete rotation','Constant-gravity flight time and rigid-body endpoint velocity determine the initial horizontal velocity.'),
('Free-fall depth error from sound-travel delay','Falling time and wave travel time determine the relative depth error; both laws are ordinary foundations.'),
('Holding force in a supplied constant-torque launcher','The actual disc contact and given hinge torque determine normal reactions and holding force.'),
('Energy released by a constant-torque launcher','The shared source apparatus specifies torque versus opening angle; mechanical work determines the wedge speed.'),
('Submerged pendulum with buoyant restoring force','The density ratio gives effective gravitational torque; ordinary small oscillations determine angular frequency.'),
('Spring stabilization of an upright hinged rod','The drawn two springs and gravity determine the linear restoring torque and stability inequality.'),
('Circular motion inside a uniform spherical dust cloud','Newtonian gravitational superposition gives enclosed mass and orbital speed/period; the dust context adds no external theory.'),
('Two-string circular motion and tension-ratio graph','Geometry, vertical balance and centripetal acceleration determine both tension branches.'),
('Sphere rolling on an accelerated slab','No-slip contact acceleration and ordinary frictional torque determine rotation direction and translation.'),
('Periodic motion in an explicitly supplied anisotropic quadratic potential','Both force components follow the given potential. Harmonic frequencies and mathematical commensurability determine the possible periods.'),
('Ideal outflow from a beaker in a turning car','Ordinary effective gravity, hydrostatic pressure and inviscid work-energy determine the outflow; no unsupplied fluid constitutive law is needed.')],
1949:[
('Frictional work on an incline before a frictionless path','The specified coefficients and incline determine dissipated energy by ordinary force work.'),
('Buoyancy of stacked blocks in water and oil','Force balance and submerged volumes determine the density ratio.'),
('Potential energies of series-connected springs','Common tension and Hooke-law energy determine the two spring energies.'),
('Relative gravitational fall with one or two free masses','Newtonian relative acceleration and time scaling determine the collision-time ratio.'),
('Gravity-radius graph for a density-graded Earth','Spherical gravitational superposition and the given density trend constrain the graph; no specialized geophysics is needed.'),
('Self-gravitating rotating dust cylinder','Newtonian gravity integrated over cylindrical symmetry and centrifugal acceleration determine density scaling; no fluid pressure or relativistic law is required.'),
('Hydrostatic load transfer from a floating boat','The floating boat increases uniform pressure at the bottom; ordinary buoyancy and support force balance determine both wire tensions.'),
('Calibrated scale squeezed between two hands','Vertical force balance and the scale load definition determine the reading.'),
('Force on a hinged board supporting a sphere','The actual wall/board contacts and lever arms require force and torque equilibrium.'),
('Momentum of a rolling/sliding ball and moving cart','Total horizontal momentum with the stated relative ball speed determines cart velocity independently of internal friction.'),
('Square-minus-circle rotational inertia','Ordinary mass integration and subtracting the removed material determine inertia.'),
('Circular-orbit energy and angular-momentum scaling','Newtonian circular speed with the specified mass/radius ratios controls both comparisons.'),
('Projectile envelope of a water spray','The launch speed is given, so ordinary ballistics and geometric scaling determine the reachable wall region without nozzle-flow theory.'),
('Projectile return after elastic wall reflection','Elastic reversal of horizontal velocity and gravitational timing determine launch speed.'),
('Tangential drag balanced by an offset rotating hand','The supplied phase geometry determines tension components and resistive force by Newton laws; no drag constitutive law must be known.'),
('Overspinning hoop friction and return time','Given initial rotation and Coulomb friction determine translation and rotation until rolling.'),
('Changing inertia from hoop to disk under the same launch','The preceding contact model is retained; inertia changes slipping duration and whether return occurs.'),
('Uncertainty sensitivity of a race-time prediction','The stated independent uncertainties and constant-acceleration equation determine short/long-distance sensitivity.'),
('Full-amplitude pendulum acceleration graph','The actual choices require gravitational energy plus radial and tangential acceleration; small-angle approximation is not needed.'),
('Upward and downward frictional travel times','Gravity components and the given coefficient determine the two constant accelerations.'),
('Grain momentum flux and accumulated freight-car load','The collection process is specified. Falling speed, impulse rate and stored weight determine normal force.'),
('Average impact pressure from a supplied stopping time','The source provides contact area and collision duration; gravitational speed and impulse determine mean pressure without fruit-material theory.'),
('Acceleration along an explicitly specified sinusoidal railway','The track profile and speed are given; differentiation determines maximum vertical acceleration.'),
('Unequal hanging lengths of a massive rope','Newtonian weight imbalance and total rope mass determine the initial acceleration.'),
('Free-fall determination of g with measurement uncertainty','Ordinary kinematics and uncertainty propagation compare the three measurement arrangements.')]
}
starts={1948:[2,2,2,3,3,3,4,4,4,5,5,6,7,7,7,7,8,8,9,9,9,10,11,11,11],1949:[2,2,2,3,3,4,4,4,5,5,6,6,7,8,8,9,9,9,10,11,11,11,12,12,12]}
ii={1948:{4,19,20,24},1949:{3,19}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==25
 for n,((physics,reason),u) in enumerate(zip(rows,units),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join([I]+([II] if n in ii[fid] else [])),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',problem_number=str(n),page_start=page,page_end=page,location_json=json.dumps({'acquisition_problem_number':u['problem_number'],'shared_context_questions':'17-18' if fid==1948 and n in (17,18) else '16-17' if fid==1949 and n in (16,17) else None}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Complete actual text/options and every question-page render inspected for file {fid}; exactly printed Q1-25, with no independent subpart units.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('All printed questions 1-25 and actual graph/apparatus pages inspected. B-paper acquisition 26-50 maps to printed 1-25 in screening only.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2019_50.json';w.writejson(p,out);w.decisions(p)
c.execute('update units set source_quality_notes=? where source_file_id=1948 and problem_number=?',('The source asks for the smallest depth with less than 5% delay error, although the ordinary model gives an upper bound. Later reproduction should check this wording against the official solution. Scope remains free fall and sound travel.','16'))
c.execute('update units set solution_used=1 where screening_unit_id=?',('raw::1185',));c.commit()
p=w.ROOT/'reviews/resume_fma_beam_focused_qc.json';w.writejson(p,[dict(screening_unit_id='raw::1185',detail='Focused qualitative-elasticity check: re-read actual 2020 B Q12 and official solution file1945 p9. The source solution explicitly uses top tension/bottom compression to balance gravity torque; no unsupplied constitutive coefficient or beam PDE is used. KEEP confirmed.')]);w.review(p)
print('Saved 50 KEEP MCQs and one targeted official-solution confirmation.')

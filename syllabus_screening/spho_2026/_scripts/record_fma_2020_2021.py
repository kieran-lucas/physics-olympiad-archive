"""Explicit statement-based decisions for another 75 independent MCQs."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves';IV='IV_thermodynamics';XII='XII_atomic_nuclear'
data={1937:[
([I],'Rolling speed graph on a flat-then-inclined track','No-slip rotational energy and gravity determine the displayed speed-time choices.'),
([I],'Horizontal velocity graph of a rolling turnaround','The common track and sign reversal determine horizontal velocity; preserve the shared introduction.'),
([I],'Linked massless-rod torque balance','The actual lever lengths and frictionless contact determine the applied force ratio.'),
([I],'Earth-rotation deflection of a vertical jump','Angular momentum and Newtonian projectile timing determine the small displacement scaling; no relativistic Earth model is used.'),
([I],'Acceleration-limited fastest train journey','Piecewise constant acceleration and braking plus ordinary mathematical optimization determine travel time.'),
([I],'Hydrostatic work in lifting a submerged open bucket','Pressure support and the changing weight of retained water determine work; ordinary hydrostatics is foundational.'),
([I],'Repeated elastic collisions with a slowly moving wall','Galilean collision velocities and the changing interval determine final speed; no quantum adiabatic invariant is needed.'),
([],'Random-sample uncertainty of independent mass measurements','The independent-error assumptions are supplied; statistical uncertainty reduction determines the sample size.'),
([I],'Effective gravity and airplane trajectory duration','Newtonian accelerating-frame force and constant-acceleration height determine the simulated-gravity duration.'),
([I],'Frictional redistribution of disk and stone angular momentum','Total angular momentum and final moment of inertia determine the shared rotation speed.'),
([I],'Flight-time ranking from projectile height curves','The actual launch/landing geometry and common gravity determine time ordering.'),
([I,II],'Spring amplitude limited by platform static friction','Spring energy determines maximum reaction; the stated friction threshold determines whether the support slides.'),
([I],'Acceleration direction along a semicircular track','The displayed velocity arrows determine normal and tangential acceleration components.'),
([I],'Drag scaling from explicitly specified variables','The statement gives all force variables and viscosity units. Dimensional analysis determines scaling without bacterial propulsion or viscous-flow theory.'),
([I],'Fastest straight-incline descent','Newtonian slope acceleration and fixed horizontal length reduce the task to trigonometric optimization.'),
([I,II],'Velocity-position graph and asymptotic motion','The rendered linear v(x) fixes acceleration by the chain rule; graph interpretation distinguishes finite stopping and harmonic motion.'),
([I],'Centripetal acceleration of two clock hands','The stipulated lengths and angular speeds determine point accelerations.'),
([I],'Smoke-plume shape under prescribed air velocity changes','All smoke/air velocity rules are supplied; ordinary advection geometry requires no turbulence theory.'),
([I],'Gravitational field of a sphere with a spherical cavity','Newtonian superposition and sphere-field integration determine the field at the drawn point.'),
([I],'Lunar surface rotation relative to solar illumination','Ordinary angular speed and circumference determine terminator speed; a standard lunar period is auxiliary data rather than external physics.'),
([I],'Rolling versus slipping energy loss on an incline','Static-friction constraints, rotation and kinetic-friction work determine final mechanical energy.'),
([I],'Contact normal and friction in an icebreaker','The hull/ice drawing supplies contact geometry. Resolving normal and Coulomb-friction forces determines downward displacement tendency.'),
([I,II],'Oscillation with a fully specified piecewise force law','The source plots the force-free interval and Hooke-law outer regions; Newtonian traversal plus harmonic timing determines the period.'),
([I],'Kepler transfer orbit to an opposite satellite','Newtonian orbital energy and period scaling determine the required tangential impulse.'),
([I],'Gravitational focusing of a stipulated isotropic pellet spray','Ordinary orbital energy/angular momentum and the supplied small-angle approximation determine the intercepted fraction.')],
1944:[
([I],'Vertical launch and specified rebound energy loss','Gravitational energy conservation before and after the stipulated collision determines launch speed.'),
([I],'Rigid-ball rolling velocity distribution in a chute','The actual two contact points define the instantaneous rotation axis; ordinary rigid-body kinematics suffices.'),
([I],'Penetration depth under a supplied force-area law','Both the wedge shape and depth-dependent contact force are stated. Work-energy and scaling determine penetration without fracture theory.'),
([I],'Corner-joint forces in a rotating square of rods','Ordinary centripetal force and rod symmetry determine each joint force; material stress constitutive theory is unnecessary.'),
([II],'Driven pendulum resonance','The stipulated shaking frequency is compared to the ordinary small-amplitude pendulum frequency.'),
([I],'Orbit adjustment under slow stellar mass loss','The quasi-circular assumption and central Newtonian gravity conserve angular momentum and determine radius change.'),
([I],'Newtonian debris trajectories near an orbiting station','Central gravitational orbits and their period/plane changes determine return; no specialized relativistic spaceflight law is required.'),
([I],'Acceleration-position graph from velocity-position data','The actual plotted velocity and chain rule determine acceleration; mathematical graph interpretation is eligible.'),
([I],'Static rope tension after adding a hanging mass','The common apparatus and equilibrium conditions require ordinary tension balance.'),
([I],'Rope sag geometry and raised-block displacement','The preceding equilibrium apparatus supplies angles and length conservation; it remains a separate printed MCQ.'),
([I],'Load limit from explicitly defined tensile strength','The source defines force per area at failure. Weight and cross-sectional area suffice without material failure theory.'),
([I,II],'Physical-pendulum periods about opposite pivots','The unknown point-mass position and given period ratio determine its location by ordinary pendulum reasoning.'),
([I],'Vertical angular momentum during a released pen flight','The stated external forces have no vertical-axis torque; ordinary angular-momentum balance controls the full question.'),
([I],'Applied-force acceleration graph with stipulated friction coefficients','Newton laws and the explicitly unusual static/kinetic coefficient ordering determine the allowed branches; no external contact model is required.'),
([I],'Hydrostatic pressure of two liquid layers','Pressure increments depend on density and depth, not vessel area; ordinary hydrostatics suffices.'),
([I,IV],'Jump height from explicitly supplied surface energy','The problem defines surface energy per area and full conversion to kinetic energy. Volume and energy scaling determine height without capillary dynamics.'),
([I],'Rain momentum flux and accumulated weight on a scale','The collection rule and rain speed/rate are given. Momentum transfer and growing mass determine force.'),
([I],'Rotational inelastic capture at a fixed pivot','Conserved angular momentum and final rotational inertia determine remaining kinetic energy.'),
([I],'Stacked roller and plate velocity constraints','The rendered contacts and no-slip conditions propagate ordinary rigid-body velocities through the stack.'),
([I],'Mean drag power under explicitly supplied quadratic resistance','The force law is provided. Work rate and the nonnegative speed variance determine the mean-power inequality.'),
([I],'Table tipping about a support-polygon edge','Center of mass, support geometry and torque balance determine the minimum horizontal force.'),
([I],'Momentum and collision energy under Galilean frame changes','Ordinary velocity addition and momentum conservation establish frame dependence; special relativity is unnecessary.'),
([I,II],'Uncertainty in a measured Hooke-law spring constant','The specified constant absolute measurement errors and force scaling determine the fractional uncertainty.'),
([I,II],'Circular motion in a zero-rest-length spring field','The supplied spring force and uniform gravity define a shifted harmonic potential; Newtonian force balance determines orbit-center displacement.'),
([I,II],'Horizontal stability of a vertically suspended two-spring mass','Hooke forces and equilibrium length geometry determine the linearized horizontal restoring coefficient.')],
1943:[
([I],'Vertical elastic bounces between floor and ceiling','Constant-gravity kinematics and elastic reversals determine the full cycle time.'),
([I],'Square-plate inertia about a diagonal','The rod inertia is given; ordinary mass integration and axis symmetry determine the plate inertia.'),
([I],'Conical pendulum force resolution','The string geometry and centripetal acceleration determine the angular frequency.'),
([I],'Weightless flight from a height-time graph','The rendered trajectory identifies the free-fall segment through ordinary gravitational acceleration.'),
([I],'Near-radial Newtonian orbit closest approach','Energy and angular momentum determine the turning point; the small-velocity limit is mathematical.'),
([I],'Support reactions within a triangular table','The given leg failure threshold and torque balance determine the allowed region; the graph choices were inspected.'),
([I],'Orbital period under radial versus tangential impulses','Newtonian orbital energy fixes period, so ordinary small-impulse expansion determines the velocity comparison.'),
([I],'Frictional stopping relative to a moving conveyor','Galilean relative velocity and constant friction determine the slipping time.'),
([I,II],'Elastic-string extension around a pulley','The source explicitly makes the elastic string an ideal spring; static tension and Hooke law determine length.'),
([I,II],'Common-mode oscillations of pulley-connected masses','The preceding apparatus is retained; effective stiffness and total kinetic energy determine the period.'),
([I],'Work on a moving escalator in the specified frame','The moving point of force application and ordinary mechanical work determine energy transfer.'),
([I],'Qualitative tensile and compressive bending stresses','Elementary torque balance of a supported horizontal beam requires tension above and compression below; no unsupplied quantitative continuum constitutive theory is needed.'),
([I,II],'Out-of-plane disk physical pendulum','Ordinary rotational inertia, the parallel/perpendicular axis relations and gravity determine the period.'),
([I],'Repeated completely inelastic mass accumulation','Momentum conservation after each specified collision determines the speed and traveled count.'),
([I],'Closing valves in an already equilibrated hydraulic system','The drawn pressure-balanced states and ordinary hydrostatics determine whether closing a connection changes piston heights.'),
([I,II],'Falling mass timed against a spring oscillator','The common release and first equilibrium passage require harmonic phase and constant-gravity fall.'),
([I,II],'Elastic collision with a moving spring-supported mass','The preceding timing data, elastic momentum exchange and gravitational energy determine return height; keep it as a separate printed MCQ.'),
([I,II],'Linked-beam equilibrium with two springs','The actual joint positions and virtual displacement geometry determine the tension relation without a specialized linkage force law.'),
([I],'Shape-change angular momentum and rotational energy','Axial symmetry and zero external torque conserve angular momentum; the stated inertia increase determines speed and energy.'),
([I],'Scale reading for an enclosed floating helium balloon','Buoyancy, air displacement and force transmission to the enclosing box determine the measured load.'),
([I],'Rapid pendulum pumping by center-of-mass relocation','The stipulated negligible standing time and intrinsic inertia permit ordinary angular-momentum conservation.'),
([I],'Two-interface frictional stopping after an impulse','The given contact coefficients and masses specify a piecewise Newtonian acceleration problem.'),
([I],'Drag scaling from specified size, speed and density','The source explicitly limits force variables. Dimensional reasoning determines the relation without fish physiology or hydrodynamic constitutive theory.'),
([I],'Maximum transmitted speed through two elastic collisions','Ordinary two-body elastic collision equations and mass optimization control the task.'),
([XII],'Counting-statistics uncertainty with a supplied decay-count rule','The source provides the square-root variance and independent intervals. Ordinary uncertainty aggregation determines observing time.')]
}
starts={1937:[2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,8,8,8,9,9,9,10,10],1944:[2,2,2,2,3,3,3,4,4,4,5,5,5,6,6,7,7,7,8,8,8,9,9,9,10],1943:[2,2,2,3,3,4,4,4,5,5,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9]}
ends={1937:{3:3,6:4,9:5,12:6,15:7,17:8,23:10},1944:{4:3,9:5,10:5,13:6,15:7,18:8,21:9,24:10},1943:{12:6,18:8,22:9}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(rows)==len(units)==25
 for n,((domains,physics,reason),u) in enumerate(zip(rows,units),1):
  assert u['decision'] is None
  ps=starts[fid][n-1];pe=ends[fid].get(n,ps)
  shared='1-2' if fid==1937 and n in (1,2) else '9-10' if fid in (1944,1943) and n in (9,10) else '16-17' if fid==1943 and n in (16,17) else None
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',problem_number=str(n),page_start=ps,page_end=pe,location_json=json.dumps({'acquisition_problem_number':u['problem_number'],'source_printed_question':str(n),'shared_context_questions':shared}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'All actual statement/options text and every question-page render inspected in complete source file {fid}; no internal choices or shared-context paragraphs promoted to extra units.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Complete paper and all actual figures read: exactly 25 independent printed MCQs, with shared introductions preserved in locations.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2020_2021_75.json';w.writejson(p,out);w.decisions(p)
c.execute('update units set source_quality_notes=? where source_file_id=1937 and problem_number=?',('The lunar period is not stated; later use needs that standard astronomical numerical datum. No new document or physics prerequisite is invented.','20'))
c.execute('update units set source_quality_notes=? where source_file_id=1944 and problem_number=?',('The source explicitly stipulates static friction smaller than kinetic friction. Preserve that unusual model assumption when reusing the problem.','14'))
c.commit();print('Saved 75 MCQ content decisions; all KEEP.')

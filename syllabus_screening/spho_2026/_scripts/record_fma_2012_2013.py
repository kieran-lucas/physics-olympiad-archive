"""Explicit decisions after full fifty-question source inspection."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1976:[
'Train-car passage: constant-acceleration displacement and successive equal lengths determine times.',
'Reflected projectile: gravity and an elastic wall reversal determine the catching trajectory.',
'Projectile flight-time bounds: the given maximum speed and range constrain angle and time by ordinary kinematics.',
'Hinged sign stability: the actual geometry, normal forces, static friction and torques determine collapse threshold.',
'Elevator maximum speed: the actual scale-time graph gives acceleration and the interval of maximum downward velocity.',
'Elevator travel distance: integrating the same measured force-time graph twice determines building height.',
'Equal-momentum energy comparison: nonrelativistic kinetic energy and given masses determine the ratio.',
'Braking energy: the work-energy theorem identifies the appropriate force-displacement product.',
'Braking momentum: the impulse theorem and constant-deceleration kinematics identify equivalent expressions.',
'Solid versus hollow sphere measurement: rolling inertia distinguishes them; external spherical gravity and buoyancy do not.',
'Normal reaction of a wedge with sliding masses: Newton laws and rendered perpendicular inclines determine the transmitted vertical load.',
'Fluid-filled rolling shell: the stipulated frictionless fluid does not acquire shell spin; supplied shell inertia and Newton laws determine initial acceleration.',
'Saturn ring velocity law: rigid-body rotation versus Newtonian orbital motion determines radial scaling; astronomy is context only.',
'Center-of-mass speed in an elastic collision: momentum conservation and relative-speed reversal determine the common-frame velocity.',
'Partially floating supported rod: ordinary buoyancy and torque about the suspended end determine immersed length.',
'Collapse time of a Newtonian dust cloud: supplied numerical prefactor and gravity-density dimensions determine the choice; no cosmological theory is involved.',
'Orbiting dumbbell tension and stability: Newtonian gravity gradients, radial force and torque determine both properties; tidal context adds no external theory.',
'Allowed two-particle state: the rendered positions/velocities must preserve center-of-mass motion, momentum and angular momentum.',
'Largest pendulum tension: energy and the radial Newton equation determine where tension peaks.',
'Maximum pendulum tension: energy at the bottom and centripetal acceleration determine the value.',
'Finite-amplitude pendulum period scaling: the ordinary pendulum equation scales with length; no small-angle restriction is needed.',
'Achilles-tendon load: the simplified foot and measured lever arms use only static torque and vertical force balance.',
'Bungee stiffness: the explicitly Hookean cord, peak tension and conserved energy determine spring constant.',
'Bungee extension: gravitational energy and the given peak force determine the maximum extension.',
'Constant-speed incline with a horizontal push: the original sliding condition fixes friction; force resolution determines the required push.'
],1979:[
'Dripping faucet: equally spaced release times and gravitational displacement determine drop height.',
'Projectile height versus range: standard ballistic formulas and the stated inequality determine the angle bound.',
'Toppling equilateral block: the center-of-mass line relative to the contact edge determines stability.',
'Three-fragment explosion: vector momentum conservation determines the third velocity.',
'Inelastic collision loss: momentum conservation fixes common velocity and hence lost kinetic energy.',
'Opposed projectiles meeting time: equal gravitational acceleration cancels from their relative separation.',
'Opposed projectiles meeting height: the shared initial conditions and Newtonian free fall determine the location.',
'Frictional spring compression: work against friction plus elastic energy equals initial kinetic energy.',
'Planetary escape speed: Newtonian gravitational potential and energy conservation determine escape.',
'Rolling race: inertia-to-mass-radius ratios determine accelerations independently of density or size for solid spheres.',
'Pulley-assisted sliding at constant speed: the changing actual rope angle and force balance determine friction and normal load.',
'Rotating support-string tensions: the displayed directions and static force balance determine tension trends.',
'Maximum speed from force-position data: work-energy and the rendered graph area determine accessible energy and speed.',
'Eccentrically drilled cylinder equilibrium: removed-mass center of gravity and static torque determine the applied force.',
'Constant-power uphill speed: work rate against gravitational force determines the sustainable speed.',
'Frequency of a two-spring mass in an accelerating cart: Hooke stiffness controls oscillations while constant acceleration shifts equilibrium.',
'Nonlinear-oscillator data: the actual logarithmic axes determine a power law without needing an external oscillator theory.',
'Released box spring oscillation: Newtonian relative motion and the gravity-shifted equilibrium control oscillator properties; box-mass assumptions need checking, not specialized physics.',
'Water-pump pipe radius: the specified lossless motor supplies gravitational and kinetic energy to the mass flow.',
'Two-scale buoyancy readings: Archimedes force and Newton third law determine load transfer between scales.',
'Layered spring compression: series/parallel Hooke stiffness and the added weight determine height change.',
'Sound intensity units: the supplied power-per-area quantity requires dimensional analysis only.',
'Apparatus sufficiency for measuring g: force, pendulum, projectile and work relations determine what the listed measurements can identify.',
'Rotating spring-linked triangle: Hooke tensions and radial Newton force determine stiffness.',
'Circular versus elliptic orbital speeds: Newtonian orbital energy and angular momentum plus the stated extrema bound the speeds.'
]}
starts={1976:[2,2,2,2,3,3,3,4,4,4,4,5,5,5,5,6,6,7,8,8,8,8,9,9,9],1979:[2,2,2,2,2,3,3,3,4,4,4,5,5,6,6,6,7,7,7,8,8,8,9,9,9]}
ii={1976:{19,20,21,23,24},1979:{8,16,17,18,21,22,23,24}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==25
 for n,(u,reason) in enumerate(zip(units,rows),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join([I]+([II] if n in ii[fid] else [])),required_physics=reason.split(':',1)[0],external_physics_if_any='',decision_reason=reason,format='multiple_choice',page_start=page,page_end=page,visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Full actual source {fid} read, all statement/options and every question-page render inspected. Exactly 25 independent MCQs, all shared contexts retained.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Complete actual paper has 25 printed MCQs; all figures and graph choices inspected.',w.now(),fid))
 if fid==1979:
  c.execute('update units set source_quality_notes=? where screening_unit_id=?',('Q18 does not give the box mass or explicitly state negligible reaction of the oscillating mass; later extraction should retain this assumption ambiguity. Scope remains ordinary Newtonian oscillations.',units[17]['screening_unit_id']))
c.commit();p=w.ROOT/'reviews/resume_fma_2012_2013_50.json';w.writejson(p,out);w.decisions(p)

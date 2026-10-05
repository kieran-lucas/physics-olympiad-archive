"""63 actual printed questions; 2007 Q26-38 are separately scored mixed items."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves'
data={1998:[
'Uniform acceleration from speed and distance: ordinary kinematics determines the acceleration.',
'Cube-corner displacement: vector geometry determines displacement independently of the crawling route.',
'Instantaneous velocity graph: the slope of the actual position-time line determines velocity.',
'Maximum displacement graph: accumulated area under the actual velocity curve determines the extremum.',
'Acceleration graph: differentiating the actual velocity segments identifies the matching graphical option.',
'Projectile range at a given angle: standard ballistic range and the known maximum determine the ratio.',
'Child landing on a sled: linear momentum conservation with opposite initial velocities determines final speed.',
'Spinning-wall riders: centripetal normal force and static friction support weight.',
'Two-dimensional collision equations: the actual component expressions are assessed by vector momentum conservation.',
'Mass from force-acceleration data: Newton law gives mass as the fitted slope.',
'Friction from force-acceleration data: the same Newton-law fit gives friction from the intercept and weight.',
'Off-center disk energy: the parallel-axis theorem changes inertia and hence rotational kinetic energy.',
'Stiffer-spring oscillation amplitude: equal initial kinetic energy and spring energy determine amplitude.',
'Reeled rotating tether energy: conserved angular momentum and the stated angular-speed doubling determine rotational energy.',
'Tabletop toppling load: actual support spacing, center of mass and static torque determine the limiting added mass.',
'Acceleration on a vertical spring: Hooke force and gravity determine the signed Newton equation.',
'Equilibrium in an accelerating box: effective weight and Hooke stiffness determine the displacement.',
'Fall toward a gravitational ring: ordinary Newtonian potential superposition and energy determine the maximum speed scaling.',
'Constant-power acceleration: kinetic-energy growth at a fixed rate and Newton law determine the time dependence.',
'Cantilever answer elimination: the source explicitly requests eliminating implausible options using stiffness, load and geometric limiting behavior; no beam-deflection equation must be known.',
'Two-body versus three-body decay: vector momentum and total kinetic energy constrain daughters; no particle interaction theory is requested.',
'Bullet-pendulum complete loop: momentum at impact, subsequent energy and the positive-tension condition determine minimum launch speed.',
'Equal-density planet comparison: Newtonian mass-radius, escape, surface-force and circular-orbit scaling determine the invariant.',
'Total bouncing time: the source supplies the restitution multiplier; gravitational flight times form a geometric series.',
'Mislaunched satellite periapsis: conserved orbital energy and angular momentum determine the closest approach.'
],2003:[
'Parametric path axis crossing: the supplied coordinate function and the zero transverse coordinate determine the time.',
'Acceleration from velocity graph: the actual local graph slope determines acceleration.',
'Average velocity from a quadratic position: endpoint displacement divided by interval determines velocity.',
'Second-second fall distance: gravitational displacement scales with elapsed time squared.',
'Force on a crate riding an accelerating sled: static contact friction provides the uphill force required by Newton law.',
'Displacement from a supplied quadratic velocity: direct time integration suffices.',
'Energy cost of successive speed increments: nonrelativistic kinetic energy determines the ratio; battery chemistry is irrelevant.',
'Gravitational potential scaling: the inverse-distance Newtonian pair potential determines energy at twice the separation.',
'Center-of-mass motion of a sliding block and wedge: no external horizontal force fixes horizontal center-of-mass position despite internal friction.',
'Equal angular acceleration of two wheels: the supplied hoop inertia, rendered radii and torque determine required forces.',
'Rotational energy ranking under equal rim forces: torque and ordinary shape inertia determine energy after equal time.',
'Rock on a balanced measuring stick: rendered support position and static torque determine stick mass.',
'Elastic-collision momentum graphs: equal-mass momentum exchange and conservation identify the actual graph choice.',
'Friction directions on accelerating driven and free wheels: translation, applied wheel torque and rolling constraint determine the two contact directions.',
'Tension of a disk-pulley falling mass: the supplied disk inertia and no-slip Newton/torque equations determine tension.',
'Baseball-basketball rebound: the stated immediate velocities and short-time momentum conservation determine outgoing speed.',
'Projectile tangential/normal acceleration ratio: the velocity direction and constant gravitational acceleration determine both projections.',
'Frictional stopping after a curved descent: gravity, the rendered lengths and friction work determine the coefficient.',
'Non-Hookean spring extension: the force law is explicitly supplied; integrating it for elastic energy plus gravity determines the turning point.',
'Repeated wall collision losses: the supplied energy-loss fraction and kinetic-energy speed dependence determine collision count.',
'Inertia of a scaled sphere: fixed-density mass scaling and the squared radius in inertia determine the factor.',
'Rocket momentum after equal force over equal distance: work-energy and the specified fixed masses determine the momentum ratio; rocket-exhaust theory is unnecessary.',
'Apparent weight on a rotating planet: gravity minus the required centripetal acceleration determines the equatorial support force.',
'Returning projectile under a constant wind force: the horizontal force is explicitly constant; ordinary two-dimensional acceleration fixes launch direction.',
'Floating-box oscillation: the buoyancy relation is explicitly supplied; immersion change supplies a linear restoring force.',
'Sliding-sled friction from travel data: constant-acceleration kinematics and slope-resolved Newton law determine friction.',
'Artificial gravity after astronauts move inward: angular momentum conservation and centripetal acceleration determine the change.',
'Largest friction without bicycle tipping: rendered center-of-mass height, wheelbase, force and torque balance determine contact loss.',
'Largest bicycle deceleration without tipping: the same Newtonian torque/contact constraint sets the acceleration.',
'Bicycle braking with unequal contact friction: the supplied front/rear coefficient ratio and both contact reactions determine the tipping boundary.',
'Radius of gyration of a rod: standard rigid-body inertia and its supplied md-squared definition determine the length ratio.',
'Physical-pendulum angular frequency: parallel-axis inertia and small-angle gravitational torque determine the specified dimensionless coefficient.',
'Largest physical-pendulum frequency: maximizing the ordinary frequency expression is mathematical optimization.',
'Angular momentum when a winding tether breaks: geometric perpendicular distance and the given tension threshold determine the momentum.',
'Energy of a winding tether: tension stays perpendicular to instantaneous velocity, so ordinary work-energy determines kinetic energy.',
'Free tether length at break: Newtonian curvature acceleration and the supplied breaking tension determine length.',
'Elastic collision followed by a breaking spring: the comparison with a given inelastic stopping event fixes spring energy, then collision conservation determines speed.',
'Total energy after collision and tether rupture: the same fixed spring breaking energy and elastic conservation determine retained energy.'
]}
starts={1998:[2,2,2,3,3,4,4,4,5,5,5,6,6,6,7,7,8,8,8,9,9,9,10,10,10],2003:[1,1,1,1,2,2,2,2,3,3,3,4,4,4,5,5,5,6,6,7,7,7,8,8,8,9,9,10,11,11,12,12,12,13,14,14,15,15]}
ii={1998:{13,16,17,24},2003:{19,25,31,32,33,37,38}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(units)==len(rows)==(25 if fid==1998 else 38)
 for n,(u,reason) in enumerate(zip(units,rows),1):
  assert u['decision'] is None;page=starts[fid][n-1]
  shared=([10] if fid==2003 and n in (29,30) else [13] if fid==2003 and n in (35,36) else [])
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join([I]+([II] if n in ii[fid] else [])),required_physics=reason.split(':',1)[0],external_physics_if_any='',decision_reason=reason,format='mixed' if fid==2003 and n>=26 else 'multiple_choice',page_start=page,page_end=page,location_json=json.dumps({'shared_intro_pages':shared,'printed_question_number':n}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Complete actual source {fid} read and every page render inspected. Each printed number is independently answered; 2007 Q26-38 also require separately scored written work. Shared question-group introductions retained; no lettered subpart independently classified.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=?,evidence=?,checked_at=? where file_id=?",(len(units),'Complete source: 25 MCQs in 2008; 38 separately numbered questions in 2007, last 13 written-plus-optical-answer mixed items. The embedded answer key is not an additional unit.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2007_2008_63.json';w.writejson(p,out);w.decisions(p)

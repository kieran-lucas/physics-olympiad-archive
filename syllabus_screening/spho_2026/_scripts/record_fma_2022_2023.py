"""Explicit content decisions for three fully read and visually inspected MCQ papers."""
import json
import workflow as w
c=w.connect();I='I_force_motion';II='II_oscillations_waves';IV='IV_thermodynamics';X='X_wave_optics'
# Each entry is one printed question; common introductions are retained as context.
data={1921:[
([I],'Average speed versus displacement velocity','Circular path length and vector displacement determine the two requested quantities.'),
([I],'Pendulum tangential and centripetal acceleration','The rendered bob position requires gravity resolution and inward radial acceleration.'),
([I],'Vertical-velocity graph of repeated projectile bounces','The actual slope and graph choices use constant gravitational acceleration and instantaneous collision changes.'),
([I],'Inclined-plane frictional work','Force balance and work against gravity/friction determine the energy supplied.'),
([I],'Connected masses on fixed pulleys','The rendered strings impose ordinary acceleration constraints and uniform tensions.'),
([I],'Conical-pendulum centripetal force','Tension components and circular acceleration determine the vertical offset.'),
([I],'Stacked-block contact and friction threshold','Newton laws and contact-force transmission determine the required static friction.'),
([I],'Binary-star center-of-mass velocities','The mass ratio and common circular angular speed determine the speeds; astronomical context adds no external law.'),
([I],'Buoyancy and gravitational energy of displaced air','Ordinary mechanical-energy bookkeeping includes the descending air replaced by the rising balloon.'),
([I],'Projectile aiming at equal launch and target heights','Ordinary ballistic range determines the launch angle.'),
([I],'Projectile height and range constraints','The two given trajectory dimensions determine velocity components and the vertical-launch height.'),
([I],'String tension before and after constraint release','Static force balance and initial pendulum radial acceleration determine the tension comparison.'),
([I],'Inclined applied force and loss of frictional contact','Static-friction capacity and decreasing normal reaction determine sliding versus lift-off.'),
([I],'Support reactions of three connected uniform rods','The actual unequal-leg geometry requires center of mass and torque balance.'),
([I],'Galaxy mass profile from a measured rotation curve','Spherical Newtonian gravity and centripetal acceleration convert the displayed v(r) to enclosed mass; no dark-matter theory is needed.'),
([I,II],'Pendulum harmonic timing with elastic wall reflection','Small-angle oscillation phase and specified restitution determine successive contact times.'),
([I],'Rotational inertia of point and distributed pendula','The rendered pivot positions determine ordinary mass-weighted squared distances.'),
([I],'Scale reading of submerged bags with differing contents','Hydrostatic buoyancy and gravity determine apparent weight; bag geometry introduces no specialized fluid law.'),
([II],'Pendulum measurement uncertainty','The standard period law and uncertainty propagation determine the uncertainty in g; measurement analysis is in scope.'),
([I,II],'Pendulum velocity-component phase curve','The displayed graph choices follow ordinary oscillation kinematics and the rigid length constraint.'),
([I],'Free hoop and bead relative orbit','Momentum conservation and the frictionless circular constraint determine relative speed and return time.'),
([I,II],'Effective spring stiffness with a movable pulley','Hooke law, common string tension and displacement constraints determine all three stiffnesses.'),
([X],'Astronomical parallax geometry','The source specifies the fixed distant objects and Earth orbit; small-angle geometry suffices without astronomical microphysics.'),
([I],'Collision-rate weighting against an oscillating plate','The stipulated elastic moving-wall collision and encounter geometry determine the speed bias; no external statistical physical theory is necessary.'),
([I],'Mechanical energy followed by horizontal projectile flight','The actual slope and ramp height determine launch energy and falling time.')],
1926:[
([I],'Vertical projectile energy and turning height','Ordinary kinetic-to-potential energy conversion determines the maximum rise.'),
([I],'Equal braking acceleration and residual speed','The same stopping distance and deceleration determine impact speed by kinematics.'),
([I],'Inelastic collision momentum and energy loss','Momentum conservation supplies the second final velocity and the lost kinetic energy.'),
([I],'Pendulum release and free projectile path','The rendered tangent and gravity determine the path after the string breaks.'),
([I],'Rolling solid-ball kinetic energy','Rotational inertia and the no-slip condition determine translational plus rotational energy.'),
([I],'Pendulum tension at greatest speed','Energy conservation and radial Newtonian acceleration determine maximum tension.'),
([],'Reading a measured semilog relation','The graph explicitly supplies the logarithmic y scale; ordinary graph interpretation determines the functional form.'),
([I],'Static block-wedge force balance','Both bodies remain at rest; whole-system horizontal force balance determines ground friction.'),
([I],'Pulley displacement ratio and inertial force','The actual single/movable-pulley arrangements require string kinematics and Newton laws.'),
([I,II],'Translating suspended rod oscillations','The parallel strings constrain the rod to ordinary pendulum-like translation; linearized gravity determines the period.'),
([I],'Newtonian potential barrier between two planets','Gravitational potential and mechanical energy determine the minimum crossing speed.'),
([I],'Concentric massless pulley acceleration ratios','The two radii supply string acceleration constraints; net force follows Newton laws.'),
([I],'Hinged laptop lift-off torque minimization','The locked geometry and center of mass determine the least torque-producing force; optimization is mathematical.'),
([I],'Speed components on a frictionless circular bowl','Energy conservation and tangent geometry determine the monotonic behavior of each component.'),
([I],'Projectile impact-height optimization','Constant-gravity flight and differentiation determine the maximizing angle.'),
([I],'Hexagonal pencil tipping versus sliding','The actual cross section fixes lever arms; static torque and friction thresholds determine rolling onset.'),
([I],'Momentum of rotating rod portions about their common center','The defining center-of-mass balance supplies the relation between first mass moments; ordinary rotational kinematics suffices.'),
([I],'Floating cork hydrostatic threshold','Archimedes force balance determines the submerged height; foundational hydrostatics is eligible.'),
([I],'Hydrostatic force with sealed dry contact patches','Integrating pressure and removing the absent underside pressure requires ordinary hydrostatics, not continuum dynamics.'),
([I],'Unforced trajectory on a frictionless guide','Zero normal force makes the supplied track an ordinary ballistic trajectory.'),
([I],'Buoyancy in an accelerating elevator','The problem excludes sloshing and oscillations; effective gravity multiplies weight and buoyancy equally, so no viscous constitutive law is needed.'),
([I],'Symmetric wedge and block constraints','The rendered angles, normal forces and Newton laws determine the downward acceleration.'),
([I],'Comparison of explicitly supplied linear and quadratic drag','The two force-speed models are stated; Newtonian vertical/horizontal coupling determines arrival ordering.'),
([I],'Kepler orbit from apocenter velocity','Newtonian gravitational energy and angular momentum determine ellipse dimensions and area.'),
([I],'Rubber-band radial tension and supporting friction','A small arc obeys ordinary force balance; integrated normal reaction and Coulomb friction determine the threshold.')],
1927:[
([I],'Elastic inclined reflection and projectile flight','The stipulated elastic collision with a 45-degree slope plus gravity determines the second contact.'),
([I],'Inertia about two diameter axes','The actual four point masses and rotated axes require only rotational-inertia geometry.'),
([I],'Seesaw torque after a fulcrum shift','The supplied balanced state and evenly spaced marks determine the new torque balance.'),
([I],'Equal-speed explosion under common gravity','Vector kinematics translates the initial velocity circle by a common gravitational displacement.'),
([I],'Relative river velocities and round-trip averaging','Ordinary velocity addition and distance/time reasoning determine average speed.'),
([I],'Work and momentum scaling under a constant force','Equal applied work over the table and nonrelativistic kinetic energy determine final momentum.'),
([I],'Atwood acceleration and support-scale reaction','Newton laws and rope tension determine the total force on the scale.'),
([I],'Repeated elastic ramp bounces','Tangent/normal velocity components and gravitational flight determine return geometry.'),
([I],'Oblique pushing force and friction threshold','Applied force components change the normal load; Coulomb static friction determines onset.'),
([I,II],'Series-parallel spring stiffness','Hooke law and displacement addition determine the effective spring constant.'),
([I],'Hydrostatic pressure with a tethered floating block','Buoyancy and vertical force balance determine bottom pressure including atmospheric contribution.'),
([I],'Inclined blocks, pulleys and minimum friction','The actual string connections and force balance determine the static-friction condition.'),
([I],'Rigid-ball ballistic pendulum and inelastic angular impulse','Angular momentum during impact and mechanical energy afterward determine height; rotational inertia is expressly in scope.'),
([I,IV],'Surface-energy decrease in stipulated droplet breakup','The statement specifies breakup and damping. Ordinary liquid volume conservation and surface energy determine the final trend without requiring a Rayleigh-Plateau instability derivation.'),
([I],'Centripetal-force deficit and rocket recoil','Newtonian circular acceleration and the displayed exhaust directions determine which thrust maintains the faster orbit.'),
([I],'Location of normal reaction from static torque balance','The source defines the equivalent resultant; ordinary gravity and friction torque determine its line of action.'),
([I],'Puck collision with a translating box','Elastic momentum exchange and relative velocity determine the next transit time.'),
([I,II],'Vertical normal mode of a rod on two springs','Hooke restoring force and rod mass determine translational oscillation frequency.'),
([I,II],'Rotational normal mode of a rod on two springs','The common apparatus and small rotation determine restoring torque and rotational inertia; it remains an independent printed MCQ.'),
([I],'Rolling hollow sphere on an accelerating plane','No-slip acceleration and rotational Newton law determine the sphere acceleration.'),
([],'Propagation of measured length and width uncertainties','Independent measurement uncertainties and the explicit area/perimeter definitions suffice; no external physics is needed.'),
([I],'Newtonian bound-orbit collision with a planet','Gravitational energy and orbital turning points determine the safe launch direction.'),
([II],'Velocity-acceleration phase graph of a harmonic oscillator','The rendered graph choices require ordinary harmonic phase relations.'),
([I],'Relative energy on a steadily moving ramp','Galilean velocities and mechanical energy in the ramp frame determine lab-frame energy gain.'),
([I],'Mutual gravitational fall time scaling','Newtonian two-body relative acceleration and mass scaling determine the time ratio.')]
}
# Inclusive source page ranges were read directly from all three complete papers.
starts={1921:[2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,6,6,7,7,7,8,8,8,9,9],1926:[2,2,2,2,2,3,3,3,3,4,4,4,5,5,6,6,6,7,7,7,8,9,9,9,9],1927:[2,2,2,3,3,3,3,4,4,4,4,5,5,6,6,6,7,7,7,8,8,8,8,9,9]}
ends={1921:{15:6,23:9},1926:{9:4,12:5,14:6,17:7,20:8},1927:{7:4,11:5,16:7,19:8,23:9}}
out=[]
for fid,rows in data.items():
 units=sorted(c.execute('select * from units where source_file_id=?',(fid,)).fetchall(),key=lambda r:int(r['problem_number']))
 assert len(rows)==len(units)==25
 for n,((domains,physics,reason),u) in enumerate(zip(rows,units),1):
  assert u['decision'] is None
  ps=starts[fid][n-1];pe=ends[fid].get(n,ps)
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='',decision_reason=reason,format='multiple_choice',problem_number=str(n),page_start=ps,page_end=pe,location_json=json.dumps({'acquisition_problem_number':u['problem_number'],'source_printed_question':str(n),'shared_context_questions':'18-19' if fid==1927 and n in (18,19) else None}),visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence=f'Read complete actual statement/options text and all physical pp2-9 renders for file {fid}. Printed 1-25 remain independent MCQ units; paper B acquisition 26-50 is mapped to its actual printed 1-25 without altering raw metadata.'))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=25,evidence=?,checked_at=? where file_id=?",('Full nine-page MCQ paper inspected: precisely 25 printed questions; shared introductions preserved, not additional or merged units.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fma_2022_2023_75.json';w.writejson(p,out);w.decisions(p)
print('Saved 75 independent MCQ content decisions; all KEEP.')

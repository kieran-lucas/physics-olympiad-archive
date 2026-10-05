"""Reviewer-authored findings for six complete, inspected BAUPC papers.

Each tuple is a separately considered top-level problem; this only persists it.
All listed statements, including garbled-text files, were visually read in full.
"""
import sys,subprocess
import workflow as w
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';X='X_wave_optics'
papers=[
 (6384,3160,2003,[
 (1,[1,1],I,'Variable-mass momentum flux and rope tension','The released folded rope requires momentum balance and gravity, with no material constitutive theory.'),
 (2,[1,1],I,'Gravity, tension and constrained unwinding','The wound string angle follows Newtonian trajectory/energy reasoning.'),
 (3,[1,1],VI,'Ohm law and self-similar resistor reduction','The nested-square infinite circuit adds geometric recursion, not external physics.'),
 (4,[2,2],VII+';'+I,'Lorentz force and supplied velocity-proportional friction','The two spiral stopping displacements determine a classical magnetic/damping ratio; the force law is supplied.'),
 (5,[2,2],I,'Elastic impulses, rotation and repeated projectile bounces','The no-slip rubber collision law and inertia are supplied; impulse/energy and gravity suffice.'),
 (6,[2,2],I,'Rolling constraints, angular momentum and circular force balance','The ball on a cone is explicitly rigid-body dynamics; optimizing its speed is mathematical difficulty rather than external theory.')]),
 (6385,3161,2002,[
 (1,[2,2],I+';'+IV,'Hydrostatic pressure and thermal expansion','Heating either trapezoidal vessel changes density/height; ordinary pressure equilibrium determines flow direction.'),
 (2,[3,3],I,'Tension, circular motion and constrained acceleration','The pulled string must stay tangent to a pole; the statement explicitly instructs ignoring relativity.'),
 (3,[3,3],I,'Projectile motion, impulsive friction and sliding work','The brick launch angle is a Newtonian range/stopping-distance optimization.'),
 (4,[4,4],I+';'+IV,'Thermal expansion and distributed static friction balance','The metal sheet creeping on a roof uses a supplied expansion relation and ordinary force balance.'),
 (5,[4,4],VI+';'+I,'Image-charge electrostatics and a supplied time-lag dissipation model','The lag of the image charge is explicitly supplied; Coulomb forces and small-velocity expansion determine damping, not microscopic conductor theory.'),
 (6,[4,4],I+';'+II,'Conical pendulum, energy and slow constraint change','The gradually winding string is Newtonian circular motion with the stated quasi-static approximation.')]),
 (6386,3164,2001,[
 (1,[2,2],I,'Rolling rigid-body motion and torque','Keeping the ball centre fixed in an accelerating cylinder uses Newton/Euler equations and the supplied inertia.'),
 (2,[2,2],X,'Geometrical reflection and isotropic emission','The reflecting cone collects light through ordinary ray geometry; the solid-angle calculation is a mathematical tool.'),
 (3,[3,3],I,'Inclined-plane Newton equations with velocity-directed friction','The asymptotic speed is an in-scope friction problem despite its coupled nonlinear algebra.'),
 (4,[3,3],III+';'+IV,'First law, ideal-gas internal energy and cycle efficiency','The P-V triangular cycle and internal energy are supplied; heat intake/rejection are standard thermodynamics.'),
 (5,[4,4],I,'Relative kinematics on a uniformly stretching support','The ant and rubber band obey a supplied kinematic stretching assumption; no elasticity theory is needed.'),
 (6,[4,4],VI,'Kirchhoff laws, superposition and resistor-network linear algebra','The arbitrary connected network requires circuit physics with a proof; mathematical generality is not an out-of-scope theory.')]),
 (6387,3166,2000,[
 (1,[1,1],I+';'+II,'Physical-pendulum energy and pivot optimization','The fastest falling uniform stick requires rigid-body inertia and gravity.'),
 (2,[1,1],VI,'Induced conductor charge, potential and field energy','Changing the right-angle plates to insulators fixes their induced charge; ordinary electrostatics determines all three work/energy parts.'),
 (3,[1,2],I+';'+III+';'+X,'Hydrostatic ideal-gas atmosphere and refraction','The refractive-index/density law is supplied; Newtonian gravity, pressure balance and Snell-law geometry suffice for the circular ray.'),
 (4,[2,2],I,'Sequential elastic collisions and continuum limiting mathematics','The semicircle of masses involves only momentum/energy transfers despite the infinite-N limit.'),
 (5,[2,2],I,'Rolling constraints and rotation on a moving surface','The sphere on the turntable requires rigid-body dynamics and supplied inertia, not a specialized material model.'),
 (6,[2,3],I+';'+II,'Variable-mass momentum and damped spring oscillations','The rope entering/leaving a floor heap loses energy through ordinary momentum transfer; the geometric approximations are specified.')]),
 (6388,3168,1999,[
 (1,[2,2],VI,'Coulomb potential integration and scale symmetry','Both sphere and cube potential ratios follow electrostatics; internal (a,b) remain one top-level problem.'),
 (2,[2,2],I,'Rolling kinematics and instantaneous velocity','The sharp parts of photographed spokes depend on motion during exposure, not imaging microphysics.'),
 (3,[2,2],I,'Combined tangential/radial acceleration and friction-limited optimization','The motorcycle shortest acceleration path is conventional Newtonian mechanics.'),
 (4,[2,2],I,'Relative planar pursuit kinematics','Both fox/rabbit path rules specify the motion completely; calculus is the additional challenge.'),
 (5,[2,2],I,'Accreting mass, momentum and geometry','The cloud/raindrop model explicitly states sticking droplets and spherical shape; no cloud microphysics is required.'),
 (6,[3,3],I+';'+II,'Elastic energy and constrained circular winding','The sticky pole and zero-natural-length spring are specified idealizations; ordinary mechanics determines the time.')]),
 (6389,3170,1998,[
 (1,[2,2],I,'Contact normal forces and translational Newton laws','The three frictionless cylinders remain in contact according to ordinary force-balance inequalities.'),
 (2,[2,2],VII+';'+I,'Lorentz-force motion and axisymmetric magnetic flux','Zero total magnetic flux and the radial field symmetry determine the outgoing direction using classical field/motion laws.'),
 (3,[2,2],I,'Newton laws, pulley constraints and infinite-chain limits','The infinite Atwood machine is a mechanics recursion, not an external physical theory.'),
 (4,[2,2],VI,'Ohm law, symmetry and resistor-network superposition','The icosahedron shape is fully defined; circuit physics suffices despite the polyhedral geometry.'),
 (5,[3,3],I,'Angular momentum, torque and slow gyroscopic precession','The stacked symmetric tops lie within the explicit rigid-body/angular-momentum syllabus; the large-spin approximation is supplied.'),
 (6,[3,3],I+';'+II,'Pendulum oscillations and slow coupled Atwood motion','Averaging the small swings and using energy/constraints determines the slow rise; mathematical multiple timescales do not add external physics.')])]
for pid,fid,year,rowspec in papers:
    src=w.connect().execute('select * from containers where source_problem_id=?',(pid,)).fetchone()
    items=[dict(number=str(n),page_start=ps[0],page_end=ps[1],format='theory',location={'top_level_label':str(n),'boundary_source':'Visually read numbered header; internal lettered parts retained.'}) for n,ps,_,_,_ in rowspec]
    b=w.ROOT/f'reviews/baupc_{year}_boundaries.json'
    w.writejson(b,[{'source_problem_id':pid,'boundary_evidence':f'BAUPC {year}: all six complete numbered problems read; actual content pages and diagrams visually inspected. The cover/header specifies six questions. Broken embedded font encodings were bypassed by direct page inspection. No internal lettered parts were split.','units':items}]);w.derive(b)
    rows=[[f'derived::{src["source_sha256"][:16]}::{pid}::{n}','KEEP',dom,phys,reason,f'BAUPC {year} Problem {n}: complete statement and diagrams visually read on source file {fid}, physical pages {ps[0]}-{ps[1]}.',ps,'theory',1,0,'high',''] for n,ps,dom,phys,reason in rowspec]
    p=w.ROOT/f'reviews/baupc_{year}.json';w.writejson(p,{'rows':rows})
    subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(p)],check=True)

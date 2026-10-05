"""Explicit actual-content OPhO reviews, including a source-withdrawn item."""
import workflow as w
c=w.connect();out=[]
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
items=[
(1,4,4,'REJECT',[],'Maximum electron speed from relativistic energy budget','Unsupplied relativistic energy-speed relation controls the entire question.'),
(2,4,4,'KEEP',[I],'Circular turning geometry, static friction and centripetal force',None),
(3,4,4,'KEEP',[I],'Water-wheel momentum, rotational energy and gravitational power with stipulated portals',None),
(4,4,4,'KEEP',[X],'Fibre total internal reflection and pulse travel-time spreading',None),
(5,5,5,'KEEP',[I,II],'Signal travel time with explicitly supplied Hubble velocity-distance model','Hubble expansion is supplied as a velocity law; the solution uses ordinary kinematics and a first-order differential equation, not cosmological field theory.'),
(6,5,5,'KEEP',[I],'Surface-tension energy and gravity at equilibrium',None),
(7,5,5,'KEEP',[I],'Rigid-body gravitational tidal torque and stability',None),
(8,5,5,'KEEP',[III,IV],'Adiabatic compression/expansion, vapour saturation and given linked vapour-pressure model',None),
(9,5,6,'KEEP',[III,IV],'Shared bottle-trick stem, adiabatic partial pressures and wall condensation',None),
(10,6,6,'KEEP',[IV],'Evaporative cooling, latent heat and heat-transfer rate',None),
(11,6,6,'KEEP',[VI],'Boundary potential, linear conduction and harmonic field symmetry',None),
(12,6,6,'KEEP',[I,II],'Beads, elastic cord segmentation and small-oscillation energy',None),
(13,7,7,'KEEP',[I],'Repeated disk impacts, restitution and averaged vertical momentum flux',None),
(14,7,7,'KEEP',[I],'Constrained cable-car motion, energy and gravitational transit time',None),
(15,7,7,'KEEP',[I,VII,VIII],'Supplied monopole field/force, Faraday induction and dissipative mechanical motion','Both nonstandard monopole relations are supplied; the remaining work is field integration, induction, resistance and Newtonian motion.'),
(16,7,8,'KEEP',[I],'Spinner rotation, contact friction and probability over initial speeds',None),
(17,8,8,'KEEP',[I],'Torque-limited tentacle grip, force balance and Coulomb friction',None),
(18,8,8,'KEEP',[I,XII],'Alpha-decay energy, recoil statistics and half-life population',None),
(19,9,9,'KEEP',[I,IV],'Supplied linear drag, rotational torque balance and frictional melting',None),
(20,9,9,'KEEP',[I,X,XI],'Specular ray paths and photon momentum pressure in two dimensions',None),
(21,9,9,'KEEP',[I,II,VI],'Spring-capacitor electrostatic attraction, equilibrium stability and energy barrier',None),
(22,9,9,'KEEP',[I,III,VI],'Classical Coulomb collision cross-section, angular momentum and Maxwell averaging','The statement explicitly treats particles classically. The solution confirms Coulomb energy/angular momentum and thermal speed averaging suffice; plasma microphysics is not required.'),
(23,10,10,'KEEP',[I,II],'Cone rolling geometry, rotational inertia and small oscillations',None),
(25,10,10,'REJECT',[],'Proper acceleration, proper time and relativistic racing trajectories','Proper-time/acceleration transformations are not supplied and structurally determine the entire race.'),
(26,10,10,'KEEP',[I,X,XI],'Prism refraction paths and net incident/outgoing photon momentum',None),
(27,10,10,'KEEP',[I,II],'Massive spring energy, rotating constraint and closed oscillatory trajectories',None),
(28,10,10,'KEEP',[II,X],'Echo ray geometry, solid-angle sums and limiting approximations','The solution uses reflected-ray geometry and asymptotic summation. Extreme ratios and difficult mathematics do not introduce external physics.'),
(29,11,11,'KEEP',[I,VII],'Uniform magnetization, equivalent surface pole/field forces and mechanical stress balance','Magnetization and magnetic forces are expressly in scope. The solution uses the ordinary surface-pole representation and field-force approximations, not microscopic condensed-matter theory.'),
(30,11,11,'REJECT',[],'Simultaneity, invariant spacetime interval and Lorentz-contracted circular trajectories','Unsupplied relativistic simultaneity and frame transformations are essential throughout.'),
(31,11,11,'REJECT',[I,VI,VII],'Relativistic hidden mechanical momentum of a magnetic dipole in an electric field','Official solution requires unsupplied hidden-momentum coupling or electromagnetic duality with a specialized prior result. Ordinary rotation and a familiar electric field alone do not supply the central insight.'),
(32,11,11,'REJECT',[III,XII],'Fusion power requiring semiclassical Coulomb-barrier tunneling probability','Official solution centrally uses an unsupplied WKB tunneling law and Gamow-type thermal average. Familiar ideal-gas and nuclear-energy portions do not supply the fusion rate.'),
(33,11,11,'KEEP',[I,III,IV],'Adiabatic pump work, balloon surface tension and gas internal energy',None),
(34,11,12,'KEEP',[III,IV],'Hydrostatic balance, latent heat, saturation equilibrium and adiabatic moist-air energy balance','The coupled model follows ordinary thermodynamic phase equilibrium, ideal gases and hydrostatics; numerical integration difficulty does not require external atmospheric theory.'),
(35,12,12,'KEEP',[I,VII,XI],'Charged-particle circular arcs and de Broglie phase interference',None)]
solutions={5,6,7,10,11,15,22,26,28,29,30,31,32,33,34}
for n,s,e,decision,domains,physics,reason in items:
 uid='raw::'+str(4250+n);u=c.execute('select * from units where screening_unit_id=?',(uid,)).fetchone();assert u and u['decision'] is None
 out.append(dict(screening_unit_id=uid,decision=decision,confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='Unsupplied special relativity' if n in (1,25,30) else 'Unsupplied hidden momentum' if n==31 else 'Unsupplied WKB tunneling' if n==32 else 'Supplied Hubble velocity law' if n==5 else 'Supplied monopole force/field' if n==15 else '',decision_reason=reason or 'The actual required physics is '+physics[0].lower()+physics[1:]+', within the syllabus or ordinary general-physics foundations.',page_start=s,page_end=e,format='numerical',visual_inspection_used=1,solution_used=int(n in solutions),boundary_status='content_boundary_verified',evidence='Complete source file 3071 read in embedded text and page renders; identified statement pages and shared stems preserved. Official solution file 3073 inspected for the listed ambiguous physical models.'))
p=w.ROOT/'reviews/resume_opho_2025_open_34.json';w.writejson(p,out);w.decisions(p)
c.execute("update units set review_status='unresolved_source_unavailable',boundary_status='source_removed_no_statement',page_start=10,page_end=10,format='unknown',visual_inspection_used=1,source_quality_notes=?,evidence=? where screening_unit_id='raw::4274'",('OPhO 2025 Open physical page 10 explicitly says Problem 24 was removed from the test. No statement exists in this paper; no physics decision manufactured.','Actual printed removal notice visually and textually inspected; source logical row retained.'))
c.execute('update units set source_quality_notes=? where screening_unit_id=?',('Official solution pp35-36 contains inconsistent methane labels/constants and a temperature table starting near 300 K despite a 320 K water statement. Scope decision uses the statement; numerical solution requires correction before future training use.','raw::4284'))
for uid in ['raw::4258','raw::4259']:c.execute('update units set source_quality_notes=? where screening_unit_id=?',('Shared stem on physical page 5 is essential; it directs the reader to a linked Buck-formula vapour-pressure calculator, not a local numerical table.',uid))
c.commit();print('Saved 34 decisions and one explicit unavailable source item')

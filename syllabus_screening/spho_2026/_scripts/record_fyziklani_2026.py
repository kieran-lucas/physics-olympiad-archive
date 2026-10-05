"""Explicit content decisions following complete 58-statement inspection."""
import json
import workflow as w
c=w.connect();fid=2839
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
rows=[
('AA',[I],'Buoyancy, mass conservation and melting volume','Floating equilibrium and conserved mass determine the water level; no specialized phase-transition model is needed.'),
('AB',[I],'Projectile flight between equal-height ramps','The supplied launch angle and river width require ordinary projectile kinematics.'),
('AC',[I],'Relative speeds upstream and downstream','Galilean addition of the given river and swimming velocities determines both travel times.'),
('AD',[],'Angular measurement averaging with a wrap at 360 degrees','This self-contained directional-data exercise uses ordinary trigonometric/statistical tools, without flocking theory.'),
('AE',[I],'Gravitational work against two friction forces','The cutting energy is supplied; the only physical calculation is mechanical work and frictional loss.'),
('AF',[],'Area ratios under a supplied uniform coating model','The statement stipulates constant coating thickness. Geometry alone determines the ratio; no fluid coating theory is required.'),
('AG',[XII],'Decay energy, power, half-life and radioactive activity','Nuclear power and activity follow the supplied per-event energy and the ordinary exponential decay law.'),
('AH',[I],'Projectile residence time and steady mass flux','Each water element follows ordinary ballistic motion; stream area, density and flight time give the airborne mass.'),
('BA',[III,XII],'Mass per crystal cell and molar particle counting','The lattice is explicitly drawn. Counting shared atoms and dividing mass by cell volume requires no condensed-matter band theory.'),
('BB',[I],'Tipping torque and limiting static friction','The specified center of mass and horizontal push reduce to torque balance and friction constraints.'),
('BC',[I,IV],'Surface-tension support with supplied temperature dependence','Ordinary surface tension as force per length and a supplied linear temperature law determine the sinking limit.'),
('BD',[I],'Conical-pendulum launch, projectile travel and pursuit','The sequential stages use force balance and ordinary kinematics; internal calculations remain one top-level problem.'),
('BE',[],'Independent spatial hit probabilities and conditional survival','The classical probability model is fully specified. The Schrodinger context requires no quantum mechanics; this is mathematical modeling practice.'),
('BF',[I],'Rolling-sphere rotational energy and gravitational height','Rigid-body inertia, rolling constraint and conservation of energy control the speed ratio.'),
('BG',[I],'Symmetric contact forces, friction and vertical support','The finger arrangement and maximum normal force are specified; ordinary force balance determines the angle.'),
('BH',[IV],'Thermal expansion of a bolt and nut','The expansion coefficient is given. General-physics linear thermal expansion and temperature conversion suffice.'),
('CA',[XII],'Half-life from a specified decayed fraction','The fictional context is removed by the ordinary exponential radioactive decay calculation.'),
('CB',[I],'Rolling rotational energy and stipulated resistive work','The source gives the resistance force; energy and the solid-cylinder inertia determine stopping distance.'),
('CC',[VI,VII],'Electric and magnetic force cancellation','The Wien-filter arrangement is explicitly defined; Coulomb and Lorentz forces suffice.'),
('CD',[I],'Ballistic water paths from a rotating nozzle','Projectile motion and rotational launch velocity determine the wall-clearance condition without fluid dynamics.'),
('CE',[II],'Doppler shifts on emission and reflection','Ordinary sound Doppler reasoning determines the returned horn frequency.'),
('CF',[I],'Composite rod-and-disk moments of inertia','The complete geometrical mass model is supplied; summing rotational energies gives the required work.'),
('CG',[I,II],'Harmonic acceleration and maximum static friction','The given sinusoidal plate motion and Coulomb friction determine the slipping threshold.'),
('CH',[VI],'Gauss flux and polyhedral symmetry','Gauss law is explicitly in scope and all twenty faces are equivalent.'),
('DA',[IV,VI],'Ohm law, heating power and supplied thermal feedback','Both resistance-temperature and temperature-power laws are supplied; no material transport theory is required.'),
('DB',[I],'Simultaneous elastic sphere collisions','The collision geometry and masses require momentum and kinetic-energy conservation.'),
('DC',[I,VI,VII],'Conical motion with Coulomb repulsion and magnetic force','All fields and charges are specified; radial force balance uses ordinary electromagnetic and mechanical laws.'),
('DD',[I],'Coriolis force and overturning torque','The Coriolis formula is explicitly supplied, and relativity is explicitly neglected; torque balance suffices.'),
('DE',[I],'Projectile clearance optimization and spring energy','Obstacle geometry, ballistic motion and elastic energy determine minimum spring stiffness; difficulty is mathematical.'),
('DF',[VI],'Coulomb-field superposition in a pentagram','The task requires only vector electrostatic superposition and geometric symmetry, not an external physical theory.'),
('DG',[I],'Rotating parabolic constraint equilibrium','Gravitational and centrifugal-force components along the prescribed curve determine the condition.'),
('DH',[I],'Relative motion and crossing-speed optimization','The rendered car/pedestrian geometry is an ordinary relative-velocity construction.'),
('EA',[I,XII],'Two-body decay energy and vector momentum with supplied dispersion','The statement supplies E=sqrt(m0^2*c^4+p^2*c^2). Conservation of energy and momentum plus geometry determine the angle; unsupplied relativity is not necessary.'),
('EB',[I,VI],'Three charged pendula in symmetric force balance','Coulomb force, gravity and tension determine the triangular equilibrium; numerical solution is mathematical.'),
('EC',[I],'Newtonian orbit after a stipulated mass/momentum change','Momentum conservation, gravitational orbital energy and Kepler motion determine the new period without relativistic dynamics.'),
('ED',[X],'Thin-film optical path and reflection phase','Interference and refraction determine the antireflection thickness; no advanced coating theory is required.'),
('EE',[I,II],'Constrained physical pendula and rod rotational inertia','Kinetic energy, potential energy and small oscillations determine the period of the three-rod linkage.'),
('EF',[VI,XI],'Photon momentum and inverse-square shell-force cancellation','Isotropic emission is stipulated. The official solution reduces photon-pressure forces to ordinary shell symmetry; no radiative-transfer theory is required.'),
('EG',[I],'Variable-mass momentum, buoyancy and drift distance','The given steady influx acts as inelastic mass capture; momentum conservation and buoyancy determine the sinking time and travel distance.'),
('EH',[I,X],'Parabolic focus geometry and changing control parameter','The mirror shape and crank relation are given; ray geometry and differentiation follow the approaching ship.'),
('FA',[I],'Angular momentum redistribution and rod inertia','The mass injection and initial rest condition are stipulated; ordinary angular momentum conservation supplies the rotation change.'),
('FB',[I,II],'Pulley rotational energy and spring oscillations','The no-slip pulley constraint and Hooke law determine the effective inertia and restoring stiffness.'),
('FC',[I],'Symmetric pursuit with explicitly supplied speed-distance law','The velocity law is supplied; vector geometry and a first-order kinematic equation determine elapsed time.'),
('FD',[I],'Hydrostatic pressure integrated over a cone','Ordinary pressure variation and surface-force resolution determine the force; no advanced continuum-fluid theory is required.'),
('FE',[I,IV],'Rotational energy converted into water internal energy','The source explicitly stipulates angular-momentum loss; within that stated model, rotational inertia and heat capacity suffice.'),
('FF',[I],'Center of gravity in an inverse-square gravitational field','Newtonian force integration and the supplied logarithmic expansion determine the center shift.'),
('FG',[VI],'Loaded voltage divider, electric power and efficiency','Ordinary resistor-network analysis and supplied lamp rating determine the resistance.'),
('FH',[IV,X],'Thin-film interference and freezing-volume change','Interference, ordinary water/ice density and conservation of mass determine the wavelength shift.'),
('GA',[I],'Cone-on-diverging-rails geometry and gravitational energy','The rendered geometry determines whether the center of mass descends; no antigravity theory is involved.'),
('GB',[X],'Light attenuation with a specified varying absorption coefficient','Ordinary Beer-Lambert attenuation and integration of the supplied concentration profile suffice; no microscopic optical-material theory is necessary.'),
('GC',[IV],'Spatially varying ruler thermal expansion','The temperature profile and expansion coefficient are supplied; integrating measurement-scale changes uses general physics and calculus.'),
('GD',[I],'Quasistatic buoyancy, gravitational energy and tipping geometry','The rendered container and buoy constraints require hydrostatics, center-of-mass energy and geometry.'),
('GE',[X],'Optical-fiber ray travel time and isotropic angular averaging','The source defines a ray model, refractive index and air cladding; total internal reflection and geometrical path averaging suffice, without guided-mode theory.'),
('GF',[VI,VII,XII],'Ion current weighting with supplied ionization cross-section ratios','All species-dependent cross-section ratios are supplied. Charge counting and two linear mixture equations suffice; microscopic ionization theory is unnecessary.'),
('GG',[XI],'Solar photon momentum absorbed and reflected by Earth','Ordinary radiation pressure and solar flux geometry determine the force.'),
('GH',[II,VI],'Charged-ring potential expansion and small oscillations','Coulomb superposition and linearized restoring force determine the period; the integrals are mathematical.'),
('HA',[I],'Time-varying slope with static and kinetic friction','The plane-motion constraint is specified; Newton laws, friction thresholds and integration determine travel distance.'),
('HB',[VI],'Conductor equilibrium, electrostatic dipole and field maximum','The official solution uses equipotential boundaries and dipole superposition, both ordinary electrostatics; no external condensed-matter theory is needed.')]
f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
pack=json.loads((w.ROOT/'cache'/f'{f["sha256"]}.statement_pack.json').read_text(encoding='utf-8'))
assert not pack['warnings'];locs={r['number']:r for r in pack['statements']}
units={r['problem_title'].split('. ',1)[0]:r for r in c.execute('select * from units where source_file_id=?',(fid,))}
assert len(units)==len(rows)==len(locs)==58
visual={'AH','BA','CE','CF','DC','DF','DH','EA','ED','EE','GA','GD','GE','GH','HB'}
solutions={'AA','AB','AC','AD','AE','AF','AG','AH','BA','BB','BC','BD','BE','BF','CF','DC','DF','DH','EA','ED','EE','EF','EG','FE','FF','GB','GC','GE','GF','GG','GH','GA','HB'}
out=[]
for number,domains,physics,reason in rows:
 u=units[number];p=locs[number];assert u['decision'] is None
 out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='Specialized dispersion relation explicitly supplied' if number=='EA' else '',decision_reason=reason,format='numerical',problem_number=number,page_start=p['page_start'],page_end=p['page_end'],location_json=json.dumps({'statement_locations':p['locations'],'acquisition_problem_number':u['problem_number'],'navigation_pack':f'{f["sha256"]}.statement_pack.json'}),visual_inspection_used=int(number in visual),solution_used=int(number in solutions),boundary_status='content_boundary_verified',evidence='Read all 58 actual statements from combined source file 2839; typography separates original slanted statements from regular-font worked solutions. Relevant equations and source diagrams inspected in page renders; same-file official solution consulted as recorded.'))
c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=58,evidence=?,checked_at=? where file_id=?",('All 58 printed labels AA-HB reconcile with raw logical rows. Complete combined-paper navigation contains no missing top-level statement; internal worked solution stages are not units.',w.now(),fid))
c.commit();p=w.ROOT/'reviews/resume_fyziklani_2026_58.json';w.writejson(p,out);w.decisions(p)
c.execute('update units set source_quality_notes=? where screening_unit_id=?',('The statement says angular momentum is not conserved due to friction, but internal water-shell friction alone would conserve total angular momentum. An external dissipative torque/rest constraint is implicit in the source energy model; clarify before later training use.',units['FE']['screening_unit_id']))
c.execute('update units set source_quality_notes=? where screening_unit_id=?',('Three occupied pentagram vertices/intersections are not uniquely specified by the text and no arrangement diagram appears. Official solution selects a particular symmetric arrangement; preserve this ambiguity for later extraction.',units['DF']['screening_unit_id']))
c.commit();print('Saved 58 actual-content numerical-unit decisions; source ambiguities retained.')

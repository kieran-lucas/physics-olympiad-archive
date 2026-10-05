"""Persist explicit actual-content reviews of all 68 printed 2025 questions."""
import json
import workflow as w
c=w.connect();fid=3101
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
rows=[
(1,[I],'Spiral winding and geometric length constraints','The strip-width and winding assumptions are supplied; no-slip geometry determines the requested dimension.'),
(2,[I],'Belt geometry and no-slip rim speeds','Ordinary circumference, path length and tangential velocity determine both belt dimensions.'),
(3,[III],'Ideal-gas changes of pressure, temperature and volume','The two stated percentage changes determine volume by the ideal-gas equation.'),
(4,[I],'Projectile trajectory over a table-tennis net','Gravity-driven flight and required apparatus dimensions determine the serve limit; sports context adds no external physics.'),
(5,[VI],'Source internal resistance and loaded terminal voltages','Ordinary circuit laws determine the internal resistance from the two load configurations.'),
(6,[I,II],'Linked rigid-body pendula and small oscillations','The supplied rods and masses determine gravitational torque and rotational inertia; linearization gives the period.'),
(7,[IV,VI],'Electrical and optical power with thermal energy balance','Both energy fluxes are supplied. Their difference and ice latent heat determine cooling; LED microscopic theory is unnecessary.'),
(8,[III],'Ideal-gas counting and stipulated surface adsorption geometry','Pressure, gas amount and the given molecular footprint determine adsorbed surface area; no adsorption isotherm or material theory is required.'),
(9,[I,VII],'Decay charge conservation and magnetic curvature','The stipulated common daughter speed and charge/mass conservation determine the child orbit by the Lorentz force.'),
(10,[I],'Static torque and wardrobe toppling threshold','Gravity and the applied supporting force determine the rotational equilibrium condition.'),
(11,[],'Rotated cube geometry and staircase inclination','The actual task is spatial geometry of the supplied cube construction; crystal structure is context and requires no condensed-matter theory.'),
(12,[VI,VII],'Current from electrical power and parallel-wire magnetic force','Ordinary voltage/current power and current magnetic interaction determine the force.'),
(13,[I,II],'Repeated spring launches and lossless rebounds','The stated reset and loss assumptions define the model; energy and ballistic timing determine the recurrence.'),
(14,[VI],'Bridge circuit with a specified voltmeter load','The rendered resistor network requires ordinary Ohm and Kirchhoff laws.'),
(15,[II,IX],'Radar echo delay and low-speed Doppler shift','Flight geometry and ordinary wave timing/Doppler reasoning determine the velocity; relativistic kinematics is not needed at the stated speed.'),
(16,[VI,VII],'Nonrelativistic electron helix in a magnetic field','The stated low electron energy, helix pitch and radius determine velocity components and magnetic induction.'),
(17,[I],'Wind force and rigid-body tipping torque','The given drag coefficient and density support the ordinary quadratic-drag definition; force and torque balance determine the threshold.'),
(18,[XII],'Radioactive decay with specified branching probabilities','Exponential decay and branch fractions determine accumulated argon; no nuclear-structure model is needed.'),
(19,[I,III],'Connected pistons, pulley force balance and ideal gas','The actual apparatus supplies all geometric constraints; tensions, gas pressure and the ideal-gas law determine equilibrium.'),
(20,[I,II],'Rolling hoop with a spring on an incline','Rotational inertia, rolling constraints and spring restoring energy determine the oscillation period.'),
(21,[VII],'Magnetic curvature of a relativistic proton','The central numerical field determination needs an unsupplied relativistic energy-momentum relation; the given energy is outside the nonrelativistic regime.'),
(22,[I,XI],'Stellar radiation balance and planetary orbital period','Black-body radiative power and Newtonian gravitation determine the new orbital period; astronomy is only the application.'),
(23,[I],'Contact normals in an explicitly supplied roughness geometry','The sinusoidal interlocking model is specified. Contact-force geometry determines the effective friction without tribology theory.'),
(24,[I,II,VI],'Charged conducting sphere bouncing between plates','Contact charging, plate field and restitution are explicitly prescribed; Newtonian motion and the given loss determine the steady frequency.'),
(25,[I],'Idealized yo-yo motion and rotational energy','The supplied cylinder dimensions and negligible turnaround time define an ordinary rolling/unwinding model.'),
(26,[I,VII,VIII],'Falling conducting square in a symmetric wire field','Magnetic flux symmetry and Faraday induction, together with gravity, determine whether a braking current occurs.'),
(27,[I],'Relativistic proton-thruster momentum flux','The thrust and entire flight time depend on unsupplied relativistic proton momentum at 1 TeV; Newtonian rocket balance alone cannot determine the requested answer.'),
(28,[I],'Cylinder rolling off a moving block and frictional catch-up','Translation, rotation and the specified friction determine the post-contact velocity.'),
(29,[I],'Propeller angular momentum, turning torque and hydrostatic trim','Rigid-body angular momentum and ordinary buoyant torque explain the boat pitch; no specialized marine-fluid model is required.'),
(30,[I,X],'Earth rotation, horizon geometry and sunrise timing','The required reasoning is ordinary relative angular motion and geometric visibility.'),
(31,[I,III],'Stipulated molecular capture and rotational gas torque','The statement supplies particle-transfer and surface-velocity assumptions. Momentum flux and rigid-body torque suffice without unsupplied continuum flow theory.'),
(32,[III,IV],'Ideal-gas heat optimization with allowed volume changes','Ideal-gas work, internal energy and isothermal/adiabatic limits determine the optimum; the optimization is mathematical.'),
(33,[I],'Lever, massive pulley and string acceleration constraints','The rendered apparatus requires rigid-body inertia, tensions and Newton laws.'),
(34,[I],'Ideal siphon energy balance and continuity','Ordinary hydrostatic work-energy and volume conservation determine flow in the given idealized geometry; no viscous flow law is needed.'),
(35,[I],'Rotating elastic beam under a specified Young modulus','Uniaxial Hooke/Young response and centrifugal force integration supply the model; general continuum-elastic wave or tensor theory is unnecessary.'),
(36,[VI],'Conductor boundaries and image-charge electrostatics','Equipotential conducting planes and Coulomb superposition determine the field; boundary geometry is mathematical.'),
(37,[I],'Specified vessel geometry and constant volume inflow','Continuity and the given surface profile determine apparent level-rise speed; exceeding c here is a geometric rate, not relativistic particle motion.'),
(38,[I,X],'Projectile shadow and geometric projection speed','Ordinary ballistics and ray geometry determine the greatest shadow speed.'),
(39,[I],'Newtonian planetary flyby scattering','Gravity, orbital energy and scattering geometry control the planetary encounter; no relativistic astronomy is required.'),
(40,[I],'Ideal draining of three hydrostatic liquid layers','Hydrostatic pressure, work-energy and continuity determine the specified ideal flow. Viscosity and capillary effects are explicitly excluded.'),
(41,[],'Cosmological redshift, expanding-space distance and light propagation','The central relation between redshift, cosmic scale factor and present distance is unsupplied. The official solution uses cosmological evolution/light-propagation laws beyond ordinary Doppler and SPhO.'),
(42,[IX,X],'Underwater radiation, Fresnel transmission and total internal reflection','The statement permits the normal-incidence transmission approximation; ordinary optical interfaces and solid-angle integration suffice.'),
(43,[III,IV],'Boltzmann equilibrium in a supplied harmonic potential','The requested spatial probability follows the expressly in-scope Boltzmann distribution and integration; Brownian stochastic dynamics is not required.'),
(44,[I],'Projectile range with air buoyancy at two temperatures','Buoyancy and ballistic acceleration determine the range correction; seasonal context introduces no specialized atmosphere theory.'),
(45,[I,III,IV],'Balloon work with a supplied elastic-energy law','The membrane energy dependence is given. Isothermal ideal-gas work and energy balance determine the result without rubber constitutive theory.'),
(46,[II,VII],'Point-dipole magnetic forces and spring oscillations','The dipole idealization, moments and spring supply an ordinary magnetic restoring-force problem.'),
(47,[IX,X],'Angular Fresnel transmission and isotropic radiation','Maxwell boundary conditions, polarization and total internal reflection determine the transmission integral; no unsupplied advanced material-optics theory is required.'),
(48,[III,IV],'Ideal-gas entropy and microstate-count ratio','The official method uses ideal-gas entropy change and Boltzmann counting. The demon story does not require an unsupplied measurement or information-dynamics model.'),
(49,[I,II],'Constrained articulated-rod metronome','The actual rod constraints determine inertia and gravitational restoring energy; small oscillations supply the period.'),
(50,[II,VI],'Conducting-sphere electrostatics and axial harmonic equilibrium','Conductor image charges, electric potential energy and axial curvature determine the oscillation; no external field theory is necessary.'),
(51,[I],'Loaded flexible rod with explicitly supplied torque-curvature law','The source supplies the constitutive relation. Torque balance and curvature geometry determine deflection; difficult integration is mathematics rather than an unsupplied elasticity prerequisite.'),
(52,[XII],'Neutron conversion with supplied cross-section and charged-track ranges','Reaction energies, ranges and detection assumptions are given. Exponential interaction probability and angular geometry suffice without semiconductor-detector microphysics.'),
(53,[I],'Superposed forces with stipulated inverse-power laws','The fictional force laws are supplied. Vector force geometry determines the requested region without external interaction theory.'),
(54,[I],'Specified repose angle on an ellipsoidal surface','The granular threshold is supplied as an angle. Surface normals and geometric integration determine the retained mound without granular constitutive physics.'),
(55,[VI],'Electron emission current with stipulated angular density and yield','The statement explicitly gives the emission model per solid angle. Charge counting and geometric integration determine escape current; surface-emission microphysics is not required.'),
(56,[I],'Acceleration-limited escape on frictional ice','The supplied friction limit defines ordinary Newtonian motion. The optimal trajectory may require difficult calculus but no external physics.'),
(57,[VI,XII],'Battery charge capacity and monovalent-ion counting','Ordinary charge-per-ion counting and molar mass determine lithium quantity and cost; no unsupplied electrochemical potential or reaction theory controls the task.'),
(58,[VI,XII],'Equal stored charge with lithium and sodium ions','The comparison uses ordinary monovalency and mass-per-ion counting; no specialized battery chemistry is needed.'),
(59,[VI],'Battery charging current with terminal voltage and wire resistance','Charge/time and Ohm law determine the cable resistance under the stipulated charging voltage.'),
(60,[VI],'Power-bank energy conversion and effective charge capacity','Given voltage levels and efficiency determine usable stored energy and output charge.'),
(61,[I],'Elastic equal-mass collision and prescribed braking','The collision and constant drag model are stated; momentum and work-energy determine travel.'),
(62,[I],'Partially elastic collision with specified energy loss','The loss fraction is given. Momentum conservation and the prescribed drag determine post-collision travel without material-collision theory.'),
(63,[I],'Two-dimensional elastic collision and maximum deflection','Momentum-vector geometry and kinetic-energy conservation determine the limiting angle.'),
(64,[I],'Oblique rigid-ball impact with a supplied tangential sticking rule','The tangential contact condition is explicitly supplied. Linear/angular impulses and rotational inertia determine the velocities; microscopic collision mechanics is unnecessary.'),
(65,[X],'Spherical-mirror illumination in a permitted paraxial limit','Ray reflection and obstacle geometry determine the illuminated fraction.'),
(66,[X],'Nonparaxial spherical-mirror ray envelope','Exact specular reflection and geometry determine image extent; leaving the paraxial approximation adds mathematical work rather than external optics.'),
(67,[X],'Parabolic reflector with small axial defocus','Ordinary ray reflection in the specified surface determines the reflected spot.'),
(68,[X],'Parabolic-reflector irradiance from an isotropic point source','Incoherent ray power and the surface-to-screen geometric mapping determine irradiance; no unsupplied diffraction or coherence theory is required.')]
f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
pack=json.loads((w.ROOT/'cache'/f'{f["sha256"]}.statement_pack.json').read_text(encoding='utf-8'))
assert not pack['warnings'];locs={r['number']:r for r in pack['statements']}
units={int(r['problem_number']):r for r in c.execute('select * from units where source_file_id=?',(fid,))}
assert len(rows)==len(locs)==len(units)==68
visual={1,2,14,15,19,20,31,33,34,39,42,48,49,50,51,52,54,55,57,58,59,64,66,68}
solutions={1,2,3,14,19,20,21,27,31,33,34,39,41,42,48,49,50,51,54,55,57,58,59,62,63,64,65,66,67,68}
out=[]
for n,domains,physics,reason in rows:
 u=units[n];number=str(n) if n<=56 else f'{"BPR"[(n-57)//4]}.{(n-57)%4+1}';p=locs[number]
 assert u['decision'] is None
 decision='REJECT' if n in (21,27,41) else 'KEEP'
 out.append(dict(screening_unit_id=u['screening_unit_id'],decision=decision,confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any=physics if decision=='REJECT' else '',decision_reason=reason,format='numerical',problem_number=number,round_or_section=u['round_or_section'] if n<=56 else u['round_or_section']+' / '+number[0],page_start=p['page_start'],page_end=p['page_end'],location_json=json.dumps({'statement_locations':p['locations'],'acquisition_problem_number':u['problem_number'],'navigation_pack':f'{f["sha256"]}.statement_pack.json'}),visual_inspection_used=int(n in visual),solution_used=int(n in solutions),boundary_status='content_boundary_verified',evidence='Read every actual statement in the 104-page combined paper, including printed B.1-B.4, P.1-P.4 and R.1-R.4. Rendered equation/apparatus/geometry pages inspected where recorded; actual official solution used where indicated. Top-level questions are retained whole.'))
p=w.ROOT/'reviews/resume_physicsbrawl_2025_68.json';w.writejson(p,out);w.decisions(p)
c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=68,evidence=?,checked_at=? where file_id=?",('Full 104-page combined paper: main 1-56 plus B.1-B.4, P.1-P.4, R.1-R.4 match all 68 acquired logical rows. Dot-labelled hurry-up headers and Q55 lacking italic credit were handled and checked against actual pages; worked solution steps are not questions.',w.now(),fid))
notes={4:'Required table/net/ball dimensions are not all tabulated; later numerical use needs ordinary apparatus specifications.',48:'The entropy comparison assumes consistently defined microstate energy bins; the statement does not explicitly spell out that convention.',50:'The claimed stable equilibrium is interpreted along the displayed axis. A future edition should clarify the axial constraint; unconstrained three-dimensional electrostatic stability is not asserted.',57:'Monovalency and lithium molar mass are not tabulated; ordinary ion counting is used by the official solution.',58:'Monovalency and sodium/lithium molar masses are not tabulated; ordinary ion counting is used by the official solution.'}
for n,note in notes.items():c.execute('update units set source_quality_notes=? where screening_unit_id=?',(note,units[n]['screening_unit_id']))
c.commit();print('Saved 65 KEEP, 3 REJECT; all 68 top-level source labels reconciled.')

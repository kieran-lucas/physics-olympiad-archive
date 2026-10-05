"""Persist the second conceptual review below; no prediction or topic classifier.

The reviewer reread the recorded actual-content evidence and required-physics
inventory for every listed unit, with statement/solution reinspection for the
boundary cases. Lists group the same prerequisite finding, not subproblems.
"""
import workflow as w

records=[]
def group(ids,note,prefix='raw::'):
    for item in ids:records.append({'screening_unit_id':prefix+str(item),'detail':note})

# Singapore Junior Physics Olympiad: each item is an independent MCQ.
sj='derived::d086c64af4c00eac::4055::'
group([1],'Second pass: elementary vector products are prerequisite university mathematics; absence of a named physics domain does not make this MCQ out of scope.',sj)
group([2,4,40,43],'Second pass: moving-mirror, straight-ray, thin-lens and total-internal-reflection reasoning is foundational optics. The listed wave-optics heading is not a closed ban on ray optics.',sj)
group([3,6,9,11,12,13,16,17,18,19,20],'Second pass: actual motion/contact/impact/rotation requirements remain Newton laws, torque, momentum and energy. Geometry and harder vector calculations introduce no external physics.',sj)
group([5,21],'Second pass: buoyancy, hydrostatic pressure and elementary ideal-flow energy are conventional general-physics foundations; rejecting because fluid topics are not separate syllabus lines would be too literal.',sj)
group([7,14,15],'Second pass: coupled springs and pendula require oscillations, constraints and energy; normal-mode mathematics is not out-of-syllabus physics.',sj)
group([8],'Second pass: the leaf-impact speed reduction is explicitly stipulated. No biological or collision-material model needs to be learned.',sj)
group([10],'Second pass: the damped-oscillator differential equation is supplied; identifying damping regimes uses the stated equation and ordinary oscillation theory.',sj)
group([22,23,24],'Second pass: gravity potential, Newtonian force superposition and orbital energy remain in scope; orbital context does not require relativity.',sj)
group([25,33],'Second pass: transformer core flux and solenoid superposition are standard magnetic-field/induction requirements, independent of apparatus familiarity.',sj)
group([26,27,28,29,30,31,34,37],'Second pass: circuit loading, charge conservation, shielding, Gauss law, Coulomb sums and network symmetry are conventional electric-field/circuit prerequisites. Infinite-network algebra is difficulty, not external physics. Q34 carries a separate answer-options quality warning.',sj)
group([32],'Second pass, also checked against companion solution page 9: Lorentz force plus E=cB gives the required wave/charge force; relativistic transformation or acceleration is not used.',sj)
group([35],'Second pass: the moving rod couples Faraday emf, resistance and magnetic force, directly within induction and mechanics.',sj)
group([36],'Second pass: magnetic levitation uses the explicitly supplied separation power law; no microscopic magnetic-material theory is needed.',sj)
group([38,42],'Second pass: displaced slits and fringe geometry use ordinary interference and optical path difference.',sj)
group([39,41,44],'Second pass: traveling-wave phase, an air-column standing wave and spherical-wave energy spreading require only ordinary wave principles.',sj)
group([45,46,48,50],'Second pass: ideal-gas energy, Carnot bound, molecular degrees of freedom and adiabatic compression remain core syllabus thermodynamics; droplet force balance in Q50 is foundational.',sj)
group([47],'Second pass: gas-wall collision rate is kinetic theory plus an order-of-magnitude estimate, not a specialist transport theory.',sj)
group([49],'Second pass: stellar setting reduces to Stefan-Boltzmann balance and inverse-square flux. No astrophysics prerequisite.',sj)

# F=ma 2025: source logical rows, not newly derived units.
group([962,965,969,970,985,986],'Second pass: component graphs, relative motion, nested circular acceleration and moving constraints require kinematics/rotation plus mathematics. No topic-title shortcut was used.')
group([963,964,971,972,973],'Second pass: elastic/inelastic collisions and pendulum rise are momentum/energy tasks. Shared stems do not merge independent numbered MCQs.')
group([966,967,968,974,975,976],'Second pass: contact statics, rolling, hinge constraints and impulse are rigid-body mechanics. Q13-Q14 shared apparatus was retained in page/location metadata; companion solution pages 10-12 verifies the method.')
group([977],'Second pass: connected bubbles require ordinary surface-tension pressure and equilibrium. This is foundational general physics, not an unsupplied specialized fluid model.')
group([978,979],'Second pass: read statement potentials, not source-authored titles. Q17 actually supplies quadratic U=-k(x^2+y^2)/2; Q18 supplies a saddle potential. Both use force as the gradient of potential.')
group([980],'Second pass: kinetic-energy flux is ordinary power; the wind-height law is given. No atmospheric-flow prerequisite.')
group([981],'Second pass: a spanner released near the ISS uses Newtonian orbital dynamics; spacecraft context does not imply special relativity.')
group([982,983],'Second pass: continuity and ideal-flow energy/hydrostatic heads are ordinary prerequisites, consistent with the SPhO hydrostatic calibration.')
group([984],'Second pass: spring calibration and uncertainty propagation are accepted experimental/data-analysis tools; MCQ format does not alter eligibility.')
group([987],'Second pass: mammalian shaking reduces to prescribed angular oscillation, centripetal shedding and energy/latent heat. Surface tension is foundational, not external biology.')
group([988],'Second pass: explicit ignore-relativity instruction controls the black-hole story; the supplied radius comparison does not require GR. Newtonian tidal/orbital energy dominates the whole A2.')
group([989],'Second pass: magnetic stress limit uses Lorentz/current force and a supplied definition of tensile stress. No elastic constitutive theory is a hidden prerequisite.')
group([990],'Second pass: one/two ants on a free disc require the same linear and angular momentum laws. Keep B1 entire.')
group([991],'Second pass: the height-dependent wave speed and Mach angle are given; propagation/refraction geometry suffices. Nonlinear shock mechanics is not required.')
group([992],'Second pass: the phase-aligned optical-mode model and final uncertainty inequality are supplied. The core is wave superposition and pulse bandwidth; retain all five parts.')

# BAUPC: six top-level numbered questions per paper, internal letters retained.
ba={1995:('a2dc3f4f2c466e77',6392),1996:('905711205a548329',6391),1997:('dfc13c25a5078678',6390),1998:('39d653a4c39cc891',6389),1999:('6a29ec8f38e6f406',6388),2000:('a4f633140fd3956b',6387),2001:('15ad6a4f9aa9791b',6386),2002:('f6d033692f222eb4',6385),2003:('e4d6f3dca986b3ee',6384),2004:('3718f60c0e82ec7a',6383)}
ba_notes={
1995:[
'Projectile grazing/nonpenetration is ordinary mechanics and geometry; optimization difficulty is irrelevant to scope.',
'The numbered Q2 deliberately groups three short-answer parts. Gas free expansion, current fields and torque are all foundational/in scope; do not derive three units from (a)-(c).',
'Current spreading through conducting Earth is Ohm law and spherical integration, not geophysical theory.',
'Revisited missing drawing against companion solution pages 3-4. The explicit LC recurrence, cutoff and energy-flow interpretation establish ordinary EM-wave/circuit physics. Changed BORDERLINE to KEEP, retained source-quality warning and paired solution.',
'Lasso geometry on a frictionless cone uses tension/force balance. The fixed versus varying loop constraint is stated.',
'Polygonal-pencil terminal rolling requires inertia, repeated inelastic impact energy and gravity. Point-axis/inelastic model is given; no material theory.' ],
1996:[
'A stacked-ball sequence is elastic collisions and energy; small mass-ratio limits are mathematical.',
'Both lettered parts use Coulomb-field symmetry or hydrostatic buoyancy. Source groups them as one Q2; no fragmentation.',
'Revisited missing cube drawing against explicit labelled reduced network in companion solution pages 2-3. Ordinary Ohm/Kirchhoff symmetry is established. Changed BORDERLINE to KEEP with missing-drawing quality flag and required companion solution.',
'Companion solution pages 3-4 confirms ballistic reflection and momentum transfer on a shaped curve, rather than an advanced continuum model.',
'Rocking-stick decay uses gravity, rotational inertia and inelastic pivot switching; supplied sums/log estimates are mathematical tools.',
'A uniformly stretching support with rolling cylinder uses constraints, torque and energy. Supplied inertial parameter is sufficient.' ],
1997:[
'The two unrelated lettered scenarios are within one source Q1. Buoyancy and Coulomb energy are conventional scope; retain source boundary.',
'Magnetic spiral with explicitly specified linear drag is Lorentz force plus Newton law. No kinetic transport theory.',
'Falling-stick contact loss is rigid-body energy and Newtonian reaction forces.',
'Successively lighter sticks require elastic impacts, moments of inertia and limiting sums, not external physics.',
'Both cone scenarios use circular force balance and rolling angular momentum, within one numbered Q5.',
'Repeated wall/block collisions are classical energy/momentum; large mass ratio is an approximation, not an advanced-theory prerequisite.' ],
1998:[
'Cylinder-stack contacts use normal forces and Newton laws.',
'Axisymmetric radial-field motion uses Lorentz force and total-flux geometry. The unusual field context adds no theory.',
'Infinite Atwood recursion is pulley constraints plus Newton law; infinite-chain algebra is difficulty only.',
'Icosahedral resistor reduction uses network symmetry and Ohm law.',
'Stacked gyroscope slow precession is explicitly covered by rigid-body torque and angular momentum.',
'Slow coupled Atwood/pendulum motion can be treated by Newtonian averaging/energy. An adiabatic-invariant route is mathematical technique, not an extra physical theory.' ],
1999:[
'Sphere and cube Coulomb potentials use integration/scale symmetry. The two requested shapes remain one numbered question.',
'Wheel blur is instantaneous rolling velocity geometry.',
'Friction-limited motorcycle path uses tangential/radial acceleration; optimal control mathematics does not change physics scope.',
'Both fox/rabbit paths are relative kinematics under one numbered Q4.',
'Raindrop accretion uses the stated sticky spherical model and variable-mass momentum; no cloud microphysics.',
'Winding a spring around a pole is given elastic energy and a geometric constraint.' ],
2000:[
'Pivot optimization remains gravitational rotational energy.',
'Grounded then insulated plates require ordinary induced charges and field energy; no quantum conductor model.',
'Planetary atmospheric refraction uses the supplied n-density law, hydrostatic ideal gas and Snell geometry. No atmospheric specialist model.',
'Many-particle collision limits are elastic momentum/energy and mathematics.',
'Turntable rolling is rigid-body kinematics and angular momentum.',
'Rope-heap mass loading of a spring is variable-mass momentum and damped oscillation. No continuum external prerequisite.' ],
2001:[
'Sphere/cylinder contact geometry and rotation are ordinary rigid-body dynamics.',
'Reflecting-cone collection requires ray geometry and isotropic power, foundational optics.',
'Velocity-directed friction and terminal inclined-plane motion use Newton laws; nonlinear algebra is not out-of-scope physics.',
'Triangular PV-cycle efficiency uses ideal-gas internal energy and the first law.',
'Stretching-rope ant motion is a prescribed kinematic model, not elasticity theory.',
'General network identity uses Kirchhoff linearity/superposition and linear algebra.' ],
2002:[
'Connected-container temperature change uses hydrostatic pressure and ordinary thermal expansion.',
'Unwinding string circular motion explicitly ignores relativity; Newtonian constraints suffice.',
'Landing brick motion uses projectile energy and impulsive/sliding friction.',
'Thermal creeping of roof uses the provided expansion coefficient and distributed friction. No continuum elasticity model.',
'Image-charge time-lag mechanism is explicitly supplied; electrostatics and dissipation reasoning suffice.',
'Slowly winding conical pendulum is Newtonian centripetal/energy dynamics.' ],
2003:[
'Folded-rope force requires variable-mass momentum flux, ordinary Newtonian mechanics.',
'Pole/string unwinding requires constrained motion and gravity.',
'Nested square network is a self-similar resistance calculation, not new physics.',
'A spiralling charge uses Lorentz force and supplied velocity-proportional friction.',
'Ball/surface no-slip/no-bounce impulse model is stated. Repeated impacts use classical translation/rotation.',
'Rolling cone combines no-slip constraints, angular momentum and circular force balance.' ],
2004:[
'Both snow-loading sled and arm-swing parts use ordinary linear/angular momentum; do not split the numbered Q1.',
'Rope on two inclines uses distributed weight and limiting static friction.',
'Isotropic radiation fraction is ordinary energy flux and solid-angle mathematics.',
'Tetrahedral RLC response is electromagnetic circuit oscillation and complex impedance.',
'Particle leaving a movable hemisphere is momentum/energy with zero-normal-force contact loss.',
'Repeated cylinder/plank rolling is rigid-body dynamics and recursion; many stages do not introduce external physics.' ]}
for year,(sha,pid) in ba.items():
    for q,note in enumerate(ba_notes[year],1):group([q],'Second pass: '+note,f'derived::{sha}::{pid}::')

# Complete EuPhO 2017-2026 archive: adverse-boundary checks in particular.
eu={
301:'Rope mode/tension uses small oscillations and energy estimates; no advanced elasticity needed.',
302:'Hot/cold rotating disc uses supplied molecular-surface model, kinetic theory and heat/energy; exotic apparatus is irrelevant.',
303:'Reread statement and solution 933 pages 1-3. The solution makes local flux locking the necessary first step and uses two image dipoles. Statement does not explain the superconducting constraint. Ideal R=0/Faraday may make it foundational, but the boundary is genuinely ambiguous. Retain BORDERLINE, not a blanket rejection of superconductivity.',
304:'Diode Shockley and thermistor relations are supplied; operate/fit the devices rather than derive semiconductor band theory.',
297:'Three hinged balls require momentum/angular momentum and energy, keeping all constrained stages together.',
298:'Given diamagnetic coefficient plus field energy/force and hydrostatic boiling condition is in scope; magnetization is explicitly listed.',
299:'Crystal-step energy laws and variational target are specified; minimization/continuum geometry, not solid-state prerequisite.',
300:'Given diffusion, molecular speed and birefringence models plus ordinary optics/data fitting are sufficient; all A-D remain one experiment.',
293:'Ice temperature inversion uses heat capacity, latent heat and graph interpretation; atmospheric setting is not external theory.',
294:'Charged rolling ball uses distributed Lorentz force and rigid-body laws.',
295:'Irregular hose jet is ballistic trajectories and collection geometry, not unsupplied fluid dynamics.',
296:'Waveguide dispersion and attenuation law are provided. Interference and fitting suffice without prior waveguide theory.',
288:'Solenoid and moving wire require magnetic interaction and Faraday induction.',
289:'Thread unwinding geometry uses Newtonian constraints and energy.',
290:'Cat-eye camera uses thin-lens/ray/reflection geometry and given imperfection caveat; ray optics is foundational.',
291:'The Rutherford scattering relation is supplied and used to fit charge/geometry. Scattering derivation is not required.',
292:'Mechanical black-box inference uses coupled spring oscillators and inertia; parameter estimation is valid experimental work.',
283:'Piston/diaphragm compression uses ideal-gas adiabatic energy and force balance.',
284:'Spatial thread friction needs normal reactions and Newton laws; difficult geometry is not extra physics.',
285:'Glass-ball dispersion/refractive photographs use foundational optics and measurement.',
286:'Hidden wire/compass experiment uses magnetic field and torque equilibrium with uncertainty.',
287:'Given thermal-transfer laws support heat-capacity/conductivity fits; the task does not require deriving a turbulence model.',
279:'Floating cylinder fluid inertia follows continuity, kinetic energy and buoyancy. Hydrostatics remains foundational.',
280:'Temperature-switch resistor model and cooling law are specified; RL transient and Joule heating are in scope.',
281:'Charged rigid dipole uses Lorentz force and translation/rotation, not quantum dipoles.',
282:'Illumination experiment supplies photometric definitions; thermal/radiation calibration and uncertainty are ordinary scope.',
274:'Thermal-lens effect gives dn/dT and uses heat flow/optical path. No microscopic thermo-optic theory.',
275:'Brick between moving planes is vector friction and terminal Newtonian motion.',
276:'Moving plate eddy-current drag requires motional induction and Ohm/continuity laws, explicitly within EM scope.',
277:'Magnetic-pendulum frequency formula is supplied; model fitting and nonlinear oscillations do not require deriving advanced field theory.',
278:'Hidden optical black box uses lenses, polarization, slits and gratings. Shared apparatus context is retained.',
270:'Sliding puck needs translation/rotation and friction; all internal stages remain one problem.',
271:'Reread actual speeds 3c/5 and 4c/5, and simultaneity/relative-velocity questions. Both substantive parts need unsupplied Lorentz transformation/velocity addition. Reject for central special relativity, not spacecraft setting.',
272:'Fabry-Perot coherent amplitudes, cavity phase and decay are interference/energy reasoning, not quantum laser dynamics.',
273:'Piezo constitutive response and empirical force law are supplied. Energy/capacitance/calibration suffice without crystal theory.',
265:'Solar reflection from cylinder requires ray/flux geometry; foundational optics passes the remove-context test.',
266:'Table/chains equilibrium and period are rigid-body potential/kinetic energy and small oscillations.',
267:'Crossed-wire field lines use magnetic superposition; differential geometry is mathematics.',
268:'Given sigmoid and network definitions reduce the deep-learning setting to resistor/potentiometer measurements. No ML training knowledge.',
269:'Hidden-pattern laser diffraction requires interference/grating spacing and uncertainty, directly in scope.',
261:'Torsional articulated jumper uses supplied torque law, rotation, center of mass and floor reaction.',
262:'Rectangular hysteresis law is given; magnetic losses plus LC dynamics and ferromagnetism are explicitly covered.',
263:'Rechecked solution 717 pages 4-6: required flow scaling follows dimensional/pressure-viscosity balance. The lubrication PDE is explicitly optional; maximum-distance estimate can be obtained without solving it. Retain KEEP after supplied-model/general-physics audit.',
264:'Acoustic levitation provides force, evaporation, shape and breakup models. Wave/force/graph reasoning and ordinary refraction suffice; no acoustic radiation-force derivation.'}
for pid,note in eu.items():group([pid],'Second pass: '+note)

# Old scans and current IPhO/APhO statements.
group([248],'Second pass: scanned original shows one Problem 1 with two cart/tension scenarios. Newton equations/relative acceleration suffice; no subpart split.')
group([249],'Second pass: copper/water/ice calorimetry is heat capacity and latent heat; scan location excludes preceding Problem 1 solution.')
group([250],'Second pass: charged ring field and weight/tension balance are electrostatics/mechanics. Adjacent supplied solution confirms method.')
group([251],'Second pass: actual scan header is Theory Problem 4, with continuation on page 2. Thin-film interference and given thermal expansion suffice; preceding solution text is excluded by location metadata.')
group([5],'Second pass: hydrogen hyperfine scaling and MOND force law are supplied. Bohr/magnetic photon calculation and Newtonian galaxy/Doppler estimates dominate; no unsupplied cosmology.')
group([6],'Second pass: Cox clock is hydrostatic barometer plus given vapour-pressure data, pulley constraint and energy/friction; all A/B remain one Theory Q2.')
group([7],'Second pass: Henry/diffusion/Stokes and bubble-neck models are given. Champagne uses gas, buoyancy, surface energy and adiabatic oscillations; all A-C remain one Theory Q3.')
group([8],'Second pass: magnetic-gradient and torsional-wire laws are supplied; calibration and uncertainty are in-scope experiment skills. The whole Earth-field experiment stays one Q1.')
group([9],'Second pass: crater and sand-drag laws are provided; image/data fits and rolling energy are in scope. Internal A/B tasks are not separately screened.')
group([10],'Second pass: reread all four pages. Standing-wave form/boundaries, two-atoms-per-state filling, coupling/scaling and local-homogeneous approximation are expressly supplied. De Broglie energy, counting, thermodynamic derivatives and force balance suffice. KEEP confidence raised from medium to high; no many-body quantum prerequisite is hidden.')
group([310],'Second pass: supplied polar-mass surrogate plus Newtonian torque and angular momentum is sufficient; Earth/precession context does not invoke GR.')
group([311],'Second pass: companion solution 966 confirms classical torque/plane-wave chain dynamics and Boltzmann mean-field probability, with de Broglie/energy-momentum relations in subsidiary B4-B5. The dominant task is supplied classical/statistical models; KEEP confidence raised to high and solution use recorded. No operator spin theory.')
group([312],'Second pass: given atmospheric/radiative/phase models support ordinary ideal-gas stability, Doppler and prism optics. Clausius-Clapeyron is supplied rather than an unsupplied meteorology requirement.')
group([313],'Second pass: induction cooker stages share one apparatus/20-point Q1 and depend on coil parameters. They remain one top-level experiment; supplied skin-depth/NTC/load laws make fitting and heat balance sufficient.')
group([79],'Second pass: image-charge representation is given and proof waived; conductor potential, charged-pendulum oscillation and field energy are direct syllabus physics.')
group([80],'Second pass: rendering restores the Bernoulli formula missing from extracted text. Hydrostatic/ideal-gas chimney flow and heat/power efficiency use supplied ordinary-flow assumptions.')
group([81],'Second pass: solution 319 page 4 allows nonrelativistic reaction kinematics; pages 7-8 use ordinary photon recoil, with exact relativistic Doppler only in the final subsidiary lab-energy request. Nuclear binding/reactions dominate independently; KEEP the whole problem.')
group([82],'Second pass: bending energy, stadium equilibrium and rigidity-to-Young relation are supplied. Experimental fitting does not need plate-elasticity theory. Internal Tasks are one E1.')
group([83],'Second pass: force polarity, graph symmetry and equilibrium are measured rather than computed from a specialized microscopic magnet model. The source explicitly separates E2 despite shared apparatus.')
group([55],'Second pass: solution 251 distinguishes unsupplied electron relativistic energy in independent B3 from nonrelativistic Doppler in B4. The extensive independent solar-cell/radiation/gravity work plus nuclear flux and kinetic theory make most of this whole T-1 useful. KEEP does not select or split subparts.')

c=w.connect(); expected={r[0] for r in c.execute('select screening_unit_id from units where decision is not null')}
actual=[r['screening_unit_id'] for r in records]
assert len(actual)==len(set(actual)), 'duplicate second review'
assert set(actual)==expected,(expected-set(actual),set(actual)-expected)
path=w.ROOT/'reviews'/'second_pass.json';w.writejson(path,records);w.review(path)
print('Actual-content second conceptual review recorded for',len(records),'units')

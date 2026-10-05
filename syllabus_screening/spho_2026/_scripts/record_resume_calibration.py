"""Explicit judgments from the resumed actual-content calibration inspection.

This is a record of human-readable AI review, not a physics classifier.
"""
import json
import workflow as w

c=w.connect(); records=[]
def add(pid,decision,domains,physics,reason,pages,visual=False,solution=False,confidence='high',external='',fmt='theory',focused=False):
    u=c.execute('select * from units where screening_unit_id=?',('raw::'+str(pid),)).fetchone()
    assert u and u['decision'] is None, 'Never overwrite earlier decisions'
    records.append(dict(screening_unit_id=u['screening_unit_id'],decision=decision,confidence=confidence,
      primary_spho_domains=domains,required_physics=physics,decision_reason=reason,
      external_physics_if_any=external,page_start=pages[0],page_end=pages[1],format=fmt,
      visual_inspection_used=int(visual),solution_used=int(solution),needs_second_review=focused,
      evidence=f"Read complete top-level statement in cached file {u['source_file_id']}, pages {pages[0]}-{pages[1]}. "+reason,
      boundary_status='content_boundary_verified',location_json=json.dumps({'top_level_label':u['problem_number'],'boundary_note':'All internal parts retained as one unit; numbered neighboring problems excluded.'})))
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light'
# Ortvay 2026, complete shared paper, questions 1-24.
data=[
 ('KEEP',II,'Acoustic propagation, reflection and paraxial geometry','The statement explicitly models sound as elastically bouncing particles; echoes require wave speed and geometrical reflection.',[1,1],False,''),
 ('KEEP',I,'Newtonian gravity, extended-mass attraction and measurement uncertainty','Earth-radius inference uses gravitational acceleration and the hill contribution; uncertainty is ordinary experimental analysis.',[1,1],False,''),
 ('KEEP',I,'Uniform front kinematics, coordinate geometry and timing uncertainty','The straight constant-speed front is supplied; temperature series are used to estimate passage times, not to derive atmospheric theory.',[2,2],False,''),
 ('KEEP',I,'Momentum, energy, contact force and ballistic motion','The movable hemisphere and departing particle are a Newtonian constrained-motion problem.',[2,2],False,''),
 ('KEEP',I,'Thrust, torque, rigid-body motion and momentum transfer','Constant outflow and approximately fixed mass/pressure are supplied; the asymptotic motion requires Newtonian force and torque.',[2,2],False,''),
 ('KEEP',I,'Constrained Newtonian motion, work and energy','Rendered rope geometry fixes the constraint; the motion requires gravity, tension and energy.',[3,3],True,''),
 ('KEEP',I,'Surface tension, pressure and gravitational force balance','Bubble-film shape follows local force balance with ordinary capillary tension and weight; numerical shape integration is mathematical difficulty.',[3,3],True,''),
 ('KEEP',I,'Newtonian gravitational potential, work and power','Excavation energy is determined by the supplied prism geometry and density, with the given power setting elapsed time.',[3,3],True,''),
 ('KEEP',I,'Rotational inertia, tension and a failure-threshold model','The task asks the contestant to construct a mechanical tearing model; a phenomenological strength parameter is sufficient.',[4,4],True,''),
 ('KEEP',I,'Conservative one-dimensional scattering and energy','The interaction is explicitly a classical pair potential; displacement inversion uses energy and trajectory integration.',[4,4],True,''),
 ('KEEP',I,'Newtonian gravity and numerical volume integration','The force between cylinder halves requires only the universal gravitational law; numerical integration does not add external physics.',[4,4],True,''),
 ('BORDERLINE',I,'Elastic loading/unloading and model identification from photographs','The snow-covered branch photographs do not establish the time history or a definite mechanical model sufficiently for a precise scope judgment.',[4,4],True,'Potentially substantial branch elasticity or instability modeling'),
 ('KEEP',I,'Buoyancy, center of mass, torque and stability','Floating-ellipsoid orientation is hydrostatic force balance and gravitational-energy stability, despite difficult geometry.',[5,5],False,''),
 ('KEEP',I,'Extended-body gravity, centrifugal potential and hydrostatic equilibrium','Quasistatic rotating water surfaces follow equipotentials; no unsupplied dynamic ocean model is required.',[5,5],False,''),
 ('REJECT','','Canonical Hamiltonian dynamics and phase-space stability','An arbitrary nonquadratic Hamiltonian is supplied, but canonical equations and their interpretation are the central unsupplied formalism, rather than Newtonian general physics.',[6,6],True,'Hamiltonian canonical mechanics'),
 ('KEEP',VII+';'+VIII,'Magnetic flux, mutual inductance and field integration','The winding geometry is visually specified; mutual induction and geometrical dependence are explicitly in scope.',[6,6],True,''),
 ('KEEP',VII,'Biot-Savart field and numerical integration of a wire contour','The rendered plot specifies both contours; field change follows ordinary magnetostatics, not an advanced material theory.',[6,6],True,''),
 ('REJECT','','Classical Heisenberg exchange model and spin-equilibrium stability','The central Heisenberg-type exchange interaction is named but its energy law and machinery are not supplied; phenomenological magnetization knowledge alone is insufficient.',[7,7],True,'Unsupplied Heisenberg exchange model'),
 ('REJECT','','Relativistic scalar-field coupling and differential scattering cross section','Calling the field a four-scalar requires an unsupplied relativistic coupling/dynamical law; a radial scalar profile alone does not provide it.',[7,7],True,'Relativistic scalar-field dynamics'),
 ('REJECT','','Quantum operator dynamics and repeated angular-momentum measurement','The effective-mass Hamiltonian does not supply quantum evolution or measurement theory, which controls the whole protocol.',[7,7],True,'Quantum operator evolution and measurement'),
 ('KEEP',I+';'+III+';'+IV,'Classical pair-force dynamics, temperature and phase-transition data analysis','The pair potential is explicit; simulation and an experimental phase diagram use Newtonian dynamics and thermal/data reasoning, without requiring a microscopic condensed-matter theory.',[8,8],True,''),
 ('REJECT','','General-relativistic cosmology and Friedmann dynamics','Deriving Friedmann equations from a Robertson-Walker metric is central and unsupplied; equations of state do not make the gravitational theory self-contained.',[8,8],True,'General relativity and cosmology'),
 ('REJECT','','Fermionic coherent states, Grassmann integration and imaginary-time path integrals','Most work is an interacting Hubbard-model path integral with anticommuting fields and Matsubara modes; supplied identities do not replace this external conceptual framework.',[9,9],False,'Many-body quantum statistical field theory'),
 ('REJECT','','Quantum wavepacket propagation and probability optimization','Optimizing a wavefunction after free evolution requires unsupplied Schrödinger dynamics and quantum probability, beyond de Broglie and hydrogen-state knowledge.',[10,10],False,'Quantum wavepacket evolution')]
for n,(decision,domains,physics,reason,pages,visual,external) in enumerate(data,5374):
    add(n,decision,domains,physics,reason,pages,visual,confidence='medium' if decision=='BORDERLINE' else 'high',external=external,fmt='data_analysis' if n in [5376,5394] else 'theory',focused=n in [5380,5391,5394])
# Physics Cup: complete 14-problem archive, not 14 subparts.
pc=[
 (6369,'KEEP',I+';'+VI,'Kinetic energy, incompressibility, supplied irrotational flow and electrostatic field analogy','Added mass is defined by liquid kinetic energy and the hint supplies zero circulation; field conservation and moving-boundary kinematics permit the electrostatic analogy without importing a fluid equation.',True,True),
 (6370,'KEEP',IV,'Entropy, reversible engines and supplied heat capacity','The nonstandard ice heat capacity is explicit; the optimization needs thermodynamic entropy and reversible heat engines.',False,False),
 (6371,'KEEP',I,'Projectile motion and elastic reflection','Parabolic-arc foci are determined by Newtonian flight and frictionless elastic impacts.',False,False),
 (6372,'KEEP',VI,'Kirchhoff networks, superposition and the supplied resistance formula','The infinite-grid resistance relation is given; short-circuit effects use ordinary circuit reasoning.',False,False),
 (6373,'KEEP',X,'Diffraction gratings, optical path and focusing','The rendered stair-height formula and cross-section specify the grating; spectral maxima require in-scope diffraction.',True,False),
 (6374,'KEEP',VI,'Kirchhoff networks and resistance bounds','The visually inspected lattice requires ordinary passive-circuit bounds; infinite size is mathematical complexity.',True,False),
 (6375,'REJECT','','Proper acceleration, Lorentz kinematics and proper time','Relativistic missile interception is the entire task; no transformation or accelerated-frame model is supplied.',False,False),
 (6376,'KEEP',VII+';'+VIII,'Magnetization, permeability, magnetic energy and inductance','The permeability and high-permeability limit are given; calculating geometry-dependent inductance stays within magnetostatics and induction.',False,False),
 (6377,'BORDERLINE',I+';'+II,'Hydrostatic equilibrium and distributed-liquid oscillation','The normal-mode frequency requires a distributed incompressible velocity field; the statement supplies a flat top boundary but not a flow model, leaving a substantial continuum-fluid prerequisite uncertain.',True,False),
 (6378,'KEEP',I+';'+III+';'+XI,'Thermal photon momentum, black-body radiation and random walks','Black-body photons transfer momentum to the sphere, and the random-walk scaling is supplied; no external scattering theory is required for the requested estimate.',False,False),
 (6379,'KEEP',VI,'Electrostatic induction, dipole response and Coulomb force','Neutral-disc attraction is electrostatic polarization; the exact prefactor is optional and does not change the physics boundary.',False,False),
 (6380,'KEEP',VI,'Kirchhoff networks and symmetry','The complete polygon network is an ordinary resistance problem; permitted algebra software is irrelevant to physics scope.',False,False),
 (6381,'KEEP',III+';'+VII+';'+VIII,'Slow magnetic induction, cyclotron energy and thermal equilibration','A classical derivation of slow transverse-energy change follows Newton-Lorentz and Faraday laws; the supplied quantum adiabatic hint does not force Landau-level theory.',False,True),
 (6382,'KEEP',X,'Thin-lens imaging and geometrical reconstruction','The ellipse and image of its center were inspected; this is foundational geometrical optics and projective geometry.',True,False)]
for pid,decision,domains,physics,reason,visual,focused in pc:
    add(pid,decision,domains,physics,reason,[1,1],visual,confidence='medium' if decision=='BORDERLINE' else 'high',external='Special relativity' if pid==6375 else ('Continuum-fluid mode structure' if pid==6377 else ''),focused=focused)
# All-Ukrainian 2025: five numbered problems, retain sections 1.1 etc.
add(2670,'KEEP',VII+';'+VI,'Kirchhoff currents and magnetic force','All four parts use the visually specified tetrahedral circuit and Ampere force.',[1,1],True)
add(2671,'KEEP',VI+';'+VIII+';'+IX,'LC energy, dissipation and forced AC circuits','Three visually inspected circuit variants test in-scope electromagnetic oscillations and circuit foundations.',[1,1],True)
add(2672,'BORDERLINE',I,'Relativistic acceleration and rigid-body collision','One substantial section requires unsupplied proper-acceleration relativity; the other is a complete Newtonian rigid-body impact. The whole problem is balanced rather than clearly dominated by usable material.',[2,2],True,confidence='medium',external='Special-relativistic acceleration')
add(2673,'KEEP',I+';'+II,'Constrained mechanics, energy and small oscillations','The helical-wire drawing was inspected; all internal stages use mechanical constraints and rigid-body energy.',[2,2],True)
add(2674,'KEEP',I+';'+XI,'Gravity, centrifugal acceleration and supplied optical reflection model','The astronomical setting reduces to gravitational accelerations and geometry of the explicitly defined reflected light.',[3,3])
# World Olympiad and Russian TST: modern-context contrast cases.
add(833,'KEEP',VII+';'+I,'Lorentz gyromotion, energy and supplied magnetic-moment conservation','The dipole field and constant orbital magnetic moment are explicitly supplied; mirror points and transit integrals need ordinary mechanics and magnetism.',[1,2],focused=True)
add(834,'KEEP',I+';'+III,'Maxwell distribution, escape speed and particle flux','Scale height, mean-free-path and density models are supplied; atmospheric loss follows kinetic theory and Newtonian gravity.',[1,3])
add(839,'KEEP',IV+';'+XI,'Carnot heat pumping, entropy and Planck radiation','Solution file 1751 p1 explicitly identifies reversed Carnot operation with a truncated Planck spectrum; semiconductor band theory is not required.',[1,1],solution=True,focused=True)
add(1954,'BORDERLINE',VII+';'+II,'Relativistic orbit-energy relations and phase oscillations','The equilibrium and critical-energy sections need unsupplied relativistic momentum; the long phase-stability section uses supplied energy gain and ordinary oscillation mathematics. Their dependency makes whole-problem usefulness genuinely near the boundary.',[1,3],confidence='medium',external='Relativistic energy-momentum and orbit-frequency relations')
add(1956,'KEEP',VI+';'+VII+';'+IX+';'+X,'Newton-Lorentz Drude response, Maxwell waves, polarization and graph fitting','Drag law, graphene dispersion, response substitutions and Faraday models are supplied; classical field response and polarization dominate all four sections.',[1,4],True,focused=True)
assert len(records)==48
path=w.ROOT/'reviews/resume_calibration_48.json';w.writejson(path,records);w.decisions(path)
print('Calibration decisions recorded:',len(records))

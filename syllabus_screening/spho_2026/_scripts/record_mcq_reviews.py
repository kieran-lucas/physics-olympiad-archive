"""Explicit reviewer-authored decisions after reading and viewing the two papers.
No predictions or keyword rules. Numbers/pages describe the provided PDFs.
"""
import re, json, subprocess, sys
import workflow as w

I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics'
VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light'
us=[
 (1,[2,2],I,'Velocity components and constant-speed kinematics','The x(t) and y(t) graphs test ordinary vector kinematics.'),
 (2,[3,3],I,'Momentum and energy in simultaneous elastic collisions','The symmetric three-disc impact requires only collision conservation laws.'),
 (3,[3,3],I,'Sequential elastic collisions and limiting cases','The slightly displaced third disc changes collision order, not the required physics.'),
 (4,[3,3],I,'Relative velocity and acceleration in planar pursuit','The cat/mouse perpendicular configuration is a Newtonian kinematics problem.'),
 (5,[4,4],I,'Contact forces, torque balance and static friction','The three stacked cylinders require ordinary rigid-body equilibrium.'),
 (6,[4,4],I,'Rolling energy and projectile range','The ramp, rolling ball and landing points use rotational energy and ballistic motion.'),
 (7,[5,5],I,'Constrained kinematics and elastic potential energy','The stair-walking spring-hinge energy is supplied; no specialized walking model is required.'),
 (8,[5,5],I,'Relative angular motion','The vertical spinning top and counterrotating platform require only frame-relative rotation.'),
 (9,[6,6],I,'Vector circular acceleration and geometric series','The nested circles make the mathematics longer without adding external physics.'),
 (10,[6,6],I,'Elastic-collision energy transfer and mass-ratio limit','The maximum transfer to a light stationary mass is ordinary two-body collision physics.'),
 (11,[6,6],I,'Elastic-collision energy transfer and mass-ratio limit','Reversing the incident mass uses the same in-scope conservation laws.'),
 (12,[6,6],I+';'+II,'Inelastic momentum transfer followed by pendulum energy','The sticking clay and subsequent swing use momentum and mechanical energy.'),
 (13,[6,7],I,'Sliding friction, rigid-body rotation and rolling onset','The puppy-launcher plots require translation/rotation equations and the no-slip condition.'),
 (14,[6,8],I,'Moment of inertia and friction-driven transition to rolling','The shell/wood/rubber comparison concerns mass distribution, not material microphysics.'),
 (15,[8,8],I,'Impulsive rigid-body dynamics and hinge constraints','The articulated rods have supplied inertias; Newtonian impulse/angular momentum suffices.'),
 (16,[8,8],I,'Surface-tension pressure and ordinary pressure equilibrium','The unequal connected bubbles require elementary interface force balance, an acceptable general-physics foundation.'),
 (17,[9,9],I,'Force from supplied potential and Newtonian trajectories','The displayed potential is negative quadratic, not an inverse-square force; its trajectory follows ordinary dynamics.'),
 (18,[9,9],I+';'+II,'Force from a saddle potential and coupled linear motion','The supplied U=kxy/2 reduces to Newtonian motion in rotated coordinates.'),
 (19,[9,9],I,'Kinetic-energy flux, power and a supplied wind-height relation','The turbine scaling is ordinary energy/power reasoning with the stated wind model.'),
 (20,[9,9],I,'Newtonian near-circular orbital motion','The ISS/spanner return question needs gravitation and small orbital perturbations, not spaceflight theory.'),
 (21,[10,10],I,'Conservation of volume flow','The pipe-area change uses elementary continuity, a general-physics foundation.'),
 (22,[10,10],I,'Mechanical energy of ideal flow and hydrostatic pressure','The piezometer heights require ordinary Bernoulli/pressure reasoning, not advanced fluid dynamics.'),
 (23,[10,10],I,'Static spring calibration and measurement uncertainty','The scales, ruler and uncertain g test force balance with standard error propagation.'),
 (24,[11,11],I,'Impulse, constrained circular motion and rotation geometry','The free-pivot rod response is rigid-body mechanics despite three-dimensional geometry.'),
 (25,[11,11],I,'Moving constraints, relative velocity and mechanical energy','The translating prism approximation is explicitly stated; Newtonian energy suffices.')]
rows=[]
for n,pages,domain,physics,reason in us:
    rows.append([961+n,'KEEP',domain,physics,reason,
      f'F=ma 2025 Q{n}: complete statement/options read from file 1914 and actual pages {pages[0]}-{pages[1]} visually inspected; shared stems retained.',
      pages,'multiple_choice',1,0,'high',''])
w.writejson(w.ROOT/'reviews/usapho_fma_2025.json',{'rows':rows,'boundary_note':'Each numbered MCQ is one unit; options are not units. Q2/Q3 and Q10/Q11 share stems; Q13/Q14 additionally use the launcher context on page 6.'})
subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(w.ROOT/'reviews/usapho_fma_2025.json')],check=True)

sj=[
 (1,'','Vector dot/cross products and orthonormal bases','This is foundational vector mathematics useful across the syllabus; no external physics is tested.'),
 (2,I+';'+X,'Reflection and relative kinematics','Stationary image of a moving man requires ordinary moving-mirror geometry.'),
 (3,I,'Planar kinematics and geometric optimization','The runners on opposite rectangle paths require only velocities and distances.'),
 (4,X,'Straight-ray geometry','Solar elevation from a shadow is foundational ray optics, not excluded by the wave-optics heading.'),
 (5,I,'Buoyancy, gravity and work-energy','The rising bubble requires accounting for displaced liquid gravitational energy.'),
 (6,I,'Inclined-plane forces and static/kinetic friction','The smallest nonzero acceleration follows friction thresholds and Newton laws.'),
 (7,I+';'+II,'Momentum and elastic energy','Two equal blocks coupled by a spring require conservation laws.'),
 (8,I,'Gravity and collisions under a supplied speed-loss rule','The repeated leaf impacts supply the unfamiliar model; energy/kinematics determines the limiting motion.'),
 (9,I,'Torque balance and support tension','The loaded suspended rod tests static equilibrium and the onset of a slack string.'),
 (10,II,'Damped harmonic motion and critical damping','The differential equation is supplied; its damping and period interpretations are in scope.'),
 (11,I,'Contact-force equilibrium and geometry','The two balls in a narrow box require ordinary normal forces and weight balance.'),
 (12,I,'Newtonian constrained motion and geometric limiting events','The table/pulley geometry is unusual, but the essential physics is string constraints and force balance.'),
 (13,I,'Projectile motion and elastic reflection','The bouncing particle in a cone requires gravity and collision geometry.'),
 (14,I+';'+II,'Pendulum energy and centripetal tension','Catching the string on a peg changes circular radius without introducing external physics.'),
 (15,II,'Coupled small oscillations and normal modes','In-phase pendulum motion with a spring is standard oscillation physics.'),
 (16,I,'Momentum and kinetic energy in elastic collisions','Equal-mass billiard scattering is directly within the collisions syllabus.'),
 (17,I,'Rolling dynamics and friction','The cylinder inertia is supplied; force and torque equations establish the contact friction.'),
 (18,I,'Work at a moving point of force application','The top-pulled rolling cylinder tests work-energy with its actual string displacement.'),
 (19,I,'Vector angular momentum of a rigid body','The tilted rotating stick tests angular velocity versus angular momentum directions; no specialist rigid-body theory is required.'),
 (20,I,'Tangential/radial acceleration and friction limit','The accelerating turntable slip criterion is ordinary circular dynamics.'),
 (21,I,'Pressure, ideal-flow energy and hydrostatics','The siphon needs ordinary Bernoulli/pressure reasoning; advanced continuum-fluid theory is unnecessary.'),
 (22,I,'Gravitational potential, energy and fall-time integration','The far-away dust particle uses explicitly listed Newtonian gravitation; the integration difficulty is not a scope exclusion.'),
 (23,I,'Superposition of Newtonian gravitational forces','The Earth/Sun height question requires ordinary gravitational force balance, not astrophysical machinery.'),
 (24,I,'Orbital energy and dissipative motion','The statement supplies circular-orbit energies; changing radius/speed uses mechanical energy.'),
 (25,VII+';'+VIII,'Magnetic flux continuity in an ideal transformer core','The unequal core areas test flux conservation and magnetic induction.'),
 (26,VI,'Ohmic circuits and meter loading','The nonideal voltmeter/ammeter problem is foundational circuit reasoning for electrical physics.'),
 (27,VI,'Capacitance, voltage and conservation of conductor charge','Initially charged capacitors in series require electrostatics and charge bookkeeping.'),
 (28,VI,'Electrostatic shielding and induced conductor charge','The central charge and external charge test conductor equilibrium.'),
 (29,VI,'Gauss law for a spherically symmetric volume charge','The hollow charged sphere is explicitly in electric-field scope.'),
 (30,VI,'Coulomb-field vector superposition','The three charges at square corners require ordinary electric-field addition.'),
 (31,VI,'Electric potential and work of charge assembly','The fourth-charge work uses the shared square-charge stem and electrostatic potential.'),
 (32,VI+';'+VII+';'+IX,'Lorentz force and electric/magnetic fields of a plane wave','The counterpropagating charge requires q(E+v cross B) and E=cB; unsupplied special relativity is not required.'),
 (33,VII,'Solenoid fields and superposition','The end-field question explicitly hints at superposition of magnetic fields.'),
 (34,VI+';'+I,'Near-sheet electric field and Newton third law','The charged plate acceleration follows electrostatic field and reaction-force reasoning.'),
 (35,VIII+';'+VII+';'+I,'Motional induction, Ohm law and magnetic force','The rod dividing two resistive loops is directly within induction and Newtonian force balance.'),
 (36,VII+';'+I,'Magnetic-force balance using a supplied power law','F proportional to r^-n is supplied; the levitating magnets require equilibrium and estimation of n, not a prior magnet model.'),
 (37,VI,'Kirchhoff laws, superposition and network symmetry','The infinite hexagonal resistor network is mathematically unusual but uses foundational circuit physics.'),
 (38,X,'Two-slit path differences and phase','Misalignment shifts the interference maximum through ordinary wave-optics geometry.'),
 (39,II,'Wave superposition and phase evolution','The counterpropagating displacement graph must be inspected; the required physics is ordinary interference.'),
 (40,X,'Thin-lens image formation','The two-lens real-image threshold is ordinary prerequisite ray optics.'),
 (41,II,'Standing waves in an air column','The bottle pitch follows acoustic standing-wave boundary conditions.'),
 (42,X,'Two-source interference and path-difference geometry','Hyperbolic fringes require wave phase and geometry, not an external theory.'),
 (43,X,'Refraction and total internal reflection','The cylinder ray diagram tests elementary optics at both side and end surfaces.'),
 (44,II,'Spherical-wave energy spreading and propagation phase','Amplitude scaling and the sign of omega are standard wave characteristics.'),
 (45,III+';'+IV,'Ideal-gas internal energy and first-law heat flow','The P-V line and monatomic heat capacity are explicitly in scope.'),
 (46,IV,'First/second laws and Carnot efficiency bound','The claimed heat engine is assessed by conservation and temperature-based efficiency.'),
 (47,III,'Molecular kinetic theory and wall-collision flux','Oxygen collision frequency is ordinary ideal-gas kinetic reasoning.'),
 (48,III+';'+IV,'Molecular degrees of freedom and adiabatic mixing energy','Monatomic/diatomic gases require ideal-gas heat capacities and conservation of internal energy.'),
 (49,XI+';'+IV,'Stefan-Boltzmann balance and inverse-square radiation flux','The Earth/Sun context reduces to listed black-body radiation and energy balance.'),
 (50,III+';'+IV+';'+I,'Adiabatic ideal gas and droplet force balance','The insulating capillary and final 3L/4 column use ordinary thermodynamics and pressure forces.')]
data=w.cache(2980); headers=[]
for page in data['pages']:
    for b in page['blocks']:
        for match in re.finditer(r'Question\s+(\d+)\b',b[4]):
            # Only block-start headings, not common-stem references.
            if match.start()==0:headers.append((int(match[1]),page['page'],b[:4]))
assert [n for n,p,b in headers]==list(range(1,51)),headers
page_map={n:p for n,p,b in headers};bbox={n:b for n,p,b in headers}
items=[]
for n in range(1,51):
    p=page_map[n];start=22 if n==31 else p
    items.append({'number':str(n),'page_start':start,'page_end':p,'format':'multiple_choice',
      'location':{'heading_page':p,'heading_bbox_pdf_points':bbox[n],
        'shared_context_pages':[22] if n==31 else [13] if n in (17,18) else [],
        'numbering_provenance':'Provided reordered LaTeX transcription; do not equate this numbering with a different original paper.'}})
w.writejson(w.ROOT/'reviews/sjpo_2026_boundaries.json',[{'source_problem_id':4055,
 'boundary_evidence':'All 35 pages read and visually inspected. Exactly 50 explicit Question 1..50 headings/options verified, each a top-level MCQ. Shared stems do not merge separately numbered MCQs. Header states independent reordered LaTeX transcription; preserve that provided numbering.',
 'units':items}]);w.derive(w.ROOT/'reviews/sjpo_2026_boundaries.json')
rows=[]
for n,domain,physics,reason in sj:
    p=page_map[n];start=22 if n==31 else p
    rows.append([f'derived::d086c64af4c00eac::4055::{n}','KEEP',domain,physics,reason,
      f'SJPO 2026 provided transcription Q{n}: complete stem/options and diagrams on page(s) {start}-{p} read and visually inspected; no topic tags used.',[start,p],'multiple_choice',1,0,'high',''])
w.writejson(w.ROOT/'reviews/sjpo_2026.json',{'rows':rows,'boundary_note':'Separate explicit top-level MCQ; retain all options and supplied/shared context. Provided transcription numbering is authoritative for this file.'})
subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(w.ROOT/'reviews/sjpo_2026.json')],check=True)

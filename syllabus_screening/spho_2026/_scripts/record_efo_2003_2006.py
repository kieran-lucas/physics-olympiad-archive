from persist_reviewed_shared_papers import save
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';X='X_wave_optics';XI='XI_quantum_light'
specs={2891:[
(VI,1,1,'Finite-resistance ammeter/voltmeter readings before and after a parallel resistor'),
(X,1,5,'Concave-mirror focus and image constructed from one incident/reflected ray'),
(I,1,1,'Slingshot elastic energy, launch range and pulling force'),
(I,1,2,'Water-pistol exit speed from piston force, nozzle areas and inviscid work/continuity'),
(X,1,2,'Moon reflectivity estimated from day/night photographic exposure and geometry'),
(I+';'+VI,2,2,'Electron-gun lift from charge current, accelerating voltage and momentum flux; relativity explicitly excluded'),
(IV,2,3,'Long-term room temperature from a cooling/heating curve without assuming linear heat loss'),
(IV+';'+XI,3,3,'Radiative heat flow across multiple shields using supplied emission/absorption law'),
(X,3,4,'Timed light pulses through a specified two-mirror lens system'),
(I,3,3,'Impulse and immediate accelerations of three hinged equal-mass balls')],
2893:[
(I,1,1,'Delayed thrown-ball interception of a released stone from an ascending balloon'),
(X,1,1,'Selecting monochromatic light with chromatic lens dispersion and an aperture'),
(IV,1,1,'Internal-energy and entropy change of water freezing at a prescribed pressure'),
(VI,1,1,'Resistor-power change after source reversal in a diode network'),
(I,1,2,'Water-tank and platform height from a jet-range versus aperture-height graph'),
(II+';'+X,2,2,'Tsunami refraction/focusing at a depth step using explicitly supplied wave speed'),
(I+';'+III,2,2,'Rising bubble spacing using explicitly supplied Stokes drag, hydrostatics and ideal-gas expansion'),
(I+';'+VI,2,2,'Charged-particle deflection through two unequal series capacitor fields'),
(I,2,3,'Orbital altitude from a space-station ground track and Earth rotation'),
(I,2,3,'Frictional equilibrium of a three-mass frame straddling a rotating platform')],
2896:[
(I,1,1,'Suspended gun recoil height and bullet speed from momentum and energy'),
(I,1,1,'Waterslide speed ratio under prescribed constant resistance and different masses'),
(VI,1,1,'Maximum safe current in parallel fuses with unequal resistance and current limits'),
(I,1,1,'Motorcycle wheel lift under acceleration; torque and rear-wheel friction'),
(I+';'+X,1,1,'Time between direct-sun loss and loss of snow-mountain reflected illumination; geometry'),
(IV,1,2,'Ice mass from a kettle temperature-time graph, heater power and latent heat'),
(X,2,2,'Laser through a transparent half-cylinder; total internal reflection and limiting ray geometry'),
(I,2,4,'Stationary tethered buttons on a rotating platform; friction directions and force balance'),
(X,2,3,'Two-mirror interference fringes and wavelength from virtual-source geometry'),
(I+';'+II+';'+VI,3,3,'Connected metal spheres in an electric field; induced charge, tension and small rotational oscillations')],
2897:[
(I,1,1,'Puck half on a moving conveyor; distributed friction and translation/rotation'),
(I,1,1,'Bottle cork extraction force/work from specified radial pressure and friction'),
(X,1,1,'Concave mirror focus constructed from point source and image'),
(I,1,2,'Tide recorder systematic error from float buoyancy and stylus-friction torque'),
(VI,2,2,'Sum of ladder-circuit voltmeter readings using branch-current differences'),
(I+';'+III,2,3,'Ballast removal after heating and venting a hydrogen aerostat'),
(I,3,3,'Minimum bird flight energy per distance from its supplied power-speed graph'),
(I,3,3,'Water-filled barrel crossing a curb; inelastic impulse and gravitational energy'),
(X,3,4,'Photographer distance from moire pattern of a perforated rectangular lamp'),
(I+';'+VII+';'+VIII,4,4,'Proton acceleration and confinement fraction after rapid cylindrical magnetic-field switch-on')]
}
experiments={
2891:[('E1',4,4,'KLAASPLAAT',X,'Measuring a glass plate refractive index with ray construction and a ruler','Refraction and experimental geometry are ordinary general physics.'),('E2',4,4,'LAMP',II,'Estimating lamp flicker frequency through controlled manual motion and timing','Temporal oscillations, repeated-pattern counting and measurement estimation suffice.')],
2893:[('E1',3,3,'Õhu tihedus',I+';'+III,'Air density inside a balloon from load/contact area, given external pressure and temperature','The given small-deformation condition makes pressure measurement and ideal-gas reasoning sufficient.'),('E2',3,3,'Kaldpind',I+';'+IV,'Measuring frictional energy dissipation on a ramp allowing speed-dependent friction','Total energy loss can be measured kinematically; no unsupplied drag law is necessary.')],
2896:[('E1',3,3,'PLAAT',I,'Measuring an irregular plate mass by center-of-mass location and lever balance','Torque equilibrium and measurement design are in scope.'),('E2',3,3,'PIRN',VI,'Determining lamp resistance power-law coefficients with specified meter characteristics','The nonlinear resistance model is supplied; circuit measurements and logarithmic fitting suffice.')],
2897:[('E1',4,4,None,I,'Measuring a wooden cylinder density with buoyancy and geometry','Hydrostatic equilibrium and measurement design are ordinary foundations.'),('E2',4,4,None,VI,'Measuring tap-water resistivity with electrodes, meter loading and circuit measurements','The task requires ordinary resistivity geometry, current/voltage measurement and experimental controls, not an electrochemical theory calculation.')]
}
overrides={
(2893,'6'):dict(external_physics_if_any='Tsunami speed-depth law supplied',decision_reason='The specialized wave-speed law is provided; refraction and ray convergence determine where the largest wave reaches shore.'),
(2893,'7'):dict(external_physics_if_any='Stokes drag relation supplied',decision_reason='The statement supplies the viscous drag law and the terminal-force-balance assumption. Buoyancy, gas compression and bubble speed/spacing are ordinary physics.'),
(2897,'8'):dict(solution_used=1,decision_reason='Official solution treats the water as freely slipping and uses a conserved tangential velocity component at impact followed by mechanical energy. No external fluid-dynamics equation is required.'),
(2897,'E1'):dict(map_solution=False,source_quality_notes='The six-page acquired solution paper ends after theory Q10; no experimental solution is mapped.'),
(2897,'E2'):dict(map_solution=False,source_quality_notes='The six-page acquired solution paper ends after theory Q10; no experimental solution is mapped.'),
}
save('resume_efo_2003_2006_48.json',specs,experiments,overrides)

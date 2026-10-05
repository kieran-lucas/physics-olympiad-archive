from persist_reviewed_shared_papers import save
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light'
specs={2899:[
(I,1,1,'No-slip equilibrium/stability of an off-center-mass sphere on a hemisphere'),
(I,1,1,'Constructing a projectile interception velocity from two positions and a specified speed'),
(X,1,1,'Maximum signaling range of a mirror versus lamp from solar angular size and illumination'),
(VI,1,2,'Four-state two-lamp signaling circuit with diodes and one inter-house conductor'),
(VI+';'+VIII+';'+IX,2,2,'Resistor-inductor-capacitor switching; instantaneous continuity and long-time currents'),
(I,2,2,'Mapping a discrete vector racing game to a friction-limited physical speed'),
(IV,2,3,'Annual heating/cooling electricity cost from supplied efficiencies and temperature-duration graph'),
(I,3,3,'Period change in a mass-transferring Newtonian binary using angular momentum and gravity'),
(III+';'+IV,3,4,'Specified four-stroke ideal-gas engine cycle and efficiency'),
(II+';'+X,4,4,'Fiber ring resonator intensity and circumference from given coupling ratio and transmission spectrum')],
2901:[
(I,1,1,'Movable wedge velocity constructed from a sliding coin velocity and momentum'),
(I,1,1,'Ice and embedded sand masses from buoyancy and water-level changes after melting'),
(VI,1,1,'Two finite-resistance voltmeters loading a potentiometer'),
(I,1,1,'Rolling speed ratio of thin tube and concentric double tube from moment of inertia'),
(IV,1,2,'Pond freezing rate from the explicitly supplied heat-conduction law and latent heat'),
(X,2,2,'Magnifier field of view with specified eye position and focal-plane paper'),
(I,2,2,'Maximum front-wheel braking deceleration with load transfer and Coulomb friction'),
(I,2,2,'Tidal disruption distance in a specified homogeneous self-gravitating moon model'),
(II+';'+X,2,3,'Equal fiber-coupler phase shift and two-coupler interference using energy conservation'),
(IV+';'+VI,3,4,'Filament heating times and periodic temperature amplitude using given resistivity graph')],
2903:[
(I,1,1,'Free surface and pressure in a horizontally accelerating water container'),
(I+';'+IV,1,1,'Heat needed for ice containing lead to lose buoyancy and sink'),
(I,1,1,'Optimal swimming angle in a faster river for crossing time and downstream drift'),
(III+';'+IV,1,1,'Pressure of a trapped air bubble in warming glycerin; supplied expansion coefficient and model limits'),
(X,1,1,'Apparent underwater depth at normal and oblique viewing angles'),
(IV+';'+VI+';'+XI,1,1,'Filament geometry/temperature from given resistivity-temperature law and Stefan-Boltzmann radiation'),
(VI,1,2,'Load resistor maximum power in a four-resistor source network'),
(I,2,2,'Minimum applied force to hold a rod against a smooth wall and floor'),
(I,2,2,'Separation of equal spheres after central or glancing elastic collisions'),
(I+';'+VI,2,2,'Sliding force between voltage-controlled capacitor plates separated by dielectric')],
2904:[
(I,1,1,'Pulling a partly dragging rope; distributed weight and friction'),
(IV,1,1,'Maximum ice formation during vacuum evaporation from an insulated water sample'),
(I,1,1,'Minimum swimming speed to intercept an anchored downstream boat'),
(VI,1,1,'Four ideal ammeter readings in a symmetric resistor circuit'),
(X,1,1,'Reconstructing an unknown single lens from surviving ray segments'),
(I+';'+III+';'+IV,1,1,'Mountain air temperature from hydrostatic pressure and explicitly supplied adiabatic approximation'),
(X,1,1,'Correcting a displaced eye near-point with a contact lens'),
(I+';'+VII+';'+VIII,1,2,'Sliding current-carrying copper wire; magnetic force, friction and induced back EMF'),
(I+';'+XI,2,2,'Radiation-pressure expulsion of a black bacterium from the Sun; supplied photon energy/momentum ratio'),
(I,2,2,'Elastic dumbbell scattering from a cylinder; rotation and impact geometry')],
2907:[
(X,1,1,'Red/violet travel-time order to a flat pond bottom using given refractive indices'),
(I,1,1,'True mass from two swapped weighings on an unequal-arm balance'),
(I+';'+VI,1,1,'Closest approach of two like-charged particles with one fixed or both free'),
(IV,1,1,'Radiator/wall heat balance and limiting ambient temperature before boiling'),
(III+';'+IV,1,1,'Air temperature delivered by an adiabatic tire pump; supplied pressure-volume law'),
(X,1,1,'Images between perpendicular and slightly wider plane mirrors; orientation and multiplicity'),
(I,1,1,'Car-crash impulse graph calibration and seat-belt versus unrestrained passenger force'),
(I,1,2,'ABS stopping distance and tire deformation using supplied friction-speed curves and tread model'),
(I,2,2,'Pulled hollow cylinder motion with localized versus uniform floor friction'),
(IV+';'+VI,2,2,'Capacitor discharge heating of a wire; electrical/thermal graphs, heat capacity and approximation error')]
}
experiments={
2899:[('E1',4,4,None,X,'Measuring a concave lens optical power with a ruler and grid','Ray geometry and scale measurements suffice.'),('E2',4,4,None,I,'Measuring pencil/glass friction with a tethered pencil equilibrium','The uniform-stick model is supplied; force/torque geometry suffices.')],
2901:[('E1',4,4,None,VI,'Measuring lamp room-temperature resistance by low-current I-V extrapolation','Circuit measurements, extrapolation and self-heating control are ordinary experimental reasoning.'),('E2',4,4,None,X,'Estimating CD-track spacing through diffraction of given visible wavelengths','Diffraction-grating physics and angular measurement are explicitly within the syllabus.')],
2903:[('E1',2,2,None,X,'Constructing a 36-degree angle using two plane mirrors and image multiplicity','Reflection geometry and counting repeated images suffice.'),('E2',2,2,None,VI,'Determining a four-component resistor/diode black-box topology from polarity-dependent ohmmeter readings','Ordinary circuit input/output reasoning suffices; material semiconductor theory is unnecessary.')],
2904:[('E1',2,2,None,X,'Measuring lens magnification versus object/lens/eye position and graphing','Lens imaging and experimental comparison with a grid are foundational optics.'),('E2',2,2,None,VI,'Measuring voltmeter and ammeter internal resistance and selecting ranges','Circuit loading and uncertainty are within the operational experimental scope.')],
2907:[('E1',2,2,None,I+';'+II,'Measuring pendulum period versus string length and deriving its fitted relation','Mechanical oscillations, graphs and experimental fitting are explicitly eligible.'),('E2',2,2,None,I,'Ranking three liquid densities using a weighted floating stick','Buoyancy and measurement design determine density ordering without chemical identification.')]
}
overrides={
(2899,'10'):dict(external_physics_if_any='Fiber coupling behavior and spectrum supplied',decision_reason='Coupling fractions and the measured spectrum are supplied. Conservation of light energy, phase resonance and wavelength spacing suffice; no evanescent-mode field calculation is requested.'),
(2901,'9'):dict(external_physics_if_any='Equal splitting specified',decision_reason='The phase relation is derived from energy conservation and wave superposition. The subsequent task is ordinary two-path interference, without deriving a guided-mode coupling theory.'),
(2901,'8'):dict(decision_reason='The homogeneous self-gravitating moon and synchronous rotation are specified; differential Newtonian gravity and first-order approximations suffice. Astrophysical material theory is not required.'),
(2904,'9'):dict(decision_reason='The supplied photon E/p=c relation reduces the exotic biological-space setting to radiation momentum flux versus inverse-square gravity.'),
(2904,'E1'):dict(source_quality_notes='Official solution labels E1/E2 are swapped relative to statements: the lens experiment is solution E2. Both occur in the same shared solution PDF; pair by content, not printed E label.'),
(2904,'E2'):dict(source_quality_notes='Official solution labels E1/E2 are swapped relative to statements: the meter experiment is solution E1. Both occur in the same shared solution PDF; pair by content, not printed E label.'),
}
save('resume_efo_1998_2002_60.json',specs,experiments,overrides)

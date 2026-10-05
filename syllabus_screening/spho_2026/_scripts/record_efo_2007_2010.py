from persist_reviewed_shared_papers import save
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';X='X_wave_optics'
specs={2883:[
(I,1,1,'Car normal force and loss of contact at the top of a circular bridge'),
(IV,1,1,'Distillation cooling-water flow from condensation heat and heat capacity'),
(VI,1,1,'Maximum solar-panel load power from the supplied current-voltage graph'),
(I,2,2,'Meshed gears tied by a tangent string; torque balance and string tension'),
(I,2,2,'Stability of a beam on a rough fixed cylinder using center-of-mass height'),
(I+';'+IV,2,2,'Dry-ice disk supported by vapor pressure; supplied saturation-pressure curve'),
(I+';'+III,3,3,'Estimated satellite collision rate from supplied shell distribution and geometric cross section'),
(VI,3,3,'LED chain rectification, resistor rating and capacitor smoothing with given diode voltage models'),
(X,3,5,'Reconstructing a thin lens and axis from four source/image points'),
(I,3,4,'Propeller rotation from a supplied column-scanning camera model and photograph')],
2885:[
(I,1,1,'Branch between blunt shears; contact geometry and static friction'),
(I,1,1,'Minimum rope tension securing a box in a braking van with friction'),
(VI,1,1,'Charge redistribution in an initially charged five-capacitor network'),
(III+';'+IV,1,2,'Train motor energy heating tunnel air treated as a diatomic ideal gas'),
(I,2,2,'Stop duration reconstructed from sampled GPS average-speed graph'),
(III+';'+IV,2,2,'Room equilibrium temperature with a heater and ventilation heat flow'),
(X,3,3,'Confocal microscope field of view from the supplied lens/aperture geometry'),
(I+';'+II,3,3,'River current and depth from a boat wake with the supplied shallow-water wave law'),
(I+';'+VI,4,4,'Inelastic encounter of debris with a tether connecting charged balls; momentum and Coulomb energy'),
(X,4,4,'Transparent floor-film thickness from angular interference fringes')],
2888:[
(I,1,1,'Dumbbell kinetic energy at its center-of-mass apex; translation and rotation'),
(I,1,1,'Total bouncing-ball time from prescribed fractional energy retention'),
(III,1,1,'Total molecular translational kinetic energy of room air from pressure and volume'),
(X,1,4,'House height from a photograph and reflected image geometry'),
(X,1,1,'Underwater point-source brightness from refraction, reflection loss and ray geometry'),
(I+';'+IV,1,2,'Superheated-water bubble radius from surface-tension pressure balance and supplied vapor-pressure slope'),
(VI,2,2,'Nonuniformly stretched wire resistance from a supplied marker-spacing graph and constant density/resistivity'),
(I+';'+II,2,2,'Liquid oscillation frequency in an inclined U-tube; supplied vertical-tube frequency'),
(I,2,3,'Rod equilibrium against a smooth cylinder and rough floor'),
(VII+';'+VIII,3,3,'Force to stretch a current-carrying solenoid; magnetic interaction/energy and supplied field')],
2889:[
(VI,1,1,'Heating-power ratio of a rectangular conducting-glass film for perpendicular electrode directions'),
(I,1,1,'Venus elongation geometry and interval using the explicitly supplied Kepler law'),
(X,1,1,'Small glass wedge angle from laser-beam deflection'),
(I,1,1,'Flywheel rotational energy density limited by explicitly defined tensile strength'),
(I,1,3,'Minimum-time return shipping schedule from a tidal-current time graph'),
(III+';'+IV,1,1,'Hydrogen/helium heating and subsequent thermal equilibration under a movable load'),
(IV,2,4,'Room equilibrium temperature via graphically supplied heater power and linear heat loss'),
(X,2,2,'Glass cube with spherical colored cavity; refraction and total internal reflection'),
(X,2,4,'Constructing convex-mirror center and virtual image in a lens-mirror system'),
(I+';'+VII,2,2,'Shape and tension of a flexible current-carrying wire in a uniform magnetic field')]
}
experiments={
2883:[('E1',4,4,'TRAAT',VI,'Measuring wire resistivity by matching lamp brightness and known resistance','Circuit comparison, geometry and uncertainty suffice; no optical detector calibration is prerequisite.'),('E2',4,4,'VENTILAATOR',I,'Estimating fan airspeed from a deflected known-mass plate','The official method uses momentum flux and torque balance, ordinary general-physics foundations.')],
2885:[('E1',4,4,'KOORMISE MASS',I,'Measuring a load exceeding the force-meter range using repeated rope wraps','Coulomb friction and tension balance permit comparison and uncertainty estimation; no material theory is required.'),('E2',4,4,'TUNDMATU VEDELIK',I+';'+III,'Measuring liquid density with a syringe and sealed bottle, controlling temperature drift','Hydrostatic pressure and isothermal ideal-gas compression control the experiment.')],
2888:[('E1',3,3,'AMPERMEETER',VI,'Calibrating a voltmeter as a milliammeter with a known resistor','Internal resistance, Ohm law and uncertainty suffice; matching EXP1 solution visually inspected.'),('E2',3,3,'PABER',I,'Measuring paper/paper friction with limited-force apparatus and uncertainty','Ordinary friction forces and measurement amplification suffice; matching EXP2 solution visually inspected.')],
2889:[('E1',2,2,'SÜSTAL',I,'Measuring water surface tension from measured syringe-drop volume and circumference','Surface-force balance with drop weight and uncertainty is foundational general physics.'),('E2',2,2,'MUST KAST',VI,'Identifying a diode/capacitor black-box topology with polarity-sensitive lamp tests','Device input/output behavior and charge storage are ordinary circuit reasoning; semiconductor band theory is unnecessary.')]
}
overrides={
(2883,'3'):dict(external_physics_if_any='Solar-panel characteristic explicitly supplied',decision_reason='The entire measured I-V curve is supplied. Optimizing U*I and computing load resistance requires no photovoltaic material theory.'),
(2883,'6'):dict(external_physics_if_any='Dry-ice vapor-pressure graph supplied',decision_reason='The pressure-temperature graph and contact-temperature assumptions are given; supporting force is pressure times area, without a Leidenfrost/flow-theory prerequisite.'),
(2885,'7'):dict(external_physics_if_any='Confocal apparatus fully specified',decision_reason='The specialized instrument is reduced to its supplied lens/aperture diagram. Paraxial ray geometry determines the field of view.'),
(2885,'8'):dict(external_physics_if_any='Shallow-water wave speed supplied'),
}
save('resume_efo_2007_2010_48.json',specs,experiments,overrides)

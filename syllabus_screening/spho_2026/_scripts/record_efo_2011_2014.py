from persist_reviewed_shared_papers import save
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';X='X_wave_optics'
specs={2884:[
(VI,1,1,'Equivalent resistance of a two-by-two wire grid'),
(II,1,1,'Violin harmonic frequencies with a pressed versus lightly touched string node'),
(I+';'+III+';'+IV,1,2,'Heating-system expansion tank; given water-density graph and isothermal compressed air'),
(X,2,2,'Periscope-glasses prism; reflection, refraction and ray-region geometry'),
(I+';'+X,2,2,'Moving comb moire spots; relative geometric pattern speed'),
(I,3,3,'Pulley rescue system force ratio with explicitly prescribed frictional loss'),
(I,3,3,'Maximum front-wheel-drive acceleration with load transfer, torque and friction'),
(I,3,3,'Initial acceleration of a light inner cylinder; displaced-water continuity and energy'),
(I,3,3,'Moving contact point of two rotating touching wire rings; rigid-motion geometry'),
(X,3,4,'Multiple images of a marked glass cylinder point; refraction and total internal reflection')],
2876:[
(X,1,1,'Inferring concave-lens focal length from a two-lens beam cross section'),
(I,1,6,'Bounce height from acoustic peak intervals and free-fall timing'),
(I,1,1,'True wind speed from opposite cyclist-relative speeds'),
(VI,1,1,'Reconstructing identical-capacitor black box from initial terminal voltages'),
(I,2,2,'Ground area visible from a geostationary satellite; Newtonian orbit and tangent geometry'),
(II+';'+I,2,5,'Pond depth from wavefront positions using explicitly supplied deep/shallow-wave speed laws'),
(X,2,2,'Digital-microscope irradiance for two conjugate lens positions'),
(IV,2,3,'Shop heat balance with a vestibule; supplied linear heat-loss and well-mixed air model'),
(I,3,3,'Possible collision locations of simultaneously launched equal-speed footballs'),
(VI+';'+I,3,3,'Work when inserting an isolated conducting plate into a charged capacitor')],
2878:[
(I+';'+IV,1,1,'Friction welding; rotational friction work and given heat capacity'),
(I,1,5,'Pipe diameter from photographed ballistic jet, volume and collection time'),
(VI,1,1,'Currents in a bridge with identical resistors and two EMF sources'),
(I+';'+III,1,1,'Depth at which a submerged basketball loses buoyancy; isothermal compression'),
(I,2,2,'Wheel steering angles for pure rolling on a turn'),
(X,2,6,'Images of a point source in a reflecting tube with a lens'),
(IV,2,7,'Lead latent heat from an oven temperature-time graph and heater power'),
(I,2,2,'Working hourglass scale-force difference; given sand flow and momentum/center-of-mass motion'),
(I+';'+VI,3,3,'Charged-particle transmission through a prescribed potential slab and angular distribution'),
(I,3,3,'Extreme slider velocity in a rotating two-rod hinged mechanism')],
2880:[
(IV,1,1,'Evaporative cooling in an insulated open flask with supplied latent heat'),
(I,1,1,'Sliding bead on a negligible-mass freely hinged rod; Newtonian free fall and geometry'),
(I,1,1,'Crosswind tipping versus sliding of a truck; torque and friction'),
(I,1,1,'Pipe diameter ratio from pressure-column heights; Bernoulli relation explicitly supplied'),
(VII,1,1,'Electron axial speed in a solenoid; supplied field and magnetic helix pitch'),
(I+';'+X,2,2,'Rolling-shutter streak lengths under camera rotation; shutter mechanism fully supplied'),
(I,2,2,'Friction condition for an off-center-mass ring on a rotating shaft'),
(X,2,2,'Focal length of a lens with one mirrored surface; paraxial refraction and reflection'),
(VI,3,3,'Nerve-membrane equilibrium charge using explicitly defined EMF/resistance/capacitance model'),
(I,3,3,'Screw jack lifting force and minimal self-locking friction; work and torque')]
}
experiments={
2884:[('E1',4,4,'FRESNELI LÄÄTS',X,'Measuring Fresnel-lens refractive index with water and focal-length observations','The lensmaker and combined-power relations are supplied; geometrical optics and parameter measurement suffice.'),('E2',4,4,'KLOTS',I,'Measuring block static friction without tilting the table','Force balance and parameter estimation are ordinary mechanics.')],
2876:[('E1',3,4,'TÄHT',VI,'Measuring three star-connected resistors with ideal and known finite-resistance voltmeter','Both internal parts are circuit-measurement reasoning, kept as one experiment.'),('E2',4,4,'PINKSIPALL',I,'Measuring ball/ruler static friction and uncertainty','Contact-force geometry and uncertainty reasoning are eligible experimental foundations.')],
2878:[('E1',3,3,'STEREOPOTENTSIOMEETER',VI,'Measuring paired-potentiometer resistance and uncertainty from a given nonlinear device','The device topology and equal fractional settings are stated; network symmetry and measurements suffice.'),('E2',4,4,'MUFFINIVORM',I,'Measuring exponent of an explicitly supplied drag power law using falling paper cups','The drag law is supplied; terminal force balance, timing and uncertainty require no external flow theory.')],
2880:[('E1',3,3,'SÜSTAL',I,'Measuring syringe needle diameter by jet height, discharge volume and time','Official solution confirms ballistic energy and volume continuity, without Poiseuille or viscous-flow theory.'),('E2',4,4,'MUST KAST',VI,'Measuring EMF and three resistances in a supplied three-terminal circuit','Ordinary circuit laws and multimeter measurements suffice.')]
}
overrides={
(2884,'8'):dict(solution_used=1,decision_reason='The solution uses volume continuity and kinetic/potential energy for the displaced water, not a specialized continuum-fluid equation. This is an ordinary general-physics energy model.'),
(2876,'6'):dict(external_physics_if_any='Deep/shallow surface-wave speed models supplied',decision_reason='Both specialized limiting wave-speed laws are explicitly supplied. Position graphs, integration and dimensional reasoning determine depth without deriving hydrodynamic dispersion.'),
(2880,'9'):dict(external_physics_if_any='Biological membrane circuit model explicitly supplied',decision_reason='The statement converts ionic chemical work into defined EMFs and gives channel resistances and membrane capacitance. Ordinary circuit equilibrium suffices; neurophysiology is context.'),
}
save('resume_efo_2011_2014_48.json',specs,experiments,overrides)

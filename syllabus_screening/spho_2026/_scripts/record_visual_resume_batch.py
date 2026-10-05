"""Persist explicit reviews of scanned British papers and inspected SJPO pages."""
import json
import workflow as w
c=w.connect(); boundaries=[]
for pid,starts,last in [(2597,[2,5,6,7,8,9,10],10),(2599,[2,6,7,8,9,10,11],11),(2601,[2,5,6,7,8,9,10,11,12],12),(2603,[2,6,7,8,9,10,11,12,12],12),(2605,[2,4,5,6,7,8,9,10,11,12],12)]:
 r=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone(); assert r['status']=='pending_boundary_review'
 boundaries.append(dict(source_problem_id=pid,boundary_evidence='All rendered statement pages inspected. Printed Q1-Q%d headings verified; compulsory general Q1 keeps its internal parts. Archive year retained despite printed following competition year.'%len(starts),units=[dict(number=str(i+1),page_start=p,page_end=(starts[i+1]-1 if i+1<len(starts) and starts[i+1]>p else p) if i+1<len(starts) else last,format='theory',location={'source_label_present':True}) for i,p in enumerate(starts)]))
p=w.ROOT/'reviews/resume_scanned_british_boundaries.json';w.writejson(p,boundaries);w.derive(p)
# Each entry below is an actual source-content judgment, not a metadata rule.
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
specs={
2593:[
([I,II,III,IV,VI,VII,X,XI,XII],'General question: energy, calorimetry, forces, waves, circuit currents, photoelectric effect, nuclear energy and elementary measurement uncertainty'),
([I],'Two stones falling and colliding elastically; velocities and motion graphs'),
([I,II],'Bungee cord with linear spring extension; energy, acceleration and maximum speed'),
([XII],'Radioactive decay, tracer dilution and background-corrected counting'),
([I],'Composite-disc centre of mass and static-friction plank equilibrium'),
([X],'Lloyd mirror interference, phase reversal and white-light fringe pattern'),
([VI],'Voltage divider, capacitor charging equilibrium and symmetric resistor lattice'),
([I],'Elliptical Kepler orbit, energy, angular momentum and swept area')],
2595:[
([I,II,III,VI,VIII,XI,XII],'General question: energy, force, wave timing, buoyancy, radiation pressure, uncertainty, circuits, induction and nuclear decay'),
([VI],'Resistor networks and supplied recurrence relations'),
([I,XI],'Binary-star circular orbit and Newtonian particle model of light deflection; statement expressly ignores relativity'),
([I],'Beam and cable equilibrium followed by projectile interception'),
([I,III,IV],'Elastic collisions and communicating ideal-gas pistons with a spring'),
([XI],'Photoelectric voltage-frequency graph, work function and uncertainty'),
([XII],'Two radioactive populations; counting efficiency and graphical decay separation'),
([I,VI,VII],'Charged-particle motion in crossed fields; later relativistic mass law explicitly supplied')],
2597:[
([I,II,III,IV,VI,X,XI,XII],'General question: nuclear conservation, force balance, circuits, thermal effects, interference, spring energy and gas compression'),
([VI],'Symmetric resistor network and equivalent resistance'),
([II],'Moving sound-source Doppler shift and frequency-time data used to infer closest approach'),
([I],'Impact-crater data and explicitly supplied energy/diameter law; graph fit and uncertainty'),
([VI,IX],'Capacitor energy and ordinary diode/RC smoothing circuit'),
([VII,VIII],'Motional EMF of aircraft and rotating conducting rod'),
([I],'Planetary period-radius power-law fit and Newtonian inference of solar mass')],
2599:[
([I,II,IV,VI,X,XII],'General question: forces, circuits, centre of mass, buoyancy, supplied resistance law, rays, waves and nuclear mass defect'),
([II],'Two-transmitter interference, geometry and received-intensity power-law graph'),
([VI,IX],'Multi-branch battery circuits and alternating-current phase superposition'),
([I,II],'Elastic impact with spring-coupled masses; centre-of-mass and oscillation motion'),
([I,IV],'Electrical heating data fit and supplied fireball radius-time scaling; dimensional exponent and uncertainty'),
([I,VI,XII],'Rutherford Coulomb approach and recoil using energy and momentum conservation'),
([I],'Projectile motion with explicitly specified constant wind force')],
2601:[
([I,II,III,IV,VI,VII,X],'General question: calorimetry, supplied current law, friction, waves, evaporation, buoyancy, circuits and magnetic torque'),
([I],'Gravity inside/outside a uniform Earth and synchronous/circular satellite orbits'),
([XII],'Sequential radioactive decay; population ratio, asymptotic limits and parameter inference'),
([I,VII],'Circular motion and helical charged-particle motion in a uniform magnetic field'),
([I,VI],'Potential of charged spheres and electrostatic capture/approach energy'),
([X],'Cubic lattice geometry and X-ray Bragg diffraction; atomic placements and diffraction geometry supplied'),
([XI],'Compton scattering with explicitly supplied relativistic energy-momentum relation'),
([I],'Venus transit geometry, orbital periods, parallax and measurement accuracy'),
([VI],'Resistor bridge limiting cases and network symmetry')],
2603:[
([I,II,III,IV,VI,XI],'General question: radiation pressure, pendulum in electric field, van der Waals equation supplied, ice friction, wave travel and graphing'),
([I,II],'Falling stone and acoustic travel-time measurements in a canyon'),
([I],'Loaded rigid rod and elastic extension of supporting wires; elastic law constants supplied'),
([I,VI,VII,VIII],'Solar-car power budget, generator induction and brushless motor switching'),
([I,II],'Historical light-speed measurements using orbital timing and rotating toothed wheel'),
([VI,VII],'Electric potential and crossed-field charged-particle deflection'),
([X],'Mirror images and two-slit/two-mirror interference'),
([I,III,XII],'Elastic neutron moderation, thermal equilibrium and ballistic pendulum'),
([XII],'Radioactive count-time fit and sequential decay dating')],
2605:[
([I,VI,XI,XII],'General question: uncertainties, photon number, rocket motion, mass-energy units, charge potential, gravity and supplied relativistic graph law'),
([I,II],'Two falling bars coupled by springs; impact, energy and normal relative motion'),
([VI,XI],'Photoelectric apparatus, electron acceleration and time-varying grid potential'),
([VI],'Cell/resistor networks, star-delta equivalence and limiting resistor values'),
([II,VII],'Magnetic current interaction and oscillation of a magnetized cork with a supplied frequency relation'),
([I],'Eclipse geometry and gravitational orbital periods, energy and turning points'),
([II],'Wave polarization, beats and acoustic Doppler effect'),
([I,II,X],'Dispersion, diffraction, radio interferometry and pulsar rotation/refractive-medium inference'),
([XI,XII],'Hydrogen transitions, positron annihilation and Compton backscattering with nonrelativistic electron energy'),
([III,IV],'Heating ice through phase changes, vaporization data and calorimetric mixing')]
}
out=[]
def record(pid,num,decision,domains,physics,reason=None,confidence='high',external='',pages=None):
 u=c.execute('select * from units where source_problem_id=? and problem_number=?',(pid,str(num))).fetchone();assert u and u['decision'] is None,(pid,num)
 out.append(dict(screening_unit_id=u['screening_unit_id'],decision=decision,confidence=confidence,primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any=external,decision_reason=reason or ('Dominant work is '+physics[0].lower()+physics[1:]+'. These are syllabus physics, ordinary foundations or explicitly supplied models.'),visual_inspection_used=1,solution_used=0,page_start=(pages or [u['page_start'],u['page_end']])[0],page_end=(pages or [u['page_start'],u['page_end']])[1],boundary_status='content_boundary_verified',evidence='Actual scanned statement, equations and figures inspected in cached page renders; entire printed top-level question retained.'))
for pid,items in specs.items():
 for n,(domains,physics) in enumerate(items,1):record(pid,n,'KEEP',domains,physics)
# MCQ items read on the specific rendered pages during boundary repairs.
mcqs=[
(4058,27,17,[VIII],'Induced EMF and loop voltmeter network'),(4058,28,17,[VIII],'Average Faraday EMF in a coil'),
(4059,1,3,[I],'Reaction time and braking distance'),(4059,2,3,[I],'Reaction time and braking-distance comparison'),(4059,3,3,[I],'Yellow-light stopping and crossing kinematics with shared stem'),
(4064,43,21,[VIII],'Dimensions of magnetic flux'),(4064,44,21,[VII,VIII],'Rotating charged ring and induced current in a neighboring loop'),(4064,45,21,[VI],'Resistance change in a triangular circuit'),
(4064,49,23,[I,VI,XII],'Coulomb closest approach of deuteron and lead nucleus'),
(4067,25,11,[IV],'Ice-steam calorimetry'),(4067,26,11,[XI],'Photoelectric stopping voltage and wavelength'),(4067,27,11,[I],'Collision force and Newton third law'),
(4069,16,8,[VI],'Equipotential neutral conductor near an external charge'),(4069,17,8,[I,VI],'Charged-particle deflection and mass ratio in uniform electric field'),(4069,18,8,[VI],'Work along equipotential surfaces'),
(4069,28,12,[I],'Vector force balance in three-force diagrams'),(4069,29,12,[I,III],'Air compression and buoyancy of an inverted test tube'),(4069,30,12,[I],'Gravity measurement from transit times at two heights'),
(4070,18,9,[II],'Standing-wave wavelengths in open/closed air columns'),(4070,19,9,[III,IV],'Ideal-gas pressure-volume cycle'),(4070,20,9,[IV],'Net heat in a circular pressure-volume cycle')]
for pid,n,page,domains,physics in mcqs:record(pid,n,'KEEP',domains,physics,pages=[page,page])
record(4064,48,'BORDERLINE',[XI],'Quantum-operation assumptions for lists of electronic and optical consumer devices','The item requires deciding which named devices rely on quantum operation; semiconductor-device knowledge is not supplied and its status as ordinary prerequisite knowledge is ambiguous.','medium','Semiconductor device operating principles',pages=[23,23])
record(4064,50,'REJECT',[],'General relativity, coordinate covariance, spacetime geometry and Mercury precession','All options test unsupplied general-relativistic conceptual knowledge; familiar orbital vocabulary does not supply the central theory.',external='General relativity',pages=[23,23])
p=w.ROOT/'reviews/resume_visual_content_81.json';assert len(out)==81,len(out);w.writejson(p,out);w.decisions(p)
print('Saved',len(out),'actual-content decisions')

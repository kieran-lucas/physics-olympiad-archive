"""Explicit content decisions for Chinese finals, US selection and Fourier experiment."""
import workflow as w
c=w.connect();out=[]
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';VIII='VIII_induction';IX='IX_em_oscillations_waves';X='X_wave_optics';XI='XI_quantum_light';XII='XII_atomic_nuclear'
specs={1695:[([I,II],'Spring projectile motion with elastic rebound and two-dimensional restoring force'),([I],'Rigid three-point framework, torque equilibrium and Coulomb friction'),([I],'Sliding/tipping stability of composite column under cable pull'),([I,VI],'Charged balls constrained to circular tracks; mechanical and Coulomb energy'),([I,VII],'Charged rotating disk, attached current loop and explicitly supplied loop magnetic field'),([III,IV],'Two ideal-gas compartments; variable heat capacities and explicitly specified dissociation energy/law'),([X],'Collimator/telescope calibration and prism refraction geometry'),([I,VI,XI],'Atomic-unit definitions and dimensional derivation of fundamental units')],
1703:[([X],'Total internal reflection and propagation in optical fibre'),([I,XI],'Energy/momentum conservation for photon absorption by free electron versus metal photoemission'),([I],'Mass sliding on a movable wedge with kinetic friction; work and energy'),([VI],'Capacitor network equilibrium charges and resistor charging heat'),([VI,VII],'Timed accelerator gates and magnetic particle trajectories with force explicitly specified'),([I,II],'Collision of two spring-coupled pairs and subsequent normal motion')],
1704:[([I],'Contact equilibrium of equal-mass balls inside a hemisphere'),([I],'Elliptical satellite trajectory, Newtonian gravitational energy and angular momentum'),([I,VII,VIII],'Driven disk generator, back EMF, acceleration/current graph and terminal state'),([I,VII],'Two particles crossing magnetic regions and minimum encounter time'),([X],'Eye-lens geometry and off-axis circular aperture/retinal blind spot'),([], 'Relativistic cyclotron energy and inelastic absorption involving composite rest mass')],
1679:[([I,II,IV,VI,IX,X],'Partial polarization, supplied hysteretic heating model, Doppler beats, RC network and water momentum flux'),([I],'String tension, variable-mass chain pickup and rigid-rod equilibrium'),([I],'Newtonian binary orbit, dimensional supplied gravitational-radiation model and frequency-time data')],
1680:[([I],'Simulated disk collisions, restitution, friction, rotation, parameter estimation and measurement uncertainty')],
891:[([II,X],'Michelson interference, detector response, supplied mirror oscillation, graph calibration and two-wavelength beating')]
}
for pid,spec in specs.items():
 us=c.execute('select * from units where source_problem_id=? order by screening_unit_id',(pid,)).fetchall();assert len(us)==len(spec)
 # Chinese source labels sort in Unicode order differently from numerical order.
 if pid in (1695,1703,1704):us=sorted(us,key=lambda u:list('一二三四五六七八').index(u['problem_number']))
 for u,(domains,physics) in zip(us,spec):
  assert u['decision'] is None
  reject=pid==1704 and u['problem_number']=='六'
  reason=('Relativistic mass-energy and momentum relations are not supplied; the orbit and composite-rest-mass calculation structurally require them.' if reject else 'Dominant work is '+physics[0].lower()+physics[1:]+', using syllabus physics, ordinary foundations or the explicitly supplied model.')
  if pid==1679 and u['problem_number']=='3':reason='The statement explicitly assumes Newtonian physics and supplies the radiation scaling and exact prefactor. No general-relativistic field theory is needed for the orbital, dimensional and data reasoning.'
  item=dict(screening_unit_id=u['screening_unit_id'],decision='REJECT' if reject else 'KEEP',confidence='high',primary_spho_domains=';'.join(domains),required_physics=physics,external_physics_if_any='Unsupplied special-relativistic dynamics' if reject else 'Gravitational radiation model supplied' if pid==1679 and u['problem_number']=='3' else '',decision_reason=reason,visual_inspection_used=1,solution_used=0,page_start=u['page_start'],page_end=u['page_end'],boundary_status='content_boundary_verified',evidence='Actual complete source statement inspected, with equations/figures in page renders. US selection also read in full embedded text; Chinese bold duplicate statements do not become extra units.')
  if pid==1679 and u['problem_number']=='3':item['needs_second_review']=True
  out.append(item)
assert len(out)==25
p=w.ROOT/'reviews/resume_mixed_content_25.json';w.writejson(p,out);w.decisions(p)
print('Saved',len(out),'actual-content reviews')

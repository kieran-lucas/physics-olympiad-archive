"""Persist explicit whole-paper physics reviews, including omitted experiments."""
import json
import workflow as w
c=w.connect()
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';X='X_wave_optics';XII='XII_atomic_nuclear'
specs={2867:[
(X,1,6,'Ray construction for displaced halves of a converging lens'),
(I,1,1,'Jet diameter versus falling distance; volume conservation and gravitational energy'),
(X,1,2,'Submerged lens above a mirror; supplied lensmaker relation and refraction'),
(I,2,2,'Pendulum catching a peg; energy and loss of string tension'),
(IV,2,2,'Layered wall insulation and condensation; supplied temperature-gradient model and vapor-pressure graph'),
(I+';'+II+';'+VI,2,3,'Spring oscillator driven by an electric field reversing with the velocity'),
(VI,3,3,'Identifying a five-resistor bridge from total and branch current/voltage'),
(I+';'+III+';'+IV,3,3,'Rising helium balloon in an explicitly supplied adiabatic-atmosphere temperature model'),
(VI,4,4,'Capacitor charging/discharging heat and charge through a nonlinear lamp; circuit energy accounting'),
(I+';'+VI,4,4,'Connected conducting balls entering an electric-field region; induction, force and energy')],
2868:[
(I,1,1,'Sled sliding on two slopes then level ground; energy and friction'),
(I,1,1,'Bicycle gear ratio, pedal work and maximum steady climb angle'),
(X,1,1,'Two-wavelength laser separation by a glass wedge; given refractive indices'),
(I,1,2,'Projectile range change for helium-filled basketball; buoyancy and effective acceleration'),
(I,2,2,'Apparent weight on a decelerating train following a circular arc'),
(VI,2,2,'Ammeter and voltmeter readings in a pentagonal resistor network'),
(III+';'+IV,2,2,'Gas temperature after pumping into a balloon; first law and pressure-volume work'),
(X,2,3,'Compact two-lens camera preserving the original field of view'),
(I,3,3,'Hinged rods over a frictionless cylinder; equilibrium and rotational stability'),
(VII+';'+I,3,3,'Electron helix trajectories and screen intensity/extent in a uniform magnetic field')],
2870:[
(IV,1,1,'Counterflow heat exchanger; mass flux and heat balance'),
(I,1,1,'Car braking uphill and downhill; gravitational work and energy'),
(I,1,1,'Cannonball altitude corrected for inverse-square gravitational potential'),
(I,1,1,'Sliding/spinning cylinder reversing translation before pure rolling; angular momentum and friction'),
(XII,1,2,'Long-time radon activity from a uranium decay chain and half-lives'),
(X,2,2,'Magnification by a glass hemisphere; paraxial refraction'),
(VI,2,2,'Switching a circuit containing an explicitly defined constant-current source'),
(X,3,3,'Three mutually perpendicular mirrors; constructing the reflected orientation'),
(I,3,3,'Reconstructing true wind from piecewise boat-relative measurements'),
(I+';'+VI,3,3,'Charged balls linked as a triangle; released constraint, momentum and electrostatic energy')],
2872:[
(I+';'+III,1,1,'Helium-balloon lift and ideal-gas density'),
(X,1,1,'Additional lens creating a specified illuminated screen disk'),
(I+';'+III,1,1,'Floating hollow cube with a bottom leak; buoyancy, hydrostatic pressure and trapped gas'),
(VI,2,2,'Three-terminal resistor black box and ideal ammeter; reconstructing circuit'),
(I,2,2,'Thrown ball inside a rotating cylindrical station; inertial-frame projectile geometry'),
(I+';'+VI,2,2,'Charged particle encountering an explicitly defined moving electrostatic potential step'),
(X,2,2,'Recovering lens center, axis and focus from a circle and elliptical image'),
(I+';'+II,2,2,'Falling box and suspended spring mass; rebound condition and contact duration'),
(I,3,3,'Slowly pulling an unequal-arm dumbbell against Coulomb friction'),
(VI,3,3,'Two thyristors in a switched circuit; current-time behavior from the supplied complete I-V graph')]
}
experiments={
2867:[('E1',4,'KLOTSI MASS',I,'Inferring a wooden block mass from repeatable rubber-band launch and stopping distances'),('E2',4,'MUST KAST',VI,'Identifying resistor, battery internal resistance and capacitance from three-terminal measurements')],
2868:[('E1',3,'RUUMALAD',I,'Measuring density ratio using lever balance and buoyancy'),('E2',3,'ÕHUPALL 2',I+';'+III,'Measuring balloon overpressure through known load and contact area')],
2870:[('E1',4,'TIIVIK',I+';'+VI,'Measuring motor power versus fan frequency and fitting the explicitly supplied power law'),('E2',4,'KILE JA PABER',I,'Measuring film/paper friction using water pressure and submerged load')],
2872:[('E1',4,'KAKS PALLI',I+';'+II,'Measuring fractional collision energy loss with suspended balls'),('E2',4,'VALGUSDIOOD',VI,'Measuring LED I-V curve with resistor voltage readings and a capacitor supply')]
}
out=[]
for fid,spec in specs.items():
 us=c.execute('select * from units where source_file_id=? and derived_from_whole_paper=0 order by source_problem_id',(fid,)).fetchall();assert len(us)==10
 for u,(dom,a,b,physics) in zip(us,spec):
  assert u['decision'] is None
  supplied='Explicitly supplied model/characteristic' if (fid,u['problem_number']) in [(2867,'5'),(2867,'8'),(2872,'6'),(2872,'10')] else ''
  reason='The dominant work is '+physics[0].lower()+physics[1:]+'. Ordinary general physics, syllabus knowledge and the stated data/models suffice.'
  if fid==2872 and u['problem_number']=='10':reason='The complete nonlinear I-V characteristic is supplied; load-line and Kirchhoff reasoning suffice without prior thyristor/semiconductor theory.'
  if fid==2872 and u['problem_number']=='6':reason='The moving potential step is fully defined. A Galilean change of frame and electrostatic/mechanical energy determine transmission or reflection; no plasma shock theory is needed.'
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=dom,required_physics=physics,external_physics_if_any=supplied,decision_reason=reason,page_start=a,page_end=b,format='theory',visual_inspection_used=1,solution_used=0,boundary_status='content_boundary_verified',evidence='Read all source pages in embedded text and visually inspected all page renders, including circuit connectivity, geometric diagrams, jet/pressure curves and thyristor characteristic. All internal lettered tasks retained together.'))
 for no,page,title,dom,physics in experiments[fid]:
  u=dict(us[0]);uid='derived::'+u['source_sha256'][:16]+'::embedded::'+no
  assert not c.execute('select 1 from units where screening_unit_id=?',(uid,)).fetchone()
  fields={k:u[k] for k in ['competition','competition_slug','competition_category','year','source_file','source_file_id','source_sha256','source_url']}
  fields.update(screening_unit_id=uid,source_problem_id=None,derived_from_whole_paper=1,round_or_section='Experimental',format='experimental',problem_number=no,problem_title=title,title_provenance='official',page_start=page,page_end=page,boundary_status='content_boundary_verified',location_json=json.dumps({'printed_label':no,'boundary_note':'Separate printed experiment absent from raw individual theory inventory; retain all measurement tasks together.'}))
  c.execute('insert into units('+','.join(fields)+') values ('+','.join('?' for _ in fields)+')',list(fields.values()))
  c.execute('insert into unit_files select ?,file_id,document_id,role from unit_files where screening_unit_id=?',(uid,us[0]['screening_unit_id']))
  evidence='Complete experimental statement and actual source page inspected; full-exam solution prints matching '+no+' '+title+' and its measurement method. Original raw paper listed only theory 1-10.'
  c.execute('insert into embedded_unit_discovery values (?,?,?,?)',(uid,fid,evidence,w.now()))
  out.append(dict(screening_unit_id=uid,decision='KEEP',confidence='high',primary_spho_domains=dom,required_physics=physics,external_physics_if_any='',decision_reason='The essential physics is ordinary force/energy/circuit reasoning; measurement design and graph fitting are explicitly eligible under the calibrated scope.',page_start=page,page_end=page,format='experimental',visual_inspection_used=1,solution_used=1,boundary_status='content_boundary_verified',evidence=evidence))
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=12,evidence=?,checked_at=? where file_id=?",('All source pages read: theory 1-10 and two printed experiments E1/E2. Administrative and repeated drawing pages are not new problems.',w.now(),fid))
c.commit();assert len(out)==48
p=w.ROOT/'reviews/resume_efo_2015_2018_48.json';w.writejson(p,out);w.decisions(p)
print('Saved',len(out),'actual-content decisions, including eight new experiments.')

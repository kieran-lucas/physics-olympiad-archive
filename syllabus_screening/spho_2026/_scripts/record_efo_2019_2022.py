"""Explicit reviews after reading all four papers and inspecting every page.

Also preserve eight printed experiments missing from the acquisition logical rows.
No physics decision is inferred by this persistence script.
"""
import json
import workflow as w
c=w.connect()
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';X='X_wave_optics';XI='XI_quantum_light'
specs={
2859:[
(I,1,1,'Headwind changes discus lift and drag; qualitative force diagram','Ordinary force and relative-air-speed reasoning suffice; the solution confirms a qualitative argument, without requiring continuum flow equations.'),
(I,1,1,'Travel-time optimization across snow and along roads','The required knowledge is constant-speed kinematics and geometric/calculus optimization.'),
(VI,1,1,'Resistance of a thin cylindrical conducting shell between opposite terminals','Ohm law, resistivity and parallel current paths control the calculation.'),
(X,1,5,'Three-lens ray construction with common focal-point geometry','Lens imaging and elementary ray geometry suffice; the drawing template is on page 5.'),
(I,2,2,'Bicycle motor torque, power and speed on a slope','Force balance and mechanical power determine the motion.'),
(III+';'+IV,2,2,'Airgun nitrogen cooling during adiabatic expansion','Ideal-gas thermodynamics is central and the adiabatic pressure-volume law is explicitly supplied.'),
(I,2,4,'Rainfall and reservoir drainage capacity from a cumulative rainfall graph','Volume conservation and graph slopes/integration suffice; the rainfall graph is on page 4.'),
(I,2,2,'Time-dependent scale force during a falling water stream','Momentum flux, free fall and weight account for the scale reading.'),
(IV+';'+XI,3,3,'Thermal radiation equilibrium of a black satellite above an emitting Earth plane','The geometry and emissivity model are supplied; radiation balance uses Stefan-Boltzmann physics.'),
(VI,3,3,'Force on a point charge from electrostatically induced plate charge','Electrostatic induction, field forces and controlled geometric approximations are the core.')],
2860:[
(I,1,1,'Horizontal projectile intercepted by an approaching person','Relative velocity and Newtonian projectile motion suffice.'),
(III+';'+IV,1,1,'Bottle pressure changes and heat-loss power during cooling','Ideal-gas pressure-temperature changes and heat capacity determine the power.'),
(X,1,1,'Point-source lens image and uniform illumination of a screen','Paraxial lens geometry and beam cross sections control the answer.'),
(I,2,2,'Minimum travel time with different acceleration/braking friction sections','Newtonian friction and time optimization are entirely in scope.'),
(VI,2,2,'Instantaneous and steady-state circuit power after capacitor switching','The inspected circuit requires capacitor continuity and ordinary resistor-network laws.'),
(I,2,2,'Apparent weight and friction of a body on a rotating sphere','Gravity, centripetal acceleration and static friction suffice.'),
(I+';'+VI,2,2,'Charge ratios for straight-line motion of three Coulomb-interacting particles','Coulomb forces, symmetry and Newtonian center-of-mass motion control the reasoning.'),
(I+';'+III,3,3,'Initial acceleration of water in an inverted open cylinder','Hydrostatic pressure, supplied vapor-pressure data and Newton force balance suffice.'),
(X,3,3,'Liquid layers over a concave mirror and coincident object-image positions','Refraction and spherical-mirror imaging are ordinary general-physics foundations.'),
(VII+';'+I,3,3,'Electron trajectory around a straight current-carrying wire','Magnetic field of a wire, Lorentz force and trajectory geometry are explicitly syllabus-aligned.')],
2861:[
(X,1,1,'Refractive index of a glass sphere focusing a paraxial incident beam','Snell law and small-angle geometry suffice.'),
(I,1,1,'Pressure in a rotating bag modeled as a liquid','The liquid model is stated; centripetal acceleration and pressure force balance are ordinary foundations.'),
(VI,1,1,'Copper pipe as a high-current meter shunt','Resistivity, cylindrical geometry and parallel circuit currents suffice.'),
(I+';'+II,2,2,'Spring-supported rider resonating with a sinusoidal road profile','The given mechanical model requires oscillator frequency and kinematic excitation.'),
(VI,2,2,'Equivalent resistance of intersecting wires on a spherical network','Symmetry and Kirchhoff circuit reasoning are sufficient.'),
(I,2,2,'Maximum projectile range from an elevated sloped surface','Projectile motion and mathematical optimization are in scope.'),
(I,3,3,'Hinged sticks gripping and lifting a cylinder','Torque balance and Coulomb static friction determine the lifting condition.'),
(X,3,5,'Reconstructing two plane mirrors from incoming and outgoing light rays','Reflection geometry is central; the required full ray template is on page 5.'),
(I+';'+III+';'+IV,3,4,'Two connected elastic balloons in vacuum after thermal equilibration','The large-strain stress law is explicitly given; pressure-force balance, ideal gas and thermal reasoning suffice.'),
(VI,4,4,'Resistance between corners versus side midpoints of a conducting square','Ohmic conduction, current-field symmetry and superposition are ordinary electromagnetism.')],
2864:[
(I,1,1,'Opposing cars braking uniformly until meeting at rest','Relative kinematics and constant acceleration are sufficient.'),
(I+';'+III+';'+IV,1,1,'Steam pressure and minimum sauna-door hinge friction torque','Ideal-gas pressure, ordinary phase change and torque balance are the dominant physics.'),
(I,1,6,'Reconstructing airplane course from a distance-time graph','Uniform-motion geometry and graph interpretation suffice; graph copies are on pages 5 and 6.'),
(I,2,2,'Plate transitioning between conveyor belts with different speeds and friction','Friction-force balance and transit kinematics suffice.'),
(I,2,2,'Curling collision with prescribed energy loss followed by frictional stopping','Momentum, energy loss and sliding friction are the central physics.'),
(VII+';'+I,2,2,'Charged-particle trajectory with magnetic curvature and two elastic wall reflections','Lorentz force, circular motion and reflection geometry are within scope.'),
(VI,3,3,'Currents in a three-square resistor network','The inspected circuit uses standard Kirchhoff and Ohm laws.'),
(X+';'+I,3,3,'Minimum apparent image speed of a fly moving past a lens','Ordinary lens imaging and differentiation/optimization determine the result.'),
(VI,3,3,'Induced charge of a grounded conducting sphere near a charged ring','Electrostatic potential and conductor equilibrium are the core knowledge.'),
(I+';'+VI,3,3,'Closed charged-particle orbit in an electric field rotating discretely by 90 degrees','Piecewise constant acceleration and Coulomb force suffice.')]
}
experiments={
2859:[('E1',3,3,'MUST KAST',VI,'Determining two diode/resistor black-box branches by calibrated voltage and current measurements','Diode nonlinearity and reverse blocking are given; resistor and measurement reasoning require no semiconductor band theory.'),('E2',3,3,'PINGPONG',I,'Measuring ball/wood friction with a tethered ping-pong ball and rulers','Static force/torque equilibrium, geometry and experimental design are in scope.')],
2860:[('E1',3,3,'MAHLAKARP',I,'Measuring juice-carton friction without using an inclined plane','Sliding/tipping balance and measurement design are ordinary mechanics.'),('E2',3,4,'MAJAPIDAMISPABER',I,'Estimating paper-fiber spacing through capillary rise and a supplied surface-force relation','The statement supplies F=sigma*l; hydrostatics, force balance and estimation suffice without specialized porous-flow theory.')],
2861:[('E1',4,4,'MASSIDE SUHE',I,'Measuring two masses ratio using string equilibrium, without a balance','Newton force balance and measured angles suffice; the internal method constraints remain one experiment.'),('E2',4,4,'MUST KAST',VI,'Identifying a four-resistor black-box network by ohmmeter measurements and shorting terminals','Circuit topology, Ohm law and parameter estimation are in scope.')],
2864:[('E1',4,4,'KUMERPEEGEL',X,'Measuring convex-mirror focal length with only a ruler and mirror','Geometrical imaging, parallax control and measurement design suffice.'),('E2',4,4,'MUST KAST',VI,'Determining three resistances and an EMF in a three-terminal black box','Kirchhoff laws and multimeter parameter estimation are sufficient.')]
}
c.execute('''create table if not exists embedded_unit_discovery(screening_unit_id text primary key references units(screening_unit_id),source_file_id integer,evidence text,discovered_at text)''')
out=[]
for fid,spec in specs.items():
 direct=c.execute('select * from units where source_file_id=? and derived_from_whole_paper=0 order by source_problem_id',(fid,)).fetchall();assert len(direct)==10
 for u,(domains,a,b,physics,reason) in zip(direct,spec):
  assert u['decision'] is None
  loc={'top_level_label':u['problem_number'],'statement_page':a,'inclusive_span_contains_other_questions':b>a,'boundary_note':'One printed theory problem; all internal parts retained. Later drawing pages are supplemental copies, not additional problems.'}
  out.append(dict(screening_unit_id=u['screening_unit_id'],decision='KEEP',confidence='high',primary_spho_domains=domains,required_physics=physics,external_physics_if_any='Supplied finite-strain elastic stress law' if fid==2861 and u['problem_number']=='9' else '',decision_reason=reason,page_start=a,page_end=b,format='theory',visual_inspection_used=1,solution_used=int(fid==2859 and u['problem_number']=='1'),boundary_status='content_boundary_verified',location_json=json.dumps(loc),evidence='Read the complete Estonian statement in cached PDF text and inspected all pages, diagrams and later graph/templates in rendered source pages. '+('Official solution page 1 confirms qualitative lift/drag reasoning.' if fid==2859 and u['problem_number']=='1' else '')))
 for no,a,b,title,domains,physics,reason in experiments[fid]:
  template=dict(direct[0]);uid='derived::'+template['source_sha256'][:16]+'::embedded::'+no
  assert not c.execute('select 1 from units where screening_unit_id=?',(uid,)).fetchone()
  fields={k:template[k] for k in ['competition','competition_slug','competition_category','year','source_file','source_file_id','source_sha256','source_url']}
  fields.update(screening_unit_id=uid,source_problem_id=None,derived_from_whole_paper=1,round_or_section='Experimental',format='experimental',problem_number=no,problem_title=title,title_provenance='official',page_start=a,page_end=b,boundary_status='content_boundary_verified',location_json=json.dumps({'printed_label':no,'boundary_note':'Separate printed experiment missing from the raw logical inventory; all internal measurement tasks stay together.'}))
  c.execute('insert into units('+','.join(fields)+') values ('+','.join('?' for _ in fields)+')',list(fields.values()))
  # Full-exam solutions explicitly print matching E1/E2; inspected those labels and content.
  c.execute('insert into unit_files select ?,file_id,document_id,role from unit_files where screening_unit_id=?',(uid,direct[0]['screening_unit_id']))
  evidence='Printed '+no+' '+title+' inspected in complete source paper and page renders. Full-exam solution explicitly prints this same experimental label/title; association verified. Not present among the ten raw theory rows.'
  c.execute('insert into embedded_unit_discovery values (?,?,?,?)',(uid,fid,evidence,w.now()))
  out.append(dict(screening_unit_id=uid,decision='KEEP',confidence='high',primary_spho_domains=domains,required_physics=physics,external_physics_if_any='Supplied surface-tension force law' if fid==2860 and no=='E2' else 'Diode behavior explicitly supplied' if fid==2859 and no=='E1' else '',decision_reason=reason,page_start=a,page_end=b,format='experimental',visual_inspection_used=1,solution_used=1,evidence=evidence,boundary_status='content_boundary_verified'))
c.commit();assert len(out)==48
p=w.ROOT/'reviews/resume_efo_2019_2022_48.json';w.writejson(p,out);w.decisions(p)
print('Saved 40 direct theory decisions and 8 newly discovered experiments.')

"""Explicit reviews of the remaining three BAUPC papers, including missing figures."""
import sys,subprocess
import workflow as w
I='I_force_motion';II='II_oscillations_waves';III='III_ideal_gas';IV='IV_thermodynamics';VI='VI_electric_field';VII='VII_magnetic_field';IX='IX_em_oscillations_waves'
papers=[
 (6390,3172,1997,[
 (1,[1,1],I+';'+VI,'Buoyancy/volume displacement and Coulomb energy','Both numbered-1 parts are ordinary general physics: melting floating ice and slow charged-particle separation.'),
 (2,[1,1],I+';'+VII,'Lorentz force and explicitly supplied linear drag','The spiral limit follows Newtonian charged-particle motion; damping is defined in the statement.'),
 (3,[2,2],I,'Rigid-body energy, moving centre of mass and loss of wall contact','The falling frictionless stick uses force/torque and mechanical-energy conservation.'),
 (4,[2,2],I,'Elastic impacts, rigid-body inertia and geometric mass limits','The successive sticks use supplied inertia and elastic-collision assumptions; the limiting sequence is mathematical.'),
 (5,[3,3],I,'Circular-motion force balance and rolling angular momentum','Both cone particle and rolling ring are within force/motion and rigid-body dynamics.'),
 (6,[4,4],I,'Repeated elastic collisions and conservation of energy','The heavy block/light particle approach uses collision momentum and the explicitly permitted small mass-ratio approximation.')]),
 (6391,3174,1996,[
 (1,[1,1],I,'Elastic collisions, gravitational energy and mass-ratio limits','The whole stacked-ball problem is completely specified in words despite absent decorative diagrams.'),
 (2,[2,2],VI+';'+I,'Charged-ring potential symmetry and buoyancy/hydrostatic forces','Both ring-field proof and immersed-balloon argument are ordinary electrostatics/statics; text specifies their geometries.'),
 (3,[3,3],VI,'Ohm law and symmetry of a cube resistor network','Circuit physics is in scope, but the referenced labelled cube drawing is absent; the A-C terminal relationship cannot be established from the statement with confidence.'),
 (4,[4,4],I,'Elastic projectile reflection, momentum transfer and surface slope','The rings and general symmetric curve are specified in text; momentum/ballistic geometry establishes the method, also confirmed by solution pages 3-4.'),
 (5,[5,5],I+';'+II,'Rocking rigid-body energy and inelastic pivot switching','The two-stick geometry and collision assumptions are fully worded; the infinite sequence is a calculus challenge, not external physics.'),
 (6,[6,6],I,'Rolling dynamics on a uniformly stretching moving support','The supplied limiting masses, inertia and band kinematics are enough; no rubber constitutive theory is needed.')]),
 (6392,3177,1995,[
 (1,[1,1],I,'Projectile energy and nonpenetration geometry','Both touching/avoiding the cylindrical pipe are Newtonian trajectory optimizations.'),
 (2,[1,1],III+';'+IV+';'+VII+';'+I,'Ideal-gas free expansion, current magnetic fields and torque','All three internal short-answer parts are in-scope general physics; do not split them into independent units.'),
 (3,[1,1],VI,'Ohmic conduction, spherical current flow and resistance integration','The earth-return telegraph resistance is ordinary electrical conduction in a stated uniform resistivity model.'),
 (4,[1,2],IX,'Forced response of an infinite LC ladder','The actual statement lacks the referenced circuit drawing. Solution pages 3-4 show an in-scope impedance recurrence, but the intended physical connections/terminals are not displayed; exclude from the main set pending source-geometry clarification.'),
 (5,[2,2],I,'Tension equilibrium and geometry on a frictionless cone','Fixed/variable lasso loops require only force balance and geometric unfolding; all assumptions are stated.'),
 (6,[2,3],I,'Rigid-body rolling, inelastic impacts and terminal energy balance','The spoke-wheel model, concentrated mass and no-bounce law are explicitly supplied; ordinary rotation and energy determine the whole task.')])]
for pid,fid,year,spec in papers:
    src=w.connect().execute('select * from containers where source_problem_id=?',(pid,)).fetchone()
    b=w.ROOT/f'reviews/baupc_{year}_boundaries.json'
    w.writejson(b,[{'source_problem_id':pid,'boundary_evidence':f'Visually read every content page of BAUPC {year}, verified six explicit numbered 1..6 units and retained all internal parts. Papers have no usable embedded text. Referenced missing drawings in 1995/1996 are recorded rather than invented.','units':[dict(number=str(n),page_start=ps[0],page_end=ps[1],format='mixed' if year==1995 and n==2 else 'theory',location={'top_level_label':str(n),'all_internal_parts_retained':True}) for n,ps,_,_,_ in spec]}]);w.derive(b)
    rows=[]
    for n,ps,dom,phys,reason in spec:
        borderline=(year,n) in [(1996,3),(1995,4)]
        solution=(year,n) in [(1996,3),(1996,4),(1995,4)]
        rows.append([f'derived::{src["source_sha256"][:16]}::{pid}::{n}','BORDERLINE' if borderline else 'KEEP',dom,phys,reason,
          f'Complete scanned BAUPC {year} Problem {n} text visually read on file {fid} page(s) {ps[0]}-{ps[1]}; referenced figures checked for actual presence. '+('Related solution page(s) were visually inspected.' if solution else ''),ps,'mixed' if year==1995 and n==2 else 'theory',1,int(solution),'medium' if borderline else 'high','No external physics established; source geometry incomplete.' if borderline else ''])
    p=w.ROOT/f'reviews/baupc_{year}.json';w.writejson(p,{'rows':rows});subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(p)],check=True)

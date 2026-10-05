"""Explicit content reviews of BAUPC 2004 and scanned IPhO 1969 statements."""
import sys, subprocess
import workflow as w
I='I_force_motion'; IV='IV_thermodynamics';VI='VI_electric_field';IX='IX_em_oscillations_waves';X='X_wave_optics'
data=[
 (1,1,I,'Variable-mass momentum balance and angular momentum','Both snowfall/sled strategies and arm swinging to avoid falling use ordinary momentum and torque, despite different contexts.'),
 (2,1,I,'Distributed weight, tension and limiting static friction','The hanging rope on inclined platforms is a Newtonian equilibrium/optimization problem; its catenary can be derived from force balance.'),
 (3,2,IX,'Isotropic radiation fraction and solid-angle geometry','The square detector requires only the supplied isotropic-emission assumption and geometrical radiation collection, not detector microphysics.'),
 (4,2,IX,'Forced RLC circuit response and complex impedance','The tetrahedral circuit is ordinary electromagnetic oscillations/network analysis with stated frequency and component relations.'),
 (5,3,I,'Conservation of momentum/energy and loss of contact','The sliding particle and moving hemisphere use Newtonian mechanics; unequal masses change the algebra, not the scope.'),
 (6,3,I,'Rolling rigid-body dynamics, constraints and recursion','All cylinders have supplied inertia; the infinite stack adds mathematics to ordinary force/torque equations.')]
items=[dict(number=str(n),page_start=p,page_end=p,format='theory',location={'top_level_label':str(n),'within_page_order':1 if n%2 else 2}) for n,p,_,_,_ in data]
w.writejson(w.ROOT/'reviews/baupc_2004_boundaries.json',[{'source_problem_id':6383,'boundary_evidence':'Read and visually inspected all three pages. Header explicitly states six questions; six numbered 1..6 starts verified. Retain 1(a,b), 3(a,b,c), and 5 general/equal-mass cases inside their whole top-level units.','units':items}]);w.derive(w.ROOT/'reviews/baupc_2004_boundaries.json')
rows=[[f'derived::3718f60c0e82ec7a::6383::{n}','KEEP',dom,physics,reason,
 f'BAUPC 2004 question {n}, complete statement and diagram on page {p} read and visually inspected.',[p,p],'theory',1,0,'high',''] for n,p,dom,physics,reason in data]
w.writejson(w.ROOT/'reviews/baupc_2004.json',{'rows':rows})
subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(w.ROOT/'reviews/baupc_2004.json')],check=True)
rows=[
 [248,'KEEP',I,'Newton second law, tension and relative acceleration','Both moving-cart equilibrium and the fixed-cart release require ordinary Newtonian constraints.', 'Scanned file 672 page 1 visually read in full; one Problem 1 with internal 1(a,b) and 2(a,b), not four independent units.',[1,1],'theory',1,0,'high',''],
 [249,'KEEP',IV,'Calorimetry, sensible heat and melting/freezing energy','The equilibrium regimes of copper, water and ice use energy conservation and supplied heat capacities/latent heat.', 'Scanned file 673 page 1 visually read. Statement begins at Problem 2 below a tail of the preceding solution; both general and numerical parts retained.',[1,1],'theory',1,0,'high',''],
 [250,'KEEP',VI+';'+I,'Axial electric field of a uniformly charged ring and force balance','The suspended charge requires Coulomb superposition, gravity and string geometry; the adjacent solution confirms this elementary method.', 'Scanned file 675 page 1 visually read, including ring geometry and supplied charges. Single Problem 3; displayed solution method also inspected.',[1,1],'theory',1,1,'high',''],
 [251,'KEEP',X+';'+IV,'Thin-film interference, reflection phase and linear thermal expansion','The two reflected beams and supplied expansion coefficient require wave optics and ordinary thermal expansion.', 'Scanned file 678 pages 1-2 visually read. Problem 4 starts near bottom of page 1 after Problem 3 solution and continues on page 2. Actual task is calculation, not an experimental procedure.',[1,2],'theory',1,0,'high','']]
w.writejson(w.ROOT/'reviews/ipho_1969_scans.json',{'rows':rows,'boundary_note':'The scanned physical page can include unrelated preceding solution text. Select the explicit Problem label, not all text on the page.'})
subprocess.run([sys.executable,str(w.ROOT/'_scripts/save_batch.py'),str(w.ROOT/'reviews/ipho_1969_scans.json')],check=True)
print([tuple(x) for x in w.connect().execute('select id,raw_title,problem_type,session,section from source_problems where id between 248 and 251')])

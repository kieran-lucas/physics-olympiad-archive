"""Verified physical-question aliases: preserve all provenance and decisions."""
import json
import workflow as w
c=w.connect()
c.execute("""create table if not exists unit_equivalences(alias_unit_id text primary key references units(screening_unit_id), canonical_unit_id text not null references units(screening_unit_id),source_sha256 text not null,evidence text not null,verified_at text not null,check(alias_unit_id!=canonical_unit_id))""")
pairs=[('raw::1111','derived::710cea32f2ecf0cc::1679::1'),('raw::1112','derived::710cea32f2ecf0cc::1679::2'),('raw::1113','derived::710cea32f2ecf0cc::1679::3'),('raw::1114','derived::730b29070b01dfdf::1680::E')]
out=[]
for canonical,alias in pairs:
 u=dict(c.execute('select * from units where screening_unit_id=?',(canonical,)).fetchone()); prior=dict(c.execute('select * from units where screening_unit_id=?',(alias,)).fetchone())
 assert u['source_sha256']==prior['source_sha256']
 evidence='Entire US 2022 camp statement read again once per physical PDF, including all six theory/four experiment pages and diagrams. Direct USAPhO and derived USA TST records point to the same printed top-level question in identical SHA-256 bytes; provenance records retained. Internal parts remain together.'
 if u['decision'] is None:
  r={k:prior[k] for k in ['decision','confidence','primary_spho_domains','required_physics','external_physics_if_any','decision_reason','format','page_start','page_end','solution_used']}
  r.update(screening_unit_id=canonical,visual_inspection_used=1,boundary_status='content_boundary_verified',evidence=evidence)
  if canonical=='raw::1114':r['problem_number']='4';r['format']='experimental'
  out.append(r)
 c.execute('insert or replace into unit_equivalences values (?,?,?,?,?)',(alias,canonical,u['source_sha256'],evidence,w.now()))
for fid,n in [(1931,3),(1934,1)]:
 c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=?,evidence=?,checked_at=? where file_id=?",(n,'Complete printed paper inspected. USAPhO/USA TST provenance aliases refer to identical physical questions; count printed questions once, retain all source rows.',w.now(),fid))
c.commit()
p=w.ROOT/'reviews/resume_us2022_direct_aliases_4.json';w.writejson(p,out)
if out:w.decisions(p)
rows=[dict(r) for r in c.execute('select * from unit_equivalences')]
w.csvout(w.ROOT/'screening_unit_equivalences.csv',rows)
print('Saved',len(out),'new content decisions and',len(rows),'verified physical-question aliases.')

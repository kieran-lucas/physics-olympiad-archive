"""Preserve source-linked lab simulator and its published source; never execute."""
import os,struct,zipfile,json
import workflow as w
c=w.connect()
base='https://github.com/USPhysicsTeam/2022-future-circular-collider'
items=[('us2022_collision_2022-final_windows.exe',base+'/releases/download/2022-final/collision-black-box-windows.exe','exe'),('us2022_collision_2022-final_source.zip','https://api.github.com/repos/USPhysicsTeam/2022-future-circular-collider/zipball/2022-final','zip')]
for name,url,kind in items:
 p=w.ROOT/'references'/name;part=p.with_name(p.name+'.part');q=p if p.exists() else part
 if kind=='zip':
  assert zipfile.is_zipfile(q)
  with zipfile.ZipFile(q) as z:
   assert z.testzip() is None
   print('Source archive',len(z.infolist()),'entries; README:',z.read(next(n for n in z.namelist() if n.endswith('/README.md'))).decode()[:600])
 else:
  b=q.read_bytes();assert len(b)==999424 and b[:2]==b'MZ'
  offset=struct.unpack('<I',b[0x3c:0x40])[0];assert b[offset:offset+4]==b'PE\x00\x00'
 if not p.exists():os.replace(part,p)
 rid=name.rsplit('.',1)[0]
 purpose='Essential simulated experiment for US 2022 camp problem 4. Statement explicitly links the USPhysicsTeam repository; published 2022-final release supplies wall/disk collision measurements. Binary retained without execution; Rust source archive retained for reproducibility.'
 c.execute('insert or replace into screening_references values (?,?,?,?,?,?,?,?,?)',(rid,'raw::1114',url,p.relative_to(w.ROOT).as_posix(),w.digest(p),p.stat().st_size,None,purpose,w.now()))
 w.writejson(p.with_name(p.name+'.provenance.json'),{'reference_id':rid,'statement_file_id':1934,'statement_repository_url':base,'release_tag':'2022-final','release_published_at':'2022-09-14T21:41:05Z','url':url,'sha256':w.digest(p),'byte_size':p.stat().st_size,'validation':'ZIP CRC passes' if kind=='zip' else 'MZ/PE signature and release asset byte size match','executable_run':False})
c.execute("update units set source_quality_notes=? where screening_unit_id in ('raw::1114','derived::730b29070b01dfdf::1680::E')",('Essential simulator acquired from the repository explicitly linked in the statement: 2022-final Windows binary and Rust source archive, validated and preserved outside raw; not executed.',))
c.commit();print('Registered two essential source-linked supplements.')

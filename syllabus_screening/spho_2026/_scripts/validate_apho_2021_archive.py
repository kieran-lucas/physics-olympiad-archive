"""Static validation only of the already acquired essential experiment software."""
import hashlib,random,re,zipfile
import workflow as w
c=w.connect();f=c.execute('select * from source_files where id=1034').fetchone()
p=w.RAW/f['local_path'];assert w.digest(p)==f['sha256']
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    members=[dict(path=i.filename,byte_size=i.file_size,sha256=hashlib.sha256(z.read(i)).hexdigest(),encrypted=bool(i.flag_bits&1)) for i in z.infolist() if not i.is_dir()]
    dll=next(i for i in z.namelist() if i.endswith('Managed/Assembly-CSharp.dll'))
    b=z.read(dll)
    strings=re.findall(rb'[ -~]{5,}',b)+[s.decode('utf-16le',errors='replace').encode() for s in re.findall(rb'(?:[ -~]\x00){5,}',b)]
    matching=sorted(set(s.decode(errors='replace') for s in strings if re.search(rb'cantilever|diffraction|experiment|laser|beam|1A|2A|2E',s,re.I)))
    appinfo={i:z.read(i).decode(errors='replace') for i in z.namelist() if i.endswith('app.info')}
    exe=next(i for i in z.namelist() if i.endswith('/APHO.exe'))
    assert z.read(exe).startswith(b'MZ') and b.startswith(b'MZ')
w.writejson(w.ROOT/'reviews/shutdown_apho_2021_software_static_validation.json',dict(checked_at=w.now(),source_file_id=1034,document_id=1090,sha256=f['sha256'],byte_size=p.stat().st_size,source_path=f['local_path'],source_url='https://olimpicos.net/files/apho/APhO_2021_ExperimentData.zip',crc_ok=True,members=members,app_info=appinfo,managed_code_matching_strings=matching,validation_status='SHA and ZIP CRC verified; Windows Unity executable and complete associated data/managed libraries preserved. Static structural check only; executable not launched, no runtime or experiment data validation claimed.',relationship_evidence='2021 general instructions1030 explicitly require APHO.exe; both actual experiment statements1044/1047 show the same APHO simulator interface with programs1A-1D and2A-2E. Existing acquisition year/source relationship1090 matches the printed instructions.',theory_qc=random.Random(2026100435).sample(['raw::328','raw::329','raw::330'],1),experiment_qc=random.Random(2026100436).sample(['raw::331','raw::332'],1)))
print(appinfo);print(matching[:65]);print('QC',random.Random(2026100435).sample(['raw::328','raw::329','raw::330'],1),random.Random(2026100436).sample(['raw::331','raw::332'],1))

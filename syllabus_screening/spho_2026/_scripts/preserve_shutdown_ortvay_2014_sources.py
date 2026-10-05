import csv,io,math,urllib.request,urllib.parse
import workflow as w
c=w.connect();u={int(r['problem_number']):r for r in c.execute('select * from units where source_file_id=3126')}
base='https://skyserver.sdss.org/dr7/en/tools/search/'
query='SELECT TOP 100 p.l, p.b, s.z FROM SpecObj s INNER JOIN Star p ON p.objID = s.bestObjID WHERE s.SpecClass = 1'
url=base+'x_sql.asp?'+urllib.parse.urlencode({'cmd':query,'format':'csv'})
with urllib.request.urlopen(url,timeout=30) as r: payload=r.read(); final=r.url
rows=list(csv.DictReader(io.StringIO(payload.decode('utf-8-sig'))));assert len(rows)==100
assert all(all(math.isfinite(float(row[k])) for k in ('l','b','z')) and 0<=float(row['l'])<=360 and -90<=float(row['b'])<=90 for row in rows)
p=w.ROOT/'references/ortvay_2014_q35_DR7_statement_sample_100.csv'
with open(p.with_suffix('.csv.part'),'wb') as f:f.write(payload);f.flush();w.os.fsync(f.fileno())
p.with_suffix('.csv.part').replace(p)
ref=dict(reference_id='ortvay_2014_q35_DR7_statement_sample_100',screening_unit_id=u[35]['screening_unit_id'],url=url,local_path=p.relative_to(w.ROOT).as_posix(),sha256=w.digest(p),byte_size=p.stat().st_size,page_count=None,purpose='Original statement TOP 100 example executed against live official DR7 endpoint; 100 finite Galactic coordinates/redshifts validated. This unordered illustrative sample is not a complete or representative exercise dataset; contestant-selected larger DR7 query remains required.',acquired_at=w.now())
c.execute('insert into screening_references values (?,?,?,?,?,?,?,?,?)',tuple(ref.values()));c.commit()
w.writejson(p.with_suffix('.csv.provenance.json'),{**ref,'original_statement_portal':'http://skyserver.sdss3.org/','verified_DR7_portal':base+'sql.asp','final_url':final,'query':query,'validation_status':'100 records; exact columns l,b,z; finite numbers; angular ranges checked','dataset_limitations':'Unordered TOP 100 example only. Do not infer full-sky coverage or survey selection from it. Source statement deliberately requires choosing/querying the larger live database.'})
availability={'checked_at':w.now(),'statement_file_id':3126,'q34':{'url':'http://ortvay.elte.hu/2014/abrak/sandstorm.ps','status':'essential_image_unavailable','evidence':'HTTP and HTTPS both return 404; original /2014/ index lists E14/H14 statements/rules/results only, no abrak directory. No image embedded on physical PDF p7. Exact-URL Internet Archive CDX attempt returned 503; no replacement image invented.','retry_url':'https://web.archive.org/cdx/search/cdx?url=ortvay.elte.hu%2F2014%2Fabrak%2Fsandstorm.ps&output=json'},'q35':{'status':'original_DR7_service_verified','original_portal':'http://skyserver.sdss3.org/','verified_portal':base+'sql.asp','data_reference_id':ref['reference_id'],'source_relation':'Official original survey DR7 archive, same schema/version named in the source. No other release substituted.'}}
w.writejson(w.ROOT/'reviews/shutdown_ortvay_2014_external_availability.json',availability)
print('Preserved validated DR7 example and explicit missing-image evidence.')

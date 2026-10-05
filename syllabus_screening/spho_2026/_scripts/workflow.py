"""Read-only acquisition access; cache, record human/model content reviews, export.

No automated physics classifier is implemented here. Decisions are supplied as
explicit reviewed records. Source PDFs are never edited, cropped or rewritten.
"""
import argparse, collections, csv, datetime, gzip, hashlib, json, os, sqlite3, sys
from pathlib import Path
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parents[3]
RAW = REPO / 'olimpicos_physics_corpus'
ROOT = REPO / 'syllabus_screening' / 'spho_2026'
CUR = REPO / 'curated' / 'spho_2026'

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()
def connect():
    c=sqlite3.connect(ROOT/'screening.sqlite',timeout=60); c.row_factory=sqlite3.Row
    c.execute('pragma foreign_keys=on'); return c
def rawconnect():
    c=sqlite3.connect(RAW.joinpath('manifest.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
    c.row_factory=sqlite3.Row; return c
def writejson(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.part')
    with open(tmp,'w',encoding='utf-8') as f:
        f.write(json.dumps(o,ensure_ascii=False,indent=2));f.flush();os.fsync(f.fileno())
    tmp.replace(p)
def writetext(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.part')
    with open(tmp,'w',encoding='utf-8') as f:
        f.write(text);f.flush();os.fsync(f.fileno())
    tmp.replace(p)
def csvout(p,rows,fields=None):
    rows=list(rows)
    fields=fields or (list(rows[0].keys()) if rows else ['screening_unit_id'])
    tmp=p.with_suffix(p.suffix+'.part')
    with open(tmp,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        f.flush();os.fsync(f.fileno())
    tmp.replace(p)

def init():
    ROOT.mkdir(parents=True,exist_ok=True); CUR.mkdir(parents=True,exist_ok=True)
    c=connect(); r=rawconnect()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS source_files(id INTEGER PRIMARY KEY,sha256 TEXT,local_path TEXT,byte_size INTEGER,mime_type TEXT,page_count INTEGER,validation_status TEXT,acquired_at TEXT);
    CREATE TABLE IF NOT EXISTS units(
      screening_unit_id TEXT PRIMARY KEY,source_problem_id INTEGER,derived_from_whole_paper INTEGER DEFAULT 0,
      competition TEXT,competition_slug TEXT,competition_category TEXT,year TEXT,round_or_section TEXT,
      format TEXT DEFAULT 'unknown',problem_number TEXT,problem_title TEXT,title_provenance TEXT,
      source_file TEXT,source_file_id INTEGER,source_sha256 TEXT,page_start INTEGER,page_end INTEGER,
      location_json TEXT,source_url TEXT,decision TEXT CHECK(decision IN ('KEEP','BORDERLINE','REJECT') OR decision IS NULL),
      confidence TEXT,primary_spho_domains TEXT,required_physics TEXT,external_physics_if_any TEXT,
      decision_reason TEXT,visual_inspection_used INTEGER DEFAULT 0,solution_used INTEGER DEFAULT 0,
      review_status TEXT DEFAULT 'pending_content_review',screened_at TEXT,evidence TEXT,
      boundary_status TEXT DEFAULT 'source_individual_boundary',reviewed_at TEXT);
    CREATE TABLE IF NOT EXISTS containers(source_problem_id INTEGER PRIMARY KEY,competition_slug TEXT,year TEXT,
      source_file_id INTEGER,source_sha256 TEXT,source_file TEXT,status TEXT DEFAULT 'pending_boundary_review',
      derived_count INTEGER,notes TEXT,reviewed_at TEXT);
    CREATE TABLE IF NOT EXISTS unit_files(screening_unit_id TEXT REFERENCES units(screening_unit_id),file_id INTEGER REFERENCES source_files(id),document_id INTEGER,role TEXT,PRIMARY KEY(screening_unit_id,file_id,document_id));
    CREATE TABLE IF NOT EXISTS extraction(file_id INTEGER PRIMARY KEY,sha256 TEXT,cache_path TEXT,page_count INTEGER,text_characters INTEGER,low_text_pages TEXT,status TEXT,error TEXT,extracted_at TEXT);
    CREATE TABLE IF NOT EXISTS review_events(id INTEGER PRIMARY KEY,screening_unit_id TEXT,pass INTEGER,reviewed_at TEXT,detail TEXT);
    CREATE TABLE IF NOT EXISTS errors(id INTEGER PRIMARY KEY,item_type TEXT,item_id TEXT,stage TEXT,code TEXT,detail TEXT,resolved INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS raw_snapshot(path TEXT PRIMARY KEY,byte_size INTEGER,sha256 TEXT);
    CREATE TABLE IF NOT EXISTS renders(file_id INTEGER,page INTEGER,path TEXT,created_at TEXT,PRIMARY KEY(file_id,page));
    ''')
    if c.execute('select count(*) from source_files').fetchone()[0]:
        print('Inventory already exists; preserved.');return
    for table in ['competitions','problems','documents','problem_documents','document_sources','archive_sections']:
        sql=r.execute('select sql from sqlite_master where name=?',(table,)).fetchone()[0]
        # Exact read-only source-table snapshot in the screening database, under prefixed names.
        cols=r.execute('select * from '+table+' limit 0').description
        c.execute('create table source_'+table+' ('+','.join('"'+v[0]+'"' for v in cols)+')')
        rows=r.execute('select * from '+table).fetchall()
        c.executemany('insert into source_'+table+' values ('+','.join('?' for _ in cols)+')',[tuple(x) for x in rows])
    c.executemany('insert into source_files values (?,?,?,?,?,?,?,?)',[tuple(x) for x in r.execute('select * from files')])
    ai={int(x['logical_problem_record_id']):x for x in csv.DictReader(open(RAW/'ai_manifest.csv',encoding='utf-8-sig',newline=''))}
    files={x['local_path']:x for x in r.execute('select * from files')}
    comps={x['id']:x for x in r.execute('select * from competitions')}
    for p in r.execute('select * from problems order by id'):
        f=files.get(ai[p['id']]['problem_file_path']); comp=comps[p['competition_id']]
        if p['inventory_granularity']=='aggregate':
            c.execute('insert into containers(source_problem_id,competition_slug,year,source_file_id,source_sha256,source_file) values (?,?,?,?,?,?)',(p['id'],comp['slug'],p['year'],f['id'] if f else None,f['sha256'] if f else None,f['local_path'] if f else None));continue
        u='raw::'+str(p['id'])
        section=' / '.join(x for x in [p['session'],p['section']] if x)
        c.execute('insert into units(screening_unit_id,source_problem_id,competition,competition_slug,competition_category,year,round_or_section,problem_number,problem_title,title_provenance,source_file,source_file_id,source_sha256,source_url) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(u,p['id'],comp['name'],comp['slug'],comp['category'],p['year'],section,p['problem_identifier'],p['raw_title'],p['title_provenance'],f['local_path'] if f else None,f['id'] if f else None,f['sha256'] if f else None,p['source_page_url']))
        c.execute('insert into unit_files select ?,d.file_id,d.id,d.document_type from source_problem_documents pd join source_documents d on d.id=pd.document_id where pd.problem_id=? and d.file_id is not null',(u,p['id']))
    c.commit();print('Initialized',c.execute('select count(*) from units').fetchone()[0],'direct units;',c.execute('select count(*) from containers').fetchone()[0],'containers.')

def snapshot(check=False):
    c=connect(); rows=[]; mismatches=[]
    expected={x['path']:x for x in c.execute('select * from raw_snapshot')}
    for i,p in enumerate(sorted(RAW.rglob('*'))):
        if not p.is_file():continue
        rel=p.relative_to(RAW).as_posix(); size=p.stat().st_size; h=digest(p)
        rows.append((rel,size,h))
        if check and (rel not in expected or size!=expected[rel]['byte_size'] or h!=expected[rel]['sha256']): mismatches.append(rel)
    if check:
        mismatches+=sorted(set(expected)-{x[0] for x in rows})
        writejson(ROOT/'raw_immutability_check.json',{'checked_at':now(),'files_checked':len(rows),'mismatches':mismatches,'unchanged':not mismatches})
        print('Raw check:',len(rows),'files;',len(mismatches),'mismatches')
    else:
        if expected:raise RuntimeError('Initial snapshot already exists; refuse to replace it')
        c.executemany('insert into raw_snapshot values (?,?,?)',rows); c.commit()
        csvout(ROOT/'raw_snapshot.csv',[dict(zip(['path','byte_size','sha256'],x)) for x in rows]);print('Snapshot',len(rows),'files')

def extract():
    c=connect();done={x[0] for x in c.execute("select file_id from extraction where status='extracted'")}
    errors=0; n=0
    for f in c.execute("select * from source_files where validation_status='valid_pdf' order by id").fetchall():
        if f['id'] in done:continue
        out=ROOT/'cache'/f['sha256'][:2]/(f['sha256']+'.json.gz')
        try:
            with fitz.open(RAW/f['local_path']) as pdf:
                pages=[]
                for i,p in enumerate(pdf):
                    # Coordinates remain available for exact within-page unit locations.
                    blocks=p.get_text('blocks',sort=True)
                    pages.append({'page':i+1,'width':p.rect.width,'height':p.rect.height,
                      'text':p.get_text('text',sort=True),'blocks':[list(b[:7]) for b in blocks if len(b)>6 and b[6]==0]})
            out.parent.mkdir(parents=True,exist_ok=True)
            temp=out.with_suffix('.part')
            with gzip.open(temp,'wt',encoding='utf-8') as g:json.dump({'file_id':f['id'],'sha256':f['sha256'],'source':f['local_path'],'pages':pages},g,ensure_ascii=False)
            temp.replace(out)
            chars=sum(len(p['text']) for p in pages); low=[p['page'] for p in pages if len(p['text'].strip())<80]
            c.execute('insert or replace into extraction values (?,?,?,?,?,?,?,?,?)',(f['id'],f['sha256'],out.relative_to(ROOT).as_posix(),len(pages),chars,json.dumps(low),'extracted',None,now()))
        except Exception as e:
            errors+=1;c.execute('insert or replace into extraction values (?,?,?,?,?,?,?,?,?)',(f['id'],f['sha256'],None,f['page_count'],0,None,'error',str(e),now()))
            c.execute('insert into errors(item_type,item_id,stage,code,detail) values (?,?,?,?,?)',('file',str(f['id']),'extraction','EXTRACTION_ERROR',str(e)))
        n+=1
        if n%50==0:c.commit();print('Extracted',n,'new PDFs',flush=True)
    c.commit();print('Cache finished;',n,'new;',errors,'errors')

def cache(file_id):
    c=connect();r=c.execute('select cache_path from extraction where file_id=?',(file_id,)).fetchone()
    if not r or not r[0]:raise RuntimeError('No extraction cache for '+str(file_id))
    with gzip.open(ROOT/r[0],'rt',encoding='utf-8') as g:return json.load(g)

def show(file_ids,pages=None):
    for fid in file_ids:
        data=cache(fid);print('\nFILE',fid,data['source'])
        for p in data['pages']:
            if pages and p['page'] not in pages:continue
            print('\nPAGE',p['page']);print(p['text'])

def render(file_ids,pages=None):
    c=connect()
    for fid in file_ids:
        f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
        with fitz.open(RAW/f['local_path']) as pdf:
            for i,p in enumerate(pdf):
                if pages and i+1 not in pages:continue
                out=ROOT/'renders'/f['sha256'][:16]/('page_%03d.png'%(i+1));out.parent.mkdir(parents=True,exist_ok=True)
                if not out.exists():p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(out)
                c.execute('insert or replace into renders values (?,?,?,?)',(fid,i+1,out.relative_to(ROOT).as_posix(),now()));print(out)
    c.commit()

def derive(path):
    c=connect(); records=json.loads(Path(path).read_text(encoding='utf-8'))
    for record in records:
        pid=record['source_problem_id'];container=c.execute('select * from containers where source_problem_id=?',(pid,)).fetchone()
        p=c.execute('select * from source_problems where id=?',(pid,)).fetchone()
        comp=c.execute('select * from source_competitions where id=?',(p['competition_id'],)).fetchone()
        assert container and record['boundary_evidence']
        for item in record['units']:
            unit_id='derived::'+container['source_sha256'][:16]+'::'+str(pid)+'::'+item['number']
            vals={'screening_unit_id':unit_id,'source_problem_id':pid,'derived_from_whole_paper':1,'competition':comp['name'],'competition_slug':comp['slug'],'competition_category':comp['category'],'year':p['year'],'round_or_section':' / '.join(x for x in [p['session'],p['section']] if x),'format':item.get('format','unknown'),'problem_number':item['number'],'problem_title':item.get('title'),'title_provenance':'unknown','source_file':container['source_file'],'source_file_id':container['source_file_id'],'source_sha256':container['source_sha256'],'page_start':item['page_start'],'page_end':item['page_end'],'location_json':json.dumps(item.get('location',{}),ensure_ascii=False),'source_url':p['source_page_url'],'boundary_status':'content_boundary_verified','evidence':record['boundary_evidence']}
            fields=list(vals);c.execute('insert or ignore into units('+','.join(fields)+') values ('+','.join('?' for _ in fields)+')',list(vals.values()))
            c.execute('insert or ignore into unit_files select ?,d.file_id,d.id,d.document_type from source_problem_documents pd join source_documents d on d.id=pd.document_id where pd.problem_id=? and d.file_id is not null',(unit_id,pid))
        count=c.execute('select count(*) from units where source_problem_id=?',(pid,)).fetchone()[0]
        assert count==len(record['units'])
        c.execute("update containers set status='expanded_content_verified',derived_count=?,notes=?,reviewed_at=? where source_problem_id=?",(count,record['boundary_evidence'],now(),pid))
    c.commit();print('Expanded',len(records),'containers')

def decisions(path):
    c=connect()
    for item in json.loads(Path(path).read_text(encoding='utf-8')):
        uid=item.pop('screening_unit_id'); old=c.execute('select * from units where screening_unit_id=?',(uid,)).fetchone();assert old,uid
        assert item.get('decision') in ['KEEP','BORDERLINE','REJECT'];assert item.get('evidence') and item.get('required_physics') and item.get('decision_reason')
        assert item.get('confidence') in ['high','medium','low']
        required_review = item.pop('needs_second_review', False) or item['decision']=='BORDERLINE' or item['confidence']!='high'
        item.update(screened_at=now(),review_status='pass_1_complete' if required_review else 'single_pass_complete')
        c.execute('update units set '+','.join(k+'=?' for k in item)+' where screening_unit_id=?',list(item.values())+[uid])
        c.execute('insert into review_events(screening_unit_id,pass,reviewed_at,detail) values (?,?,?,?)',(uid,1,now(),item['evidence']))
    c.commit();print('Saved content decisions')

def review(path):
    c=connect()
    for x in json.loads(Path(path).read_text(encoding='utf-8')):
        uid=x['screening_unit_id'];assert c.execute('select decision from units where screening_unit_id=?',(uid,)).fetchone()[0]
        if not c.execute('select 1 from review_events where screening_unit_id=? and pass=2 and detail=?',(uid,x['detail'])).fetchone():
            c.execute('insert into review_events(screening_unit_id,pass,reviewed_at,detail) values (?,?,?,?)',(uid,2,now(),x['detail']))
        c.execute("update units set review_status='pass_2_complete',reviewed_at=? where screening_unit_id=?",(now(),uid))
    c.commit();print('Saved second reviews')

def export():
    c=connect(); rows=[dict(x) for x in c.execute("select *,coalesce(decision,'UNRESOLVED_ERROR') as accounting_status from units order by competition_slug,year,source_problem_id,screening_unit_id")]
    fields=list(rows[0]) if rows else ['screening_unit_id']
    csvout(ROOT/'all_decisions.csv',rows,fields)
    for decision in ['KEEP','BORDERLINE','REJECT']:csvout(ROOT/(decision.lower()+'.csv'),[x for x in rows if x['decision']==decision],fields)
    csvout(ROOT/'derived_units.csv',[x for x in rows if x['derived_from_whole_paper']],fields)
    rem=[]
    for x in rows:
        if not x['decision']:rem.append({'item_type':'unit','item_id':x['screening_unit_id'],'stage':'source_unavailable' if x['review_status']=='unresolved_source_unavailable' else 'content_review','competition_slug':x['competition_slug'],'year':x['year'],'source_problem_id':x['source_problem_id'],'source_file_id':x['source_file_id'],'source_file':x['source_file'],'source_sha256':x['source_sha256'],'detail':x['source_quality_notes'] if x['review_status']=='unresolved_source_unavailable' else 'Actual-content review and location verification pending; no physics decision assigned.'})
        elif x['review_status'] not in ('pass_2_complete','single_pass_complete'):rem.append({'item_type':'unit','item_id':x['screening_unit_id'],'stage':'second_review','competition_slug':x['competition_slug'],'year':x['year'],'source_problem_id':x['source_problem_id'],'source_file_id':x['source_file_id'],'source_file':x['source_file'],'source_sha256':x['source_sha256'],'detail':'Pass 1 saved; required focused review pending.'})
    for x in c.execute("select * from containers where status!='expanded_content_verified'"):
        rem.append({'item_type':'container','item_id':str(x['source_problem_id']),'stage':'top_level_boundary_review','competition_slug':x['competition_slug'],'year':x['year'],'source_problem_id':x['source_problem_id'],'source_file_id':x['source_file_id'],'source_file':x['source_file'],'source_sha256':x['source_sha256'],'detail':'Container is not a screening unit; identify/verify every contained top-level question before physics review.'})
    rf=['item_type','item_id','stage','competition_slug','year','source_problem_id','source_file_id','source_file','source_sha256','detail']
    if c.execute("select 1 from sqlite_master where name='paper_boundary_audit'").fetchone():
        for x in c.execute("select a.*,f.local_path,f.sha256 from paper_boundary_audit a join source_files f on f.id=a.file_id where a.status!='full_paper_boundaries_verified'"):
            u=c.execute('select competition_slug,year from units where source_file_id=? limit 1',(x['file_id'],)).fetchone()
            rem.append(dict(item_type='physical_paper',item_id=str(x['file_id']),stage='paper_boundary_audit',competition_slug=u['competition_slug'],year=u['year'],source_problem_id=None,source_file_id=x['file_id'],source_file=x['local_path'],source_sha256=x['sha256'],detail='Verify complete printed top-level inventory; derive missing questions without altering raw rows or repeating completed content decisions.'))
    csvout(ROOT/'remaining.csv',rem,rf)
    err=[{'item_type':x['item_type'],'item_id':x['item_id'],'stage':x['stage'],'code':'SOURCE_REMOVED_STATEMENT_UNAVAILABLE' if x['stage']=='source_unavailable' else 'UNRESOLVED_ERROR_REVIEW_PENDING','detail':x['detail']} for x in rem]
    err += [dict(x) for x in c.execute('select item_type,item_id,stage,code,detail from errors where resolved=0')]
    csvout(ROOT/'screening_errors.csv',err,['item_type','item_id','stage','code','detail'])
    decisions=collections.Counter(x['decision'] or 'UNRESOLVED_ERROR' for x in rows)
    formats=collections.Counter(x['format'] for x in rows if x['decision'])
    bycomp=[]
    for comp in c.execute('select slug,name from source_competitions order by slug'):
        group=[x for x in rows if x['competition_slug']==comp['slug']]; counts=collections.Counter(x['decision'] or 'UNRESOLVED_ERROR' for x in group)
        bycomp.append({'competition_slug':comp['slug'],'competition':comp['name'],'identified_units':len(group),**{k:counts[k] for k in ['KEEP','BORDERLINE','REJECT','UNRESOLVED_ERROR']},'containers_pending':c.execute("select count(*) from containers where competition_slug=? and status!='expanded_content_verified'",(comp['slug'],)).fetchone()[0]})
    csvout(ROOT/'competition_coverage.csv',bycomp)
    domains=collections.Counter()
    for x in rows:
        if x['decision']=='KEEP':domains.update(filter(None,(x['primary_spho_domains'] or '').split(';')))
    stat={'updated_at':now(),'run_status':'INCOMPLETE' if rem or err else 'COMPLETE','direct_units':sum(not x['derived_from_whole_paper'] for x in rows),'derived_units':sum(x['derived_from_whole_paper'] for x in rows),'identified_units':len(rows),'decisions':dict(decisions),'screened_formats':dict(formats),'keep_domains':dict(domains),'pending_content_units':sum(not x['decision'] for x in rows),'remaining_queue_items':len(rem),'containers_pending':sum(x['item_type']=='container' for x in rem),'containers_expanded':c.execute("select count(*) from containers where status='expanded_content_verified'").fetchone()[0],'pdfs_cached':c.execute("select count(*) from extraction where status='extracted'").fetchone()[0],'source_rows_accounted':c.execute('select count(*) from source_problems').fetchone()[0],'boundary_inventory_complete':not any(x['item_type']=='container' for x in rem),'identified_unit_reconciliation':len(rows)==sum(decisions.values()),'unexplained_identified_units':0}
    writejson(ROOT/'progress.json',stat)
    stat['awaiting_content_review']=sum(not x['decision'] and x['review_status']!='unresolved_source_unavailable' for x in rows)
    stat['explicit_statement_unavailable']=sum(x['review_status']=='unresolved_source_unavailable' for x in rows)
    stat['focused_reviews_pending']=sum(bool(x['decision']) and x['review_status'] not in ('pass_2_complete','single_pass_complete') for x in rows)
    stat['pending_physical_paper_boundary_audits']=sum(x['stage']=='paper_boundary_audit' for x in rem)
    stat['boundary_inventory_complete']=not any(x['stage'] in ('paper_boundary_audit','top_level_boundary_review') for x in rem)
    stat['registered_inventory_is_provisional']=not stat['boundary_inventory_complete']
    writejson(ROOT/'progress.json',stat)
    print(json.dumps(stat,ensure_ascii=False,indent=2))

def materialize():
    c=connect(); CUR.mkdir(parents=True,exist_ok=True)
    selected=c.execute("select * from units where decision='KEEP' and confidence!='low' and review_status in ('pass_2_complete','single_pass_complete')").fetchall()
    used={}; associations=[]
    for u in selected:
        docs=c.execute('select uf.*,f.local_path,f.sha256,f.byte_size,f.page_count,d.document_scope from unit_files uf join source_files f on f.id=uf.file_id join source_documents d on d.id=uf.document_id where uf.screening_unit_id=?',(u['screening_unit_id'],)).fetchall()
        solutions=[d for d in docs if d['role']=='solution']
        solutions.sort(key=lambda d:(d['document_scope']!='problem','_tex' in d['local_path'],-(d['page_count'] or 0),d['file_id']))
        primary=[d for d in docs if d['file_id']==u['source_file_id']]
        assert primary,'Selected statement lacks provenance'
        # Preserve every confidently associated solution, including answer keys
        # and complementary worked versions. SHA storage remains unique.
        chosen=primary[:1]+solutions+[d for d in docs if d['role'] not in ['problem','combined','solution','administrative','reference_website']]
        for d in chosen:
            used[d['file_id']]=d; associations.append((u['screening_unit_id'],d['file_id'],d['document_id'],d['role']))
    m=sqlite3.connect(CUR/'manifest.sqlite');m.executescript('''CREATE TABLE IF NOT EXISTS files(file_id INTEGER PRIMARY KEY,source_file TEXT,curated_file TEXT,sha256 TEXT,byte_size INTEGER,page_count INTEGER,materialization TEXT,verified_sha256 TEXT);CREATE TABLE IF NOT EXISTS selected_problems(screening_unit_id TEXT PRIMARY KEY,metadata_json TEXT);CREATE TABLE IF NOT EXISTS problem_files(screening_unit_id TEXT,file_id INTEGER,document_id INTEGER,role TEXT,PRIMARY KEY(screening_unit_id,file_id,document_id));CREATE TABLE IF NOT EXISTS provenance(document_id INTEGER PRIMARY KEY,metadata_json TEXT);''')
    # A focused audit can revise a new decision. Remove stale curated membership
    # while retaining all still-selected physical files and their existing links.
    current_ids={u['screening_unit_id'] for u in selected}
    for (uid,) in m.execute('select screening_unit_id from selected_problems').fetchall():
        if uid not in current_ids:
            m.execute('delete from problem_files where screening_unit_id=?',(uid,))
            m.execute('delete from selected_problems where screening_unit_id=?',(uid,))
    for fid,rel,expected in m.execute('select file_id,curated_file,sha256 from files').fetchall():
        if fid not in used:
            obsolete=(CUR/rel).resolve();obsolete.relative_to((CUR/'files').resolve())
            assert obsolete!= (RAW/rel).resolve()
            if obsolete.exists():
                assert digest(obsolete)==expected
                obsolete.unlink() # Unlink curated entry only; never write raw bytes.
            m.execute('delete from problem_files where file_id=?',(fid,))
            m.execute('delete from files where file_id=?',(fid,))
    m.execute('delete from provenance where document_id not in (select document_id from problem_files)')
    hard=copy=0; mapping={}
    import shutil
    for fid,d in used.items():
        src=RAW/d['local_path']; dest=CUR/'files'/Path(d['local_path']).relative_to('originals');dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            assert digest(dest)==d['sha256']; kind='hardlink' if os.path.samefile(src,dest) else 'copy'
        else:
            try:os.link(src,dest);kind='hardlink'
            except OSError:shutil.copy2(src,dest);kind='copy'
        got=digest(dest);assert got==d['sha256']
        hard+=kind=='hardlink';copy+=kind=='copy';rel=dest.relative_to(CUR).as_posix();mapping[fid]=rel
        m.execute('insert or replace into files values (?,?,?,?,?,?,?,?)',(fid,d['local_path'],rel,d['sha256'],d['byte_size'],d['page_count'],kind,got))
    reference_mapping={}; reference_rows=[]
    m.execute('''create table if not exists reference_files(reference_id text primary key,screening_unit_id text,url text,source_file text,curated_file text,sha256 text,byte_size integer,page_count integer,materialization text,verified_sha256 text,purpose text)''')
    if c.execute("select 1 from sqlite_master where name='screening_references'").fetchone():
        reference_rows=c.execute("select r.* from screening_references r join units u on u.screening_unit_id=r.screening_unit_id where u.decision='KEEP' and u.review_status in ('single_pass_complete','pass_2_complete')").fetchall()
    # screening_references records source/problem relationships; it is not a
    # physical inventory. A shared experiment archive must be stored once.
    physical_refs={}
    for r in sorted(reference_rows,key=lambda r:r['reference_id']):
        physical_refs.setdefault(r['sha256'],r)
    wanted_refs={r['reference_id'] for r in physical_refs.values()}
    wanted_ref_paths={'references/'+Path(r['local_path']).name for r in physical_refs.values()}
    m.execute('''create table if not exists reference_associations(reference_id text primary key,screening_unit_id text,physical_reference_id text,url text,source_file text,sha256 text,purpose text)''')
    m.execute('delete from reference_associations')
    for rid,rel,sha in m.execute('select reference_id,curated_file,sha256 from reference_files').fetchall():
        if rid not in wanted_refs:
            obsolete=(CUR/rel).resolve();obsolete.relative_to((CUR/'references').resolve())
            if obsolete.exists() and rel not in wanted_ref_paths:
                assert digest(obsolete)==sha;obsolete.unlink()
            m.execute('delete from reference_files where reference_id=?',(rid,))
    reference_paths={}
    for r in physical_refs.values():
        src=ROOT/r['local_path'];dest=CUR/'references'/Path(r['local_path']).name;dest.parent.mkdir(exist_ok=True)
        assert digest(src)==r['sha256']
        if not dest.exists():
            try:os.link(src,dest)
            except OSError:shutil.copy2(src,dest)
        assert digest(dest)==r['sha256'];kind='hardlink' if os.path.samefile(src,dest) else 'copy'
        hard+=kind=='hardlink';copy+=kind=='copy';rel=dest.relative_to(CUR).as_posix()
        reference_paths[r['sha256']]=rel
        m.execute('insert or replace into reference_files values (?,?,?,?,?,?,?,?,?,?,?)',(r['reference_id'],r['screening_unit_id'],r['url'],r['local_path'],rel,r['sha256'],r['byte_size'],r['page_count'],kind,r['sha256'],r['purpose']))
    for r in reference_rows:
        assert digest(ROOT/r['local_path'])==r['sha256']
        canonical=physical_refs[r['sha256']]['reference_id']
        reference_mapping.setdefault(r['screening_unit_id'],[]).append(reference_paths[r['sha256']])
        m.execute('insert into reference_associations values (?,?,?,?,?,?,?)',(r['reference_id'],r['screening_unit_id'],canonical,r['url'],r['local_path'],r['sha256'],r['purpose']))
    equivalences={r['alias_unit_id']:r['canonical_unit_id'] for r in c.execute('select * from unit_equivalences')} if c.execute("select 1 from sqlite_master where name='unit_equivalences'").fetchone() else {}
    out=[]
    for u in selected:
        row=dict(u);row['canonical_screening_unit_id']=equivalences.get(u['screening_unit_id'],u['screening_unit_id']);sols=[a for a in associations if a[0]==u['screening_unit_id'] and a[3]=='solution']
        primary_solution=sols[0][1] if sols else None
        row.update(curated_file=mapping[u['source_file_id']],solution_file=mapping[primary_solution] if sols else '',sha256=u['source_sha256'],other_relevant_files=json.dumps(sorted({mapping[a[1]] for a in associations if a[0]==u['screening_unit_id'] and a[1] not in (u['source_file_id'],primary_solution)})),curated_status='reviewed_KEEP_subset_run_incomplete')
        row['other_relevant_files']=json.dumps(sorted(set(json.loads(row['other_relevant_files']))|set(reference_mapping.get(u['screening_unit_id'],[]))|set(reference_mapping.get(equivalences.get(u['screening_unit_id'],u['screening_unit_id']),[]))))
        out.append(row);m.execute('insert or replace into selected_problems values (?,?)',(u['screening_unit_id'],json.dumps(row,ensure_ascii=False)))
    expected_associations=set(associations)
    for existing in m.execute('select * from problem_files').fetchall():
        if tuple(existing) not in expected_associations:
            m.execute('delete from problem_files where screening_unit_id=? and file_id=? and document_id=?',tuple(existing[:3]))
    m.executemany('insert or ignore into problem_files values (?,?,?,?)',associations)
    for did in sorted({a[2] for a in associations}):
        d=dict(c.execute('select * from source_documents where id=?',(did,)).fetchone());d['document_sources']=[dict(x) for x in c.execute('select * from source_document_sources where document_id=?',(did,))]
        if c.execute("select 1 from sqlite_master where name='supplementary_associations'").fetchone():
            d['screening_supplementary_associations']=[dict(x) for x in c.execute('select * from supplementary_associations where document_id=?',(did,))]
        m.execute('insert or replace into provenance values (?,?)',(did,json.dumps(d,ensure_ascii=False)))
    m.commit();m.row_factory=sqlite3.Row
    csvout(CUR/'selected_problems.csv',out,list(out[0]) if out else ['screening_unit_id','curated_file'])
    m.execute('''create view if not exists all_files as select cast(file_id as text) file_id,source_file,curated_file,sha256,byte_size,page_count,materialization,verified_sha256,'acquisition' source_storage_root,'' source_url from files union all select 'reference::'||reference_id,source_file,curated_file,sha256,byte_size,page_count,materialization,verified_sha256,'screening',url from reference_files''')
    m.commit()
    csvout(CUR/'manifest.csv',[dict(x) for x in m.execute('select * from all_files order by file_id')])
    csvout(CUR/'source_linked_references.csv',[dict(x) for x in m.execute('select * from reference_files')],['reference_id','screening_unit_id','url','source_file','curated_file','sha256','byte_size','page_count','materialization','verified_sha256','purpose'])
    csvout(CUR/'source_linked_reference_associations.csv',[dict(x) for x in m.execute('select * from reference_associations')],['reference_id','screening_unit_id','physical_reference_id','url','source_file','sha256','purpose'])
    stats={'selected_units':len(selected),'verified_distinct_selected_questions':len({equivalences.get(u['screening_unit_id'],u['screening_unit_id']) for u in selected}),'unique_physical_files':len(used)+len(physical_refs),'raw_acquisition_files':len(used),'source_linked_reference_files':len(physical_refs),'source_linked_reference_associations':len(reference_rows),'byte_size':sum(d['byte_size'] for d in used.values())+sum(r['byte_size'] for r in physical_refs.values()),'hardlinks':hard,'copies':copy,'hash_mismatches':0,'selection_is_complete':False}
    writejson(CUR/'materialization.json',stats);print(json.dumps(stats,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['init','snapshot','check_raw','extract','show','render','derive','decisions','review','export','materialize']);ap.add_argument('items',nargs='*');ap.add_argument('--pages',type=int,nargs='+');args=ap.parse_args()
    if args.action=='init':init()
    elif args.action in ['snapshot','check_raw']:snapshot(args.action=='check_raw')
    elif args.action=='extract':extract()
    elif args.action in ['show','render']:globals()[args.action]([int(x) for x in args.items],args.pages)
    elif args.action in ['derive','decisions','review']:globals()[args.action](args.items[0])
    else:globals()[args.action]()

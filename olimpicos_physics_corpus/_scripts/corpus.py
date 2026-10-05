"""Olimpicos Physics acquisition. Run discover, download, export; SQLite is canonical."""
import sys, re, json, csv, sqlite3, hashlib, time, os, zipfile, logging, threading
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse, unquote
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
UA = 'OlimpicosPhysicsCorpus/1.0 (public research archive; conservative acquisition)'
logging.getLogger('pypdf').setLevel(logging.ERROR)
sys.stdout.reconfigure(encoding='utf-8')
def now(): return datetime.now(timezone.utc).isoformat()
def db():
    c=sqlite3.connect(ROOT/'manifest.sqlite', timeout=60); c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON'); c.execute('PRAGMA journal_mode=WAL'); return c
def schema(c):
    c.executescript('''
    CREATE TABLE IF NOT EXISTS competitions(id INTEGER PRIMARY KEY,slug TEXT UNIQUE,name TEXT,full_name TEXT,category TEXT,source_page_url TEXT,discovered_at TEXT,discovery_status TEXT,notes TEXT);
    CREATE TABLE IF NOT EXISTS archive_sections(id INTEGER PRIMARY KEY,competition_id INTEGER REFERENCES competitions(id),year TEXT,session TEXT,section TEXT,source_page_url TEXT,expected_problems INTEGER,UNIQUE(competition_id,year,session,section));
    CREATE TABLE IF NOT EXISTS problems(id INTEGER PRIMARY KEY,competition_id INTEGER REFERENCES competitions(id),archive_section_id INTEGER REFERENCES archive_sections(id),year TEXT,session TEXT,section TEXT,problem_identifier TEXT,source_key TEXT UNIQUE,raw_title TEXT,title_provenance TEXT,problem_type TEXT,source_page_url TEXT,source_topics TEXT,source_subtopics TEXT,publication_status TEXT,inventory_granularity TEXT,notes TEXT);
    CREATE TABLE IF NOT EXISTS files(id INTEGER PRIMARY KEY,sha256 TEXT UNIQUE,local_path TEXT UNIQUE,byte_size INTEGER,mime_type TEXT,page_count INTEGER,validation_status TEXT,acquired_at TEXT);
    CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY,competition_id INTEGER REFERENCES competitions(id),year TEXT,session TEXT,section TEXT,raw_link_label TEXT,document_type TEXT,document_scope TEXT,source_page_url TEXT,direct_url TEXT,hosting TEXT,original_filename TEXT,discovered_at TEXT,notes TEXT,status TEXT DEFAULT 'pending',file_id INTEGER REFERENCES files(id),http_status INTEGER,response_mime_type TEXT,final_url TEXT,attempts INTEGER DEFAULT 0,last_error TEXT,UNIQUE(competition_id,year,session,section,direct_url,document_type));
    CREATE TABLE IF NOT EXISTS problem_documents(problem_id INTEGER REFERENCES problems(id),document_id INTEGER REFERENCES documents(id),relationship TEXT,PRIMARY KEY(problem_id,document_id));
    CREATE TABLE IF NOT EXISTS document_sources(id INTEGER PRIMARY KEY,document_id INTEGER REFERENCES documents(id),source_page_url TEXT,locator TEXT,raw_link_label TEXT,source_attribute TEXT,UNIQUE(document_id,source_page_url,locator,source_attribute));
    CREATE TABLE IF NOT EXISTS issues(id INTEGER PRIMARY KEY,competition_id INTEGER,problem_id INTEGER,document_id INTEGER,kind TEXT,source_url TEXT,detail TEXT,resolved INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,direct_url TEXT,attempted_at TEXT,status TEXT,http_status INTEGER,detail TEXT);
    '''); c.commit()
def text(el,selector=None):
    x=el.select_one(selector) if selector else el
    return x.get_text(' ',strip=True) if x else ''
def role(label,classes=''):
    l=label.lower()
    if 'k-combined' in classes or ('problem' in l and 'solution' in l): return 'combined'
    if 'latex' in l and 'source' in l: return 'latex_source'
    if 'solution' in l or 'k-solutions' in classes: return 'solution'
    if 'marking' in l: return 'marking_scheme'
    if 'answer' in l: return 'answer_sheet'
    if 'data' in l: return 'experimental_data'
    if 'instruction' in l: return 'instructions'
    if 'errata' in l: return 'errata'
    if any(w in l for w in ['results','ranking','statistics','minutes','ceremony','photograph','proceedings']): return 'administrative'
    if 'problem' in l or 'k-problems' in classes or l=='latex pdf': return 'problem'
    if 'website' in l or 'archive' in l or 'creativecommons' in l: return 'reference_website'
    return 'supplementary'
def discover():
    c=db(); schema(c)
    comps=json.loads((ROOT/'metadata/competitions_discovered.json').read_text(encoding='utf-8'))
    for comp in comps:
        slug=comp['slug']; page=comp['url']; s=BeautifulSoup((ROOT/'metadata/pages'/f'{slug}.html').read_text(encoding='utf-8'),'html.parser')
        done=c.execute('SELECT discovery_status FROM competitions WHERE slug=?',(slug,)).fetchone()
        if done and done[0] in ['discovered','processed']:
            print('inventory already present',slug,flush=True);continue
        c.execute('INSERT OR IGNORE INTO competitions(slug,name,full_name,category,source_page_url,discovered_at,discovery_status,notes) VALUES(?,?,?,?,?,?,?,?)',(slug,comp['name'],comp['full_name'],comp['category'],page,now(),'processing',''))
        cid=c.execute('SELECT id FROM competitions WHERE slug=?',(slug,)).fetchone()[0]
        source_title_note=any('Titles marked' in p.text for p in s.select('p.source'))
        li_ids={}; section_pids={}; band_info={}
        articles=s.select('article')
        if not articles:c.execute('INSERT INTO issues(competition_id,kind,source_url,detail) VALUES(?,?,?,?)',(cid,'parse_warning',page,'No archive articles found'))
        for ai,art in enumerate(articles):
            year=text(art,'.year') or None
            if year and not re.fullmatch(r'\d{4}(?:[-–/]\d{2,4})?',year):
                c.execute('INSERT INTO issues(competition_id,kind,source_url,detail) VALUES(?,?,?,?)',(cid,'parse_warning',page,'Ambiguous year: '+year));year=None
            session=''
            for bi,el in enumerate(art.select('.stage,.band')):
                if 'stage' in el.get('class',[]): session=text(el,'.slabel');continue
                section=text(el,'.rlabel'); rows=[li for li in el.select('li') if li.select_one('.n')]
                counts=[text(x) for x in el.select('.bandhead .rcount') if re.match(r'^\d+ problems?$',text(x))]
                expected=int(counts[0].split()[0]) if counts else None
                c.execute('INSERT OR IGNORE INTO archive_sections(competition_id,year,session,section,source_page_url,expected_problems) VALUES(?,?,?,?,?,?)',(cid,year,session,section,page+'#'+art.get('id',''),expected))
                secid=c.execute('SELECT id FROM archive_sections WHERE competition_id=? AND year IS ? AND session=? AND section=?',(cid,year,session,section)).fetchone()[0]
                if expected is None or expected!=len(rows):c.execute('INSERT INTO issues(competition_id,kind,source_url,detail) VALUES(?,?,?,?)',(cid,'parse_warning',page,f'{year} {session} {section}: displayed {expected}, parsed {len(rows)}'))
                pids=[]
                for ri,li in enumerate(rows):
                    ident=text(li,'.n'); title=text(li,'.t'); b=li.select_one('button[data-g]'); key=b['data-g'] if b else f'{slug}:{year}:{session}:{section}:{ident}'
                    aggregate=title.lower() in ['all problems','all questions','problems and solutions']
                    notes='Source enumerates an aggregate paper as a problem row; identifiers are source row identifiers, not individual questions inside the PDF.' if aggregate else ''
                    status='not_published' if li.select_one('.none') else 'linked'
                    prov='source_authored' if li.select_one('.gen') and source_title_note else 'unknown'
                    c.execute('INSERT OR IGNORE INTO problems(competition_id,archive_section_id,year,session,section,problem_identifier,source_key,raw_title,title_provenance,problem_type,source_page_url,source_topics,source_subtopics,publication_status,inventory_granularity,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(cid,secid,year,session,section,ident,key,title,prov,section if section.lower() in ['theory','experimental'] else None,page+'#'+art.get('id',''),li.get('data-t',''),li.get('data-s',''),status,'aggregate' if aggregate else 'individual',notes))
                    pid=c.execute('SELECT id FROM problems WHERE source_key=?',(key,)).fetchone()[0];pids.append(pid);li_ids[id(li)]=pid
                section_pids[id(el)]=pids;band_info[id(el)]=(year,session,section,secid)
        # Every archive hyperlink and embedded transcription is inventoried; duplicated UI links retain source occurrences.
        for ai,art in enumerate(articles):
            year=text(art,'.year') or None
            for ni,node in enumerate(art.select('a[href],button[data-x],button[data-tp],button[data-ts],button[data-z]')):
                band=node.find_parent(class_='band'); li=node.find_parent('li'); session='';section=''
                if band: _,session,section,_=band_info[id(band)]
                attrs=[('href',node['href'],text(node), ' '.join(node.get('class',[])))] if node.name=='a' else [(k,node[k],{'data-x':'LaTeX transcription (.tex)','data-tp':'LaTeX PDF','data-ts':'LaTeX solution PDF','data-z':'LaTeX source (.zip)'}[k],'') for k in ['data-x','data-tp','data-ts','data-z'] if node.get(k)]
                for attr,href,label,classes in attrs:
                    url=urljoin(page,href);typ='latex_source' if attr=='data-x' else role(label,classes)
                    pids=[]
                    if li and id(li) in li_ids:pids=[li_ids[id(li)]]
                    elif band:pids=section_pids[id(band)]
                    aggregate=bool(pids) and all(c.execute('SELECT inventory_granularity FROM problems WHERE id=?',(pid,)).fetchone()[0]=='aggregate' for pid in pids)
                    scope='problem' if li and not aggregate else ('round' if session or section not in ['','Problems'] else 'full_exam') if band else 'year'
                    if aggregate and section not in ['Problems','']:scope='round'
                    if not li and band and len(pids)==1 and not aggregate:scope='problem'
                    if typ in ['reference_website','administrative']:status='index_only'
                    else:status='pending'
                    filename=unquote(Path(urlparse(url).path).name)
                    note='Embedded source-provided material URL.' if attr!='href' else ''
                    c.execute('INSERT OR IGNORE INTO documents(competition_id,year,session,section,raw_link_label,document_type,document_scope,source_page_url,direct_url,hosting,original_filename,discovered_at,notes,status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(cid,year,session,section,label,typ,scope,page+'#'+art.get('id',''),url,'olimpicos' if urlparse(url).hostname=='olimpicos.net' else 'external',filename,now(),note,status))
                    did=c.execute('SELECT id FROM documents WHERE competition_id=? AND year IS ? AND session=? AND section=? AND direct_url=? AND document_type=?',(cid,year,session,section,url,typ)).fetchone()[0]
                    c.execute('INSERT OR IGNORE INTO document_sources(document_id,source_page_url,locator,raw_link_label,source_attribute) VALUES(?,?,?,?,?)',(did,page,f'article[{ai}]/material[{ni}]',label,attr))
                    for pid in pids:c.execute('INSERT OR IGNORE INTO problem_documents VALUES(?,?,?)',(pid,did,'individual_link' if li and not aggregate else 'shared_paper'))
            # Catch unexpected enumerated rows outside a band.
            for li in art.select('li'):
                if li.select_one('.n') and id(li) not in li_ids:c.execute('INSERT INTO issues(competition_id,kind,source_url,detail) VALUES(?,?,?,?)',(cid,'parse_warning',page,'Enumerated row outside parsed bands: '+text(li)))
        # Source links in the competition introduction, excluding universal navigation/social links.
        for ni,a in enumerate(s.select('a[href]')):
            if a.find_parent('article') or not a['href'].startswith(('http','/files/')) or 'discord.gg' in a['href']:continue
            url=urljoin(page,a['href']);label=text(a);typ=role(label)
            if Path(urlparse(url).path).suffix.lower() not in ['.pdf','.zip','.tex','.xlsx','.xls','.pptx','.docx']:typ='reference_website'
            c.execute('INSERT INTO documents(competition_id,year,session,section,raw_link_label,document_type,document_scope,source_page_url,direct_url,hosting,original_filename,discovered_at,notes,status) SELECT ?,NULL,?,?,?,?,?,?,?,?,?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM documents WHERE competition_id=? AND direct_url=?)',(cid,'','',label,typ,'competition',page,url,'external',unquote(Path(urlparse(url).path).name),now(),'Introduction/source reference; external websites are indexed without crawling their independent archives.','index_only' if typ=='reference_website' else 'pending',cid,url))
        c.execute("UPDATE competitions SET discovery_status='discovered' WHERE id=?",(cid,));c.commit()
        print('inventoried',slug,flush=True)
    export()
    if not (ROOT/'metadata/pre_download_inventory.sqlite').exists():
        snapshot=sqlite3.connect(ROOT/'metadata/pre_download_inventory.sqlite');c.backup(snapshot);snapshot.close()
    print('Discovery snapshot saved',flush=True)

_local=threading.local();_robots={};_lock=threading.Lock();_last_request={}
def session():
    if not hasattr(_local,'session'):
        _local.session=requests.Session();_local.session.headers['User-Agent']=UA
    return _local.session
def allowed(url):
    origin=f'{urlparse(url).scheme}://{urlparse(url).netloc}'
    with _lock:
        if origin not in _robots:
            x=session().get(origin+'/robots.txt',timeout=(15,30));rp=RobotFileParser();rp.set_url(origin+'/robots.txt')
            if x.status_code==200:rp.parse(x.text.splitlines())
            elif x.status_code in [401,403]:rp.parse(['User-agent: *','Disallow: /'])
            elif x.status_code>=500:raise RuntimeError('robots.txt server failure '+str(x.status_code))
            else:rp.parse(['User-agent: *','Allow: /'])
            _robots[origin]=rp
            (ROOT/'metadata'/('robots_'+urlparse(url).netloc.replace(':','_')+'.txt')).write_text(x.text,encoding='utf-8')
        rp=_robots[origin]
        return rp.can_fetch(UA,url),rp.crawl_delay(UA) or .12
def validate(path,expected,mime):
    size=path.stat().st_size
    if not size:raise ValueError('Zero-byte response')
    with path.open('rb') as f:head=f.read(4096)
    if head.lstrip().lower().startswith((b'<!doctype html',b'<html')) or 'text/html' in mime:raise ValueError('HTML returned instead of document')
    pages=None
    if expected=='.pdf' or head.startswith(b'%PDF-'):
        if not head.startswith(b'%PDF-'):raise ValueError('PDF magic missing')
        with path.open('rb') as f:f.seek(max(0,size-4096));tail=f.read()
        if b'%%EOF' not in tail:raise ValueError('PDF EOF marker missing; possible truncation')
        reader=PdfReader(path,strict=False);pages=len(reader.pages)
        if not pages:raise ValueError('PDF has no pages')
        mime='application/pdf';status='valid_pdf'
    elif expected in ['.zip','.xlsx','.docx','.pptx'] or head.startswith(b'PK\x03\x04'):
        with zipfile.ZipFile(path) as z:
            bad=z.testzip()
            if bad:raise ValueError('ZIP CRC failed: '+bad)
        mime='application/zip' if expected=='.zip' else mime;status='valid_archive'
    elif expected=='.tex':
        data=path.read_bytes().decode('utf-8-sig')
        if '\\' not in data:raise ValueError('Transcription lacks TeX commands')
        mime='text/x-tex';status='valid_tex'
    else:status='valid_nonempty'
    sha=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
    return sha,size,mime,pages,status
def acquire(item,passno):
    url=item['direct_url'];part=ROOT/'originals'/('_transfer_'+str(item['id'])+'.part');http=None;mime='';final=url
    try:
        ok,delay=allowed(url)
        if not ok:return dict(status='access_restricted',error='robots.txt disallows URL',http=None,url=url)
        origin=urlparse(url).netloc
        with _lock:
            wait=max(0,_last_request.get(origin,0)+delay-time.monotonic())
            if wait:time.sleep(wait)
            _last_request[origin]=time.monotonic()
        with session().get(url,stream=True,timeout=(20,90)) as r:
            http=r.status_code;mime=r.headers.get('Content-Type','').split(';')[0].lower();final=r.url
            if http!=200:
                status='source_unavailable' if http in [404,410] else 'access_restricted' if http in [401,403,429] else 'HTTP_error'
                return dict(status=status,error=f'HTTP {http}',http=http,mime=mime,url=final,retry_after=r.headers.get('Retry-After'))
            with part.open('wb') as f:
                for chunk in r.iter_content(256*1024):
                    if chunk:f.write(chunk)
            expected_length=r.headers.get('Content-Length')
            if expected_length and not r.headers.get('Content-Encoding') and part.stat().st_size!=int(expected_length):raise ValueError('Content-Length mismatch')
        try:sha,size,actual,pages,validation=validate(part,Path(urlparse(url).path).suffix.lower(),mime)
        except Exception as e:return dict(status='validation_failed',error=str(e),http=http,mime=mime,url=final)
        return dict(status='downloaded',sha=sha,size=size,actual_mime=actual,pages=pages,validation=validation,part=str(part),http=http,mime=mime,url=final)
    except Exception as e:return dict(status='unknown_error',error=type(e).__name__+': '+str(e),http=http,mime=mime,url=final)
    finally:
        # Valid parts are consumed atomically by the main thread. Invalid parts remain visibly incomplete until retry.
        pass
def safe(name):return re.sub(r'[^a-zA-Z0-9._-]+','_',name).strip(' ._')[:100] or 'document'
def download():
    c=db();schema(c)
    for passno in range(1,4):
        if passno>1:time.sleep(3*2**(passno-2))
        candidates=list(c.execute("SELECT d.*,c.slug FROM documents d JOIN competitions c ON c.id=d.competition_id WHERE d.status IN ('pending','HTTP_error','unknown_error','validation_failed') ORDER BY d.id"))
        # URL duplicates are fetched once; distinct document references retain provenance and file associations.
        groups={}
        for row in candidates:groups.setdefault(row['direct_url'],[]).append(dict(row))
        print(f'Download pass {passno}: {len(groups)} URLs, {len(candidates)} document records',flush=True)
        with ThreadPoolExecutor(max_workers=3) as ex:
            futures={ex.submit(acquire,items[0],passno):items for items in groups.values()}
            for n,future in enumerate(as_completed(futures),1):
                items=futures[future];res=future.result();fid=None;dup=False
                c.execute('INSERT INTO attempts(direct_url,attempted_at,status,http_status,detail) VALUES(?,?,?,?,?)',(items[0]['direct_url'],now(),res['status'],res.get('http'),res.get('error','')))
                if res['status']=='downloaded':
                    existing=c.execute('SELECT id FROM files WHERE sha256=?',(res['sha'],)).fetchone()
                    if existing:fid=existing[0];dup=True;Path(res['part']).unlink(missing_ok=True)
                    else:
                        item=items[0];name=safe(Path(item['original_filename']).stem)+'__'+res['sha'][:16]+Path(item['original_filename']).suffix.lower()
                        relative=Path('originals')/safe(item['slug'])/safe(item['year'] or 'unknown-year')/name;target=ROOT/relative;target.parent.mkdir(parents=True,exist_ok=True)
                        if target.exists():
                            if hashlib.file_digest(target.open('rb'),'sha256').hexdigest()!=res['sha']:raise RuntimeError('Deterministic filename collision')
                            Path(res['part']).unlink(missing_ok=True)
                        else:os.replace(res['part'],target)
                        cur=c.execute('INSERT INTO files(sha256,local_path,byte_size,mime_type,page_count,validation_status,acquired_at) VALUES(?,?,?,?,?,?,?)',(res['sha'],relative.as_posix(),res['size'],res['actual_mime'],res['pages'],res['validation'],now()));fid=cur.lastrowid
                for j,item in enumerate(items):
                    status='content_duplicate' if fid and (dup or j>0) else res['status']
                    c.execute('UPDATE documents SET status=?,file_id=?,http_status=?,response_mime_type=?,final_url=?,attempts=attempts+1,last_error=? WHERE id=?',(status,fid,res.get('http'),res.get('mime'),res.get('url'),res.get('error'),item['id']))
                c.commit()
                if n%50==0 or n==len(groups):print(f'pass {passno}: {n}/{len(groups)}, files={c.execute("SELECT count(*) FROM files").fetchone()[0]}, last={res["status"]}',flush=True)
                if res.get('http')==429:
                    # Halt new requests for this host on a rate-limit response; record queued items for a later authorized normal run.
                    with _lock:_last_request[urlparse(items[0]['direct_url']).netloc]=time.monotonic()+max(60,int(res.get('retry_after') or 60))
        export()
    print('Download/retry passes finished',flush=True)

def write_csv(name,rows,headers=None):
    rows=list(rows)
    if headers is None:headers=list(rows[0].keys()) if rows else ['id']
    with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers);w.writeheader();w.writerows(dict(r) for r in rows)
def export():
    c=db();schema(c)
    for table in ['competitions','problems','documents','files','problem_documents','document_sources','archive_sections']:
        write_csv(table+'.csv',c.execute('SELECT * FROM '+table),[r[1] for r in c.execute('PRAGMA table_info('+table+')')])
    write_csv('errors.csv',c.execute("SELECT 'document' AS entity,d.id,c.slug,d.year,d.session,d.section,d.direct_url,d.status,d.attempts,d.last_error AS detail FROM documents d JOIN competitions c ON c.id=d.competition_id WHERE d.status IN ('pending','HTTP_error','unknown_error','validation_failed','access_restricted') UNION ALL SELECT CASE WHEN i.kind='parse_warning' THEN 'parser' ELSE 'source' END,i.id,c.slug,dd.year,dd.session,dd.section,i.source_url,i.kind,0,i.detail FROM issues i LEFT JOIN competitions c ON c.id=i.competition_id LEFT JOIN documents dd ON dd.id=i.document_id WHERE i.resolved=0"),['entity','id','slug','year','session','section','direct_url','status','attempts','detail'])
    write_csv('missing_or_unavailable.csv',c.execute("SELECT 'problem' AS entity,p.id,c.slug,p.year,p.session,p.section,p.source_page_url AS source_url,p.publication_status AS status,'Individual file not published; consult problem_documents for shared-paper availability.' AS detail FROM problems p JOIN competitions c ON c.id=p.competition_id WHERE p.publication_status='not_published' UNION ALL SELECT 'document',d.id,c.slug,d.year,d.session,d.section,d.direct_url,d.status,d.last_error FROM documents d JOIN competitions c ON c.id=d.competition_id WHERE d.status IN ('source_unavailable','access_restricted') UNION ALL SELECT 'document',d.id,c.slug,d.year,d.session,d.section,d.direct_url,i.kind,i.detail FROM issues i JOIN documents d ON d.id=i.document_id JOIN competitions c ON c.id=d.competition_id WHERE i.kind='source_content_mismatch' AND i.resolved=0"),['entity','id','slug','year','session','section','source_url','status','detail'])
    ai=[]
    for p in c.execute('SELECT p.*,c.name AS competition,c.slug,c.category,c.notes AS competition_notes FROM problems p JOIN competitions c ON c.id=p.competition_id ORDER BY p.id'):
        docs=list(c.execute('SELECT d.*,f.local_path,f.page_count FROM problem_documents pd JOIN documents d ON d.id=pd.document_id LEFT JOIN files f ON f.id=d.file_id WHERE pd.problem_id=? ORDER BY d.id',(p['id'],)))
        statements=[d for d in docs if d['document_type'] in ['problem','combined'] and d['local_path']]
        solutions=[d for d in docs if d['document_type'] in ['solution','combined'] and d['local_path']]
        primary=next((d for d in statements if 'tex' not in d['original_filename']),statements[0] if statements else None)
        sol=next((d for d in solutions if 'tex' not in d['original_filename']),solutions[0] if solutions else None)
        other=[d['local_path'] for d in docs if d['local_path'] and d!=primary and d!=sol]
        other += [r[0] for r in c.execute("SELECT DISTINCT f.local_path FROM documents d JOIN files f ON f.id=d.file_id WHERE d.competition_id=? AND ((d.year IS ? AND d.document_scope='year') OR d.document_scope='competition')",(p['competition_id'],p['year']))]
        other=sorted(set(other)-{primary['local_path'] if primary else '',sol['local_path'] if sol else ''})
        band=c.execute('SELECT source_band_index FROM archive_sections WHERE id=?',(p['archive_section_id'],)).fetchone()[0] if any(r[1]=='source_band_index' for r in c.execute('PRAGMA table_info(archive_sections)')) else None
        ai.append(dict(competition=p['competition'],competition_slug=p['slug'],competition_category=p['category'],year=p['year'],session=p['session'],section=p['section'],archive_section_id=p['archive_section_id'],source_band_index=band,problem_id=p['problem_identifier'],source_problem_key=p['source_key'],logical_problem_record_id=p['id'],problem_title=p['raw_title'],title_provenance=p['title_provenance'],problem_type=p['problem_type'],inventory_granularity=p['inventory_granularity'],document_scope=primary['document_scope'] if primary else '',problem_file_path=primary['local_path'] if primary else '',solution_file_path=sol['local_path'] if sol else '',solution_document_scope=sol['document_scope'] if sol else '',other_relevant_files=json.dumps(sorted(set(other)),ensure_ascii=False),page_count=primary['page_count'] if primary else None,source_page_url=p['source_page_url'],source_topics=p['source_topics'],source_subtopics=p['source_subtopics'],publication_status=p['publication_status'],notes=p['notes'],source_archive_notes=p['competition_notes']))
    write_csv('ai_manifest.csv',ai)
    write_csv('metadata/residual_queue.csv',c.execute("SELECT d.id AS document_id,d.direct_url,d.status,d.attempts,d.last_error FROM documents d WHERE d.status IN ('pending','HTTP_error','unknown_error','validation_failed','access_restricted')"),['document_id','direct_url','status','attempts','last_error'])
    write_csv('metadata/residual_issues.csv',c.execute('SELECT * FROM issues WHERE resolved=0'),[r[1] for r in c.execute('PRAGMA table_info(issues)')])
    c.close()
if __name__=='__main__':
    {'discover':discover,'download':download,'export':export}[sys.argv[1]]()

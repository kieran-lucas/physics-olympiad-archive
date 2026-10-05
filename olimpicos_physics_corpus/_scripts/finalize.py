"""Post-acquisition metadata correction, exhaustive reconciliation and disk verification."""
import json, re, sqlite3, hashlib, os, sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from collections import Counter
from bs4 import BeautifulSoup
from corpus import ROOT, db, export, write_csv, safe, now

def finalize():
    c=db(); checks=[]
    # Canonical storage owner is determined by source metadata, independently of completion order.
    for f in list(c.execute('SELECT * FROM files')):
        d=c.execute('SELECT d.*,c.slug FROM documents d JOIN competitions c ON c.id=d.competition_id WHERE file_id=? ORDER BY c.slug,d.year,d.original_filename,d.direct_url,d.id LIMIT 1',(f['id'],)).fetchone()
        name=safe(Path(d['original_filename']).stem)+'__'+f['sha256'][:16]+Path(d['original_filename']).suffix.lower()
        rel=Path('originals')/safe(d['slug'])/safe(d['year'] or 'unknown-year')/name
        old=ROOT/f['local_path'];new=ROOT/rel
        if old!=new:
            new.parent.mkdir(parents=True,exist_ok=True)
            if new.exists():
                with new.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
                if digest!=f['sha256']:raise RuntimeError('Canonical file collision')
                old.unlink()
            else:os.replace(old,new)
            c.execute('UPDATE files SET local_path=? WHERE id=?',(rel.as_posix(),f['id']))
    shared=[]
    for f in c.execute("SELECT f.* FROM files f WHERE (SELECT count(DISTINCT pd.problem_id) FROM documents d JOIN problem_documents pd ON pd.document_id=d.id WHERE d.file_id=f.id AND d.document_type IN ('problem','solution','combined'))>1").fetchall():
        refs=list(c.execute("SELECT DISTINCT p.* FROM problems p JOIN problem_documents pd ON pd.problem_id=p.id JOIN documents d ON d.id=pd.document_id WHERE d.file_id=? AND d.document_type IN ('problem','solution','combined')",(f['id'],)))
        individual=list(c.execute("SELECT * FROM documents WHERE file_id=? AND (document_scope='problem' OR instr(notes,'Identical SHA-256 bytes')>0) AND document_type IN ('problem','solution','combined')",(f['id'],)))
        if not individual:continue
        secs={p['archive_section_id'] for p in refs}
        scope='unknown'
        if len(secs)==1:
            total=c.execute('SELECT count(*) FROM problems WHERE archive_section_id=?',(next(iter(secs)),)).fetchone()[0]
            if total==len(refs):scope='round' if refs[0]['session'] or refs[0]['section'] not in ['','Problems'] else 'full_exam'
        note='Identical SHA-256 bytes are source-linked to multiple logical problem rows. Scope reviewed from the complete set of source relationships; no individual PDF is asserted.'
        for d in individual:
            c.execute('UPDATE documents SET document_scope=?,notes=CASE WHEN instr(notes,?)>0 THEN notes ELSE notes || ? END WHERE id=?',(scope,note,' '+note,d['id']))
            c.execute("UPDATE problem_documents SET relationship='shared_file' WHERE document_id=?",(d['id'],))
        shared.append(dict(file_id=f['id'],path=f['local_path'],logical_problems=len(refs),scope=scope,document_records_corrected=len(individual)))
    (ROOT/'reports/shared_file_scope_review.json').write_text(json.dumps(shared,indent=2),encoding='utf-8')
    c.commit()
    # Independently reread all saved HTML, checking every href/data material URL and every source number.
    for comp in c.execute('SELECT * FROM competitions'):
        s=BeautifulSoup((ROOT/'metadata/pages'/f'{comp["slug"]}.html').read_text(encoding='utf-8'),'html.parser')
        expected=set(); rows=0;bands=0;years=[]
        for art in s.select('article'):
            year=art.select_one('.year').get_text(strip=True);years.append(year)
            rows+=len(art.select('li .n'));bands+=len(art.select('.band'))
            for a in art.select('a[href]'):expected.add(urljoin(comp['source_page_url'],a['href']))
            for b in art.select('button'):
                for attr in ['data-x','data-tp','data-ts','data-z']:
                    if b.get(attr):expected.add(urljoin(comp['source_page_url'],b[attr]))
        for a in s.select('a[href]'):
            if not a.find_parent('article') and a['href'].startswith(('http','/files/')) and 'discord.gg' not in a['href']:expected.add(urljoin(comp['source_page_url'],a['href']))
        actual={r[0] for r in c.execute('SELECT direct_url FROM documents WHERE competition_id=?',(comp['id'],))}
        actual_years={r[0] for r in c.execute('SELECT DISTINCT year FROM archive_sections WHERE competition_id=?',(comp['id'],))}
        actual_rows=c.execute('SELECT count(*) FROM problems WHERE competition_id=?',(comp['id'],)).fetchone()[0]
        actual_bands=c.execute('SELECT count(*) FROM archive_sections WHERE competition_id=?',(comp['id'],)).fetchone()[0]
        result=dict(competition=comp['slug'],source_years=len(years),source_bands=bands,source_rows=rows,source_unique_urls=len(expected),missing_urls=sorted(expected-actual),extra_urls=sorted(actual-expected),year_difference=sorted(set(years)^actual_years),logical_rows_match=rows==actual_rows,bands_match=bands==actual_bands)
        checks.append(result)
        if result['missing_urls'] or result['year_difference'] or not result['logical_rows_match'] or not result['bands_match']:
            c.execute('INSERT INTO issues(competition_id,kind,source_url,detail) VALUES(?,?,?,?)',(comp['id'],'parse_warning',comp['source_page_url'],json.dumps(result)))
        else:c.execute("UPDATE competitions SET discovery_status='processed' WHERE id=?",(comp['id'],))
    (ROOT/'reports/discovery_reconciliation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    disk=[]
    for f in c.execute('SELECT * FROM files'):
        p=ROOT/f['local_path'];errors=[]
        if not p.exists():errors.append('missing on disk')
        else:
            if p.stat().st_size!=f['byte_size']:errors.append('size mismatch')
            with p.open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
            if sha!=f['sha256']:errors.append('hash mismatch')
        if errors:disk.append(dict(file_id=f['id'],path=f['local_path'],errors=errors))
    stored={str((ROOT/f[0]).resolve()).casefold() for f in c.execute('SELECT local_path FROM files')}
    orphans=[str(p.relative_to(ROOT)) for p in (ROOT/'originals').rglob('*') if p.is_file() and str(p.resolve()).casefold() not in stored and p.suffix!='.part']
    parts=[str(p.relative_to(ROOT)) for p in (ROOT/'originals').glob('*.part')]
    fk=list(c.execute('PRAGMA foreign_key_check'));integrity=c.execute('PRAGMA integrity_check').fetchone()[0]
    terminal=['downloaded','content_duplicate','already_present','index_only','source_unavailable','access_restricted','HTTP_error','validation_failed','unknown_error']
    unexplained=list(c.execute('SELECT id,status FROM documents WHERE status NOT IN ('+','.join('?' for _ in terminal)+')',terminal))
    no_sources=c.execute('SELECT count(*) FROM documents WHERE id NOT IN (SELECT document_id FROM document_sources)').fetchone()[0]
    no_mapping=c.execute('SELECT count(*) FROM problems WHERE id NOT IN (SELECT problem_id FROM problem_documents)').fetchone()[0]
    canonical_failures=len(disk)+len(orphans)+len(parts)+len(fk)+(integrity!='ok')+len(unexplained)+no_sources+no_mapping
    summary=dict(generated_at=now(),competitions=c.execute('SELECT count(*) FROM competitions').fetchone()[0],processed_competitions=c.execute("SELECT count(*) FROM competitions WHERE discovery_status='processed'").fetchone()[0],competition_years=c.execute('SELECT count(*) FROM (SELECT DISTINCT competition_id,year FROM archive_sections)').fetchone()[0],archive_sections=c.execute('SELECT count(*) FROM archive_sections').fetchone()[0],year_sessions=c.execute('SELECT count(*) FROM (SELECT DISTINCT competition_id,year,session FROM problems)').fetchone()[0],logical_problem_rows=c.execute('SELECT count(*) FROM problems').fetchone()[0],aggregate_rows=c.execute("SELECT count(*) FROM problems WHERE inventory_granularity='aggregate'").fetchone()[0],document_records=c.execute('SELECT count(*) FROM documents').fetchone()[0],unique_files=c.execute('SELECT count(*) FROM files').fetchone()[0],file_bytes=c.execute('SELECT coalesce(sum(byte_size),0) FROM files').fetchone()[0],distinct_acquired_urls=c.execute('SELECT count(DISTINCT direct_url) FROM documents WHERE file_id IS NOT NULL').fetchone()[0],not_published_individual_rows=c.execute("SELECT count(*) FROM problems WHERE publication_status='not_published'").fetchone()[0],source_authored_titles=c.execute("SELECT count(*) FROM problems WHERE title_provenance='source_authored'").fetchone()[0],parser_warnings=c.execute("SELECT count(*) FROM issues WHERE kind='parse_warning' AND resolved=0").fetchone()[0],document_statuses=dict(c.execute('SELECT status,count(*) FROM documents GROUP BY status').fetchall()),validation_statuses=dict(c.execute('SELECT validation_status,count(*) FROM files GROUP BY validation_status').fetchall()),sqlite_integrity=integrity,foreign_key_violations=len(fk),disk_verification_failures=disk,orphan_files=orphans,part_files=parts,unexplained_document_records=[dict(x) for x in unexplained],documents_without_provenance=no_sources,problems_without_document_mapping=no_mapping,canonical_reconciliation_failures=canonical_failures)
    summary['sha256_duplicate_downloads_avoided']=summary['distinct_acquired_urls']-summary['unique_files']
    summary['redundant_document_copies_avoided']=sum(summary['document_statuses'].get(x,0) for x in ['downloaded','content_duplicate','already_present'])-summary['unique_files']
    summary['unresolved_document_errors']=sum(summary['document_statuses'].get(x,0) for x in ['pending','HTTP_error','validation_failed','unknown_error','access_restricted'])
    summary['source_content_mismatches']=c.execute("SELECT count(*) FROM issues WHERE kind='source_content_mismatch' AND resolved=0").fetchone()[0]
    summary['unresolved_errors']=summary['unresolved_document_errors']+summary['parser_warnings']+summary['source_content_mismatches']
    summary['zero_unexplained_records']=canonical_failures==0 and summary['parser_warnings']==0
    (ROOT/'reports/summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    coverage=[]
    for comp in c.execute('SELECT * FROM competitions'):
        cid=comp['id'];statuses=dict(c.execute('SELECT status,count(*) FROM documents WHERE competition_id=? GROUP BY status',(cid,)).fetchall())
        coverage.append(dict(competition=comp['name'],slug=comp['slug'],category=comp['category'],processed=comp['discovery_status'],years=c.execute('SELECT count(DISTINCT year) FROM archive_sections WHERE competition_id=?',(cid,)).fetchone()[0],sections=c.execute('SELECT count(*) FROM archive_sections WHERE competition_id=?',(cid,)).fetchone()[0],logical_problem_rows=c.execute('SELECT count(*) FROM problems WHERE competition_id=?',(cid,)).fetchone()[0],document_records=sum(statuses.values()),downloadable_document_records=sum(n for k,n in statuses.items() if k!='index_only'),acquired_document_records=sum(statuses.get(k,0) for k in ['downloaded','content_duplicate','already_present']),unique_files_referenced=c.execute('SELECT count(DISTINCT file_id) FROM documents WHERE competition_id=?',(cid,)).fetchone()[0],index_only=statuses.get('index_only',0),individual_not_published=c.execute("SELECT count(*) FROM problems WHERE competition_id=? AND publication_status='not_published'",(cid,)).fetchone()[0],unavailable_documents=statuses.get('source_unavailable',0),download_failures=sum(statuses.get(k,0) for k in ['pending','HTTP_error','unknown_error','access_restricted']),validation_failures=statuses.get('validation_failed',0),duplicate_document_storage_avoided=statuses.get('content_duplicate',0),source_content_mismatches=c.execute("SELECT count(*) FROM issues WHERE competition_id=? AND kind='source_content_mismatch' AND resolved=0",(cid,)).fetchone()[0],unresolved_parser_warnings=c.execute("SELECT count(*) FROM issues WHERE competition_id=? AND kind='parse_warning' AND resolved=0",(cid,)).fetchone()[0]))
    write_csv('reports/competition_coverage.csv',coverage)
    c.commit();export();print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':finalize()

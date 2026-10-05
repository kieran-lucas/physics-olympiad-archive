"""Give each source DOM band its own identity, even when adjacent bands share a label."""
import sqlite3,re,json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from corpus import ROOT,db,text
c=db()
if not any(r[1]=='source_band_index' for r in c.execute('PRAGMA table_info(archive_sections)')):
    c.commit();c.execute('PRAGMA foreign_keys=OFF')
    c.execute('CREATE TABLE IF NOT EXISTS archive_sections_new(id INTEGER PRIMARY KEY,competition_id INTEGER REFERENCES competitions(id),year TEXT,session TEXT,section TEXT,source_page_url TEXT,expected_problems INTEGER,source_band_index INTEGER,UNIQUE(competition_id,source_page_url,source_band_index))')
    c.execute('INSERT INTO archive_sections_new(id,competition_id,year,session,section,source_page_url,expected_problems,source_band_index) SELECT *,-id FROM archive_sections')
    c.execute('DROP TABLE archive_sections');c.execute('ALTER TABLE archive_sections_new RENAME TO archive_sections')
    c.commit();c.execute('PRAGMA foreign_keys=ON')
if not any(r[1]=='archive_section_id' for r in c.execute('PRAGMA table_info(documents)')):
    c.execute('ALTER TABLE documents ADD COLUMN archive_section_id INTEGER REFERENCES archive_sections(id)')
seen=set();changes=json.loads((ROOT/'reports/band_identity_repairs.json').read_text(encoding='utf-8')) if (ROOT/'reports/band_identity_repairs.json').exists() else []
for comp in c.execute('SELECT * FROM competitions').fetchall():
    s=BeautifulSoup((ROOT/'metadata/pages'/f'{comp["slug"]}.html').read_text(encoding='utf-8'),'html.parser')
    for art in s.select('article'):
        year=text(art,'.year');session='';bandindex=0;bandcount=len(art.select('.band'))
        for band in art.select('.stage,.band'):
            if 'stage' in band.get('class',[]):session=text(band,'.slabel');continue
            bandindex+=1;section=text(band,'.rlabel');page=comp['source_page_url']+'#'+art['id']
            rows=[li for li in band.select('li') if li.select_one('.n')]
            pids=[]
            for li in rows:
                b=li.select_one('button[data-g]');key=b['data-g'];pids.append(c.execute('SELECT id FROM problems WHERE source_key=?',(key,)).fetchone()[0])
            match=c.execute('SELECT id FROM archive_sections WHERE competition_id=? AND source_page_url=? AND source_band_index=?',(comp['id'],page,bandindex)).fetchone()
            if match:secid=match[0]
            else:
                old=c.execute('SELECT archive_section_id FROM problems WHERE id=?',(pids[0],)).fetchone()[0]
                if old not in seen:
                    secid=old;c.execute('UPDATE archive_sections SET source_band_index=?,expected_problems=? WHERE id=?',(bandindex,len(rows),secid))
                else:
                    secid=c.execute('INSERT INTO archive_sections(competition_id,year,session,section,source_page_url,expected_problems,source_band_index) VALUES(?,?,?,?,?,?,?)',(comp['id'],year,session,section,page,len(rows),bandindex)).lastrowid
                    changes.append(dict(competition=comp['slug'],year=year,section=section,band_index=bandindex,problem_ids=pids,new_section_id=secid))
            seen.add(secid)
            for pid in pids:c.execute('UPDATE problems SET archive_section_id=? WHERE id=?',(secid,pid))
            urls=set()
            for a in band.select('a[href]'):urls.add(urljoin(comp['source_page_url'],a['href']))
            for b in band.select('button'):
                for attr in ['data-x','data-tp','data-ts','data-z']:
                    if b.get(attr):urls.add(urljoin(comp['source_page_url'],b[attr]))
            for url in urls:
                c.execute('UPDATE documents SET archive_section_id=? WHERE competition_id=? AND year=? AND direct_url=? AND section=?',(secid,comp['id'],year,url,section))
                if bandcount>1:
                    c.execute("UPDATE documents SET document_scope=?,notes=notes || ? WHERE competition_id=? AND year=? AND direct_url=? AND document_scope='full_exam'",('round' if comp['slug']=='mosphys' else 'unknown',' Shared paper belongs to one of multiple distinct source bands in this year; band identity preserved independently of repeated display labels.',comp['id'],year,url))
        c.commit()
c.execute("UPDATE issues SET resolved=1 WHERE kind='parse_warning' AND detail LIKE '%bands_match%' AND competition_id IN (SELECT id FROM competitions WHERE slug IN ('oibf','mosphys'))")
c.commit()
(ROOT/'reports/band_identity_repairs.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print('Distinct source bands:',c.execute('SELECT count(*) FROM archive_sections').fetchone()[0],'; additional band identities:',len(changes))
print('FK violations:',c.execute('PRAGMA foreign_key_check').fetchall())

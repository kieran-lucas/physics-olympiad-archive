import sqlite3,json
from pathlib import Path
from bs4 import BeautifulSoup
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite')
for slug,cid in c.execute('select slug,id from competitions').fetchall():
 s=BeautifulSoup((Path('olimpicos_physics_corpus/metadata/pages')/(slug+'.html')).read_text(encoding='utf-8'),'html.parser')
 notes=[x.get_text(' ',strip=True) for x in s.select('header p,p.source')]
 c.execute('update competitions set notes=? where id=?',(json.dumps(notes,ensure_ascii=False),cid))
# Correct shared section papers to round scope, while maintaining one physical file.
c.execute("update documents set document_scope='round',notes=notes || ' Scope corrected in audit: source links a section paper, rather than the whole exam.' where document_scope='full_exam' and section not in ('','Problems')")
for did,page,label in c.execute('select id,source_page_url,raw_link_label from documents where id not in (select document_id from document_sources)').fetchall():
 c.execute('insert into document_sources(document_id,source_page_url,locator,raw_link_label,source_attribute) values(?,?,?,?,?)',(did,page,'introduction/source-reference',label,'href'))
# The source expressly identifies WoPhO final vs selection problem groups in its archive note.
cid=c.execute("select id from competitions where slug='wopho'").fetchone()[0]
for year in ['2011','2012','2013']:
 ps=c.execute('select id,problem_identifier from problems where competition_id=? and year=? order by id',(cid,year)).fetchall()
 for idx,(pid,ident) in enumerate(ps):
  sess='final round' if year in ['2011','2012'] and idx>=len(ps)-3 else 'selection rounds'
  note='Round attribution explicitly provided in the Olimpicos archive note: last three questions in 2011/2012 are final round; all other questions are selection rounds.'
  c.execute('update problems set session=?,notes=notes || ? where id=?',(sess,note,pid))
  c.execute('update documents set session=?,notes=notes || ? where id in (select document_id from problem_documents where problem_id=?)',(sess,note,pid))
c.commit()
print('metadata corrections saved')

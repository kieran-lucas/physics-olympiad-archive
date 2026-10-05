import sqlite3,re
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite')
for pid,title,section in c.execute("select p.id,p.raw_title,p.section from problems p join competitions c on c.id=p.competition_id where c.slug='spho' and p.raw_title like 'Paper %'").fetchall():
 if re.fullmatch(r'Paper [12] 1',title):
  c.execute("update problems set inventory_granularity='aggregate',notes='Source row represents an entire Paper 1/2; its identifier is the archive row identifier. Actual PDF contains multiple questions, as confirmed by the paper instructions.' where id=?",(pid,))
  c.execute("update documents set document_scope='round' where id in (select document_id from problem_documents where problem_id=?)",(pid,))
c.commit()

import sqlite3,pymupdf
from pathlib import Path
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite')
for name in ['NBPhO_2021_Q1.pdf','NBPhO_2019_Q1.pdf','IPhO_2022_S1.pdf','WoPhO_2012_Q10.pdf','WoPhO_2012_S10.pdf']:
 row=c.execute('select f.local_path,f.page_count from documents d join files f on f.id=d.file_id where d.original_filename=?',(name,)).fetchone()
 if row:
  doc=pymupdf.open(Path('olimpicos_physics_corpus')/row[0]); t='\n'.join(p.get_text() for p in list(doc)[:2]);print(name,row,'HEAD',t[:2200], 'TAIL',doc[-1].get_text()[:600])
print('NB2021',c.execute("select expected_problems from archive_sections s join competitions c on c.id=s.competition_id where c.slug='nbpho' and year='2021'").fetchall())

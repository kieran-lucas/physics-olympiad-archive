import sqlite3,pymupdf
from pathlib import Path
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
print('mixed-role files',c.execute("select c.slug,f.id,f.local_path,group_concat(distinct d.document_type),count(distinct d.direct_url) from files f join documents d on d.file_id=f.id join competitions c on c.id=d.competition_id where document_type in ('problem','solution','combined') group by f.id having count(distinct d.document_type)>1").fetchall())
for slug,year in [('fyziklani','2026'),('fyziklani','2006'),('physicsbrawl','2025'),('opho','2020')]:
 for d in c.execute('select d.*,f.local_path from documents d join files f on f.id=d.file_id join competitions c on c.id=d.competition_id where c.slug=? and d.year=? and d.document_type=?',(slug,year,'problem')):
  doc=pymupdf.open(Path('olimpicos_physics_corpus')/d['local_path']);t='\n'.join(p.get_text() for p in list(doc)[:8]);print(d['original_filename'],'PAGES',len(doc),'TEXT',t[:6000])
  if slug=='fyziklani' and year=='2026':
   for idx in [3,4,5]:doc[idx].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(f'olimpicos_physics_corpus/reports/fyziklani_2026_page_{idx+1}.png')

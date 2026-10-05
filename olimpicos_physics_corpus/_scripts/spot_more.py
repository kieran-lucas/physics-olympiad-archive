import sqlite3
from pathlib import Path
import pymupdf
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
for pattern in ['IPhO_1967_Q1.pdf','EuPhO_2026_Q1.pdf','EuPhO_2026_S1.pdf','APhO_2021_ExperimentData.zip','NBPhO_2026_Q1.pdf','WoPhO_2012_Q10.pdf','WoPhO_2012_S10.pdf']:
 for d in c.execute('select d.*,f.local_path,f.page_count from documents d join files f on f.id=d.file_id where original_filename=?',(pattern,)):
  print(pattern,dict(d))
  if pattern.endswith('.pdf'):
   doc=pymupdf.open(Path('olimpicos_physics_corpus')/d['local_path']);t='\n'.join(p.get_text() for p in list(doc)[:2]);print(t[:2600])
   if pattern=='IPhO_1967_Q1.pdf':doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save('olimpicos_physics_corpus/reports/legacy_ipho_1967.png')

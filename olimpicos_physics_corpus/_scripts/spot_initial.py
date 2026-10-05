import sqlite3,json
from pathlib import Path
from pypdf import PdfReader
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
samples=[('ipho','2026','Theory','1','problem'),('ipho','2026','Theory','1','solution'),('ipho','2025','Theory','2','problem'),('ipho','2025','Theory','2','solution'),('ipho','1967','Theory','1','problem'),('eupho','2026','Theory','1','problem'),('eupho','2026','Theory','1','solution')]
for slug,year,section,ident,role in samples:
 rows=c.execute('select d.*,f.local_path,f.page_count,p.raw_title from problems p join competitions c on c.id=p.competition_id join problem_documents pd on pd.problem_id=p.id join documents d on d.id=pd.document_id join files f on f.id=d.file_id where c.slug=? and p.year=? and p.section=? and p.problem_identifier=? and d.document_type=? and d.original_filename not like ?',(slug,year,section,ident,role,'%tex%')).fetchall()
 for row in rows:
  p=Path('olimpicos_physics_corpus')/row['local_path'];r=PdfReader(p);t='\n'.join((x.extract_text() or '') for x in r.pages[:2]);print(dict(row));print(t[:4500]);print('\n')

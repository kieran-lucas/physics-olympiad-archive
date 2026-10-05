import sqlite3,pymupdf,json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
report=[]
for slug,year in [('fyziklani','2026'),('physicsbrawl','2025'),('usapho','2022')]:
 ds=c.execute('select d.*,f.local_path from documents d join files f on f.id=d.file_id join competitions c on c.id=d.competition_id where c.slug=? and d.year=? and d.original_filename in (?,?,?)',(slug,year,'Fyziklani_2026_Q1-58.pdf','PhysicsBrawl_2025_Q1-68.pdf','Fma_2022_Q1-25.pdf')).fetchall()
 for d in ds:
  doc=pymupdf.open(Path('olimpicos_physics_corpus')/d['local_path']);t='\n'.join(p.get_text() for p in doc)
  headings=re.findall(r'(?m)^Problem\s+([A-Z]{2}|[A-Z]\.\d+|\d+)\b',t) if slug in ['fyziklani','physicsbrawl'] else re.findall(r'(?m)^\s*(\d+)\.\s+[A-Z]',t)
  headings=list(dict.fromkeys(headings));mapped=c.execute('select count(*) from problem_documents where document_id=?',(d['id'],)).fetchone()[0]
  item=dict(slug=slug,year=year,filename=d['original_filename'],path=d['local_path'],source_mapped_problem_rows=mapped,explicit_pdf_headings=headings,pdf_heading_count=len(headings));report.append(item);print(item)
Path('olimpicos_physics_corpus/reports/full_paper_problem_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

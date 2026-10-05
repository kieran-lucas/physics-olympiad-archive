import sqlite3,pymupdf,json,zipfile
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
samples=['IPhO_2026_Q1.pdf','IPhO_2026_S1.pdf','IPhO_2025_Q2.pdf','IPhO_2025_S2.pdf','EuPhO_2026_Q1.pdf','EuPhO_2026_S1.pdf','IPhO_1967_Q1.pdf','IPhO_1967_S1.pdf','IPhO_2022_S1.pdf','NBPhO_2019_Q1.pdf','NBPhO_2019_S1.pdf','WoPhO_2012_Q11.pdf','WoPhO_2012_S11.pdf','Fma_2022_Q1-25.pdf','Fma_2022_S1-25.pdf','RuTST_2026_X_Q1.pdf','RuTST_2026_X_S1.pdf','RuTST_2026_Y_Q1.pdf','RuTST_2026_Y_S1.pdf','BPhO_2024_1_Q1.pdf','BPhO_2024_1_S1.pdf','BPhO_2024_2_Q1.pdf','Fyziklani_2026_Q1-58.pdf','Fyziklani_2026_S1-58.pdf','PhysicsBrawl_2025_Q1-68.pdf','Ortvay_1997_Q1-42.pdf','SPhO_2002_Q1.pdf','SPhO_2023_Q1.pdf','SPhO_2023_Q2.pdf','TwPhO_2026_Q1-6.pdf','APhO_2021_ExperimentData.zip']
checks=[]
for pattern in samples:
 ds=c.execute('select d.*,f.local_path,f.page_count from documents d join files f on f.id=d.file_id where original_filename=?',(pattern,)).fetchall()
 if not ds:print('PENDING/UNKNOWN SAMPLE',pattern);continue
 for d in ds:
  p=Path('olimpicos_physics_corpus')/d['local_path'];item=dict(d)
  if p.suffix.lower()=='.pdf':
   doc=pymupdf.open(p);t='\n'.join(page.get_text() for page in doc);item['first_page_text']=doc[0].get_text()[:2000];item['last_page_text']=doc[-1].get_text()[:1000];item['numbered_headings']=__import__('re').findall(r'(?m)^\s*(?:Problem\s*)?\d+[. :][^\n]{0,90}',t)[:100]
   if len(doc[0].get_text().strip())<50:
    image=Path('olimpicos_physics_corpus/reports')/(pattern+'.png');doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(image);item['rendered_image']=str(image)
   print(pattern,d['page_count'],'HEAD',item['first_page_text'][:500],'TAIL',item['last_page_text'][:200],'HEADINGS',item['numbered_headings'][:15])
  elif p.suffix.lower()=='.zip':
   with zipfile.ZipFile(p) as z:item['archive_members']=z.namelist();print(pattern,'ARCHIVE',z.namelist()[:20])
  checks.append(item)
Path('olimpicos_physics_corpus/reports/spot_check_evidence.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
# Find an actual scanned page among older material, without OCR.
for d in c.execute("select d.*,f.local_path from documents d join files f on f.id=d.file_id where d.document_type='problem' and d.year<'2010' order by d.year,c.id".replace('c.id','d.id')):
 try:
  doc=pymupdf.open(Path('olimpicos_physics_corpus')/d['local_path'])
  if len(doc[0].get_text().strip())<50:
   doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save('olimpicos_physics_corpus/reports/scanned_sample.png');Path('olimpicos_physics_corpus/reports/scanned_sample.json').write_text(json.dumps(dict(d),indent=2),encoding='utf-8');print('SCANNED SAMPLE',dict(d));break
 except Exception:pass

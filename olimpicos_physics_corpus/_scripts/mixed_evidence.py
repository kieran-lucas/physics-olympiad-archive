import sqlite3,pymupdf,json
from pathlib import Path
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
rows=c.execute("select f.id,f.local_path,c.slug,group_concat(distinct d.document_type) as roles from files f join documents d on d.file_id=f.id join competitions c on c.id=d.competition_id where d.document_type in ('problem','solution') group by f.id having count(distinct d.document_type)>1").fetchall()
checks=[]
for f in rows:
 doc=pymupdf.open(Path('olimpicos_physics_corpus')/f['local_path']);ts=[p.get_text() for p in doc];t='\n'.join(ts)
 sample=dict(f);sample['pages']=len(doc);sample['first_nonempty_text']=next((s[:1000] for s in ts if s.strip()),'');sample['last_page_text']=ts[-1][:800]
 sample['marker_lines']=[line.strip() for line in t.splitlines() if any(word in line.lower() for word in ['solutions','solution','решени','řešení','答案','解答','評分','問題','questions','problems'])][:15]
 checks.append(sample)
 if f['slug'] not in ['fyziklani','physicsbrawl']:print(json.dumps(sample,ensure_ascii=False))
Path('olimpicos_physics_corpus/reports/mixed_role_evidence.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['TwPhO_2026_Q1-6.pdf','OPhO_2022_Q1-35.pdf','RMPh_2021_Q4.pdf','OSN_2024_Q1-40.pdf']:
 d=c.execute('select f.local_path from documents d join files f on f.id=d.file_id where d.original_filename=?',(name,)).fetchone()
 if d:
  doc=pymupdf.open(Path('olimpicos_physics_corpus')/d[0]);doc[min(1,len(doc)-1)].get_pixmap(matrix=pymupdf.Matrix(1,1)).save('olimpicos_physics_corpus/reports/'+name+'.png')
print('Mixed-role file count',len(checks))

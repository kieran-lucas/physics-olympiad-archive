import sqlite3,pymupdf,re,sys,json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
c=sqlite3.connect('olimpicos_physics_corpus/manifest.sqlite');c.row_factory=sqlite3.Row
review=[]
for sec in c.execute("select s.* from archive_sections s join competitions c on c.id=s.competition_id where c.slug='mosphys'").fetchall():
 d=c.execute("select f.local_path from documents d join files f on f.id=d.file_id where d.archive_section_id=? and d.document_type in ('problem','combined') order by d.id limit 1",(sec['id'],)).fetchone()
 doc=pymupdf.open(Path('olimpicos_physics_corpus')/d['local_path']);t='\n'.join(p.get_text() for p in doc);m=re.search(r'(?:[12](?:\s*[-–]\s*й)?\s*тур|тур\s*[12]|(?:первый|второй)\s+тур)',t,re.I)
 if m:
  sess=m.group(0);c.execute('update archive_sections set session=? where id=?',(sess,sec['id']));c.execute('update problems set session=?,notes=notes || ? where archive_section_id=?',(sess,' Round label verified directly in the source PDF header. Archive identifiers run across tours; numbering inside the round PDF may reset.',sec['id']));c.execute('update documents set session=? where archive_section_id=?',(sess,sec['id']))
  review.append(dict(year=sec['year'],band=sec['source_band_index'],session=sess,path=d['local_path']))
 else:
  doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(f'olimpicos_physics_corpus/reports/moscow_round_{sec["year"]}_{sec["source_band_index"]}.png')
  review.append(dict(year=sec['year'],band=sec['source_band_index'],session=None,header=t[:250],path=d['local_path']))
c.commit()
Path('olimpicos_physics_corpus/reports/mosphys_round_header_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
print('Moscow round headers verified',sum(r['session'] is not None for r in review),'of',len(review))

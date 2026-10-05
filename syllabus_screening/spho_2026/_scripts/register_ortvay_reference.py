"""Validate an explicitly source-linked reference downloaded by normal curl HTTPS.

Acquire if absent with Windows curl.exe --fail --location --output <path>.part
https://arxiv.org/pdf/2412.13580v2 . Windows certificate trust was used after
Python's newly installed CA store failed; certificate checking was not disabled.
"""
import os
import pymupdf as fitz
import workflow as w
p=w.ROOT/'references/arxiv_2412.13580v2.pdf'
if not p.exists():
 part=p.with_suffix('.pdf.part')
 with fitz.open(part) as d:assert len(d)>0 and not d.is_repaired
 os.replace(part,p)
with fitz.open(p) as d:
 pages=len(d)
 for pn,page in enumerate(d,1):
  text=page.get_text()
  if 'Figure 10:' in text:
   print('FIGURE10 PAGE',pn,text)
   dest=w.ROOT/'renders/arxiv_2412.13580v2_figure10.png'
   page.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(dest)
   print(dest)
c=w.connect();c.execute('''create table if not exists screening_references(reference_id text primary key,screening_unit_id text references units(screening_unit_id),url text,local_path text,sha256 text,byte_size integer,page_count integer,purpose text,acquired_at text)''')
c.execute('insert or replace into screening_references values (?,?,?,?,?,?,?,?,?)',('arxiv_2412.13580v2','raw::5420','https://arxiv.org/pdf/2412.13580v2',p.relative_to(w.ROOT).as_posix(),w.digest(p),p.stat().st_size,pages,'Explicitly linked in Ortvay 2025 Q23; finite binary spin-state graph and Figure 10 needed to interpret its topology task.',w.now()));c.commit()
w.writejson(w.ROOT/'references/arxiv_2412.13580v2.provenance.json',dict(c.execute('select * from screening_references where reference_id=?',('arxiv_2412.13580v2',)).fetchone()))
print('Reference PDF validated and provenance registered outside immutable acquisition corpus.')

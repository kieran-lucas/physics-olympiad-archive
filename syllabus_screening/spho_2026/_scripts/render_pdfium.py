"""Cached alternate rendering for source pages with MuPDF glyph/layout failures."""
import argparse,hashlib
import pypdfium2 as pdfium
import workflow as w
p=argparse.ArgumentParser();p.add_argument('file_id',type=int);p.add_argument('pages',type=int,nargs='+');a=p.parse_args()
c=w.connect();f=c.execute('select * from source_files where id=?',(a.file_id,)).fetchone();assert f
source=w.RAW/f['local_path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==f['sha256']
pdf=pdfium.PdfDocument(source);records=[]
for n in a.pages:
 assert 1<=n<=len(pdf)
 dest=w.ROOT/'renders'/f['sha256'][:16]/f'page_{n:03d}_pdfium.png';dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  page=pdf[n-1];bitmap=page.render(scale=2);bitmap.to_pil().save(dest);bitmap.close();page.close()
 records.append(dict(file_id=a.file_id,source_sha256=f['sha256'],page=n,path=dest.relative_to(w.ROOT).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),renderer='pypdfium2',version=pdfium.PYPDFIUM_INFO.version,created_or_verified_at=w.now()))
 print(dest)
pdf.close();w.writejson(w.ROOT/'renders'/f['sha256'][:16]/'pdfium_render_validation.json',records)

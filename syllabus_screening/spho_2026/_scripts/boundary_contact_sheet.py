"""Rendered page overview for boundary inspection; never a physics classifier."""
import sys
from PIL import Image,ImageDraw
import pymupdf as fitz
import workflow as w
fid=int(sys.argv[1]);c=w.connect();f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
pages=[int(x) for x in sys.argv[2:]] or list(range(1,f['page_count']+1))
folder=w.ROOT/'renders'/f['sha256'][:16];folder.mkdir(parents=True,exist_ok=True)
with fitz.open(w.RAW/f['local_path']) as doc:
 for offset in range(0,len(pages),8):
  group=pages[offset:offset+8];thumbs=[]
  for number in group:
   p=doc[number-1];image_path=folder/f'page_{number:03d}.png'
   if not image_path.exists():p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(image_path)
   c.execute('insert or replace into renders values (?,?,?,?)',(fid,number,image_path.relative_to(w.ROOT).as_posix(),w.now()))
   img=Image.open(image_path).convert('RGB');img.thumbnail((620,880))
   thumbs.append((number,img))
  height=max(img.height for _,img in thumbs)+28
  sheet=Image.new('RGB',(1260,((len(thumbs)+1)//2)*height),'#ddd');draw=ImageDraw.Draw(sheet)
  for i,(number,img) in enumerate(thumbs):
   x=(i%2)*630;y=(i//2)*height;draw.text((x+10,y+6),f'FILE {fid} / PHYSICAL PAGE {number}',fill='black');sheet.paste(img,(x,y+25))
  path=folder/f'boundary_contact_{group[0]:03d}_{group[-1]:03d}.jpg';sheet.save(path,quality=92);print(path)
c.commit()

"""Typography-based navigation pack for source statements in combined PDFs.

This exposes text for content reading; it never decides syllabus eligibility.
Specific 2026 Fyziklani layout: bold Problem XX, slanted statement, italic
author anecdote terminating the statement. Full extraction and page renders
remain available to verify equations, diagrams and any uncertain boundary.
"""
import re,sys
import pymupdf as fitz
import workflow as w
fid=int(sys.argv[1]);c=w.connect();f=c.execute('select * from source_files where id=?',(fid,)).fetchone()
pack=[];active=None;warnings=[]
with fitz.open(w.RAW/f['local_path']) as doc:
 for pn,page in enumerate(doc,1):
  for b in page.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    spans=line['spans'];text=''.join(s['text'] for s in spans)
    m=re.match(r'^(?:Problem|Úloha) ([A-Za-z]+(?:\.\d+|\d*)|\d+)\s',text)
    if m and text.startswith('Úloha ') and not re.fullmatch(r'[A-Z]{2}|\d+',m[1]):m=None
    if m:
     if active:warnings.append('Unterminated '+active['number'])
     active={'number':m[1],'heading':text,'page_start':pn,'page_end':pn,'text':[],'locations':[]};pack.append(active)
     continue
    if active:
     # Source 2025 Brawl Q55 has no italic author credit. Its actual regular-font
     # solution starts with this inspected sentence; do not absorb the solution.
     if fid==3101 and active['number']=='55' and text.startswith('First, we compute'):
      active['terminated_by_explicit_solution_start']=True;active=None;continue
     # Header/footer use separate bold fonts and are not statement content.
     if spans and all(('Roman8-Bold' in s['font'] or ('Roman9-Bold' in s['font'] and s['text'].strip().isdigit())) for s in spans):continue
     # An italic Hint label is statement evidence, not an author credit.
     if re.match(r'^(?:Hint|Nápověda)\b',text.lstrip()):
      active['text'].append(text);active['page_end']=pn
      active['locations'].append({'page':pn,'bbox':list(line['bbox'])})
      continue
     kept=[];end=False
     for s in spans:
      if re.fullmatch(r'LMRoman\d+-Italic',s['font']):end=True;break
      kept.append(s['text'])
     if ''.join(kept).strip():
      active['text'].append(''.join(kept));active['page_end']=pn
      active['locations'].append({'page':pn,'bbox':list(line['bbox'])})
     if end:active['terminated_by_author_note']=True;active=None
if active:warnings.append('Unterminated '+active['number'])
for r in pack:r['text']='\n'.join(r['text'])
w.writejson(w.ROOT/'cache'/f'{f["sha256"]}.statement_pack.json',{'file_id':fid,'statements':pack,'warnings':warnings})
lower=int(sys.argv[2]) if len(sys.argv)>2 else 0;upper=int(sys.argv[3]) if len(sys.argv)>3 else len(pack)
print('FILE',fid,'statements',len(pack),'warnings',warnings)
for r in pack[lower:upper]:print('\n'+r['heading']+' / PAGES '+str(r['page_start'])+'-'+str(r['page_end'])+'\n'+r['text'])

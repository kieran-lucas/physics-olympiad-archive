"""Locate complete selected printed numbered statements in an existing cache.

Only a reading aid. Printed page renders/boundary evidence remain authoritative.
"""
import re,sys
import workflow as w
fid=int(sys.argv[1]);data=w.cache(fid)
text='\n'.join('\nPHYSICAL PAGE '+str(p['page'])+'\n'+p['text'] for p in data['pages'])
for number in map(int,sys.argv[2:]):
    start=re.search(r'(?m)^\s*'+str(number)+r'\.\s',text)
    if not start:raise RuntimeError('Heading not found; inspect full cache/render for '+str(number))
    end=re.search(r'(?m)^\s*'+str(number+1)+r'\.\s',text[start.end():])
    statement=text[start.start():start.end()+end.start() if end else len(text)]
    print('\nFILE',fid,'PRINTED Q',number,'\n'+statement)

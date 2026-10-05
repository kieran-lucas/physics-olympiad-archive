"""Print cached source headings for actual boundary review; never classify physics.

Candidates require source inspection and explicit acceptance before derivation.
"""
import re,sys
import workflow as w
c=w.connect()
for slug in sys.argv[1:]:
 for r in c.execute("select * from containers where competition_slug=? and status!='expanded_content_verified' order by year desc,source_problem_id",(slug,)):
  d=w.cache(r['source_file_id']); hits=[]
  for p in d['pages']:
   lines=p['text'].splitlines()
   for i,s in enumerate(lines):
    if re.search(r'^\s*(?:Problem|Question|Qu)\s*\d+(?:\.(?!\d))?(?:\s|$)|^\s*\d+\s+Question\s+\d+|^\s*Section\s+[A-Z]\b|【문제\s*\d+】',s):
     hits.append({'page':p['page'],'heading':s.strip(),'previous':' '.join(lines[max(0,i-2):i]).strip()})
  print(r['source_problem_id'],r['source_file_id'],slug,r['year'],'pages',len(d['pages']),'chars',sum(len(p['text']) for p in d['pages']))
  print(hits)

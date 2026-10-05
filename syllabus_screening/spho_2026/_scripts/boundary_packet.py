"""Display cached page boundary evidence for manual inventory review.

This does not infer boundaries, change decisions, or mark papers complete.
Reuse prior full statement inspections; inspect renders for unreadable pages.
"""
import argparse
import re
import workflow as w

p=argparse.ArgumentParser()
p.add_argument('competition')
p.add_argument('--limit',type=int,default=30)
p.add_argument('--offset',type=int,default=0)
p.add_argument('--max-pages',type=int,default=10000)
p.add_argument('--compact',action='store_true')
p.add_argument('--brief',action='store_true',help='Compact inventory display; still includes every page')
a=p.parse_args()
c=w.connect()
rows=c.execute("""select b.file_id,f.page_count from paper_boundary_audit b
 join source_files f on f.id=b.file_id
 where b.status!='full_paper_boundaries_verified' and f.page_count<=?
 and exists(select 1 from units u where u.source_file_id=b.file_id
 and u.competition_slug=?) order by b.file_id limit ? offset ?""",
 (a.max_pages,a.competition,a.limit,a.offset)).fetchall()
for r in rows:
    us=c.execute('select problem_number,page_start,page_end,evidence from units where source_file_id=?',(r['file_id'],)).fetchall()
    print('\nFILE',r['file_id'],'PAGES',r['page_count'],'UNITS',len(us) if a.brief else [(u[0],u[1],u[2]) for u in us])
    print('PRIOR',us[0][3][:95])
    for page in w.cache(r['file_id'])['pages']:
        lines=[re.sub(r'\s+',' ',x.strip()) for x in page['text'].splitlines() if x.strip()]
        candidates=[x[:100] for x in lines if re.search(r'(?i)^(?:problem\s+[A-Z\d]|question\s*\d|(?:theoretical|experimental)\s+(?:question|problem)|part\s*[ABCD]|[TQЕE]\d[-\s]|задача\s*\d)',x)]
        if a.brief:
            useful=[x for x in lines if not re.search(r'(?i)(?:Fyziklani.*(?:year|February)|Physics Brawl.*(?:year|November)|^FYKOS$)',x)]
            print(page['page'],'H', [x[:52] for x in candidates], 'TXT', ' | '.join(useful[:2])[:48] if not candidates else '', 'END',' | '.join(lines[-2:])[:18] if not candidates else '')
        elif a.compact:
            useful=[x for x in lines if not re.fullmatch(r'(?:Road to .*|Logo| Задачи)',x)]
            print(page['page'],' | '.join(useful[:2])[:85],'H',candidates,'END',' | '.join(lines[-2:])[:35])
        else:
            print(page['page'],'TOP',' | '.join(lines[:3])[:105],'LABELS',candidates,'END',' | '.join(lines[-2:])[:55])

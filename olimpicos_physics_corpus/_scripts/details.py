from bs4 import BeautifulSoup
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
for slug in ['rutst','ipho','fyziklani','usapho','oibf']:
 s=BeautifulSoup((Path('olimpicos_physics_corpus/metadata/pages')/(slug+'.html')).read_text(encoding='utf-8'),'html.parser')
 print('\n',slug)
 if slug=='rutst': print(str(s.select_one('article'))[:9000])
 print('title notes',[(x.name,x.get('class'),x.get_text(' ',strip=True)) for x in s.find_all(['p','small']) if any(w in x.text.lower() for w in ['title','name','named'])][:15])
 print('other links',[(a.text,a.get('href')) for a in s.select('a[href]') if '/files/' in a['href'] and not a.find_parent('article')][:20])
 print('disabled', [str(x) for x in s.select('article .none')][:5])
 print('article last',str(s.select('article')[-1])[:1500])

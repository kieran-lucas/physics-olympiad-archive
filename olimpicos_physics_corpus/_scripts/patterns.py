from pathlib import Path
from bs4 import BeautifulSoup
import requests
for slug in ['ipho','fyziklani','bpho','rutst','opho','physbrawl','ortvay']:
 p=Path('olimpicos_physics_corpus/metadata/pages')/(slug+'.html')
 if not p.exists():
  x=requests.get('https://olimpicos.net/'+slug+'/',timeout=45);p.write_bytes(x.content)
 s=BeautifulSoup(p.read_bytes(),'html.parser',from_encoding='utf-8')
 print('\nARCHIVE',slug,'articles',len(s.select('article')),'scripts',[(t.get('src'),len(t.text)) for t in s.select('script')])
 print(str(s.select_one('article'))[:10500])
 print('BEFORE:',s.select_one('main').get_text(' ',strip=True)[:1100])
 print('EXTRA:',[(a.get_text(' ',strip=True),a.get('href')) for a in s.select('main a[href]') if not a.find_parent('article')][:20])

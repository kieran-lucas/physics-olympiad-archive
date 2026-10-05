from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse
import sys
sys.stdout.reconfigure(encoding='utf-8')
links=[];extra=[]
for p in Path('olimpicos_physics_corpus/metadata/pages').glob('*.html'):
 if p.stem in ['physics','robots.txt','russia-tst']:continue
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for a in s.select('article a[href]'):
  links.append(a)
  if not a['href'].lower().endswith('.pdf'): extra.append((p.stem,a.text,a['href']))
 print(p.stem,'nonarticle',[(a.text,a['href']) for a in s.select('a[href]') if not a.find_parent('article') and (a['href'].startswith('http') or '/files/' in a['href'])], 'bands',Counter(tuple(b.get('class',[])) for b in s.select('article .band')))
print('extensions',Counter(Path(urlparse(a['href']).path).suffix for a in links))
print('extras',extra[:100])
print('li class',Counter(tuple(a.get('class',[])) for a in links))
p=Path('olimpicos_physics_corpus/metadata/pages/ipho.html');s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser');print('scripts', [x.text for x in s.select('script') if x.text][:2500])

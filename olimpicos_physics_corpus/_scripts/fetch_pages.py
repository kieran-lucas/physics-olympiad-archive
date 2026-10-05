import requests,time,json,sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
r=Path('olimpicos_physics_corpus/metadata/pages')
s=BeautifulSoup((r/'physics.html').read_bytes().decode('utf-8'),'html.parser')
cs=[]
for a in s.select('a.hub-card'):
 u=urljoin('https://olimpicos.net/physics/',a['href']);slug=u.split('/')[-2]
 c=dict(slug=slug,url=u,name=a.select_one('.hub-ini').text,full_name=a.select_one('.hub-name').text,category=a.find_parent('div').find_previous_sibling('h2').text)
 cs.append(c)
 p=r/(slug+'.html')
 if not p.exists():
  x=requests.get(u,timeout=60);x.raise_for_status();p.write_bytes(x.content);time.sleep(.3)
 t=BeautifulSoup(p.read_bytes().decode('utf-8'),'html.parser')
 ars=t.select('article'); bands=t.select('article .band')
 print(slug,len(ars),len(bands),len(t.select('article li .n')),len(t.select('article a[href]')),'extras',[(a.text,a.get('href')) for a in t.select('main a[href]') if not a.find_parent('article')][:5],flush=True)
(r.parent/'competitions_discovered.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',len(cs))

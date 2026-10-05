import requests
from bs4 import BeautifulSoup
from pathlib import Path
r=Path('olimpicos_physics_corpus/metadata/pages')
for slug in ['robots.txt','physics/','ipho/','fyziklani/','bpho/','russia-tst/']:
 u='https://olimpicos.net/'+slug
 x=requests.get(u,timeout=45)
 (r/(slug.strip('/').replace('/','_')+'.html')).write_bytes(x.content)
 s=BeautifulSoup(x.content,'html.parser')
 print(u,x.status_code,len(x.content))
 print(str(s.find('main'))[:18000] if slug!='robots.txt' else x.text)

import requests,json,time
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
u='https://olimpicos.net/physics/'
r=requests.get(u,timeout=60,headers={'User-Agent':'OlimpicosPhysicsCorpus/1.0 (public research archive; conservative acquisition)'});r.raise_for_status()
Path('olimpicos_physics_corpus/metadata/landing_final.html').write_bytes(r.content)
s=BeautifulSoup(r.content.decode('utf-8'),'html.parser');live=[urljoin(u,a['href']) for a in s.select('a.hub-card')];old=[c['url'] for c in json.loads(Path('olimpicos_physics_corpus/metadata/competitions_discovered.json').read_text(encoding='utf-8'))]
result=dict(final_live_competitions=len(live),new_urls=sorted(set(live)-set(old)),removed_urls=sorted(set(old)-set(live)),scope_unchanged=set(live)==set(old))
Path('olimpicos_physics_corpus/reports/landing_scope_recheck.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)

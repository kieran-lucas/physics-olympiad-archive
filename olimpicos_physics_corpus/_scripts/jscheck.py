import requests
from bs4 import BeautifulSoup
from pathlib import Path
from collections import Counter
s=BeautifulSoup(Path('olimpicos_physics_corpus/metadata/pages/ipho.html').read_text(encoding='utf-8'),'html.parser')
u='https://olimpicos.net/assets/v/page.7e9767faf4.js'
x=requests.get(u,timeout=40);Path('olimpicos_physics_corpus/metadata/page.js').write_bytes(x.content)
print('JS',x.text[:5000])
print('embedded',Counter(k for p in Path('olimpicos_physics_corpus/metadata/pages').glob('*.html') for b in BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser').select('article button') for k in b.attrs if k in ['data-x','data-tp','data-ts','data-z']))
print('sample tex', requests.get('https://olimpicos.net/api/latex/ipho/1967-1.tex',timeout=40).status_code)

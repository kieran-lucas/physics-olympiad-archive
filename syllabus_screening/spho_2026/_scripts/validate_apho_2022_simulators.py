"""Validate preserved original JavaScript in an isolated headless browser.

No original source is edited. Every request is intercepted; only ZIP members
are served. External icon fonts are blocked and are not needed for physics.
"""
import zipfile, mimetypes, hashlib, re, subprocess
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
import workflow as w
p=next((w.ROOT/'references').glob('apho2022_simulators_*.zip'))
z=zipfile.ZipFile(p);assert z.testzip() is None
prefix=z.namelist()[0].split('/')[0]+'/'
members={n[len(prefix):]:z.read(n) for n in z.namelist() if not n.endswith('/')}
result=dict(checked_at=w.now(),archive=str(p.relative_to(w.ROOT)),sha256=w.digest(p),byte_size=p.stat().st_size,commit='5f5ccc6c003c3fc4f037007eee4c1f9c93d7391e',source_url='https://github.com/apho2022/apho2022.github.io',archive_url='https://codeload.github.com/apho2022/apho2022.github.io/zip/5f5ccc6c003c3fc4f037007eee4c1f9c93d7391e',members=[dict(path=k,byte_size=len(v),sha256=hashlib.sha256(v).hexdigest()) for k,v in members.items()],notes=['Raw acquisition corpus untouched. ZIP CRC checked. Existing experimental statements 1022 and 1026 match ZIP statements by SHA-256. Simulator HTML credits the same statement authors and HBCSE contact; index describes backup of original APhO 2022 site. Current original domain redirects to unrelated content; it was not used as the simulator source. No explicit repository license file found; attribution preserved, no new redistribution rights asserted.'],runtime={})
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(viewport=dict(width=1600,height=1100))
 def serve(route):
  parsed=urlparse(route.request.url)
  path=unquote(parsed.path.lstrip('/'))
  if parsed.netloc!='127.0.0.1:38909' or path not in members:
   route.abort();return
  route.fulfill(status=200,content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream',body=members[path])
 context.route('**/*',serve)
 for name in ['ABB','MBB']:
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:38909/'+name+'/simulation.html',wait_until='load')
  page.wait_for_timeout(700)
  if name=='ABB':
   page.locator('#simul-start-time-input').fill('5');page.locator('#simul-end-time-input').fill('55');page.locator('#time-step-input').fill('0.02')
   page.get_by_role('button',name='Plot Graph').click()
   data=page.evaluate('({count:signals.length,finite:signals.filter(Number.isFinite).length,min:Math.min(...signals.filter(Number.isFinite)),max:Math.max(...signals.filter(Number.isFinite)),firstTime:timestamps[0],lastTime:timestamps.at(-1),chart:!!graph})')
   assert data['finite']>2400 and data['chart'] and 543<data['min']<547,data
   page.locator('#vel-input').fill('10');page.locator('#vel-angle-input').fill('0')
   page.get_by_role('button',name='Plot Graph').click()
   data['moving_detector_gamma0']=page.evaluate('detectors[0].velocity(0)')
   assert data['moving_detector_gamma0']==[10,10,0]
   data['known_source_defect']='Detector construction passes v*cos(gamma) as both vx and vy and does not convert gamma degrees to radians. Gamma=0 and v=10 demonstrably gives [10,10,0], instead of [10,0,0]. Stationary-detector methods used in the official solution remain available. Original code retained without repair.'
  else:
   data=page.evaluate('({canvas:[canvas.width,canvas.height],field:[B_x,B_y],dipoleMoment:dipole_moment,chart:!!graph})')
   assert data['chart'] and all(isinstance(a,(int,float)) for a in data['field']),data
   page.locator('#measure-button').click();page.wait_for_timeout(800)
   data['measurement_samples']=page.evaluate('timestamps.length')
   assert data['measurement_samples']>5,data
   page.locator('#measure-button').click()
   data['coverage']='Initial apparatus rendering, finite field display, graph initialization and measurement toggle/sample generation checked. Full drag/drop or parameter-inference experiment not performed; no contestant measurements fabricated.'
  data['page_errors']=errors;assert not errors,errors
  shot=w.ROOT/'reviews'/('shutdown_apho_2022_'+name+'_runtime.png')
  page.screenshot(path=str(shot),full_page=True)
  result['runtime'][name]=data;page.close()
 context.close();browser.close()
result['validation_status']='archive_crc_sha_and_local_headless_loading_checked; known_acoustic_moving_detector_defect_disclosed; full_experiment_not_performed'
w.writejson(w.ROOT/'reviews/shutdown_apho_2022_simulator_validation.json',result)
print(result['validation_status'])
print(result['runtime'])

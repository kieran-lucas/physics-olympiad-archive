"""Apply source header/location corrections established during visual/content audit."""
import json,re
import workflow as w
c=w.connect()
def update(pid,label,section=None,note=None,bbox=None):
    uid='raw::'+str(pid);u=c.execute('select * from units where screening_unit_id=?',(uid,)).fetchone()
    loc=json.loads(u['location_json'] or '{}');loc['top_level_label']=label
    loc['archive_catalogue_identifier']=c.execute('select problem_identifier from source_problems where id=?',(pid,)).fetchone()[0]
    if note:loc['header_provenance_note']=note
    if bbox:loc['heading_page'],loc['heading_bbox_pdf_points']=bbox
    c.execute('update units set problem_number=?,round_or_section=?,location_json=? where screening_unit_id=?',(label,section or u['round_or_section'],json.dumps(loc,ensure_ascii=False),uid))

for pid,label in [(304,'1'),(291,'1'),(292,'2'),(286,'E1'),(287,'E2')]:
    update(pid,label,note='Actual source experiment header, rather than sequential archive catalogue number.')
for pid in [300,296]:
    update(pid,None,note='The inspected experimental document has a title but no explicit top-level question number; retain NULL rather than the archive sequential catalogue index.')
for pid in range(261,283):
    u=c.execute('select * from units where screening_unit_id=?',('raw::'+str(pid),)).fetchone()
    label=json.loads(u['location_json'])['top_level_label']
    if label.startswith(('T','E')):update(pid,label,note='Actual printed top-level T/E label; original archive catalogue identifier retained separately.')
for pid,label in [(310,'Q1'),(311,'Q2'),(312,'Q3'),(313,'Q1')]:
    update(pid,label,'Experimental' if pid==313 else 'Theory',note='Actual Q label in the official APhO 2025 header; theory/experiment remain distinct.')
for pid in [248,249,250,251]:update(pid,str(pid-247),'Theory',note='Actual scanned Theory Problem header; preceding solution text on some pages is not part of this screening unit.')
for pid,label,section in [(79,'1','Theory'),(80,'2','Theory'),(81,'3','Theory'),(82,'1','Experimental'),(83,'2','Experimental'),(55,'T-1','Theory')]:
    update(pid,label,section,note='Actual printed top-level problem header, with all internal Tasks retained.')
update(291,'1',bbox=(1,[28.34600067138672,52.475257873535156,161.6078643798828,71.986083984375]))
update(292,'2',bbox=(1,[302.61907958984375,375.8673400878906,398.26519775390625,395.378173828125]))

# Record the already inspected numbered F=ma headings; no new units/decisions.
data=w.cache(1914)
for q in range(1,26):
    found=[]
    for p in data['pages']:
        for b in p['blocks']:
            if re.match(r'^\s*'+str(q)+r'\.\s',b[4]):found.append((p['page'],b[:4]))
    assert len(found)==1,(q,found)
    pid=961+q;u=c.execute('select location_json from units where screening_unit_id=?',('raw::'+str(pid),)).fetchone()
    loc=json.loads(u[0]);loc.update(heading_page=found[0][0],heading_bbox_pdf_points=found[0][1])
    if q in [13,14]:loc['shared_context_pages']=[6]
    c.execute('update units set location_json=? where screening_unit_id=?',(json.dumps(loc),'raw::'+str(pid)))
for pid in range(987,993):
    u=c.execute('select location_json from units where screening_unit_id=?',('raw::'+str(pid),)).fetchone();loc=json.loads(u[0]);loc['shared_reference_pages']=[3]
    c.execute('update units set location_json=? where screening_unit_id=?',(json.dumps(loc),'raw::'+str(pid)))
c.commit();print('Saved actual question headers and inspected within-page locations')

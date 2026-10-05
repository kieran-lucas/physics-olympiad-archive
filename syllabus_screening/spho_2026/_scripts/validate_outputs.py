"""Validate the checkpoint and materialized reviewed subset without touching raw."""
import collections,json,os,sqlite3,zipfile
from pathlib import Path
import pymupdf as fitz
import workflow as w

c=w.connect();m=sqlite3.connect(w.CUR/'manifest.sqlite');m.row_factory=sqlite3.Row
units=[dict(r) for r in c.execute('select * from units')]
reviewed=[r for r in units if r['decision']]
selected=[r for r in reviewed if r['decision']=='KEEP' and r['confidence']!='low' and r['review_status'] in ('pass_2_complete','single_pass_complete')]
containers=[dict(r) for r in c.execute('select * from containers')]
issues=[]
def check(ok,label):
    if not ok:issues.append(label)

check(c.execute('pragma integrity_check').fetchone()[0]=='ok','screening sqlite integrity')
check(m.execute('pragma integrity_check').fetchone()[0]=='ok','curated sqlite integrity')
check(not c.execute('pragma foreign_key_check').fetchall(),'screening foreign key check')
check(len(units)==len({u['screening_unit_id'] for u in units}),'unit IDs unique')
direct=[u for u in units if not u['derived_from_whole_paper']]
source_rows=c.execute('select count(*) from source_problems').fetchone()[0]
check(len(direct)+len(containers)==source_rows,'source row reconciliation')
check(not ({u['source_problem_id'] for u in direct}&{x['source_problem_id'] for x in containers}),'containers/direct disjoint')
for container in containers:
    derived=[u for u in units if u['derived_from_whole_paper'] and u['source_problem_id']==container['source_problem_id']]
    check((len(derived)==container['derived_count']) if container['status']=='expanded_content_verified' else not derived,'container derived count '+str(container['source_problem_id']))
for u in reviewed:
    check(u['review_status'] in ('pass_2_complete','single_pass_complete') or u['review_status']=='pass_1_complete','recognized review checkpoint '+u['screening_unit_id'])
    if u['review_status']=='single_pass_complete':
        check(u['confidence']=='high' and u['decision']!='BORDERLINE','single-pass eligibility '+u['screening_unit_id'])
    check(bool(u['evidence'] and u['required_physics'] and u['decision_reason']),'actual-content evidence '+u['screening_unit_id'])
    f=c.execute('select * from source_files where id=?',(u['source_file_id'],)).fetchone()
    check(bool(f),'primary file record '+u['screening_unit_id'])
    if f:
        check((w.RAW/f['local_path']).is_file(),'source file exists '+u['screening_unit_id'])
        check(u['source_sha256']==f['sha256'],'source SHA provenance '+u['screening_unit_id'])
        check(1<=u['page_start']<=u['page_end']<=f['page_count'],'page bounds '+u['screening_unit_id'])
        check(bool(c.execute('select 1 from unit_files where screening_unit_id=? and file_id=?',(u['screening_unit_id'],f['id'])).fetchone()),'statement relationship '+u['screening_unit_id'])

# A logical equivalence may join exact reprints in different physical PDFs.
equivalence_rows=[dict(r) for r in c.execute('select * from unit_equivalences')]
equivalences={r['alias_unit_id']:r['canonical_unit_id'] for r in equivalence_rows}
by_id={u['screening_unit_id']:u for u in units}
for r in equivalence_rows:
    alias=by_id.get(r['alias_unit_id']);canonical=by_id.get(r['canonical_unit_id'])
    check(bool(alias and canonical),'equivalence endpoints '+r['alias_unit_id'])
    check(r['canonical_unit_id'] not in equivalences,'flat canonical equivalence '+r['alias_unit_id'])
    check(bool(r['evidence'] and r['verified_at']),'source-grounded equivalence '+r['alias_unit_id'])
    if alias and canonical:
        check(r['source_sha256']==alias['source_sha256'],'alias source SHA '+r['alias_unit_id'])
        if alias['decision'] and canonical['decision']:
            check(alias['decision']==canonical['decision'],'equivalent decisions agree '+r['alias_unit_id'])

curated_rows=[dict(r) for r in m.execute('select * from files')]
check(len(curated_rows)==len({r['sha256'] for r in curated_rows}),'curated content deduplication')
check({u['screening_unit_id'] for u in selected}=={r[0] for r in m.execute('select screening_unit_id from selected_problems')},'all reviewed KEEP materialized; no other decision materialized')
validation=[]
for row in curated_rows:
    src=w.RAW/row['source_file'];dest=w.CUR/row['curated_file']
    result={'file_id':row['file_id'],'curated_file':row['curated_file'],'sha256':row['sha256'],'byte_size':row['byte_size'],'page_count':None,'validation_status':'valid','kind':None,'error':''}
    try:
        check(dest.is_file(),'curated exists '+str(row['file_id']))
        check(dest.stat().st_size==row['byte_size'],'curated byte size '+str(row['file_id']))
        check(w.digest(dest)==row['sha256'],'curated hash '+str(row['file_id']))
        check(os.path.samefile(src,dest) if row['materialization']=='hardlink' else True,'hardlink identity '+str(row['file_id']))
        with open(dest,'rb') as f:magic=f.read(16)
        if magic.startswith(b'%PDF-'):
            with fitz.open(dest) as pdf:
                check(pdf.is_pdf and len(pdf)>0,'PDF opens '+str(row['file_id']))
                check(not pdf.is_repaired,'PDF repair required '+str(row['file_id']))
                check(len(pdf)==row['page_count'],'PDF page count '+str(row['file_id']))
                result.update(kind='pdf',page_count=len(pdf))
        elif zipfile.is_zipfile(dest):
            with zipfile.ZipFile(dest) as z:
                check(z.testzip() is None,'ZIP CRC '+str(row['file_id']))
            result['kind']='zip'
        else:
            check(bool(magic),'nonzero supporting file '+str(row['file_id']))
            result['kind']='tex' if dest.suffix.lower()=='.tex' else 'other'
        original=c.execute('select * from source_files where id=?',(row['file_id'],)).fetchone()
        check(bool(original) and original['sha256']==row['sha256'],'physical provenance '+str(row['file_id']))
    except Exception as e:
        issues.append('file validation '+str(row['file_id'])+': '+str(e))
        result.update(validation_status='failed',error=str(e))
    validation.append(result)

for a in m.execute('select * from problem_files'):
    check(bool(m.execute('select 1 from files where file_id=?',(a['file_id'],)).fetchone()),'curated association physical file')
    check(bool(m.execute('select 1 from selected_problems where screening_unit_id=?',(a['screening_unit_id'],)).fetchone()),'curated association KEEP unit')
    check(bool(m.execute('select 1 from provenance where document_id=?',(a['document_id'],)).fetchone()),'curated document provenance')
    d=c.execute('select file_id from source_documents where id=?',(a['document_id'],)).fetchone()
    check(bool(d) and d['file_id']==a['file_id'],'source document-to-file mapping')
    check(bool(c.execute('select 1 from unit_files where screening_unit_id=? and file_id=? and document_id=? and role=?',tuple(a)).fetchone()),'current screening relationship preserved')

references=[dict(r) for r in m.execute('select * from reference_files')] if m.execute("select 1 from sqlite_master where name='reference_files'").fetchone() else []
for r in references:
    src=w.ROOT/r['source_file'];dest=w.CUR/r['curated_file']
    check(dest.is_file() and dest.stat().st_size==r['byte_size'],'source-linked reference exists and size')
    check(w.digest(dest)==r['sha256']==w.digest(src),'source-linked reference SHA provenance')
    check(os.path.samefile(src,dest) if r['materialization']=='hardlink' else True,'reference hardlink identity')
    check(r['screening_unit_id'] in {u['screening_unit_id'] for u in selected},'reference belongs to KEEP')
    origin=c.execute('select * from screening_references where reference_id=?',(r['reference_id'],)).fetchone()
    check(origin and origin['url']==r['url'] and origin['sha256']==r['sha256'],'explicit source reference URL provenance')
    kind='other'
    if dest.suffix.lower()=='.pdf':
        with fitz.open(dest) as pdf:
            check(pdf.is_pdf and not pdf.is_repaired and len(pdf)==r['page_count'],'source reference PDF structure')
        kind='pdf'
    elif zipfile.is_zipfile(dest):
        with zipfile.ZipFile(dest) as z:check(z.testzip() is None,'source reference ZIP CRC')
        kind='zip'
    elif dest.suffix.lower()=='.exe':
        import struct
        data=dest.read_bytes();offset=struct.unpack('<I',data[0x3c:0x40])[0]
        check(data[:2]==b'MZ' and data[offset:offset+4]==b'PE\x00\x00','source reference PE structure')
        kind='exe'
    validation.append({'file_id':'reference::'+r['reference_id'],'curated_file':r['curated_file'],'sha256':r['sha256'],'byte_size':r['byte_size'],'page_count':r['page_count'],'validation_status':'valid','kind':kind,'error':''})
check(len({r['sha256'] for r in curated_rows+references})==len(curated_rows)+len(references),'all-file SHA deduplication')

# A physical reference may support multiple KEEP units. Verify every preserved
# relationship independently of the one-per-SHA physical inventory above.
reference_associations=[dict(r) for r in m.execute('select * from reference_associations')]
expected_references=[dict(r) for r in c.execute("select r.* from screening_references r join units u on u.screening_unit_id=r.screening_unit_id where u.decision='KEEP' and u.review_status in ('single_pass_complete','pass_2_complete')")]
check({r['reference_id'] for r in reference_associations}=={r['reference_id'] for r in expected_references},'all selected reference relationships preserved')
physical_by_id={r['reference_id']:r for r in references}
origin_by_id={r['reference_id']:r for r in expected_references}
selected_by_id={u['screening_unit_id'] for u in selected}
for a in reference_associations:
    physical=physical_by_id.get(a['physical_reference_id']);origin=origin_by_id.get(a['reference_id'])
    check(bool(physical and origin),'reference association endpoints '+a['reference_id'])
    if physical and origin:
        check(a['sha256']==physical['sha256']==origin['sha256'],'shared reference hash '+a['reference_id'])
        check(a['screening_unit_id']==origin['screening_unit_id'] and a['screening_unit_id'] in selected_by_id,'shared reference KEEP unit '+a['reference_id'])
        check(a['url']==origin['url'] and a['purpose']==origin['purpose'] and a['source_file']==origin['local_path'],'shared reference full provenance '+a['reference_id'])
        metadata=m.execute('select metadata_json from selected_problems where screening_unit_id=?',(a['screening_unit_id'],)).fetchone()
        check(bool(metadata) and physical['curated_file'] in json.loads(json.loads(metadata[0])['other_relevant_files']),'shared reference selected metadata '+a['reference_id'])
        check(w.digest(w.ROOT/a['source_file'])==a['sha256'],'shared reference source hash '+a['reference_id'])

decisions=collections.Counter(u['decision'] or 'UNRESOLVED_ERROR' for u in units)
domain_rows=[]
names=['I_force_motion','II_oscillations_waves','III_ideal_gas','IV_thermodynamics','V_real_gas','VI_electric_field','VII_magnetic_field','VIII_induction','IX_em_oscillations_waves','X_wave_optics','XI_quantum_light','XII_atomic_nuclear']
for domain in names:
    counts=collections.Counter(u['decision'] for u in reviewed if domain in (u['primary_spho_domains'] or '').split(';'))
    domain_rows.append({'domain':domain,**{d:counts[d] for d in ['KEEP','BORDERLINE','REJECT']}})
format_rows=[]
for fmt in ['theory','multiple_choice','short_answer','numerical','experimental','data_analysis','mixed','unknown']:
    counts=collections.Counter(u['decision'] for u in reviewed if u['format']==fmt)
    format_rows.append({'format':fmt,'reviewed':sum(counts.values()),**{d:counts[d] for d in ['KEEP','BORDERLINE','REJECT']}})
stats={
'checked_at':w.now(),'run_status':'INCOMPLETE',
'source_rows':source_rows,'direct_units_in_inventory':len(direct),'whole_paper_containers':len(containers),
'identified_top_level_units':len(units),'reviewed_units':len(reviewed),
'verified_equivalence_records':len(equivalence_rows),
'reviewed_units_after_verified_equivalences':len({equivalences.get(u['screening_unit_id'],u['screening_unit_id']) for u in reviewed}),
'reviewed_direct_units':sum(not u['derived_from_whole_paper'] for u in reviewed),
'reviewed_derived_units':sum(u['derived_from_whole_paper'] for u in reviewed),
'decisions':dict(decisions),'decision_percentages_of_reviewed':{d:round(decisions[d]*100/len(reviewed),3) for d in ['KEEP','BORDERLINE','REJECT']},
'pending_known_units':sum(not u['decision'] for u in units),
'awaiting_content_review':sum(not u['decision'] and u['review_status']!='unresolved_source_unavailable' for u in units),
'statement_unavailable_units':sum(u['review_status']=='unresolved_source_unavailable' for u in units),
'pending_containers':sum(x['status']!='expanded_content_verified' for x in containers),
'full_top_level_inventory_known':all(x['status']=='expanded_content_verified' for x in containers) and bool(c.execute("select 1 from sqlite_master where name='paper_boundary_audit'").fetchone()) and c.execute("select count(*) from paper_boundary_audit where status!='full_paper_boundaries_verified'").fetchone()[0]==0,
'embedded_unindexed_units_discovered':c.execute('select count(*) from units where derived_from_whole_paper=1 and source_problem_id is null').fetchone()[0],
'formats':format_rows,'domains':domain_rows,
'selected_statement_physical_files':len({u['source_file_id'] for u in selected}),
'selected_all_physical_files':len(curated_rows)+len(references),'selected_raw_acquisition_files':len(curated_rows),'source_linked_reference_files':len(references),'curated_byte_size':sum(r['byte_size'] for r in curated_rows+references),
'source_linked_reference_associations':len(reference_associations),
'hardlinks':sum(r['materialization']=='hardlink' for r in curated_rows+references),'copies':sum(r['materialization']=='copy' for r in curated_rows+references),
'validated_file_types':dict(collections.Counter(r['kind'] for r in validation)),
'pdf_pages_validated':sum(r['page_count'] or 0 for r in validation),
'visual_inspection_reviewed_units':sum(u['visual_inspection_used'] for u in reviewed),
'solution_used_reviewed_units':sum(u['solution_used'] for u in reviewed),
'reviewed_source_sha256_count':len({u['source_sha256'] for u in reviewed}),
'zero_unexplained_identified_units':len(units)==sum(decisions.values()),
'zero_unexplained_source_rows':len(direct)+len(containers)==source_rows,
'whole_corpus_screening_complete':False,'validation_issues':issues,
'actual_operational_errors':c.execute('select count(*) from errors where resolved=0').fetchone()[0]
}
w.csvout(w.ROOT/'file_validation.csv',validation)
w.csvout(w.ROOT/'domain_statistics.csv',domain_rows)
w.csvout(w.ROOT/'format_statistics.csv',format_rows)
w.writejson(w.ROOT/'validation.json',stats)
print(json.dumps(stats,ensure_ascii=False,indent=2))
assert not issues,issues

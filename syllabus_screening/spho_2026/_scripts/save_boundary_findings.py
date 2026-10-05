"""Persist manually inspected missing units and complete-paper evidence.

Input contains explicit boundaries and physics decisions; no classification or
boundary inference is performed by this helper. Existing decisions are retained.
"""
import json
import sys
from pathlib import Path
import workflow as w
import fast_scope

def save(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    c=w.connect(); decisions=[]
    with c:
        for paper in data['papers']:
            fid=paper['file_id']
            source=c.execute('select * from units where source_file_id=? order by derived_from_whole_paper,screening_unit_id limit 1',(fid,)).fetchone()
            assert source is not None
            for item in paper.get('missing',[]):
                uid='derived::'+source['source_sha256'][:16]+'::embedded::'+item['label']
                assert not c.execute('select 1 from units where screening_unit_id=?',(uid,)).fetchone(), ('Already registered',uid)
                fields={k:source[k] for k in ['competition','competition_slug','competition_category','year','source_file','source_file_id','source_sha256','source_url']}
                fields.update(screening_unit_id=uid,source_problem_id=None,derived_from_whole_paper=1,round_or_section=item['section'],format=item['format'],problem_number=item['label'],problem_title=item.get('title',''),title_provenance='official' if item.get('title') else 'unknown',page_start=item['start'],page_end=item['end'],boundary_status='content_boundary_verified',location_json=json.dumps({'printed_label':item['label'],'boundary_note':paper['evidence']}))
                c.execute('insert into units('+','.join(fields)+') values('+','.join('?' for _ in fields)+')',list(fields.values()))
                c.execute("insert into unit_files select ?,file_id,document_id,role from unit_files where screening_unit_id=? and role!='solution'",(uid,source['screening_unit_id']))
                c.execute('insert into embedded_unit_discovery values(?,?,?,?)',(uid,fid,paper['evidence'],w.now()))
                decisions.append(dict(screening_unit_id=uid,decision=item['decision'],confidence=item.get('confidence','high'),required_physics=item['physics'],decision_reason=item['reason'],evidence=item['evidence'],visual_inspection_used=int(item.get('render',False)),solution_used=0))
            primary_ids={r[0] for r in c.execute('select screening_unit_id from units where source_file_id=?',(fid,))}
            for occurrence in paper.get('existing_sources',[]):
                uid=occurrence['screening_unit_id']
                assert c.execute('select 1 from units where screening_unit_id=?',(uid,)).fetchone()
                assert occurrence.get('evidence') and occurrence['start']<=occurrence['end']
                doc=c.execute("select document_id from unit_files where screening_unit_id=? and file_id=? and role='problem'",(source['screening_unit_id'],fid)).fetchone()
                assert doc is not None, ('Missing original document relationship',fid)
                c.execute('insert or ignore into unit_files values(?,?,?,?)',(uid,fid,doc[0],'problem'))
                primary_ids.add(uid)
            # Multiple acquisition records can name the same printed problem.
            # Keep every source relationship, but count known identities once.
            canonical_ids=set()
            for uid in primary_ids:
                seen=set()
                while True:
                    assert uid not in seen, ('Equivalence cycle',uid)
                    seen.add(uid)
                    alias=c.execute('select canonical_unit_id from unit_equivalences where alias_unit_id=?',(uid,)).fetchone()
                    if alias is None: break
                    uid=alias[0]
                canonical_ids.add(uid)
            observed=len(canonical_ids)
            assert observed==paper['observed_units'], (fid,observed,paper['observed_units'])
            assert paper['evidence']
            c.execute("update paper_boundary_audit set status='full_paper_boundaries_verified',observed_units=?,evidence=?,checked_at=? where file_id=?",(observed,paper['evidence'],w.now(),fid))
    c.close()
    target=w.ROOT/'reviews'/data['decision_batch']
    w.writejson(target,decisions)
    if decisions: fast_scope.save(target)
    else: fast_scope.checkpoint()

if __name__=='__main__': save(sys.argv[1])

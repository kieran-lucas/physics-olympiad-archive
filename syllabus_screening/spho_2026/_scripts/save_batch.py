"""Persist explicit content judgements written by the reviewing agent.

The input rows ARE the physics review; this script only fills provenance, dates,
and common fields. It does not predict any decision from source metadata.
"""
import json, sys
from pathlib import Path
import workflow as w

path=Path(sys.argv[1]); batch=json.loads(path.read_text(encoding='utf-8'))
c=w.connect(); records=[]
for row in batch['rows']:
    pid,decision,domains,physics,reason,evidence,pages,fmt,visual,solution,confidence,external=row
    uid=('raw::'+str(pid)) if isinstance(pid,int) else pid
    u=c.execute('select * from units where screening_unit_id=?',(uid,)).fetchone();assert u
    records.append(dict(screening_unit_id=uid,decision=decision,primary_spho_domains=domains,
      required_physics=physics,decision_reason=reason,evidence=evidence,
      page_start=pages[0],page_end=pages[1],format=fmt,visual_inspection_used=visual,
      solution_used=solution,confidence=confidence,external_physics_if_any=external,
      location_json=json.dumps({**json.loads(u['location_json'] or '{}'),'top_level_label':batch.get('labels',{}).get(str(pid),u['problem_number']),
        'boundary_note':batch.get('boundary_note','Retain all internal parts of this source top-level problem.')},ensure_ascii=False),
      boundary_status='content_boundary_verified'))
out=path.with_suffix('.decisions.json');w.writejson(out,records);w.decisions(out)

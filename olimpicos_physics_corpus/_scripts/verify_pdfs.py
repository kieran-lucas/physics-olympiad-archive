"""Independent lightweight verification of every acquired PDF; no OCR/text classification."""
import json
import pymupdf
from corpus import ROOT,db,now
c=db();results=[];failures=[]
for f in c.execute("SELECT * FROM files WHERE validation_status='valid_pdf'"):
    try:
        with pymupdf.open(ROOT/f['local_path']) as doc:
            result=dict(file_id=f['id'],local_path=f['local_path'],pypdf_page_count=f['page_count'],mupdf_page_count=doc.page_count,requires_password=doc.needs_pass)
            if doc.page_count!=f['page_count'] or doc.needs_pass:failures.append(result)
            results.append(result)
    except Exception as e:failures.append(dict(file_id=f['id'],local_path=f['local_path'],error=str(e)))
report=dict(verified_at=now(),pdfs_checked=len(results),failures=failures,total_pdf_pages=sum(x['mupdf_page_count'] for x in results),minimum_pages=min(x['mupdf_page_count'] for x in results),maximum_pages=max(x['mupdf_page_count'] for x in results))
(ROOT/'reports/independent_pdf_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'reports/independent_pdf_page_counts.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))

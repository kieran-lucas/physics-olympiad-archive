"""Apply content-grounded findings from reports/mixed_role_evidence.json; retain raw source labels."""
import json
from corpus import ROOT,db
c=db()
evidence=json.loads((ROOT/'reports/mixed_role_evidence.json').read_text(encoding='utf-8'))
# Full text inspected: these source-labelled solution URLs return statement-only files.
statement_only={'OIbF_2015_S1.pdf','OIbF_2015_S2.pdf','OIbF_2015_S3.pdf','OIbF_2014_S1-3.pdf','RMPh_2021_S4.pdf'}
report=[]
for e in evidence:
    fid=e['id']
    docs=list(c.execute("SELECT * FROM documents WHERE file_id=? AND document_type IN ('problem','solution')",(fid,)))
    mismatch=any(d['original_filename'] in statement_only for d in docs)
    if mismatch:
        for d in docs:
            if d['original_filename'] not in statement_only:continue
            note='Source link is labelled Solution, but its PDF is byte-identical to the statement and contains no solutions. Corrected normalized document_type to problem; original label, URL and bytes retained. A genuine solution was not supplied at this URL.'
            c.execute("UPDATE documents SET document_type='problem',notes=notes || ? WHERE id=?",(' '+note,d['id']))
            if not c.execute("SELECT 1 FROM issues WHERE document_id=? AND kind='source_content_mismatch'",(d['id'],)).fetchone():
                c.execute('INSERT INTO issues(competition_id,document_id,kind,source_url,detail) VALUES(?,?,?,?,?)',(d['competition_id'],d['id'],'source_content_mismatch',d['direct_url'],note))
            for p in c.execute('SELECT problem_id FROM problem_documents WHERE document_id=?',(d['id'],)).fetchall():
                if not c.execute('SELECT 1 FROM problems WHERE id=? AND instr(notes,?)>0',(p[0],note)).fetchone():
                    c.execute('UPDATE problems SET notes=notes || ? WHERE id=?',(' '+note,p[0]))
        report.append(dict(file_id=fid,path=e['local_path'],actual_content='statement_only',result='source_solution_link_mismatch'))
    else:
        # Every remaining mixed-role file was reviewed in native text. Statements and substantive answers/solutions coexist.
        for d in docs:
            c.execute("UPDATE documents SET document_type='combined',notes=notes || ? WHERE id=?",(' Content review: the physical PDF contains statements plus worked solutions, marking information or substantive answers. Source problem/solution link labels are preserved separately.',d['id']))
        report.append(dict(file_id=fid,path=e['local_path'],actual_content='combined',result='normalized_role_corrected'))
c.commit()
(ROOT/'reports/content_role_review.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Reviewed',len(report),'mixed-role files; source solution mismatches:',c.execute("SELECT count(*) FROM issues WHERE kind='source_content_mismatch'").fetchone()[0])

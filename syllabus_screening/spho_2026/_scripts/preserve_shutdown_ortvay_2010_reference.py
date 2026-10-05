import fitz
import workflow as w
c=w.connect();u=c.execute('select screening_unit_id from units where source_file_id=3130 and problem_number=?',('32',)).fetchone()[0]
p=w.ROOT/'references/ortvay_2010_q32_Berry_Mondragon_1987.pdf';part=p.with_suffix('.pdf.part');assert not p.exists()
d=fitz.open(part);assert len(d)==22 and not d.is_encrypted
for page in d:assert page.rect.width>0 and page.rect.height>0
d.close();part.replace(p)
ref=dict(reference_id='ortvay_2010_q32_Berry_Mondragon_1987',screening_unit_id=u,url='https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/07/berry161.pdf',local_path=p.relative_to(w.ROOT).as_posix(),sha256=w.digest(p),byte_size=p.stat().st_size,page_count=22,purpose='Exact research paper explicitly cited in Q32: Berry and Mondragon, Proc R Soc A 412 (1987) 53-74, DOI 10.1098/rspa.1987.0080. Author-hosted copy recovered via author publications entry 161. Physical pp1-8 actually rendered/read: explicit Pauli matrices, full coordinate PDE, current and scalar-wall boundary model supply the problem prerequisite. Copyright retained; no unrelated quantum reference added.',acquired_at=w.now())
c.execute('insert into screening_references values (?,?,?,?,?,?,?,?,?)',tuple(ref.values()));c.commit()
w.writejson(p.with_suffix('.pdf.provenance.json'),{**ref,'author_publication_index':'https://michaelberryphysics.wordpress.com/publications/','original_statement_citation':'M. V. Berry and R. J. Mondragon, Proc. R. Soc. London, Ser. A 412, 53-74 (1987)','validation_status':'22-page nonencrypted readable image PDF; title/authors/year/page range visually confirmed. Physical pp1-8 inspected, equations 3,6-12,30-42 define matrices/PDE/current/no-flux/scalar-wall model. No OCR needed.','role':'Statement-cited model/boundary reference, not an official solution of the annular task. Later paper sections not claimed inspected.','copyright_note':'Public author-hosted original copy, copyright remains with original rightsholder; preserved for source-linked archival use.'})
print('Preserved exact cited model paper with validated hash and inspection evidence.')

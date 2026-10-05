import fitz
import workflow as w
c=w.connect();u=c.execute('select screening_unit_id from units where source_file_id=3129 and problem_number=?',('40',)).fetchone()[0]
p=w.ROOT/'references/ortvay_2011_q40_US_life_tables_2007.pdf';part=p.with_suffix('.pdf.part');assert not p.exists()
d=fitz.open(part);assert len(d)==61 and not d.is_encrypted
assert 'United States Life Tables, 2007' in d[0].get_text()
for n in (8,9):assert 'Table 1. Life table for the total population' in d[n-1].get_text()
for page in d:assert page.rect.width>0 and page.rect.height>0
d.close();part.replace(p)
ref=dict(reference_id='ortvay_2011_q40_US_life_tables_2007',screening_unit_id=u,url='https://www.cdc.gov/nchs/data/nvsr/nvsr59/nvsr59_09.pdf',local_path=p.relative_to(w.ROOT).as_posix(),sha256=w.digest(p),byte_size=p.stat().st_size,page_count=61,purpose='Real life-table data available from the original statement-linked CDC Life Tables portal: US 2007 period table report published 28 September 2011. Complete total-population age/death/survival table spans physical pp8-9, actually read and rendered. Historical 2007 dataset explicitly chosen, not contemporary individual mortality guidance.',acquired_at=w.now())
c.execute('insert into screening_references values (?,?,?,?,?,?,?,?,?)',tuple(ref.values()));c.commit()
w.writejson(p.with_suffix('.pdf.provenance.json'),{**ref,'original_statement_url':'http://www.cdc.gov/nchs/products/life_tables.htm','verified_portal':'https://www.cdc.gov/nchs/products/life_tables.htm','validation_status':'61 nonencrypted readable pages; report title/year verified; actual total-population complete age table pp8-9 inspected, including terminal 100+ category.','selection_note':'Statement allows real US/country tables without fixing a year. This official report was published before the 2011 contest. Data choice remains explicit; no private account or other dataset needed.'})
print('Preserved validated official life tables linked through the statement portal.')

"""Explicit year/round associations verified during the content/material audit."""
import workflow as w
c=w.connect()
c.execute('create table if not exists supplementary_associations(screening_unit_id TEXT,document_id INTEGER,relationship TEXT,evidence TEXT,PRIMARY KEY(screening_unit_id,document_id))')
groups=[
 ('eupho','2018','theory',951,'Printed Theory marking scheme covers the three source theory problems.'),
 ('eupho','2018','experimental',952,'Printed experimental marking scheme covers the membrane experiment and its internal A-D tasks.'),
 ('eupho','2019','theory',930,'Year-level Theory marking-scheme PDF contains the three theory-problem marking criteria.'),
 ('eupho','2020','experimental',902,'ZIP member names Exp1 and Exp2, each on Windows/OSX/Linux, correspond to the two simulation experiments. Contents inventoried; binaries were not executed.'),
 ('eupho','2021','experimental',873,'ZIP members E1_hidden_wire_win.exe and E2_hot_cylinder_win.exe explicitly match the two experiments. Contents inventoried; binaries were not executed.'),
 ('ipho','2010','experimental',336,'Experiment instructions physical page 2 supplies scale and press operations explicitly referenced by both problem statements.'),
 ('ipho','2025','theory',29,'Theory instruction PDF page 2 is the General Data Sheet with constants used by the selected theory material.'),
 ('ipho','2025','experimental',30,'Experiment instructions specify measurement-table/graph quantities and uncertainty conventions for the selected experimental round.')
]
for comp,year,fmt,did,evidence in groups:
 d=c.execute('select * from source_documents where id=?',(did,)).fetchone();assert d and d['year']==year and d['file_id']
 units=c.execute("select screening_unit_id from units where competition_slug=? and year=? and format=? and decision='KEEP'",(comp,year,fmt)).fetchall();assert units
 for u in units:
  c.execute('insert or ignore into unit_files values (?,?,?,?)',(u[0],d['file_id'],did,d['document_type']))
  c.execute('insert or replace into supplementary_associations values (?,?,?,?)',(u[0],did,'associated_round_or_year_material; not asserted as problem-specific',evidence))
c.commit()
print('Associated verified year-level experiment data, marking schemes and substantive instructions')

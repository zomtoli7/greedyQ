"""Draft artifact integrity; never claim these tests exercise a CBC runtime."""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile
import xml.etree.ElementTree as ET
from jsonschema import Draft202012Validator
from tools.check_cbc_reference import REFERENCE, check_reference, validate_design

ROOT = Path(__file__).resolve().parents[1]


class CBCDraftTests(unittest.TestCase):
    def setUp(self):
        self.attributes = (REFERENCE / 'design/attributes.csv').read_text()
        self.design = (REFERENCE / 'design/design.csv').read_text()

    def changed_design(self, change):
        rows = list(csv.reader(io.StringIO(self.design)));change(rows)
        buffer = io.StringIO();csv.writer(buffer).writerows(rows);return buffer.getvalue()

    def test_golden_tables_and_expected_choices_match(self):
        report = check_reference()
        self.assertEqual((4,2,8,16,24),tuple(report[k] for k in ['attributes','blocks','tasks','profiles','synthetic_export_rows']))
        self.assertFalse(report['cbc_live_runtime_implemented'])
        self.assertFalse(report['statistical_efficiency_established'])

    def test_draft_schema_accepts_fixture_but_not_fielding_or_unsupported_modes(self):
        schema=json.loads((REFERENCE.parent/'design.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator=Draft202012Validator(schema)
        config=json.loads((REFERENCE/'study.design.json').read_text())
        self.assertEqual([],list(validator.iter_errors(config)))
        config['fielding_approval']=True
        self.assertTrue(list(validator.iter_errors(config)))
        config['fielding_approval']=False;config['block_assignment']['method']='adaptive'
        self.assertTrue(list(validator.iter_errors(config)))

    def test_blank_csvs_require_researcher_input(self):
        root = REFERENCE.parent / 'templates'
        with self.assertRaisesRegex(ValueError,'Blank template'):
            validate_design((root/'attributes-blank.csv').read_text(),(root/'design-blank.csv').read_text())

    def test_partial_duplicate_unknown_and_none_rows_are_rejected(self):
        cases = [
            (lambda r:r[1].__setitem__(3,''),'Partial'),
            (lambda r:r.append(r[1][:]),'Duplicate alternative'),
            (lambda r:r[1].__setitem__(3,'unknown'),'Unknown level'),
            (lambda r:r[1].__setitem__(2,'none'),'configured separately'),
            (lambda r:r[0].__setitem__(4,r[0][3]),'duplicate headers'),
            (lambda r:r.pop(),'number of alternatives'),
            (lambda r:r[2].__setitem__(slice(3,None),r[1][3:]),'Identical profiles'),
        ]
        for change,error in cases:
            with self.subTest(error=error),self.assertRaisesRegex(ValueError,error):
                validate_design(self.attributes,self.changed_design(change))

    def test_duplicate_or_conflicting_attribute_codes_are_rejected(self):
        rows=self.attributes.splitlines()
        with self.assertRaisesRegex(ValueError,'Duplicate level'):
            validate_design(self.attributes+'\n'+rows[1],self.design)
        with self.assertRaisesRegex(ValueError,'Conflicting attribute'):
            validate_design(self.attributes.replace('monthly_price,Monthly fee,p20','monthly_price,Other label,p20'),self.design)

    def test_bom_unicode_and_string_ids_are_preserved(self):
        attributes='\ufeff'+self.attributes.replace('Monthly fee','월 요금 中文').replace(',p10,',',001,')
        design=self.design.replace(',p10,',',001,')
        self.assertEqual(16,validate_design(attributes,design)['profiles'])
        with self.assertRaisesRegex(ValueError,'Unknown level'):
            validate_design(attributes,design.replace(',001,',',1,'))

    def test_blank_xlsx_has_exact_sheets_headers_no_formulas_macros_or_external_links(self):
        file=REFERENCE.parent/'templates/cbc-design-template.xlsx'
        ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        with zipfile.ZipFile(file) as archive:
            names=archive.namelist()
            self.assertFalse(any('vbaProject' in n or 'externalLinks/' in n for n in names))
            book=ET.fromstring(archive.read('xl/workbook.xml'))
            self.assertEqual(['Attributes','Design'],[s.attrib['name'] for s in book.findall('s:sheets/s:sheet',ns)])
            strings=[]
            if 'xl/sharedStrings.xml' in names:
                strings=[''.join(node.itertext()) for node in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('s:si',ns)]
            expected=[['attribute_id','attribute_label','level_id','level_label'],['block_id','task_id','alternative_id','attribute_1','attribute_2','attribute_3','attribute_4']]
            for index,name in enumerate(['xl/worksheets/sheet1.xml','xl/worksheets/sheet2.xml']):
                sheet=ET.fromstring(archive.read(name));self.assertEqual([],sheet.findall('.//s:f',ns))
                cells=sheet.findall('.//s:row[@r="1"]/s:c',ns)
                headers=[]
                for cell in cells:
                    value=cell.find('s:v',ns)
                    headers.append(strings[int(value.text)] if cell.attrib.get('t')=='s' else ''.join(cell.find('s:is',ns).itertext()) if cell.find('s:is',ns) is not None else value.text)
                self.assertEqual(expected[index],headers)
                for row in sheet.findall('.//s:row',ns):
                    if int(row.attrib['r'])>1:
                        self.assertEqual([],row.findall('s:c/s:v',ns))

    def test_cbc_is_not_activated_in_v02_registry(self):
        registry=json.loads((ROOT/'registry/guide-index.json').read_text())
        self.assertNotIn('cbc',registry['components'])
        result=subprocess.run([sys.executable,'tools/resolve_guide.py','--profile','cbc'],cwd=ROOT,capture_output=True)
        self.assertNotEqual(0,result.returncode)

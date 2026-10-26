"""CBC reference import tests, including hostile workbook inputs."""
import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from greedyq.cbc import CBCError, import_design, parse_csv, read_xlsx, load_design, build_preview

ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/'drafts/v0.3/cbc/golden-reference'
S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'


def workbook(attributes,design,formula=False,external=False,merged=False,shared=False):
    """Minimal independently authored OOXML test input, not a user workbook."""
    strings=[]
    def sheet(rows):
        doc=ET.Element('{'+S+'}worksheet');data=ET.SubElement(doc,'{'+S+'}sheetData')
        for ri,row in enumerate(rows,1):
            r=ET.SubElement(data,'{'+S+'}row',r=str(ri))
            for ci,value in enumerate(row,1):
                c=ET.SubElement(r,'{'+S+'}c',r=chr(64+ci)+str(ri),t='s' if shared else 'inlineStr')
                if shared:
                    strings.append(value);ET.SubElement(c,'{'+S+'}v').text=str(len(strings)-1)
                else:ET.SubElement(ET.SubElement(c,'{'+S+'}is'),'{'+S+'}t').text=value
                if formula and ri==2 and ci==1:ET.SubElement(c,'{'+S+'}f').text='1+1'
        if merged:
            cells=ET.SubElement(doc,'{'+S+'}mergeCells');ET.SubElement(cells,'{'+S+'}mergeCell',ref='A1:B1')
        return ET.tostring(doc,encoding='utf-8')
    a=sheet(list(csv.reader(io.StringIO(attributes))));d=sheet(list(csv.reader(io.StringIO(design))))
    shared_xml=ET.Element('{'+S+'}sst')
    for value in strings:ET.SubElement(ET.SubElement(shared_xml,'{'+S+'}si'),'{'+S+'}t').text=value
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr('xl/workbook.xml',f'<workbook xmlns="{S}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Attributes" sheetId="1" r:id="rId1"/><sheet name="Design" sheetId="2" r:id="rId2"/></sheets></workbook>')
        links='<Relationship Id="remote" Target="https://example.invalid/secret" TargetMode="External"/>' if external else ''
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="worksheets/sheet2.xml"/>'+links+'</Relationships>')
        z.writestr('xl/worksheets/sheet1.xml',a);z.writestr('xl/worksheets/sheet2.xml',d)
        if shared:z.writestr('xl/sharedStrings.xml',ET.tostring(shared_xml,encoding='utf-8'))
    return buffer.getvalue()


class CBCImportTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((GOLD/'study.design.json').read_text())
        self.a=(GOLD/'design/attributes.csv').read_text();self.d=(GOLD/'design/design.csv').read_text()

    def model(self,a=None,d=None,config=None):
        return import_design(config or self.config,self.a if a is None else a,self.d if d is None else d)

    def error(self,code,**kwargs):
        with self.assertRaises(CBCError) as caught:self.model(**kwargs)
        self.assertEqual(code,caught.exception.code)

    def test_csv_inline_and_shared_string_workbooks_produce_identical_models(self):
        expected=self.model()
        for shared in [False,True]:
            self.assertEqual(expected,import_design(self.config,workbook=workbook(self.a,self.d,shared=shared)))
        self.assertEqual(2,len(expected['blocks']));self.assertEqual(4,len(expected['attributes']))
        self.assertEqual(expected,load_design(GOLD))

    def test_existing_blank_workbook_requires_input(self):
        p=GOLD.parent/'templates/cbc-design-template.xlsx'
        with self.assertRaises(CBCError) as error:import_design(self.config,workbook=p.read_bytes())
        self.assertEqual('CBC002',error.exception.code)

    def test_workbook_formula_external_link_and_merge_are_rejected(self):
        for options,code in [({'formula':True},'CBC011'),({'external':True},'CBC011'),({'merged':True},'CBC012')]:
            with self.subTest(options=options),self.assertRaises(CBCError) as error:import_design(self.config,workbook=workbook(self.a,self.d,**options))
            self.assertEqual(code,error.exception.code)

    def test_invalid_archives_paths_dtd_and_macros_are_rejected(self):
        with self.assertRaises(CBCError):read_xlsx(b'not an archive')
        for path,data,code in [('xl/vbaProject.bin',b'macro','CBC011'),('xl/externalLinks/link.xml',b'<x/>','CBC011'),('../outside.xml',b'<x/>','CBC010'),('xl/attack.xml',b'<!DOCTYPE x [<!ENTITY y SYSTEM "file:///private">]><x>&y;</x>','CBC010')]:
            buf=io.BytesIO(workbook(self.a,self.d))
            with zipfile.ZipFile(buf,'a') as z:z.writestr(path,data)
            with self.subTest(path=path),self.assertRaises(CBCError) as error:read_xlsx(buf.getvalue())
            self.assertEqual(code,error.exception.code)

    def test_csv_quoted_fields_bom_unicode_and_leading_zero_codes(self):
        a='\ufeff'+self.a.replace('Monthly fee','"월 요금, 中文"').replace(',p10,',',001,')
        d=self.d.replace(',p10,',',001,').replace('\n','\r\n')
        m=self.model(a,d);self.assertEqual('월 요금, 中文',m['attributes'][0]['label']);self.assertEqual('001',m['attributes'][0]['levels'][0]['id'])
        self.error('CBC006',a=a,d=d.replace(',001,',',1,'))
        header,rows=parse_csv('a,b\n"line\nnext","He said ""yes"""\n');self.assertEqual('line\nnext',rows[0]['a']);self.assertEqual('He said "yes"',rows[0]['b'])

    def test_malformed_csv_blank_partial_and_duplicate_headers(self):
        self.error('CBC002',a='attribute_id,attribute_label,level_id,level_label\n')
        self.error('CBC003',d=self.d.replace(',p10,',',,',1))
        self.error('CBC002',d=self.d.replace('content_format','monthly_price',1))
        for text in ['a,b\n"unterminated,b','a,b\n"a"bad,b','a,b\nab"c,d']:
            with self.assertRaises(CBCError) as error:parse_csv(text)
            self.assertEqual('CBC001',error.exception.code)

    def test_duplicate_keys_profiles_none_and_unknown_levels(self):
        self.error('CBC006',d=self.d+self.d.splitlines()[1]+'\n')
        self.error('CBC006',d=self.d.replace('task_1,a,','task_1,none,',1))
        self.error('CBC006',d=self.d.replace(',p10,',',unknown,',1))
        rows=list(csv.reader(io.StringIO(self.d)));rows[2][3:]=rows[1][3:];out=io.StringIO();csv.writer(out).writerows(rows);self.error('CBC006',d=out.getvalue())

    def test_counts_weight_modes_and_fielding_are_explicit(self):
        for change,code in [(lambda c:c.update(alternatives_per_task=3),'CBC006'),(lambda c:c.update(tasks_per_block=5),'CBC006'),(lambda c:c.update(fielding_approval=True),'CBC005'),(lambda c:c['block_assignment'].update(method='adaptive'),'CBC005'),(lambda c:c['block_assignment']['weights'].update(block_c=1),'CBC005'),(lambda c:c['block_assignment']['weights'].update(block_a=True),'CBC005'),(lambda c:c.update(attribute_ids=['wrong']),'CBC002'),(lambda c:c.update(task_order='reshuffle_on_refresh'),'CBC005'),(lambda c:c.update(unknown_setting=True),'CBC005')]:
            c=copy.deepcopy(self.config);change(c)
            with self.subTest(change=change):self.error(code,config=c)

    def test_confirmed_prohibitions_none_disabled_and_source_orders(self):
        c=copy.deepcopy(self.config);c['prohibitions']=[{'monthly_price':'p10','content_format':'video'}];self.error('CBC006',config=c)
        c['prohibitions']=[{'unknown':'p10'}];self.error('CBC005',config=c)
        c.pop('prohibitions');c['none']['enabled']=False;c.update(task_order='source_order',alternative_order='source_order');self.assertFalse(self.model(config=c)['none']['enabled'])

    def test_hash_changes_with_labels_rules_and_levels_but_not_csv_newline_format(self):
        base=self.model();self.assertEqual(base,self.model(d=self.d.replace('\n','\r\n')))
        self.assertNotEqual(base['design_sha256'],self.model(a=self.a.replace('Monthly fee','Fee'))['design_sha256'])
        c=copy.deepcopy(self.config);c['none']['enabled']=False;self.assertNotEqual(base['design_sha256'],self.model(config=c)['design_sha256'])

    def test_prototype_keys_invalid_ids_and_corrupt_archives_fail_closed(self):
        c=copy.deepcopy(self.config);c['study_id']='constructor';self.error('CBC004',config=c)
        c['study_id']='unsafe id';self.error('CBC004',config=c)
        self.error('CBC004',a=self.a.replace(',p10,',',bad id,'))
        b=bytearray(workbook(self.a,self.d));b[60]^=0xff
        with self.assertRaises(CBCError):read_xlsx(bytes(b))

    def test_build_is_self_contained_and_escapes_authored_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            out,model=build_preview(GOLD,Path(tmp)/'preview.html')
            html=out.read_text();self.assertNotIn('__CBC_',html);self.assertIn('greedyQCBC',html);self.assertNotIn('src="https:',html)
            c=copy.deepcopy(self.config);c['research_question']='</script><img src=x onerror=alert(1)>'
            root=Path(tmp)/'study';(root/'design').mkdir(parents=True);(root/'study.design.json').write_text(json.dumps(c));(root/'design/attributes.csv').write_text(self.a);(root/'design/design.csv').write_text(self.d)
            p,_=build_preview(root);self.assertIn('\\u003c/script>',p.read_text());self.assertNotIn('</script><img',p.read_text())

    def test_source_path_escape_and_cli_failure_do_not_leave_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);c=copy.deepcopy(self.config);c['attributes_source']='../outside.csv';(root/'study.design.json').write_text(json.dumps(c))
            with self.assertRaises(CBCError):load_design(root)
            output=root/'out.html';result=subprocess.run([sys.executable,'-m','greedyq','cbc-build',str(root),'--output',str(output)],cwd=ROOT,capture_output=True)
            self.assertNotEqual(0,result.returncode);self.assertFalse(output.exists())

    def test_export_metadata_names_are_reserved_and_malformed_prohibitions_are_reported(self):
        c=copy.deepcopy(self.config);c['attribute_ids'][0]='chosen'
        self.error('CBC004',a=self.a.replace('monthly_price','chosen'),d=self.d.replace('monthly_price','chosen'),config=c)
        c=copy.deepcopy(self.config);c['prohibitions']=[{'monthly_price':[]}];self.error('CBC005',config=c)

    def test_json_integral_numbers_have_cross_language_integer_semantics(self):
        c=copy.deepcopy(self.config);c['alternatives_per_task']=2.0;c['tasks_per_block']=4.0;c['block_assignment']['weights']={'block_a':1.0,'block_b':1.0}
        self.assertEqual(self.model(),self.model(config=c))

    def test_descriptive_inspection_counts_without_statistical_claim(self):
        from greedyq.cbc import inspect_design
        report=inspect_design(self.model())
        self.assertEqual((2,8,16),(report['blocks'],report['tasks'],report['profiles']))
        self.assertTrue(all(sum(levels.values())==16 for levels in report['level_frequencies'].values()))
        self.assertFalse(report['statistical_efficiency_established'])
        self.assertEqual([],report['unused_levels'])

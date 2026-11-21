import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pdf_watermarking_claim_audit.audit import audit, evidence, paragraphs
from pdf_watermarking_claim_audit.phrases import PDFWATERMARKING, NOPDFWATERMARKING, GENERIC_NAMES
EXPECTED_YES = ('add watermark to pdf', 'adds watermark to pdf', 'adding watermark to pdf', 'add watermarks to pdf', 'adds watermarks to pdf', 'adding watermarks to pdf', 'watermark pdf', 'watermarks pdf', 'watermarking pdf', 'watermark pdfs', 'watermarks pdfs', 'watermarking pdfs', 'add watermark to pdfs', 'adds watermark to pdfs', 'adding watermark to pdfs', 'apply watermark to pdf', 'applies watermark to pdf', 'applying watermark to pdf', 'pdf watermark', 'pdf watermarks', 'pdf watermarking', 'watermark pdf document', 'watermarks pdf document', 'watermarking pdf document', 'watermark pdf file', 'watermarks pdf file', 'watermarking pdf file', 'add text watermark', 'adds text watermark', 'adding text watermark', 'add image watermark', 'adds image watermark', 'adding image watermark', 'stamp pdf', 'stamps pdf', 'stamping pdf', 'stamp watermark', 'stamps watermark', 'stamping watermark', 'watermark pdf page', 'watermarks pdf page', 'watermarking pdf page', 'insert watermark', 'inserts watermark', 'inserting watermark', 'add watermark to pdf file', 'adds watermark to pdf file', 'adding watermark to pdf file', 'watermark pdf pages', 'watermarks pdf pages')
EXPECTED_NO = ('no pdf watermarking', 'does not add watermark to pdf', 'does not add watermarks to pdf', 'does not watermark pdf', 'does not watermark pdfs', 'does not add watermark to pdfs', 'does not apply watermark to pdf', 'does not watermark pdf document', 'does not watermark pdf file', 'does not add text watermark', 'does not add image watermark', 'does not stamp pdf', 'does not stamp watermark', 'does not watermark pdf page', 'does not insert watermark', 'does not add watermark to pdf file', 'no pdf watermark', 'does not support pdf watermarking', 'without pdf watermarking', 'pdf watermarking not supported', 'no pdf watermarking support', 'does not watermark pdf pages', 'pdf watermarking not available', 'no watermark pdf')
EXPECTED_GENERIC = ('add_watermark', 'add_watermarks', 'apply_watermark', 'apply_watermarks', 'watermark_pdf', 'watermark_pdfs', 'add_watermark_to_pdf', 'insert_watermark', 'stamp_watermark', 'add_text_watermark', 'add_image_watermark', 'watermark_page', 'watermark_pages', 'watermark_document', 'add_pdf_watermark', 'apply_pdf_watermark', 'create_watermark', 'add_watermark_image', 'add_watermark_text', 'watermark_pdf_file', 'watermark_pdf_files', 'add_watermark_overlay', 'apply_watermark_overlay', 'stamp_watermark_on_pdf')

class AuditTests(unittest.TestCase):
    def test_phrase_oracle(self):
        self.assertEqual(PDFWATERMARKING, EXPECTED_YES)
        self.assertEqual(NOPDFWATERMARKING, EXPECTED_NO)
        self.assertEqual(GENERIC_NAMES, EXPECTED_GENERIC)
        self.assertEqual((len(set(EXPECTED_YES)), len(set(EXPECTED_NO)), len(set(EXPECTED_GENERIC))), (50, 24, 24))

    def test_routes(self):
        cases = [
            'from pypdf import PdfReader\nPdfReader()\np.merge_page(w)',
            'import pypdf\npypdf.PdfReader()\np.merge_page(w)',
            'from PyPDF2 import PdfReader\nPdfReader()\np.merge_page(w)',
            'import PyPDF2\nPyPDF2.PdfReader()\np.merge_page(w)',
            'import pypdf as pdf\nr=pdf.PdfReader()\np=r.pages[0]\np.merge_page(w)',
            'import pypdf\npypdf.PdfReader()\np.merge_transformed_page(w)',
            'from PyPDF2 import PdfReader as R\nR()\np.mergePage(w)',
            'import PyPDF2\nPyPDF2.PdfReader()\np.mergeTransformedPage(w)',
            'from fitz import open as op\nop()\np.show_pdf_page()',
            'from fitz import Document as D\nD()\np.show_pdf_page()',
            'import fitz\nd=fitz.open()\np=d[0]\np.show_pdf_page()',
            'import fitz\nfitz.Document()\np.show_pdf_page()',
            'import pymupdf\npymupdf.open()\np.show_pdf_page()',
            'import pymupdf\npymupdf.Document()\np.show_pdf_page()',
            'from pdfrw import PageMerge as M\nM(p).add(w)',
            'import pdfrw as p\np.PageMerge(x).add(w)',
            'from lib import add_watermark as f\nf()',
        ]
        cases += ['import fitz\nfitz.open()\np.%s(rotate=%d)' % (method, angle) for method in ('insert_text', 'insert_textbox') for angle in (90,180,270)]
        cases += ['import pymupdf\npymupdf.open()\np.insert_text(rotate=90)']
        cases += ['x.%s()' % name for name in EXPECTED_GENERIC]
        for case in cases:
            with self.subTest(case=case): self.assertTrue(evidence(case))

    def test_not_evidence(self):
        cases = ['import '+x for x in ('pypdf','PyPDF2','fitz','pymupdf','pdfrw','pikepdf','reportlab')]
        cases += ['import %s\n%s.PdfReader()' % (lib,lib) for lib in ('pypdf','PyPDF2')]
        cases += ['p.%s()' % m for m in ('merge_page','mergePage','merge_transformed_page','mergeTransformedPage','show_pdf_page','add')]
        cases += ['import pypdf\npypdf.PdfWriter()\np.merge_page()', 'import pypdf\npypdf.PdfReader()\np.write()', 'import pypdf\npypdf.PdfReader()\np.extract_text()', 'import pypdf\npypdf.PdfReader()\np.mergePage()', 'import PyPDF2\nPyPDF2.PdfReader()\np.merge_transformed_page()']
        cases += ['import PyPDF2\nPyPDF2.PdfReader()\np.%s()' % x for x in ('mergeRotatedPage','mergeRotatedTranslatedPage','mergeRotatedScaledPage','mergeRotatedScaledTranslatedPage','mergeScaledPage','mergeScaledTranslatedPage')]
        cases += ['import fitz\nfitz.open()', 'import fitz\nfitz.open()\np.save()', 'p.insert_text(rotate=90)', 'import fitz\nfitz.open()\np.insert_image()', 'import pdfrw\npdfrw.PageMerge()', 'import pdfrw\npdfrw.PageMerge().render()']
        cases += ['import fitz\nfitz.open()\np.%s(%s)' % (method,arg) for method in ('insert_text','insert_textbox') for arg in ('','rotate=0','rotate=angle','rotate=45','rotate="90"')]
        cases += ['from reportlab.pdfgen import canvas\ncanvas.Canvas().save()', 'import pypdf\npypdf.PdfWriter().append(x)', 'import PyPDF2\nPyPDF2.PdfWriter().merge(x)', 'import fitz\nfitz.open().insert_pdf(x)', 'import pypdf\npypdf.PdfWriter().add_page(x)', 'import pypdf\npypdf.PdfWriter().encrypt(x)', 'import pypdf\npypdf.PdfReader().rotate(90)', 'import fitz\nfitz.open().set_rotation(90)', 'import pypdf\npypdf.PdfWriter().update_page_form_field_values(x)', 'import pyhanko\npyhanko.sign_pdf()', 'import pdfplumber\npdfplumber.open()', 'from pdfminer.high_level import extract_text\nextract_text()', '"pdf watermarking"', 'x.add_watermark', 'def add_watermark(): pass\nx.add_watermark()', 'from x import add_watermark\nadd_watermark = 1\nadd_watermark()', 'import pypdf\nwith x as pypdf: pass\npypdf.PdfReader()\np.merge_page()', 'import fitz\nfitz: int = 1\nfitz.open()\np.show_pdf_page()', 'def x(:']
        cases += ['import subprocess\nsubprocess.run([%r])' % cmd for cmd in ('qpdf','pdftk','gs')]
        cases += ['client.%s()' % method for method in ('parse','begin_analyze_document','process_document','analyze_document','universal_ai','load_data','ocr','upload','Client')]
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_audit_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); doc=root/'README.md'; src=root/'app.py'
            doc.write_text('pdf watermarking')
            self.assertEqual(audit(root)['findings'][0]['severity'],'HIGH')
            self.assertEqual(audit(root)['findings'][0]['rule'],'documented-pdf-watermarking-claim-false')
            src.write_text('x.add_watermark()')
            self.assertEqual(audit(root)['verdict'],'PASS')
            doc.write_text('no pdf watermarking')
            result=audit(root); self.assertEqual(result['findings'][0]['rule'],'documented-no-pdf-watermarking-claim-false')
            src.unlink(); self.assertEqual(audit(root)['verdict'],'PASS')
            doc.write_text('pdf watermarking'); tests=root/'tests'; tests.mkdir(); (tests/'test_x.py').write_text('x.add_watermark()')
            self.assertEqual(audit(root)['findings'][0]['severity'],'MEDIUM')
            self.assertEqual(audit(root, fail_on='medium')['verdict'],'FAIL')
            for args, code in [([],0),(['--fail-on','medium'],2)]:
                p=subprocess.run([sys.executable,'-m','pdf_watermarking_claim_audit','audit',str(root),'--json']+args,capture_output=True,text=True)
                self.assertEqual(p.returncode,code); self.assertIn('message',json.loads(p.stdout)['findings'][0])
            doc.write_text('```\npdf watermarking\n```'); self.assertEqual(audit(root)['findings'],[])
            doc.write_text('`pdf watermarking`'); self.assertTrue(audit(root)['findings'])
            doc.write_text('nothing here'); self.assertEqual(audit(root)['findings'],[])
            self.assertEqual(subprocess.run([sys.executable,'-m','pdf_watermarking_claim_audit','--version'],capture_output=True,text=True).stdout.strip(),'0.1.0')

    def test_scope_ignore_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'README.md').write_text('pdf watermarking')
            (root/'a.py').write_text('import pypdf\npypdf.PdfReader()')
            (root/'b.py').write_text('p.merge_page()')
            self.assertEqual(audit(root)['verdict'],'FAIL')
            (root/'a.py').write_text('x.add_watermark()')
            self.assertEqual(audit(root,ignore=['a.py'])['verdict'],'FAIL')
            (root/'a.py').rename(root/'target.txt'); (root/'a.py').symlink_to(root/'target.txt')
            self.assertEqual(audit(root)['verdict'],'FAIL')

    def test_readme_self_audit(self):
        self.assertEqual(audit(Path(__file__).resolve().parents[1])['findings'], [])

if __name__ == '__main__': unittest.main()

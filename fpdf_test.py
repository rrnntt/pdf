import unittest
from fpdf import FPDF
import os.path

hello_world = 'Hello World!'
hello_world_file = 'out/fpdf/HelloWorld.pdf'

class TestFPDF(unittest.TestCase):
    
    def tearDown(self):
        if os.path.exists(hello_world_file):
            os.remove(hello_world_file)
    
    def test_hello_world(self):
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial','B',16)
        pdf.cell(40,10,hello_world)
        pdf.output(hello_world_file,'F')
        self.assertTrue(os.path.exists(hello_world_file))
        
    def test_pdf_write(self):
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial','',12)
        pdf.write(30, 'small text')
        pdf.set_font('Arial','',24)
        pdf.write(30, 'Large text')
        pdf.output('out/fpdf/test_pdf_write.pdf', 'F')

    def test_ttf(self):
        pdf=FPDF()
        pdf.add_font('test','','font/lmroman7-italic.ttf',uni=True)
        pdf.add_page()
        pdf.set_font('test', '', 14)
        pdf.write(10, 'hello')
        pdf.set_font('test', '', 24)
        pdf.write(10, 'hello')
        pdf.output('out/fpdf/test_ttf.pdf', 'F')
        

    def test_pdf_cell(self):
        pdf=FPDF()
        pdf.c_margin = 0.0
        pdf.add_font('symbol','','font/DejaVuSans.ttf',uni=True)
        pdf.add_page()
        f = 0.81
        font_name = 'times'
        
        text = 'small text'
        pdf.set_font(font_name,'',12)
        x,y = pdf.get_x(), pdf.get_y()
        w = pdf.get_string_width(text)
        h = pdf.font_size_pt / pdf.k
        pdf.cell(w, h, text)
        pdf.rect(x, y, w, h, '')
        pdf.line(x, y + f * h, x + w, y + f * h)
        
        text = 'Large text'
        pdf.set_font(font_name,'',24)
        x,y = pdf.get_x(), pdf.get_y()
        w = pdf.get_string_width(text)
        h = pdf.font_size_pt / pdf.k
        pdf.cell(w,h, text)
        pdf.rect(x, y, w, h, '')
        pdf.line(x, y + f * h, x + w, y + f * h)
        
        text = 'Larger text'
        pdf.set_font(font_name,'',48)
        x,y = pdf.get_x(), pdf.get_y()
        w = pdf.get_string_width(text)
        h = pdf.font_size_pt / pdf.k
        pdf.cell(w,h, text)
        pdf.rect(x, y, w, h, '')
        pdf.line(x, y + f * h, x + w, y + f * h)
        
        pdf.output('out/fpdf/test_pdf_cell.pdf', 'F')

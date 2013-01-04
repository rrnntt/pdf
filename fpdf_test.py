import unittest
from fpdf import FPDF

hello_world = 'Hello World!'
hello_world_file = 'out/HelloWorld.pdf'

class TestFPDF(unittest.TestCase):
    
    def test_hello_world(self):
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial','B',16)
        pdf.cell(40,10,hello_world)
        pdf.output(hello_world_file,'F')
        self.assertTrue(True )
        

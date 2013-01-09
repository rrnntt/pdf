# -*- coding: UTF-8 -*-
import unittest
import latex_parser as lp
from fpdf import FPDF

class TestLatexParsers(unittest.TestCase):
    
    def test_CommandParser(self):
        
        p = lp.CommandParser()
        s = '\\alpha \\beta'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), '\\alpha')
        
        p = lp.CommandParser()
        s = '\\Alpha \\beta'
        p.match( s )
        self.assertFalse( p.hasMatch() )

    def test_greek_letters(self):
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu','','font/DejaVuSansCondensed.ttf',uni=True)
        pdf.set_font('DejaVu','',16)
        
        p = lp.ListParser( lp.CommandParser() )
        s = r'\alpha\beta\gamma'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        res =  p[0].docItem.writePDF()+' '+p[1].docItem.writePDF()+' '+p[2].docItem.writePDF()
        self.assertEquals( res, u'\u03b1 \u03b2 \u03b3')
        
        pdf.write(0, res)
        pdf.output('HelloWorld.pdf', 'F')
        
    def test_WordParser(self):
        
        p = lp.WordParser()
        s = r'alpha\beta'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), 'alpha')
        self.assertEquals( p.docItem.writePDF(), 'alpha')
        
        p = lp.WordParser()
        s = r'beta alpha'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), 'beta')
        self.assertEquals( p.docItem.writePDF(), 'beta')
        
    def test_ParagraphItemParser(self):
        
        p = lp.ParagraphItemParser()
        s = r'alpha \alpha'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), 'alpha')
        self.assertEquals( p.docItem.writePDF(), 'alpha')
        
        p = lp.ParagraphItemParser()
        s = r'\alpha alpha'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), r'\alpha')
        self.assertEquals( p.docItem.writePDF(), u'\u03b1')
        
    def test_ParagraphParaser(self):
        
        p = lp.ParagraphParser()
        s = r'\alpha+\beta=gamma'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), r'\alpha+\beta=gamma' )
        self.assertEquals( p.docItem.writePDF(), u'α + β =gamma ' )
        
        p = lp.ParagraphParser()
        f = open('20k_c1.txt','rU')
        s = f.read()
        f.close()
        p.match(s)
        self.assertTrue( p.hasMatch() )
        
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu','','font/DejaVuSansCondensed.ttf',uni=True)
        pdf.set_font('DejaVu','',11)
        pdf.write(10, p.docItem.writePDF())
        pdf.output('test.pdf', 'F')

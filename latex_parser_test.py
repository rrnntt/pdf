# -*- coding: UTF-8 -*-
import unittest
import latex_parser as lp
from fpdf import FPDF

long_string = 'The year 1866 was marked by a bizarre development, an unexplained and downright  inexplicable phenomenon that surely no one has forgotten. Without getting into those rumors that upset civilians in the seaports and deranged the public'

class TestLatexParsers(unittest.TestCase):
    
    def test_CommandParser(self):
        
        p = lp.CommandParser(lp.ParagraphItemCreator)
        s = '\\alpha \\beta'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), '\\alpha')
        
        p = lp.CommandParser(lp.ParagraphItemCreator)
        s = '\\ALPHA \\beta'
        p.match( s )
        self.assertFalse( p.hasMatch() )

    def test_greek_letters(self):
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu','','font/DejaVuSansCondensed.ttf',uni=True)
        pdf.set_font('DejaVu','',16)
        
        p = lp.ListParser( lp.CommandParser(lp.ParagraphItemCreator) )
        s = r'\alpha\beta\gamma'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        res =  p[0].docItem.writePDF()+' '+p[1].docItem.writePDF()+' '+p[2].docItem.writePDF()
        self.assertEquals( res, u'\u03b1 \u03b2 \u03b3')
        
        pdf.write(0, res)
        pdf.output('test_greek_letters.pdf', 'F')
        
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

    def test_Word_cellPDF(self):
        
        p = lp.WordParser()
        s = r'alpha\beta'
        p.match(s)
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), 'alpha')
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu','','font/DejaVuSansCondensed.ttf',uni=True)
        pdf.set_font('times','',11)
        
        p.docItem.resizePDF( pdf )
        p.docItem.cellPDF( pdf )

        p.docItem.resizePDF( pdf, p.docItem.rect.x1() + 10, p.docItem.rect.y0() )
        p.docItem.cellPDF( pdf )

        p.docItem.resizePDF( pdf, p.docItem.rect.x1() + 10, p.docItem.rect.y0() )
        p.docItem.cellPDF( pdf )
        
        r = p.docItem.rect

        p = lp.CommandParser(lp.ParagraphItemCreator)
        p.match(r'\alpha')
        pdf.set_font('DejaVu','',11)

        p.docItem.resizePDF( pdf, r.x1() + 10, r.y0() )
        p.docItem.cellPDF( pdf )
        
        pdf.output('test_Word_cellPDF.pdf', 'F')
        

    def test_Paragraph_cellPDF(self):
        
        p = lp.ParagraphParser()
        s = 'The year 1866 was marked by a bizarre development, an unexplained and downright  inexplicable phenomenon that surely no one has forgotten. Without getting into those rumors that upset civilians in the seaports and deranged the public'
        s += r'\alpha, \beta, \gamma'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        p.docItem.textAlignment = 'c'
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('symbol','','font/DejaVuSansCondensed.ttf',uni=True)
        pdf.set_font('symbol','',16)
        p.docItem.resizePDF(pdf)
        p.docItem.cellPDF(pdf)
        pdf.output('test_Paragraph_cellPDF.pdf', 'F')
        
    def test_initPDF(self):
        
        p = lp.ParagraphParser()
        s = 'The year 1866 was marked by a bizarre development'
        s += r' \alpha, \beta, \gamma Hello!'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        doc = p.docItem
        pdf=FPDF()
        lp.initPDF(pdf)
        doc.resizePDF(pdf)
        doc.cellPDF(pdf)
        pdf.output('test_initPDF.pdf', 'F')
        
    def test_Greek(self):
        
        p = lp.ParagraphParser()
        s = r'alpha: \alpha, beta: \beta, gamma: \gamma, delta: \delta, epsilon: \epsilon, zeta: \zeta, eta: \eta, '
        s += r'theta: \theta, iota: \iota, kappa: \kappa, lambda: \lambda, mu: \mu, nu: \nu, xi: \xi, omicron: \omicron, '
        s += r'pi: \pi, rho: \rho, sigma: \sigma, varsigma: \varsigma, tau: \tau, upsilon: \upsilon, phi: \phi, varphi: \varphi, '
        s += r'chi: \chi, psi: \psi, omega: \omega, '
        s += r'Alpha: \Alpha, Beta: \Beta, Gamma: \Gamma, Delta: \Delta, Epsilon: \Epsilon, Zeta: \Zeta, Eta: \Eta, '
        s += r'Theta: \Theta, Iota: \Iota, Kappa: \Kappa, Lambda: \Lambda, Mu: \Mu, Nu: \Nu, Xi: \Xi, Omicron: \Omicron, '
        s += r'Pi: \Pi, Rho: \Rho, Sigma: \Sigma, Tau: \Tau, Upsilon: \Upsilon, Phi: \Phi, '
        s += r'Chi: \Chi, Psi: \Psi, Omega: \Omega '
        p.match( s )
        self.assertTrue( p.hasMatch() )
        doc = p.docItem
        pdf=FPDF()
        lp.initPDF(pdf)
        doc.resizePDF(pdf)
        doc.cellPDF(pdf)
        pdf.output('test_greek.pdf', 'F')
        
    def test_Two_Paragraphs(self):
        
        s = long_string
        pdf = FPDF()
        lp.initPDF(pdf)

        p1 = lp.ParagraphParser()
        p1.match( s )
        self.assertTrue( p1.hasMatch() )
        par1 = p1.docItem
        par1.resizePDF(pdf)
        par1.cellPDF(pdf)

        p2 = lp.ParagraphParser()
        p2.match( s )
        self.assertTrue( p1.hasMatch() )
        par2 = p2.docItem
        par2.resizePDF(pdf, 0, par1.rect.height() + 5)
        par2.cellPDF(pdf)
        
        par2.resizePDF(pdf, 0, 40)
        par2.cellPDF(pdf)
        
        par2.width = -1
        par2.resizePDF(pdf, 20, 60)
        par2.cellPDF(pdf)
        
        pdf.output('test_Two_Paragraphs.pdf', 'F')
        
    def test_Title(self):
        
        pdf = FPDF()
        lp.initPDF(pdf)
        title = lp.Title()
        title.appendItem(lp.Word('The'))
        title.appendItem(lp.Word('Title'))
        title.resizePDF(pdf)
        title.cellPDF(pdf)
        pdf.output('test_Title.pdf', 'F')
        
    def test_TitleParser(self):
        pdf = FPDF()
        lp.initPDF(pdf)
        s = r'\title {The Title}  ' 
        p = lp.TitleParser()
        p.match( s )
        self.assertTrue( p.hasMatch() )
        p.docItem.resizePDF(pdf)
        p.docItem.cellPDF(pdf)
        pdf.output('test_TitleParser.pdf', 'F')
        
    def test_DocumentParser(self):
        
        p = lp.DocumentParser()
        s = r'  \title { The Title}' + long_string + ' \n\n ' + long_string
        p.match(s)
        self.assertTrue( p.hasMatch() )
        doc = p.docItem
        doc.setPDF(FPDF())
        doc.outputPDF('test_DocumentParser.pdf')
        
    def test_Paragraphs_with_maths(self):
        
        s = 'Hello, $$maths$$ maths!'
        pdf = FPDF()
        lp.initPDF(pdf)

        p = lp.ParagraphParser()
        p.match( s )
        self.assertTrue( p.hasMatch() )
        par = p.docItem
        par.resizePDF(pdf)
        par.cellPDF(pdf)
        
        pdf.output('test_Paragraphs_with_maths.pdf', 'F')
        
        
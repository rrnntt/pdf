import unittest
from fpdf import FPDF
from document import *

def BRACKETS( *item ):
    block = InlineMathBlock(*item)
    bb = MathBigBrackets()
    bb.appendItem(block)
    return bb

b = InlineMathBlock
v = MathVariable
si = MathSign
sy = Symbol
br = BRACKETS
ss = MathSubSuperscript
sm = MathSum
f = MathFrac
fun = MathFunction
n = MathNumber
w = Word

class TestDocument(unittest.TestCase):
    
    def dummy_refit(self):
        pass
    
    def assertNotRaise(self, obj, *args, **kwargs):
        try:
            obj(*args, **kwargs)
        except:
            #print 'Assertion failed: exception raised'
            raise
    
    def do_for_each_DocItem_class(self, item):
        """These assertions must be done for each child class of DocItem"""
        # A doc item must inherit from DocItem
        self.assertTrue(isinstance(item,DocItem))
        pdf = FPDF()
        initPDF(pdf)
        if hasattr(item,'style'):
            setFontPDF(pdf,item.style)
        
        self.assertTrue(hasattr(item, 'text'))
    
        # All doc items must have resizePDF(pdf,x,y) - method to resize ite.rect
        # which is the bounding rectangle for the item
        self.assertTrue(hasattr(item, 'resizePDF'))
        self.assertNotRaise(item.resizePDF,pdf,1,2)
        
        # All doc items must have rect of type rect.Rect - bounding rectangle of the item -
        # all content must be inside this rect
        self.assertTrue(hasattr(item, 'rect'))
        self.assertTrue(isinstance(item.rect,rect.Rect))
        #self.assertEqual(item.rect.x0(), 1.0) # this may be untrue for MathFrac
        #self.assertEqual(item.rect.y0(), 2.0) # this may be untrue for MathPower
        
        # All doc items must have cellPDF(pdf) - method to output the content of the item
        # into a PDF. The output must be within bounding rectangle item.rect 
        self.assertTrue(hasattr(item, 'cellPDF'))
        self.assertNotRaise(item.cellPDF,pdf)
        
        # All doc items must have refit() method - for moving the item's content to fit 
        # its bounding rect. This method can be called by a parent item to re-position
        # its children.
        self.assertTrue(hasattr(item, 'refit'))
        self.assertNotRaise(item.refit)
    
    def test_DocItem(self):
        """It's a base class for all doc items"""
        # It's not supposed to be instantiated directly
        self.assertRaises(Exception, self.do_for_each_DocItem_class,DocItem())

    def test_MultiItem(self):
        """Test the base calss for complex doc items"""
        item = MultiItem()
        item.appendItem(DocItem())
        item.appendItem(DocItem())
        item.appendItem(DocItem())
        self.assertEqual(len(item.items), 3)
        self.assertTrue(isinstance(item.items[0],DocItem))
        self.assertTrue(isinstance(item.items[1],DocItem))
        self.assertTrue(isinstance(item.items[2],DocItem))

    def test_MultiItem_getUnionRect(self):
        item = MultiItem()
        # add some items
        item.appendItem(DocItem())
        # resize their rects
        item.items[0].rect = rect.Rect(0,0,1,2)
        item.rect = item.getUnionRect()
        self.assertEqual(item.rect.p0(),item.items[0].rect.p0())
        self.assertEqual(item.rect.p1(),item.items[0].rect.p1())
        
    def test_MultiItem_refit(self):
        item = MultiItem()
        # add some items
        item.appendItem(DocItem())
        item.appendItem(DocItem())
        item.appendItem(DocItem())
        # resize their rects
        item.items[0].rect = rect.Rect(0,0,1,2)
        item.items[1].rect = rect.Rect(0,0,1,2)
        item.items[2].rect = rect.Rect(0,0,1,2)
        # define some dummy refit methods
        item.items[0].refit = self.dummy_refit
        item.items[1].refit = self.dummy_refit
        item.items[2].refit = self.dummy_refit
        # align childrens rects left starting at x = 1.0
        rect.alignLeft([item.items[0].rect, item.items[1].rect, item.items[2].rect], 1, 100, 0)
        # set muli-item's rect to be union of the rects of its children
        item.rect = item.getUnionRect()
        # check that
        self.assertEquals(item.rect.p0(), item.items[0].rect.p0())
        self.assertEquals(item.rect.p1(), item.items[2].rect.p1())
        self.assertEquals(item.rect.p0(), rect.Point(1,0))
        self.assertEquals(item.rect.p1(), rect.Point(4,2))
        # translate the multi-item to Point(100,50)
        item.rect.translate(rect.Point(99,50))
        item.refit()
        self.assertEquals(item.rect, rect.Rect(100,50,103,52))

    
    def test_MultiItem_refit_multuitem(self):
        # test that child multi-item also refits its items
        item = MultiItem()
        child = MultiItem()
        child.appendItem(DocItem())
        # add some items
        item.appendItem(DocItem())
        item.appendItem(child)
        # resize their rects
        item.items[0].rect = rect.Rect(0,0,1,2)
        child.items[0].rect = rect.Rect(0.5,1,3,4)
        # define some dummy refit methods
        item.items[0].refit = self.dummy_refit
        child.items[0].refit = self.dummy_refit
        child.rect = child.getUnionRect()
        item.rect = item.getUnionRect()
        self.assertEqual(item.rect, rect.Rect(0,0,3,4))
        self.assertEqual(child.rect, child.items[0].rect)
        item.rect.translate(100,50)
        item.refit()
        self.assertEqual(item.rect, rect.Rect(100,50,103,54))
        self.assertEqual(item.items[0].rect, rect.Rect(100,50,101,52))
        self.assertEqual(child.rect, rect.Rect(100.5,51,103,54))
        self.assertEqual(child.rect, child.items[0].rect)
        
    def test_TextItem(self):
        """It's a base class for text based items"""
        # It's not supposed to be instantiated directly
        self.assertRaises(Exception, self.do_for_each_DocItem_class,TextItem())
    
    def test_Word(self):
        self.do_for_each_DocItem_class(Word('word'))

        w = Word('word')
        pdf = FPDF()
        initPDF(pdf)
        # the bounding rect is't empty
        w.resizePDF(pdf, 1, 2)
        self.assertGreater(w.rect.x1(), w.rect.x0())
        self.assertGreater(w.rect.y1(), w.rect.y0())
        self.assertEqual(w.text, 'word')
        self.assertEqual(w.style, 'body')
        w.cellPDF(pdf)
        pdf.output('out/document/test_Word.pdf', 'F')
        
    def test_Symbol(self):
        self.do_for_each_DocItem_class(Symbol('alpha'))

        w = Symbol('alpha')
        pdf = FPDF()
        initPDF(pdf)
        setFontPDF(pdf, w.style)
        # the bounding rect is't empty
        w.resizePDF(pdf, 1, 2)
        self.assertGreater(w.rect.x1(), w.rect.x0())
        self.assertGreater(w.rect.y1(), w.rect.y0())
        self.assertEqual(w.text, 'alpha')
        self.assertEqual(w.style, 'symbol')
        w.cellPDF(pdf)
        pdf.output('out/document/test_Symbol.pdf', 'F')

    def test_MathVariable(self):
        self.do_for_each_DocItem_class(MathVariable('var'))

        w = MathVariable('var')
        pdf = FPDF()
        initPDF(pdf)
        setFontPDF(pdf, w.style)
        # the bounding rect is't empty
        w.resizePDF(pdf, 1, 2)
        self.assertGreater(w.rect.x1(), w.rect.x0())
        self.assertGreater(w.rect.y1(), w.rect.y0())
        self.assertEqual(w.text, 'var')
        self.assertEqual(w.style, 'math-var')
        w.cellPDF(pdf)
        pdf.output('out/document/test_MathVariable.pdf', 'F')
        
    def test_MathSign(self):
        self.do_for_each_DocItem_class(MathSign('var'))

        pdf = FPDF()
        initPDF(pdf)
        setFontPDF(pdf, 'math-symbol')

        plus = MathSign('+')
        plus.resizePDF(pdf, 4, 2)
        minus = MathSign('-')
        minus.resizePDF(pdf, 1, 2)
        self.assertGreater(minus.rect.x1(), minus.rect.x0())
        self.assertGreater(minus.rect.y1(), minus.rect.y0())
        self.assertGreater(plus.rect.x1(), plus.rect.x0())
        self.assertGreater(plus.rect.y1(), plus.rect.y0())
        #self.assertEqual(w.text, 'var')
        self.assertEqual(minus.style, 'math-symbol')
        minus.cellPDF(pdf)
        plus.cellPDF(pdf)
        pdf.output('out/document/test_MathSign.pdf', 'F')
        
    def test_InlineMathBlock(self):
        self.do_for_each_DocItem_class(InlineMathBlock())

        pdf = FPDF()
        initPDF(pdf)
        
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))
        block.appendItem(MathSign('-'))
        block.appendItem(MathVariable('z'))
        
        block.resizePDF(pdf, 10, 20)
        block.cellPDF(pdf)
        pdf.output('out/document/test_InlineMathBlock.pdf', 'F')
        
    def test_MathFun(self):
        self.do_for_each_DocItem_class(InlineMathBlock())

        pdf = FPDF()
        initPDF(pdf)
        
        block = InlineMathBlock()
        block.appendItem(MathFunction('tan'))
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('='))
        block.appendItem(MathFunction('sin'))
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('/'))
        block.appendItem(MathFunction('cos'))
        block.appendItem(MathVariable('x'))
        
        block.resizePDF(pdf, 10, 20)
        block.cellPDF(pdf)
        
        block.moveTo(10, 30)
        block.cellPDF(pdf)
        
        pdf.output('out/document/test_MathFunction.pdf', 'F')
                
    def test_ScaleFont(self):
        self.do_for_each_DocItem_class(InlineMathBlock())

        pdf = FPDF()
        initPDF(pdf)
        
        block = InlineMathBlock()
        block.appendItem(MathFunction('tan'))
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('='))
        block.appendItem(MathFunction('sin'))
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('/'))
        block.appendItem(MathFunction('cos'))
        block.appendItem(MathVariable('x'))
        
        block.resizePDF(pdf, 10, 20)
        block.cellPDF(pdf)
        
        block.scaleFont(0.8)
        block.resizePDF(pdf, 10, 30)
        block.cellPDF(pdf)
        
        block.scaleFont(2.0)
        block.resizePDF(pdf, 10, 40)
        block.cellPDF(pdf)
        
        pdf.output('out/document/test_ScaleFactor.pdf', 'F')

    def test_MathPower(self):
        tmp = MathPower()
        tmp.appendItem(MathVariable('x'))
        tmp.appendItem(MathVariable('2'))
        self.do_for_each_DocItem_class(tmp)

        pdf = FPDF()
        initPDF(pdf)
        
        p = MathPower()
        p.appendItem(MathVariable('x'))
        p.appendItem(MathVariable('a'))
        p.resizePDF(pdf, 10, 20)
        p.cellPDF(pdf)
        
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))
        
        p = MathPower()
        p.appendItem(MathVariable('q'))
        p.appendItem(block)
        p.resizePDF(pdf, 10, 30)
        p.cellPDF(pdf)
        
        
        pdf.output('out/document/test_MathPower.pdf', 'F')

    def test_MathBrackets(self):
        tmp = MathBrackets()
        tmp.appendItem(MathVariable('x'))
        self.do_for_each_DocItem_class(tmp)

        pdf = FPDF()
        initPDF(pdf)
        
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))

        brackets = MathBrackets()
        brackets.appendItem(block)

        brackets.resizePDF(pdf, 10, 10)
        brackets.cellPDF(pdf)
        
        p = MathPower()
        p.appendItem(brackets)
        p.appendItem(MathVariable('q'))
        p.resizePDF(pdf, 10, 20)
        p.cellPDF(pdf)

        pdf.output('out/document/test_MathBrackets.pdf', 'F')

    def test_MathFrac(self):
        tmp = MathFrac()
        tmp.appendItem(MathVariable('x'))
        tmp.appendItem(MathVariable('2'))
        self.do_for_each_DocItem_class(tmp)

        pdf = FPDF()
        initPDF(pdf)
        
        #---------------------------
        p = MathFrac()
        p.appendItem(MathVariable('x'))
        p.appendItem(MathVariable('y'))
        p.resizePDF(pdf, 10, 20)
        p.cellPDF(pdf)
        
        #---------------------------
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(p)
        block.resizePDF(pdf, 10, 40)
        block.cellPDF(pdf)

        #---------------------------
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))

        p = MathFrac()
        p.appendItem(block)
        p.appendItem(MathVariable('y'))
        p.resizePDF(pdf, 10, 60)
        p.cellPDF(pdf)
        
        #---------------------------
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))

        p = MathFrac()
        p.appendItem(MathVariable('y'))
        p.appendItem(block)
        p.resizePDF(pdf, 10, 80)
        p.cellPDF(pdf)
        
        pdf.output('out/document/test_MathFrac.pdf', 'F')

    def test_MathBigBrackets(self):
        tmp = MathBigBrackets()
        tmp.appendItem(MathVariable('x'))
        self.do_for_each_DocItem_class(tmp)

        pdf = FPDF()
        initPDF(pdf)
        
        #---------------------------
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))

        p = MathFrac()
        p.appendItem(MathVariable('y'))
        p.appendItem(block)

        brackets = MathBigBrackets()
        brackets.appendItem(p)

        brackets.resizePDF(pdf, 10, 10)
        brackets.cellPDF(pdf)
        
        brackets = MathBigBrackets('{','}')
        brackets.appendItem(p)

        brackets.resizePDF(pdf, 10, 30)
        brackets.cellPDF(pdf)
        
        brackets = MathBigBrackets('{','')
        brackets.appendItem(p)

        brackets.resizePDF(pdf, 10, 50)
        brackets.cellPDF(pdf)
        
        brackets = MathBigBrackets('',']')
        brackets.appendItem(p)

        brackets.resizePDF(pdf, 10, 70)
        brackets.cellPDF(pdf)
        
        pdf.output('out/document/test_MathBigBrackets.pdf', 'F')

    def test_MathBigBrackets1(self):

        pdf = FPDF()
        initPDF(pdf)
        
        brackets = MathBigBrackets('(',')', b( f(n('1'),n('2'))) )
        brackets.resizePDF(pdf, 10, 20)
        brackets.cellPDF(pdf)
        
        pdf.output('out/document/test_MathBigBrackets1.pdf', 'F')

    def test_MathBelowAndAbove(self):
        tmp = MathBelowAndAbove()
        tmp.appendItem(MathVariable('x'))
        self.do_for_each_DocItem_class(tmp)
        
        pdf = FPDF()
        initPDF(pdf)
        
#        block = InlineMathBlock()
#        block.appendItem(MathVariable('n'))
#        block.appendItem(MathSign('='))
#        block.appendItem(MathVariable('0'))
        
        sigma = Symbol('Sigma')
        sigma.scaleFont(2.0)

        s = MathBelowAndAbove()
        s.appendItem(sigma)
        s.appendItem(InlineMathBlock(MathVariable('n'),MathSign('='),MathNumber('0')))
        s.appendItem(MathVariable('N'))
        
        s.resizePDF(pdf, 10, 10)
        s.cellPDF(pdf)
        
        pi = Symbol('Pi')
        pi.scaleFont(2.0)

        prod = MathBelowAndAbove(pi,
                                 InlineMathBlock(MathVariable('i'),MathSign('='),MathNumber('1')),
                                 MathVariable('M')
                                 )
        
        prod.resizePDF(pdf, 10, 40)
        prod.cellPDF(pdf)
        
        lim = MathBelowAndAbove(MathFunction('lim'),
                                InlineMathBlock(MathVariable('x'),MathSign('->'),MathVariable('4'))
                                )
        
        lim.resizePDF(pdf, 10, 60)
        lim.cellPDF(pdf)
        
        tilde = MathBelowAndAbove(Symbol('beta'),
                                  None,
                                  MathSign('~')
                                  )
        
        tilde.resizePDF(pdf, 10, 80)
        tilde.cellPDF(pdf)
        
        pdf.output('out/document/test_MathBelowAndAbove.pdf', 'F')
        
    def test_MathColumn(self):
        self.do_for_each_DocItem_class(MathColumn())

        pdf = FPDF()
        initPDF(pdf)
        
        block = MathColumn(InlineMathBlock(MathVariable('x'),MathSign('='),MathVariable('0')),
                           InlineMathBlock(MathVariable('y'),MathSign('='),MathVariable('0')),
                           InlineMathBlock(MathVariable('z'),MathSign('='),MathVariable('0'))
                           )
        
        block.resizePDF(pdf, 10, 20)
        block.cellPDF(pdf)
        pdf.output('out/document/test_MathColumn.pdf', 'F')
        
    def test_MathSum(self):
        self.do_for_each_DocItem_class(MathSum())

        pdf = FPDF()
        initPDF(pdf)
        
        summ = MathSum(InlineMathBlock(MathVariable('i'),MathSign('='),MathVariable('1')),
                     MathVariable('M')
                     )
        
        summ.resizePDF(pdf, 10, 20)
        summ.cellPDF(pdf)
        
        pdf.output('out/document/test_MathSum.pdf', 'F')

    def test_MathProd(self):
        self.do_for_each_DocItem_class(MathProd())

        pdf = FPDF()
        initPDF(pdf)
        
        prod = MathProd(InlineMathBlock(MathVariable('i'),MathSign('='),MathVariable('1')),
                     MathVariable('M')
                     )
        
        prod.resizePDF(pdf, 10, 10)
        prod.cellPDF(pdf)
        
        pdf.output('out/document/test_MathProd.pdf', 'F')

    def test_MathSubSuperscript(self):
        self.do_for_each_DocItem_class(MathSubSuperscript(MathVariable('x'),MathVariable('2')))

        pdf = FPDF()
        initPDF(pdf)
        
        #----------------------------
        sss = MathSubSuperscript(MathVariable('x'),MathVariable('n'),MathVariable('2'))
        sss.resizePDF(pdf, 10, 10)
        sss.cellPDF(pdf)
        
        #----------------------------
        sss = MathSubSuperscript(MathVariable('x'),MathVariable('i'))
        sss.resizePDF(pdf, 10, 20)
        sss.cellPDF(pdf)
        
        #----------------------------
        block = InlineMathBlock()
        block.appendItem(MathVariable('x'))
        block.appendItem(MathSign('+'))
        block.appendItem(MathVariable('y'))

        brackets = MathBrackets()
        brackets.appendItem(block)

        sss = MathSubSuperscript(brackets,None,MathVariable('p'))
        sss.resizePDF(pdf, 10, 40)
        sss.cellPDF(pdf)
        
        pdf.output('out/document/test_MathSubSuperscript.pdf', 'F')

    def test_formulas(self):
        
        pdf = FPDF()
        initPDF(pdf)
        
        formula = b( v('x'), si('-'), sy('alpha'), si('+'), n('1'), si('='), n('0') )
        formula.resizePDF(pdf,10,10)
        formula.cellPDF(pdf)
        
        formula = b( 
                ss( br( v('x'), si('-'), v('y') ), None, n('2') ),
                si('+'), v('x'),
                si('-'), f( v('x'), b(v('x'), si('-'), v('y')) ), 
                si('+'), b( sm(b(v('i'),si('='),n('1')),v('N')), n('2'),ss(v('z'),v('i')))
              )
        formula.resizePDF(pdf,10,30)
        formula.cellPDF(pdf)
        
        pdf.output('out/document/test_Formulas.pdf', 'F')
        
    def test_Paragraph(self):
        self.do_for_each_DocItem_class(Paragraph())
        
        pdf = FPDF()
        initPDF(pdf)
        pdf.set_line_width(2)
        pdf.line(0, 20, 300, 20)
        
        par = Paragraph()
        par.addItems(*[w('Hello'),w('world!')])
        par.addItems(w('Formula:'),b(v('x'),si('+'),f(sy('alpha'),n('2'))))
        par.resizePDF(pdf)
        par.cellPDF(pdf)
        par.showRect(pdf)
        
        par = Paragraph(100)
        par.addItems(w('I'),w('have'),w('my'),w('width'),w('set.'))
        par.resizePDF(pdf)
        par.cellPDF(pdf)
        par.showRect(pdf)
        
        pdf.output('out/document/test_Paragraph.pdf', 'F')
        
    def test_Document(self):
        
        pdf = FPDF('P','mm',(100,40))
        
        doc = Document()
        
        title = Title()
        title.addItems(w('Hello'),w('world!'))
        par = Paragraph()
        words = []
        for i in range(50):
            words.append(w('hello '+str(i+1)))
        par.addItems(*words)

        doc.appendParagraph(title) 
        doc.appendParagraph(par) 
        doc.setPDF(pdf)
        doc.outputPDF('out/document/test_Paragraph1.pdf')
        

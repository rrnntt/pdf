import unittest
from fpdf import FPDF
from document import *

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
        self.assertEqual(item.rect.x0(), 1.0)
        self.assertEqual(item.rect.y0(), 2.0)
        
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
        pdf.output('out/test_Word.pdf', 'F')
        
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
        pdf.output('out/test_Symbol.pdf', 'F')

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
        pdf.output('out/test_MathVariable.pdf', 'F')
        
    def test_MathSign(self):
        self.do_for_each_DocItem_class(MathSign('var'))

        pdf = FPDF()
        initPDF(pdf)
        setFontPDF(pdf, 'math-symbol')

        plus = MathSign('+')
        plus.resizePDF(pdf, 4, 2)
        w = MathSign('-')
        w.resizePDF(pdf, 1, 2)
        self.assertGreater(w.rect.x1(), w.rect.x0())
        self.assertGreater(w.rect.y1(), w.rect.y0())
        #self.assertEqual(w.text, 'var')
        self.assertEqual(w.style, 'math-symbol')
        w.cellPDF(pdf)
        plus.cellPDF(pdf)
        print w.rect,plus.rect
        pdf.output('out/test_MathSign.pdf', 'F')
        
        
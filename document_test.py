import unittest
from fpdf import FPDF
from document import *

class TestDocument(unittest.TestCase):
    
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
        # align childrens rects
        rect.alignLeft([item.items[0].rect, item.items[1].rect, item.items[2].rect], 1, 100, 0)
        print item.items[0].rect, item.items[1].rect, item.items[2].rect
        # set muli-item's rect to be union of the rects of its children
        item.rect = item.getUnionRect()
        # check that
        self.assertEquals(item.rect.p0(), item.items[0].rect.p0())
        self.assertEquals(item.rect.p1(), item.items[2].rect.p1())

    
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
        
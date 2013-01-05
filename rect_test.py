import unittest
from rect import Rect
from point import Point

class TestRect(unittest.TestCase):
    
    def test_init(self):
        
        r = Rect()
        self.assertEqual(r.p0(), Point())
        self.assertEqual(r.p1(), Point())
        
        r = Rect(1,2,3,4)
        self.assertEqual(r.p0(), Point(1,2))
        self.assertEqual(r.p1(), Point(3,4))
        
        r = Rect( Point(3,4), Point(1,2) )
        self.assertEqual(r.p0(), Point(3,4))
        self.assertEqual(r.p1(), Point(1,2))

        self.assertRaises(Exception, Rect, 1)       # wrong type of argument
        self.assertRaises(Exception, Rect, 1, 2)    # arguments are of wrong types
        self.assertRaises(Exception, Rect, 1, 2, 3) # wrong number of arguments
        
        rr = Rect( r )
        self.assertEqual(r.p0(), rr.p0())
        self.assertEqual(r.p1(), rr.p1())
        
    def test_str(self):
        
        r = Rect(1,2,3,4)
        s = str(r)
        self.assertEqual(s, '([1.0,2.0],[3.0,4.0])')
        
    def test_isEmpty(self):
        
        self.assertTrue( Rect(1,2,1,2).isEmpty() )
        self.assertTrue( Rect(1,2+1e-14,1,2).isEmpty() )
        self.assertTrue( Rect(1+1e-14,2,1,2).isEmpty() )
        self.assertFalse( Rect(1+1e-14,2+1e-14,1,2).isEmpty() )
        
    def test_span(self):
        
        r = Rect( 1,2, 5,1 )
        self.assertEquals( r.xSpan(), 4.0 )
        self.assertEquals( r.ySpan(), -1.0 )
        self.assertEquals( r.width(), 4.0 )
        self.assertEquals( r.height(), 1.0 )
        
    def test_center(self):
        
        r = Rect( 1,2, 5,6 )
        c = r.center()
        self.assertTrue( c.isNear(Point(3,4)) )
        
    def test_moveCenter(self):
        
        r = Rect( 1,2, 5,6 )
        r.moveCenter(Point(0, 0))
        c = r.center()
        self.assertTrue( c.isNear(Point()) )
        self.assertEquals( r.xSpan(), 4.0 )
        self.assertEquals( r.ySpan(), 4.0 )
        
        r = Rect( 1,2, 5,1 )
        r.moveCenter(Point(0, 0))
        c = r.center()
        self.assertTrue( c.isNear(Point()) )
        self.assertEquals( r.xSpan(), 4.0 )
        self.assertEquals( r.ySpan(), -1.0 )
        
    def test_vertex(self):
        
        r = Rect( 1,2, 5,6 )
        self.assertTrue( r.vertex(0).isNear( Point(1,2) ) )
        self.assertTrue( r.vertex(1).isNear( Point(1,6) ) )
        self.assertTrue( r.vertex(2).isNear( Point(5,6) ) )
        self.assertTrue( r.vertex(3).isNear( Point(5,2) ) )
        
        r.setVertex(0, Point(3,4))
        self.assertTrue( r.p0().isNear( Point(3,4) ) )
        self.assertTrue( r.p1().isNear( Point(5,6) ) )
        
        r.setVertex(1, Point(1,2))
        self.assertTrue( r.p0().isNear( Point(1,4) ) )
        self.assertTrue( r.p1().isNear( Point(5,2) ) )
        
        r.setVertex(2, Point(7,8))
        self.assertTrue( r.p0().isNear( Point(1,4) ) )
        self.assertTrue( r.p1().isNear( Point(7,8) ) )
        
        r.setVertex(3, Point(10,0))
        self.assertTrue( r.p0().isNear( Point(1,0) ) )
        self.assertTrue( r.p1().isNear( Point(10,8) ) )
        
        
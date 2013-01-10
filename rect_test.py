import unittest
from rect import Rect, _justifyX, justifyX
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
        
    def test_translate(self):
        
        r = Rect(1,2,3,4)
        r.translate(Point(0.5,-0.2))
        self.assertTrue( r.p0().isNear(Point(1.5,1.8)) )
        self.assertTrue( r.p1().isNear(Point(3.5,3.8)) )
        
    def test_adjust(self):
        
        r = Rect(1,2,3,4)
        r.adjust(Point(-0.5,-0.2), Point(0.2,0.5))
        self.assertTrue( r.p0().isNear(Point(0.5,1.8)) )
        self.assertTrue( r.p1().isNear(Point(3.2,4.5)) )
        
    def test_include(self):
        
        r = Rect(1,2,3,4)
        r.include( Point(1.5, 3.4) )
        self.assertTrue( r.p0().isNear(Point(1,2)) )
        self.assertTrue( r.p1().isNear(Point(3,4)) )
        
        r.include( Point(0, 0) )
        self.assertTrue( r.p0().isNear(Point(0,0)) )
        self.assertTrue( r.p1().isNear(Point(3,4)) )

        r.include( Point(2, 5) )
        self.assertTrue( r.p0().isNear(Point(0,0)) )
        self.assertTrue( r.p1().isNear(Point(3,5)) )
        
    def test_unite(self):
        r1 = Rect(1,2,3,4)
        r2 = Rect(2,3,6,7)
        r = Rect( r1 )
        r.unite(r2)
        self.assertTrue(r.contains(r1) and r.contains(r2))
        r1.adjust(Point(-1e-14,-1e-14),Point(1e-14,1e-14))
        self.assertFalse( r.contains( r1 ) )
        self.assertFalse( r1.contains( r ) )
    
    def test_flip(self):
        pass
                 
    def test_contains(self):
        
        r = Rect(1,2,3,4)
        self.assertFalse( r.contains(Point(0,0)) )
        self.assertFalse( r.contains(Point(2,4.1)) )
        self.assertTrue( r.contains(Point(2,3)) )
        self.assertTrue( r.contains(Rect(2,3,2.6,3.3)) )
        self.assertTrue( r.contains(Rect(2.6,3.3,2,3)) )
        r1 = Rect( r )
        r1.adjust(Point(-1e-14,-1e-14),Point(1e-14,1e-14))
        self.assertFalse( r.contains( r1 ) )
        
    def test__justify(self):
        
        _justifyX([], 0, 1)
        
        r = Rect(0,1,1,2)
        _justifyX([r], 1.1,2.2)
        self.assertTrue(r.p0().isNear(Point(1.1,1.0)))
        self.assertAlmostEqual(r.width(), 1.0)
        self.assertAlmostEqual(r.height(), 1.0)
        
        rlist = [Rect(0,1,1,2), Rect(0,1,1,2), Rect(0,1,1,2)]
        _justifyX(rlist, 10, 13)
        self.assertAlmostEqual(rlist[0].x0(), 10)
        self.assertAlmostEqual(rlist[0].x1(), 11)
        self.assertAlmostEqual(rlist[0].y0(), 1)
        self.assertAlmostEqual(rlist[0].y1(), 2)
        
        self.assertAlmostEqual(rlist[1].x0(), 11)
        self.assertAlmostEqual(rlist[1].x1(), 12)
        self.assertAlmostEqual(rlist[1].y0(), 1)
        self.assertAlmostEqual(rlist[1].y1(), 2)
        
        self.assertAlmostEqual(rlist[2].x0(), 12)
        self.assertAlmostEqual(rlist[2].x1(), 13)
        self.assertAlmostEqual(rlist[2].y0(), 1)
        self.assertAlmostEqual(rlist[2].y1(), 2)
        
        rlist = [Rect(0,1,1,2), Rect(0,1,1,2), Rect(0,1,1,2)]
        _justifyX(rlist, 10, 12)
        self.assertAlmostEqual(rlist[0].x0(), 10)
        self.assertAlmostEqual(rlist[0].x1(), 11)
        self.assertAlmostEqual(rlist[0].y0(), 1)
        self.assertAlmostEqual(rlist[0].y1(), 2)
        
        self.assertAlmostEqual(rlist[1].x0(), 10.5)
        self.assertAlmostEqual(rlist[1].x1(), 11.5)
        self.assertAlmostEqual(rlist[1].y0(), 1)
        self.assertAlmostEqual(rlist[1].y1(), 2)
        
        self.assertAlmostEqual(rlist[2].x0(), 11)
        self.assertAlmostEqual(rlist[2].x1(), 12)
        self.assertAlmostEqual(rlist[2].y0(), 1)
        self.assertAlmostEqual(rlist[2].y1(), 2)
        
    def test_justify(self):
        
        justifyX([], 0, 1)
        
        r = Rect(0,1,1,2)
        n = justifyX([r], 1.1,2.2)
        self.assertEqual(n, 1)
        self.assertTrue(r.p0().isNear(Point(1.1,1.0)))
        self.assertAlmostEqual(r.width(), 1.0)
        self.assertAlmostEqual(r.height(), 1.0)
        
        r = Rect(0,1,1,2)
        n = justifyX([r], 1.1,2.0)
        self.assertEqual(n, 0)
        self.assertTrue(r.p0().isNear(Point(0.0,1.0)))
        self.assertAlmostEqual(r.width(), 1.0)
        self.assertAlmostEqual(r.height(), 1.0)
        
        rlist = [Rect(0,1,1,2), Rect(0,1,1,2), Rect(0,1,1,2)]
        n = justifyX(rlist, 10, 12)
        self.assertEqual(n, 2)
        self.assertAlmostEqual(rlist[0].x0(), 10)
        self.assertAlmostEqual(rlist[0].x1(), 11)
        self.assertAlmostEqual(rlist[0].y0(), 1)
        self.assertAlmostEqual(rlist[0].y1(), 2)
        
        self.assertAlmostEqual(rlist[1].x0(), 11)
        self.assertAlmostEqual(rlist[1].x1(), 12)
        self.assertAlmostEqual(rlist[1].y0(), 1)
        self.assertAlmostEqual(rlist[1].y1(), 2)
        
        self.assertAlmostEqual(rlist[2].x0(), 0)
        self.assertAlmostEqual(rlist[2].x1(), 1)
        self.assertAlmostEqual(rlist[2].y0(), 1)
        self.assertAlmostEqual(rlist[2].y1(), 2)
        
        rlist = [Rect(0,1,1,2), Rect(0,1,1,2), Rect(0,1,1,2)]
        n = justifyX(rlist, 10, 14)
        self.assertEqual(n, 3)
        self.assertAlmostEqual(rlist[0].x0(), 10)
        self.assertAlmostEqual(rlist[0].x1(), 11)
        self.assertAlmostEqual(rlist[0].y0(), 1)
        self.assertAlmostEqual(rlist[0].y1(), 2)
        
        self.assertAlmostEqual(rlist[1].x0(), 11.5)
        self.assertAlmostEqual(rlist[1].x1(), 12.5)
        self.assertAlmostEqual(rlist[1].y0(), 1)
        self.assertAlmostEqual(rlist[1].y1(), 2)
        
        self.assertAlmostEqual(rlist[2].x0(), 13)
        self.assertAlmostEqual(rlist[2].x1(), 14)
        self.assertAlmostEqual(rlist[2].y0(), 1)
        self.assertAlmostEqual(rlist[2].y1(), 2)
        
        rlist = [Rect(0,1,1,2), Rect(0,1,1,2), Rect(0,1,1,2)]
        n = justifyX(rlist, 10, 14, 0.6)
        #print rlist[0], rlist[1], rlist[2]
        self.assertEqual(n, 2)
        
        self.assertAlmostEqual(rlist[0].x0(), 10)
        self.assertAlmostEqual(rlist[0].x1(), 11)
        self.assertAlmostEqual(rlist[0].y0(), 1)
        self.assertAlmostEqual(rlist[0].y1(), 2)
        
        self.assertAlmostEqual(rlist[1].x0(), 13)
        self.assertAlmostEqual(rlist[1].x1(), 14)
        self.assertAlmostEqual(rlist[1].y0(), 1)
        self.assertAlmostEqual(rlist[1].y1(), 2)
        
        self.assertAlmostEqual(rlist[2].x0(), 0)
        self.assertAlmostEqual(rlist[2].x1(), 1)
        self.assertAlmostEqual(rlist[2].y0(), 1)
        self.assertAlmostEqual(rlist[2].y1(), 2)
        


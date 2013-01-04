import unittest
from point import Point

class TestPoint(unittest.TestCase):
    
    def test_init(self):
        
        p = Point()
        self.assertEqual(p.x(), 0.0)
        self.assertEqual(p.y(), 0.0)
        
        p = Point(1.0, 2.0)
        self.assertEqual(p.x(), 1.0)
        self.assertEqual(p.y(), 2.0)
        
        p = Point(1.0)
        self.assertEqual(p.x(), 1.0)
        self.assertEqual(p.y(), 0.0)
        
        p = Point(1, 2)
        self.assertEqual(p.x()/2, 0.5)
        self.assertEqual(p.y()/4, 0.5)
        
        p = Point('1.1', '2.2')
        self.assertEqual(p.x(), 1.1)
        self.assertEqual(p.y(), 2.2)
        
        self.assertRaises(ValueError, Point, 'a')
        self.assertRaises(ValueError, Point, 0, 'a')
        self.assertRaises(ValueError, Point, 'a', 'b')
        
    def test_compare(self):
        
        p1 = Point(1.2, 2.3)
        p2 = Point(1.2, 2.3)
        self.assertTrue( p1 == p2 )
        self.assertEqual(p1, p2)
        p2 = Point(1.2, 2.0)
        self.assertNotEqual(p1, p2)
        p2 = Point(1.0, 2.3)
        self.assertNotEqual(p1, p2)
        p2 = Point(1.0, 2.0)
        self.assertNotEqual(p1, p2)
        self.assertTrue( p1 != p2 )
        
    def test_isNear(self):
        self.assertTrue(Point(1,2).isNear(Point(1.0+1e-16, 2.0)))
        self.assertTrue(Point(1,2).isNear(Point(1.0, 2.0+1e-16)))
        self.assertTrue(Point(1,2).isNear(Point(1.0+1e-16, 2.0+1e-16)))
        self.assertFalse(Point(1,2).isNear(Point(1.0+1e-14, 2.0)))
        self.assertFalse(Point(1,2).isNear(Point(1.0, 2.0+1e-14)))
        self.assertFalse(Point(1,2).isNear(Point(1.0+1e-14, 2.0+1e-14)))
        
    def test_isNearZero(self):
        self.assertTrue(Point().isNearZero())
        self.assertTrue(Point(1e-16,0).isNearZero())
        self.assertTrue(Point(0,1e-16).isNearZero())
        self.assertTrue(Point(1e-16,1e-16).isNearZero())
        self.assertFalse(Point(1e-14,0).isNearZero())
        self.assertFalse(Point(0,1e-14).isNearZero())
        self.assertFalse(Point(1e-14,1e-14).isNearZero())
        
    def test_x_y(self):
        p = Point(1.2, 2.3)
        self.assertEqual(p.x(), 1.2)
        self.assertEqual(p.y(), 2.3)
        
    def test_set(self):
        p = Point()
        p.set(1.2, 2.3)
        self.assertEqual(p.x(), 1.2)
        self.assertEqual(p.y(), 2.3)
        
    def test_copy(self):
        
        p1 = Point(1.2, 2.3)
        # copying pointer
        p2 = p1
        self.assertEqual(p1, p2)
        p2.set(4, 5)
        self.assertEqual(p1, p2)
        # copying data
        p3 = Point( p2 )
        self.assertEqual(p3, p2)
        p3.set(10, 20)
        self.assertNotEqual(p3, p2)
        self.assertEqual(p2.x(), 4)
        self.assertEqual(p2.y(), 5)
        self.assertEqual(p3.x(), 10)
        self.assertEqual(p3.y(), 20)
        
    def test_str(self):
        
        p = Point(1.2, 2.3)
        s = str(p)
        self.assertEqual(s, '[1.2,2.3]')
        
    def test_add_number(self):

        p1 = Point(1.2, 2.3)
        p2 = p1 + 1.1
        self.assertEqual(p2, Point(2.3,3.4))
        self.assertEqual(p1 + 1.1, Point(2.3,3.4))
        p1 += 2.2
        # sum is not exact !?
        self.assertTrue(p1.isNear(Point(3.4,4.5)))
        
    def test_add_point(self):

        p1 = Point(1.2, 2.3)
        p2 = Point(2.1, 3.2)
        self.assertEqual(p1 + p2, Point(3.3,5.5))
        p1 += Point(2,3)
        self.assertTrue(p1.isNear(Point(3.2,5.3)))
        
    def test_sub_number(self):
        
        p1 = Point(1.2, 2.3)
        p2 = p1 - 1.1
        self.assertTrue(p2.isNear( Point(0.1,1.2)) )
        self.assertTrue((p1 - 1.1).isNear( Point(0.1,1.2) ))
        p1 -= 1.1
        self.assertTrue(p1.isNear( Point(0.1,1.2) ) )
        
    def test_sub_point(self):

        p1 = Point(1.2, 2.3)
        p2 = Point(2.1, 3.2)
        self.assertTrue((p2 - p1).isNear(Point(0.9,0.9)))
        p1 -= Point(0.2,0.3)
        self.assertTrue(p1.isNear(Point(1,2)))
        
    def test_translate(self):
        p = Point(1,2)
        p.translate(0.1, -0.2)
        self.assertTrue( p.isNear(Point(1.1,1.8)) )
        p.translate( Point(-1,2) )
        self.assertTrue( p.isNear(Point(0.1,3.8)) )
        
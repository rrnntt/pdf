import point
from point import Point

"""

Axes aligned rectangle. It is defined by its two diagonal points p0 == (x0,y0) and p1 == (x1,y1).
Point p0 is assumed to be in the bottom-left corner of the rectangle and point p1
is in the top-right corner. 
 
The left border of the rectangle is always at x0 regardless whether x0 < x1 or not.
The right border is always at x1.
The bottom border of the rectangle is always at y0 regardless whether y0 < y1 or not.
The top border is always at y1. ???

"""
class Rect:
    
    def __init__(self, x0 = None, y0 = None, x1 = None, y1 = None):
        """
        Init the rectangle. If 4 arguments are given the first two are x0 and y0 and the other two
        are x1 and y1. If two arguments are given they must have type Point and the fist defines 
        the bottom-left corner and the second one defines the top-right corner. If no arguments
        are given the empty default Rect is created with both points at (0,0). Any other number of
        arguments are not allowed.
        """
        if x0 == None:
            self._p0 = Point()
            self._p1 = Point()
        elif y1 != None:
            self._p0 = Point(x0,y0)
            self._p1 = Point(x1,y1)
        elif x1 != None:
            raise Exception('Rect is given wrong number of arguments.')
        elif  y0 == None:
            if isinstance(x0, Rect):
                self._p0 = Point( x0.p0() )
                self._p1 = Point( x0.p1() )
            else:
                raise Exception('Rect is given arguments of wrong type.')
        elif not isinstance(x0,Point) or not isinstance(y0,Point):
            raise Exception('Rect is given arguments of wrong type.')
        else:
            self._p0 = Point( x0 )
            self._p1 = Point( y0 )
                
    def p0(self):
        """ Return the bottom-left point """
        return self._p0;

    def p1(self):
        """ Return the top-right point """
        return self._p1;

    def __str__(self):
        """ Convert to string (print) """
        return '(' + str(self._p0) + ',' + str(self._p1) + ')'
    
    def xSpan(self):
        """ p1.x - p0.x  """
        return self._p1.x() - self._p0.x()
    
    def ySpan(self):
        """ p1.y - p0.y  """
        return self._p1.y() - self._p0.y()
    
    def width(self):
        """ Get the size of the Rect in x direction """
        return abs( self.xSpan() )
    
    def height(self):
        """ Get the size of the Rect in y direction """
        return abs( self.ySpan() )
    
    def isEmpty(self):
        """ Check if this Rect is empty ie has a zero area """
        return self.width() <= point.tolerance or self.height() <= point.tolerance

    def center(self):
        """ Get the centre of this Rect """
        return Point( ( self._p0.x() + self._p1.x() ) / 2, ( self._p0.y() + self._p1.y() ) / 2 )
    
    def moveCenter(self, c):
        """ Translate this Rect such that its center moves to c """
        dp = c - self.center()
        self._p0 += dp
        self._p1 += dp
        
    def vertex(self, i):
        """ 
        Get i-th vertex (Point) of this Rect. If p0 is in the bottom-left corner then 
        the vertices are numbered in the clockwise direction starting with p0.
        """
        if i == 0:
            return self._p0
        elif i == 1:
            return Point(self._p0.x(), self._p1.y())
        elif i == 2:
            return self._p1
        elif i == 3:
            return Point(self._p1.x(), self._p0.y())

    def setVertex(self, i, p):
        """ Set i-th vertex (Point) of this Rect. Other vertices change accordingly. """
        if not isinstance(p, Point):
            raise Exception('A vertex is a Point')
        if i == 0:
            self._p0 = Point( p )
        elif i == 1:
            self._p0.set( p.x(), self._p0.y() )
            self._p1.set( self._p1.x(), p.y() )
        elif i == 2:
            self._p1 = Point( p )
        elif i == 3:
            self._p0.set( self._p0.x(), p.y() )
            self._p1.set( p.x(), self._p1.y() )

    def translate(self, dp):
        """ Translate this Rect by vector (Point) dp """
        if not isinstance( dp, Point):
            raise Exception('Translation vector must have type Point')
        self._p0 += dp
        self._p1 += dp

    def adjust(self, dp0, dp1):
        """ Adjust the Rect by translating p0 and p1 by dp0 and dp1 respectively"""
        self._p0 += dp0
        self._p1 += dp1
        
    def include(self, p):
        """ Expand the rectangle if needed to include a point. """
        x0 = self._p0.x()
        y0 = self._p0.y()
        x1 = self._p1.x()
        y1 = self._p1.y()
        if (p.x() - x0) / self.xSpan() < 0:
            x0 = p.x()
        elif (p.x() - x1) / self.xSpan() > 0:
            x1 = p.x();
        if (p.y() - y0) / self.ySpan() < 0:
            y0 = p.y()
        elif (p.y() - y1) / self.ySpan() > 0:
            y1 = p.y()
        self._p0 = Point(x0,y0)
        self._p1 = Point(x1,y1)
        
    def unite(self, r):
        """ 
        Unite this Rect with another. The result is that this Rect changes to
        include both former self and the other rect. 
        """
        self.include(r.p0())
        self.include(r.p1())
        
    def xFlip(self):
        """ Flip the rect horizontally """
        x0 = self._p0.x()
        y0 = self._p0.y()
        x1 = self._p1.x()
        y1 = self._p1.y()
        self._p0 = Point(x1,y0)
        self._p1 = Point(x0,y1)
        
    def yFlip(self):
        """ Flip the rect vertically """
        x0 = self._p0.x()
        y0 = self._p0.y()
        x1 = self._p1.x()
        y1 = self._p1.y()
        self._p0 = Point(x0,y1)
        self._p1 = Point(x1,y0)
        
    def contains(self, p):
        """ Check if this rect contains a point or another rect. """
        x0 = self._p0.x()
        y0 = self._p0.y()
        x1 = self._p1.x()
        y1 = self._p1.y()
        if isinstance( p, Point ):
            x = p.x()
            y = p.y()
            if x0 < x1:
                dx = x - x0
            else:
                dx = x - x1;
            if dx < 0 or dx > self.width():
                return False
            if y0 < y1:
                dy = y - y0
            else:
                dy = y - y1
            if dy < 0 or dy > self.height():
                return False
            return True
        else:
            return self.contains( p.p0() ) and self.contains( p.p1() )

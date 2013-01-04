tolerance = 1e-15

"""
A 2D point.
"""
class Point:
    
    def __init__(self, x = None, y = None):
        """ Constructor """
        if x != None:
            if isinstance(x, Point):
                self._x = x._x
                self._y = x._y
                return
            else:
                self._x = float(x)
        else:
            self._x = 0.0
        if y != None:
            self._y = float(y)
        else:
            self._y = 0.0
    
    def x(self):
        """ Get the x component """
        return self._x
            
    def y(self):
        """ Get the y component """
        return self._y
    
    def set(self, x, y):
        """ Set new values of x and y """
        self._x = float( x )
        self._y = float( y )
        
    def translate(self, dx, dy = None):
        """ Translate this point by a vector """
        if isinstance(dx, Point):
            self += dx
        else:
            self._x += float( dx )
            self._y += float( dy )
        
    def __eq__(self, other):
        """ Comparison == """
        if isinstance(other, Point):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    def __ne__(self, other):
        """ Comparison != """
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def isNear(self, other, xtolerance = tolerance, ytolerance = None):
        """ For approximate comparissons """
        if ytolerance == None:
            ytolerance = xtolerance
        return abs(self._x - other._x) <= xtolerance and abs(self._y - other._y) <= ytolerance 
    
    def isNearZero(self, xtolerance = tolerance, ytolerance = None):
        """ Check if this point is near (0,0) """
        return self.isNear(Point(), xtolerance, ytolerance)
    
    def __str__(self):
        """ Convert to string (print) """
        return '[' + str(self._x) + ',' + str(self._y) + ']'

    def __iadd__(self, other):
        """ Add a points or a number to this point """
        if isinstance(other, Point):
            self._x += other._x
            self._y += other._y
        else:
            f = float(other)
            self._x += f
            self._y += f
        return self

    def __add__(self, other):
        """ Add two points or add a number to a point and return the result """
        p = Point(self._x, self._y)
        p += other
        return p

    def __isub__(self, other):
        """ Subtract a points or a number from this point """
        if isinstance(other, Point):
            self._x -= other._x
            self._y -= other._y
        else:
            f = float(other)
            self._x -= f
            self._y -= f
        return self

    def __sub__(self, other):
        """ Subtract two points or subtract a number from a point and return the result """
        p = Point(self._x, self._y)
        p -= other
        return p

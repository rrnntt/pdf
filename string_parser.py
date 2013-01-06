

"""
Defines string parsing classes. Parsers can be combined to parse complex syntaxes.
"""

class Parser:
    """
    Base class for all parsers.
    """
    def __init__(self):
        # If this parser had a match _hasMatch is set to True
        self._hasMatch = False
        # Set to True when this parser has a match but it is en empty sub-string.
        #self._empty = False
        # Starting index of the matching sub-string
        self._start = 0
        # size of the matching sub-string
        self._size = 0
        # Set to true if the concrete parser can match an empty string, ie 
        # an empty string satisfies the match criteria.
        self._canMatchEmpty = False
        
    def clone(self):
        """
        Virtual copy constructor.
        Concrete parsers must implement this method
        """
        raise Exception('This is unimplemented parser')
    
    def match(self, s, i = 0, n = -1):
        """
        Tries to match string s starting at index i and search maximum of n characters.
        If n is negative search to the end of the string.
        Return True if match was found and False if not.
        """
        self._hasMatch = False
        s_len = len(s)
        # handle empty string: if can match empty strings return True
        # if not return False
        if s_len == 0 or n == 0 or i >= s_len:
            self._start = i + n
            self._size = 0
            self._hasMatch = self._canMatchEmpty
            #self._empty = True
            return self._hasMatch

        if n < 0 or n > s_len:
            n = s_len
            
        self._start = i
        self._hasMatch,self._size  = self._test(s, i, n) 
        #if self._size == 0:
        #    self._empty = True # why do I need this?
        
        return self._hasMatch
        

    def hasMatch(self):
        """
        Checks if this parser had a match.
        """
        return self._hasMatch

    def _test(self, s, i, n):
        """
        Virtual protected method implemented in the concrete parsers wich test the string
        for a match. Returns tuple (has_match, size_of_match)
        
        The idea is that this method doesn't change the state of this class directly but only
        states whether there is a match or not ( + give the size of the matching sub-string )
        
        Implementations do not have to check validity of i and n with respect to indexing s 
        because they are checked in match(s,i,n) which calls _test(). n must be checked however
        to be big enough for a particular parser, eg a parser matching string 'hello' much check
        that n is at least 5.
        
        ?? should n == 0 be checked ??
        """
        raise Exception('_test method not implemented')
    
    def getMatch(self, s):
        """
        Return the matching sub-string of s or raise Exception if there is no match.
        """
        if not self._hasMatch:
            raise Exception('There is no match')
        
        s_len = len(s)
        if self._start >= s_len or self._start + self._size >= s_len:
            raise Exception('Matching string is npt sub-string of s')
        
        return s[self._start : self._start + self._size]
        


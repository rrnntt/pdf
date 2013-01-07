"""
Defines string parsing classes. Parsers can be combined to parse complex syntaxes.
"""

class Parser:
    """Base class for all parsers."""
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
        """Virtual copy constructor.
        
        Concrete parsers must implement this method
        """
        raise Exception('This is unimplemented parser')
    
    def match(self, s, start = 0, end = -1):
        """Try to find a match in a string.
         
        Match string s starting at index start and upto index end (index of last character + 1).
        
        Args:
            s (str): a string to find a match in.
            start (int): starting index in s (default 0)
            end (int): ending index in s (default -1 meaning to the end of the string)
        Return:
            True if match was found and False if not.
        """
        self._hasMatch = False
        s_len = len(s)
        # n: length of the searchable sub-string
        n = end - start
        # handle empty string: if can match empty strings return True
        # if not return False
        if s_len == 0 or n == 0 or start >= s_len:
            self._start = start
            self._size = 0
            self._hasMatch = self._canMatchEmpty
            return self._hasMatch

        if n < 0 or end > s_len:
            end = s_len
            n = s_len - start
            
        self._start = start
        self._hasMatch,size = self._test(s, start, end)
        # make sure _size is 0 if there is no match
        if self._hasMatch:
            if size > n:
                raise Exception('Wrong size returned by a parser')
            self._size = size
        else:
            self._size = 0 
        
        return self._hasMatch
        

    def hasMatch(self):
        """Checks if this parser had a match."""
        return self._hasMatch

    def _test(self, s, start, end):
        """Virtual protected method implemented in the concrete parsers wich test the string for a match. 
        
        Args:
            s (str): a string to find a match in.
            start (int): starting index in s.
            end (int): ending index in s.
        Return:
            tuple (has_match, size_of_match)
        
        The idea is that this method doesn't change the state of this class directly but only
        states whether there is a match or not ( + give the size of the matching sub-string )
        
        Implementations do not have to check validity of i and n with respect to indexing s 
        because they are checked in match(s,i,n) which calls _test(). n must be checked however
        to be big enough for a particular parser, eg a parser matching string 'hello' much check
        that n is at least 5.
        """
        raise Exception('_test method not implemented')
    
    def getMatch(self, s):
        """Return the matching sub-string of s or raise Exception if there is no match."""
        if not self._hasMatch:
            raise Exception('There is no match')

        if self._size == 0 and self._canMatchEmpty:
            return ''
                
        s_len = len(s)
        if self._start >= s_len or self._start + self._size > s_len:
            raise Exception('Matching string is not sub-string of s')
        
        return s[self._start : self._start + self._size]
        

class CharParser(Parser):
    """Match a single character from a list."""
    def __init__(self, s):
        """
        Constructor. Initializes the parser with a list of characters to choose from.
        s is a string with characters to match. s cannot be empty. 
        """
        Parser.__init__(self)
        self._chars = s
        if len(s) == 0:
            raise Exception('List of characters cannot be empty')
    
    def _test(self, s, start, end):
        """Implements the match test."""
        if s[start] in self._chars:
            return (True, 1)
        else:
            return (False, 0)
        
    def clone(self):
        """Implements cloning."""
        return CharParser(self._chars)
        
class NotCharParser(Parser):
    """Match a single character not from a list."""
    def __init__(self, s):
        """
        Constructor. Initializes the parser with a list of characters to choose from.
        s is a string with characters to match. s cannot be empty. 
        """
        Parser.__init__(self)
        self._chars = s
        if len(s) == 0:
            raise Exception('List of characters cannot be empty')
    
    def _test(self, s, start, end):
        """Implements the match test."""
        if s[start] not in self._chars:
            return (True, 1)
        else:
            return (False, 0)
        
    def clone(self):
        """Implements cloning."""
        return NotCharParser(self._chars)
        
class StringParser(Parser):
    """Match a string exactly."""
    def __init__(self, s):
        """
        Constructor. Initializes the parser with a string to match with.
        s cannot be empty. 
        """
        Parser.__init__(self)
        self._string = s
        if len(s) == 0:
            raise Exception('String cannot be empty')
    
    def _test(self, s, start, end):
        """Implements the match test."""
        string_length = len(self._string) 
        if s[start : start + string_length] == self._string:
            return (True, string_length)
        else:
            return (False, 0)
        
    def clone(self):
        """
        Implements cloning.
        """
        return StringParser(self._string)
        
    
class NotStringParser(Parser):
    """Match all characters until a certain string is found"""
    def __init__(self, s):
        """Constructor. 
        
        Initializes the parser with a string to match with.
        
        Args:
            s (str): the pattern string, cannot be empty. 
        """
        Parser.__init__(self)
        self._string = s
        if len(s) == 0:
            raise Exception('String cannot be empty')
    
    def _test(self, s, start, end):
        """Implements the match test."""
        j = s.find( self._string, start, end )
        n = end - start
        # if _string not found all of s matches
        if j < 0 or n < len(self._string):
            return (True, n)

        size = j - start
        if size == 0:
            return (False, 0)
        
        return (True, size)
        
    def clone(self):
        """Implements cloning."""
        return NotStringParser(self._string)
        
class ZeroOrMoreSpaces(Parser):
    """Match any number (including zero) of consequtive empty space characters.
    
    The empty space characters are ' ', '\t', '\n'. Always has a match.
    """
    def __init__(self):
        """Constructor."""
        Parser.__init__(self)
        self._chars = ' \t\n'
        self._canMatchEmpty = True
        
    def clone(self):
        """Implements cloning."""
        return ZeroOrMoreSpaces()

    def _test(self, s, start, end):
        """Implements the match test."""
        for i in range(start,end):
            if s[i] not in self._chars:
                return (True, i - start)
        return (True, end - start)

class MultiParser(Parser):
    """Base class for a complex parser containing other parsers."""
    def __init__(self):
        """Constructor."""
        Parser.__init__(self)
        self._parsers = []
        
    def clone(self):
        """Implements cloning. Clones all child parsers."""
        p = MultiParser()
        for c in self._parsers:
            p.addParser( c.clone() )
        return p
        
    def addParser(self, p):
        """Add a child parser.
        
        Args:
            p (Parser): a child parser.
        """
        if not isinstance(p, Parser):
            raise Exception('A Parser expected.')
        self._parsers.append(p)
        
    def __getitem__(self, i):
        """Return i-th child parser."""
        return self._parsers[i]
    
    def __len__(self):
        """Return number of child parsers."""
        return len(self._parsers)
        
class SeqParser(MultiParser):
    """Sequential parser: a sequence of parsers which all must match.""" 
    def __init__(self):
        """Constructor."""
        MultiParser.__init__(self)

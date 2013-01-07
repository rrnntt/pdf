import unittest
import string_parser as sp
from string_parser import Parser

class ABCParser(Parser):
    """
    Test parser matching string 'ABC'
    """
    def _test(self, s, i, n):
        
        if n < 3:
            return (False, 0)
        
        if s[i:i+3] == 'ABC':
            return (True, 3)
        else:
            return (False, 0)
        
class BlankSpaceParser(Parser):
    """
    Test parser matching a space character or making an empty match. Always makes a match.
    To test Parser.match(s,i,n) handling empty matches.
    """
    def _test(self, s, i , n):
        if n == 0:
            return (True, 0)
        if s[i] == ' ':
            return (True, 1)
        else:
            return (True, 0)
        
class WrongSizeParser(Parser):
    """
    Returns a very big size of the matched string. To test that Parser.match(s,i,n) can detect this.
    """
    def _test(self, s, i , n):
        return (True, 10000)

class TestStringParser(unittest.TestCase):
    
    def test_match(self):
        # matching the whole string
        p1 = ABCParser()
        p1.match('ABC')
        self.assertTrue(p1.hasMatch())
        self.assertEqual(p1.getMatch('ABC'), 'ABC')
        # matching at start of the string
        p2 = ABCParser()
        p2.match('ABC123')
        self.assertTrue(p2.hasMatch())
        # doesn't match at start of the string
        p3 = ABCParser()
        p3.match(' ABC ')
        self.assertFalse(p3.hasMatch())
        # match at offset from start of the string
        p4 = ABCParser()
        p4.match(' ABC ', 1)
        self.assertTrue(p4.hasMatch())

        p5 = BlankSpaceParser()
        p5.match(' s')
        self.assertTrue(p5.hasMatch())

        p6 = BlankSpaceParser()
        p6.match('ss', 1)
        self.assertTrue(p6.hasMatch())
        
        # starting index out of range
        p7 = ABCParser()
        p7.match('ABC', 3)
        self.assertFalse(p7.hasMatch())
        
        # n is greater than the string length 
        p8 = ABCParser()
        p8.match('ABC', 0, 10)
        self.assertTrue(p8.hasMatch())
        
        # n is smaller than the string length
        p9 = ABCParser()
        p9.match('ABC', 0, 2)
        self.assertFalse(p9.hasMatch())
        
        p = WrongSizeParser()
        self.assertRaises(Exception, p.match, 'ABC')
        

    def test_getMatch(self):
        
        p2 = ABCParser()
        p2.match('ABC123')
        self.assertEqual( p2.getMatch('ABC123'), 'ABC' )

        p5 = BlankSpaceParser()
        p5.match(' s')
        self.assertEqual( p5.getMatch(' s'), ' ' )

        p6 = BlankSpaceParser()
        p6.match('ss', 1)
        self.assertEqual( p6.getMatch(' s'), '' )

    def test_CharParser(self):
        # initialization with empty strings is not allowed 
        self.assertRaises(Exception, sp.CharParser, '' )
        
        c = sp.CharParser('ab')
        # has no match just after creation
        self.assertFalse( c.hasMatch() )
        s = 'ambs'
        c.match(s)
        self.assertTrue(c.hasMatch())
        self.assertEqual(c.getMatch(s), 'a')

        c1 = sp.CharParser('ab')
        c1.match(s, 2)
        self.assertTrue(c1.hasMatch())
        self.assertEqual(c1.getMatch(s), 'b')

        c2 = sp.CharParser('ab')
        c2.match('')
        self.assertFalse(c2.hasMatch())
        
        # clone returns a cleanly initialized copy
        cc = c2.clone()
        self.assertEqual(cc._chars, 'ab')
        self.assertFalse(cc.hasMatch())

    def test_NotCharParser(self):
        # initialization with empty strings is not allowed 
        self.assertRaises(Exception, sp.NotCharParser, '' )
        
        c = sp.NotCharParser('ab')
        # has no match just after creation
        self.assertFalse( c.hasMatch() )
        
        s = 'ambs'
        c.match(s)
        self.assertFalse(c.hasMatch())

        c1 = sp.NotCharParser('ab')
        c1.match(s, 1)
        self.assertTrue(c1.hasMatch())
        self.assertEqual(c1.getMatch(s), 'm')

        c2 = sp.NotCharParser('ab')
        c2.match('')
        self.assertFalse(c2.hasMatch())
        
        # clone returns a cleanly initialized copy
        cc = c2.clone()
        self.assertEqual(cc._chars, 'ab')
        self.assertFalse(cc.hasMatch())

    def test_StringParser(self):
        # initialization with empty strings is not allowed 
        self.assertRaises(Exception, sp.StringParser, '' )
        
        s = 'hello world!'
        p = sp.StringParser('hello')
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'hello')

        s = 'world hello!'
        p = sp.StringParser('hello')
        p.match(s,6)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'hello')

        s = 'Hello'
        p = sp.StringParser('hello')
        p.match(s)
        self.assertFalse(p.hasMatch())

    def test_NotStringParser(self):
        # initialization with empty strings is not allowed 
        self.assertRaises(Exception, sp.NotStringParser, '' )
        
        s = 'stop here'
        p = sp.NotStringParser('here')
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'stop ')
        
        s = ''
        p = sp.NotStringParser('here')
        p.match(s)
        self.assertFalse(p.hasMatch())
        
        s = 'stop there'
        p = sp.NotStringParser('here')
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'stop t')
        
        s = 'dont stop'
        p = sp.NotStringParser('here')
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'dont stop')
        
        s = 'here dont stop'
        p = sp.NotStringParser('here')
        p.match(s,0,3)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'her')
        
        s = 'here dont stop'
        p = sp.NotStringParser('here')
        p.match(s,1,5)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'ere d')
        
        s = 'here dont stop'
        p = sp.NotStringParser('here')
        p.match(s,10,15)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'stop')
        

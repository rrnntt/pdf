import unittest
import string_parser as sp
from string_parser import Parser

class ABCParser(Parser):
    """Test parser matching string 'ABC'"""
    def _test(self, s, start, end):
        n = end - start
        if n < 3:
            return (False, 0)
        
        if s[start:start+3] == 'ABC':
            return (True, 3)
        else:
            return (False, 0)
        
    def clone(self):
        return ABCParser()
        
class BlankSpaceParser(Parser):
    """Test parser matching a space character or making an empty match. 
    
    Always makes a match. To test Parser.match(s,start,end) handling empty matches.
    """
    def _test(self, s, start , end):
        if start == end:
            return (True, 0)
        if s[start] == ' ':
            return (True, 1)
        else:
            return (True, 0)
        
    def clone(self):
        return BlankSpaceParser()
        
class WrongSizeParser(Parser):
    """
    Returns a very big size of the matched string. To test that Parser.match(s,i,n) can detect this.
    """
    def _test(self, s, start , end):
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
        
    def test_AllNotCharParser(self):
        # initialization with empty strings is not allowed 
        self.assertRaises(Exception, sp.AllNotCharParser, '' )
        
        p = sp.AllNotCharParser(' (')
        s = 'function   (x)'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'function')
        
        p = sp.AllNotCharParser(' (')
        s = 'function( x )'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'function')
        

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
        p.match(s,1,6)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'ere d')
        
        s = 'here dont stop'
        p = sp.NotStringParser('here')
        p.match(s,10,15)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'stop')
        
    def test_ZeroOrMoreSpaces(self):
        
        s = '   hello!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'   ')
        
        s = 'hello   world!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s,5)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'   ')

        s = 'hello      world!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s,5)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'      ')

        s = 'hello      world!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s,5,8)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'   ')

        s = 'hello      world!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s,1)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'')

        s = 'hello\n     \tworld!'
        p = sp.ZeroOrMoreSpaces()
        p.match(s,5)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'\n     \t')

        s = ''
        p = sp.ZeroOrMoreSpaces()
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'')
        
    def test_AllParser(self):
        
        p = sp.AllParser()
        s = 'stuff 12@'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),s)
        
        p = sp.AllParser()
        s = ''
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),s)
        
        
    def test_MultiParser(self):
        
        p = sp.MultiParser()
        p0 = ABCParser()
        p1 = BlankSpaceParser()
        p.addParser(p0)
        p.addParser(p1)
        
        self.assertEqual(len(p), 2)
        self.assertEqual(p[0], p0)
        self.assertEqual(p[1], p1)
        
        c = p.clone()
        self.assertEqual(len(c), 2)
        self.assertTrue( isinstance(c,sp.MultiParser) )
        self.assertTrue( isinstance(c[0],ABCParser) )
        self.assertTrue( isinstance(c[1],BlankSpaceParser) )
        self.assertNotEqual(c, p)
        self.assertNotEqual(c[0], p0)
        self.assertNotEqual(c[1], p1)
        
    def test_SeqParser(self):
        
        s = 'Hello   World!'
        p = sp.SeqParser()
        p.addParser(sp.StringParser('Hello'))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.StringParser('World!'))
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),s)
        
        s = 'HelloWorld!'
        p = sp.SeqParser()
        p.addParser(sp.StringParser('Hello'))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.StringParser('World!'))
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),s)
        
        s = 'hello   World!'
        p = sp.SeqParser()
        p.addParser(sp.StringParser('Hello'))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.StringParser('World!'))
        p.match(s)
        self.assertFalse(p.hasMatch())
        
        s = 'Hello   World'
        p = sp.SeqParser()
        p.addParser(sp.StringParser('Hello'))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.StringParser('World!'))
        p.match(s)
        self.assertFalse(p.hasMatch())
        
        s = 'function(   x )'
        p = sp.SeqParser()
        p.addParser(sp.AllNotCharParser(' ('))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.CharParser('('))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.AllNotCharParser(' )'))
        p.addParser(sp.ZeroOrMoreSpaces())
        p.addParser(sp.CharParser(')'))
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),s)
        res = p[0].getMatch(s) + p[2].getMatch(s) + p[4].getMatch(s) + p[6].getMatch(s)
        self.assertEqual(res,'function(x)')
        
    def test_AltParser(self):
        
        s = 'hello'
        p = sp.AltParser()
        p.addParser( sp.StringParser('hello') )
        p.addParser( sp.StringParser('world') )
        p.match( s )
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'hello')
        self.assertTrue( p.goodParser() )
        self.assertEqual(p.goodParser().getMatch(s),'hello')
        
        s = 'world!'
        p = sp.AltParser()
        p.addParser( sp.StringParser('hello') )
        p.addParser( sp.StringParser('world!') )
        p.match( s )
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'world!')
        self.assertTrue( p.goodParser() )
        self.assertEqual(p.goodParser().getMatch(s),'world!')
        
    def test_BracketsParser(self):
        
        p = sp.BracketsParser()
        s = '(< a + b >)   '
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'(< a + b >)')
        self.assertEqual(p[0].getMatch(s),'< a + b >')
        
        p = sp.BracketsParser('(<', '>)')
        s = '(< a + b >)   '
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'(< a + b >)')
        self.assertEqual(p[0].getMatch(s),' a + b ')

        p = sp.BracketsParser()
        s = '((a) + b*(c+sin(x)))   '
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'((a) + b*(c+sin(x)))')
        self.assertEqual(p[0].getMatch(s),'(a) + b*(c+sin(x))')
        
    def test_AlphaParser(self):
        
        p = sp.AlphaParser()
        s = 'Alpha123'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'Alpha')
        
        p = sp.AlphaParser()
        s = 'Alpha Beta'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'Alpha')
        
        p = sp.AlphaParser()
        s = 'Alpha( Beta )'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'Alpha')
        
class TestListParser(unittest.TestCase):
    
    def test_ListParser(self):
        
        p = sp.ListParser( sp.CharParser('a') )
        s = 'aaab'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'aaa')
        self.assertTrue(p[2] == p.lastToken())
        self.assertEqual(len(p),3)
        self.assertTrue(p[-1].hasMatch())
        
        p = sp.ListParser( sp.CharParser('a') )
        p.match('')
        self.assertFalse(p.hasMatch())
        self.assertEqual(len(p),0)
        self.assertEqual(p.lastToken(), None)
        
        p = sp.ListParser( sp.CharParser('a'), True )
        p.match('')
        self.assertTrue(p.hasMatch())
        self.assertEqual(len(p),0)
        self.assertEqual(p.lastToken(), None)
        
        # has match if 'zero' argument is True
        p = sp.ListParser( sp.CharParser('a'), True )
        s = 'bbb'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'')
        self.assertEqual(len(p),0)
        self.assertEqual(p.lastToken(), None)
        
        p = sp.ListParser( (sp.NotCharParser(','),sp.CharParser(',')) )
        s = 'h,e,l,l,o'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'h,e,l,l,o')
        res = p[0].getMatch(s)+p[2].getMatch(s)+p[4].getMatch(s)+p[6].getMatch(s)+p[8].getMatch(s)
        self.assertEqual(res,'hello')
        self.assertEqual(len(p),9)
        self.assertTrue(p[8] == p.lastToken())

        p = sp.ListParser( (sp.CharParser('helo'),sp.CharParser(',')) )
        s = 'h,e,l,l,o,w'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertTrue(p._canLastBeEmpty)
        self.assertEqual(p.getMatch(s),'h,e,l,l,o,')
        res = p[0].getMatch(s)+p[2].getMatch(s)+p[4].getMatch(s)+p[6].getMatch(s)+p[8].getMatch(s)
        self.assertEqual(res,'hello')
        self.assertEqual(len(p),11)
        self.assertTrue(p[10] == p.lastToken()) # shouldn't last token be None? or last good?

        p = sp.ListParser( (sp.NotCharParser(','),sp.CharParser(',')) )
        s = 'h,e,l,l,o,'
        p.match(s)
        self.assertTrue(p.hasMatch())
        self.assertEqual(p.getMatch(s),'h,e,l,l,o,')
        res = p[0].getMatch(s)+p[2].getMatch(s)+p[4].getMatch(s)+p[6].getMatch(s)+p[8].getMatch(s)
        self.assertEqual(res,'hello')
        # token parser failed on the last empty token doesn't have a match
        self.assertEqual(len(p),11)
        self.assertTrue(p[10] == p.lastToken()) # shouldn't last token be None? or last good?

        p = sp.ListParser( (sp.NotCharParser(','),sp.CharParser(','), False) )
        s = 'h,e,l,l,o,'
        p.match(s)
        self.assertFalse(p.hasMatch())
        self.assertEqual(p.lastToken(), None)
        
    def xtest_lookAtParent(self):
        
        class MockParser(sp.CharParser):
            def __init__(self, s):
                sp.CharParser.__init__(self, s)
                
            def clone(self):
                return MockParser(self._chars)
                
            def lookAtParent(self, parser, s):
                if isinstance(parser, sp.ListParser):
                    last = parser.lastToken()
                    if last:
                        last.mess = last.getMatch(s)+' is followed by '+self.getMatch(s)+'\n'
                        #print last.mess
                        
        mock = MockParser('abc')
        p = sp.ListParser( mock )
        p.match('bca')
        self.assertEqual( p[0].mess, 'b is followed by c\n' )
        self.assertEqual( p[1].mess, 'c is followed by a\n' )
                
        mock = MockParser('abc')
        p = sp.ListParser( (mock,sp.CharParser(',')) )
        p.match('a,b,c')
        self.assertEqual( p[0].mess, 'a is followed by b\n' )
        self.assertEqual( p[2].mess, 'b is followed by c\n' )
        
        mock = MockParser('abc')
        p = sp.ListParser( (mock,sp.CharParser(','),True) )
        p.match('b,a,c')
        self.assertEqual( p[0].mess, 'b is followed by a\n' )
        self.assertEqual( p[2].mess, 'a is followed by c\n' )
        
        mock = MockParser('abc')
        p = sp.ListParser( (mock,sp.CharParser(','),True) )
        p.match('a,c,b,')
        self.assertEqual( p[0].mess, 'a is followed by c\n' )
        self.assertEqual( p[2].mess, 'c is followed by b\n' )
                

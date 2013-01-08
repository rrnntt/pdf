import unittest
import latex_parser as lp

class TestLatexParsers(unittest.TestCase):
    
    def test_CommandParser(self):
        
        p = lp.CommandParser()
        s = '\\alpha \\beta'
        p.match( s )
        self.assertTrue( p.hasMatch() )
        self.assertEquals( p.getMatch(s), '\\alpha')
        
        p = lp.CommandParser()
        s = '\\Alpha \\beta'
        p.match( s )
        self.assertFalse( p.hasMatch() )

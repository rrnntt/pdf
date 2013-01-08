"""Simple latex parser"""
from string_parser import *

# commands without arguments
command_names_0 = ['alpha', 'beta', 'gamma']

class CommandParser(Parser):
    """Parses a latex command of the form: \command_name ."""
    def __init__(self):
        """Constructor."""
        Parser.__init__(self)
        self._nameParser = SeqParser()
        self._nameParser.addParser( CharParser('\\') )
        self._nameParser.addParser( AlphaParser() )
        
    def clone(self):
        """Implement cloning"""
        return CommandParser()
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self._nameParser.match(s, start, end)
        if not self._nameParser.hasMatch():
            return (False, 0)
        
        if self._nameParser[1].getMatch(s) in command_names_0:
            return self._simpleCommand(start)
        
        return (False, 0)

    def _simpleCommand(self, start):
        return (True, self._nameParser.getEnd() - start)
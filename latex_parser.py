"""Simple latex parser"""
from string_parser import *
from document import *
    
######################################################################################
#        Parsers
######################################################################################
""" Commands without arguments:
Dictionaries containing DocItem class names with constructors taking
a single argument - the command name
"""
# command names for commands which can be found inside a paragraph
para_command_names_0 = {}
for name,code in symbols.iteritems():
    para_command_names_0[name] = Symbol
    
# names for commands appearing outside paragraphs
doc_command_names_0 = {}

""" Commands with 1 arguments:
Dictionaries containing DocItem class names with constructors taking
two arguments: the command name, and the argument
"""
# names for commands appearing outside paragraphs
doc_command_names_1 = {'title': Title,
                  }

#---------------------------------------------------------------------------------
class LatexParser(Parser):
    """Base class for latex parsers."""
    def __init__(self, mode = 'body'):
        """Constructor.
    
        Args:
            mode (str): a latex mode: 'body' or 'math'
        """
        Parser.__init__(self)
        self.mode = mode
        self.docItem = None

#---------------------------------------------------------------------------------
class CommandParser(LatexParser):
    """Parses a latex command of the form: \command_name ."""
    def __init__(self, creator, mode = 'body'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.nameParser = SeqParser()
        self.nameParser.addParser( CharParser('\\') )
        self.nameParser.addParser( AlphaParser() )
        self.creator = creator
        
    def clone(self):
        """Implement cloning"""
        return CommandParser(self.creator, self.mode)
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self.nameParser.match(s, start, end)
        if not self.nameParser.hasMatch():
            return (False, 0)

        name = self.nameParser[1].getMatch(s)        
#        if name in command_names_0:
#            self.docItem = command_names_0[name](name)
#            return (True, self.nameParser.getEnd() - start)
        self.docItem = self.creator(name)
        if self.docItem: 
            return (True, self.nameParser.getEnd() - start)
        
        return (False, 0)

#---------------------------------------------------------------------------------
class WordParser(LatexParser):
    """Parses a normal word."""
    def __init__(self, mode = 'body'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.parser = AllNotCharParser(' \t\n\\')
        
    def clone(self):
        """Implement cloning"""
        return WordParser(self.mode)
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        self.docItem = Word(self.parser.getMatch(s))
        self.docItem.style = self.mode
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
def ParagraphItemCreator(cmd_name, arg1 = None):
    if cmd_name in para_command_names_0:
        return para_command_names_0[cmd_name](cmd_name)
    return None
    
#---------------------------------------------------------------------------------
class MathVariableParser(LatexParser):
    def __init__(self):
        LatexParser.__init__(self, mode='math-var')

    def clone(self):
        """Implement cloning"""
        return MathVariableParser()
    
    def _test(self, s, start, end):
        parser = AlphaParser()
        parser.match(s, start, end)
        if not parser.hasMatch():
            return (False, 0)
        self.docItem = MathVariable(parser.getMatch(s))
        return (True, parser.getEnd() - start)

#---------------------------------------------------------------------------------
class MathSignParser(LatexParser):
    def __init__(self):
        LatexParser.__init__(self, mode='math-var')

    def clone(self):
        """Implement cloning"""
        return MathSignParser()
    
    def _test(self, s, start, end):
        parser = CharParser('+-=><,!/')
        parser.match(s, start, end)
        if not parser.hasMatch():
            return (False, 0)
        self.docItem = MathSign(parser.getMatch(s))
        return (True, parser.getEnd() - start)

#---------------------------------------------------------------------------------
class MathSymbolParser(LatexParser):
    def __init__(self):
        LatexParser.__init__(self, mode='math-var')

    def clone(self):
        """Implement cloning"""
        return MathSymbolParser()
    
    def _test(self, s, start, end):
        parser = SeqParser()
        parser.addParser( CharParser('\\') )
        parser.addParser( AlphaParser() )
        parser.match(s, start, end)
        if not parser.hasMatch():
            return (False, 0)
        name = parser[1].getMatch(s)
        if name in symbols:
            self.docItem = Symbol(name)
            return (True, parser.getEnd() - start)
        elif name in funs:
            self.docItem = MathFunction(name)
            return (True, parser.getEnd() - start)
        else:
            return (False, 0)

#---------------------------------------------------------------------------------
class MathNumberParser(LatexParser):
    def __init__(self):
        LatexParser.__init__(self, mode='math-var')

    def clone(self):
        """Implement cloning"""
        return MathNumberParser()
    
    def _test(self, s, start, end):
        parser = SeqParser()
        parser.addParser( ListParser(DigitParser()) )
        parser.addParser( ListParser(CharParser('.'),True,1) )
        parser.addParser( ListParser(DigitParser(),True) )
        parser.match(s, start, end)
        if not parser.hasMatch():
            return (False, 0)
        name = parser.getMatch(s)
        self.docItem = MathNumber(name)
        return (True, parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class MathFracParser(LatexParser):
    def __init__(self, inner_parser):
        LatexParser.__init__(self, mode='math-var')
        self.inner_parser = inner_parser

    def clone(self):
        """Implement cloning"""
        return MathFracParser()
    
    def _test(self, s, start, end):
        numerator = self.inner_parser()
        denominator = self.inner_parser()
        parser = SeqParser()
        parser.addParser( StringParser('\\frac') )
        parser.addParser( ZeroOrMoreSpaces() )
        parser.addParser( BracketsParser('{','}',numerator) )
        parser.addParser( ZeroOrMoreSpaces() )
        parser.addParser( BracketsParser('{','}',denominator) )
        parser.match(s, start, end)
        if not parser.hasMatch():
            return (False, 0)
        self.docItem = MathFrac()
        self.docItem.appendItem( numerator.docItem )
        self.docItem.appendItem( denominator.docItem )
        return (True, parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class InlineMathItemParser(LatexParser):
    """Parser for an item in a paragraph: a word or a command."""
    def __init__(self, recursion_parser):
        """Constructor."""
        LatexParser.__init__(self)
        self.recursion_parser = recursion_parser
        self.parser = AltParser()
        self.parser.addParser( MathSymbolParser() )
        self.parser.addParser( MathSignParser() )
        self.parser.addParser( MathVariableParser() )
        self.parser.addParser( MathNumberParser() )
        self.parser.addParser( MathFracParser(self.recursion_parser) )
        
    def clone(self):
        """Implement cloning"""
        return InlineMathItemParser(self.recursion_parser)

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        good = self.parser.goodParser()
        if isinstance( good, LatexParser ):
            self.docItem = good.docItem
        else:
            return (False, 0)
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class InlineMathParser(LatexParser):
    """Parses a inlined (in line with text in a paragraph) math expression."""
    def __init__(self, mode = 'body'):
        """Constructor."""
        LatexParser.__init__(self)
        self.parser = SeqParser()
        self.parser.addParser( ZeroOrMoreSpaces() )
        self.itemParser = ListParser( (InlineMathItemParser(InlineMathParser), ZeroOrMoreSpaces()) )
        self.parser.addParser( self.itemParser )
        
    def clone(self):
        """Implement cloning"""
        return InlineMathParser()
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)

        doc = InlineMathBlock()
        n = len(self.itemParser)
        for i in range(0,n,2):
            p = self.itemParser[i]
            if p.docItem:
                doc.appendItem(p.docItem)
        self.docItem = doc
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class ItemInBracketsParser(LatexParser):
    """Parses a inlined (in line with text in a paragraph) math expression."""
    def __init__(self, bra, ket, innerParser):
        """Constructor."""
        LatexParser.__init__(self)
        self.parser = BracketsParser(bra, ket, innerParser)
        
    def clone(self):
        """Implement cloning"""
        return ItemInBracketsParser()
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        self.docItem = self.parser[0].docItem
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class ParagraphItemParser(LatexParser):
    """Parser for an item in a paragraph: a word or a command."""
    def __init__(self, mode = 'body'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.parser = AltParser()
        self.parser.addParser( CommandParser(ParagraphItemCreator, mode) )
        self.parser.addParser( ItemInBracketsParser('$','$',InlineMathParser()) )
        self.parser.addParser( WordParser(mode) )
        
    def clone(self):
        """Implement cloning"""
        p = ParagraphItemParser(self.mode)
        return p

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        good = self.parser.goodParser()
        if isinstance( good, LatexParser ):
            self.docItem = good.docItem
        else:
            # maybe it's an error?
            self.docItem = Word(self.parser.getMatch(s))
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class ParagraphSpaces(Parser):
    """Match 1 or more consequtive empty space characters.
    
    The empty space characters are ' ', '\t', '\n'. Fails if meets the paragraph ending sequence '\n\n'.
    """
    def __init__(self):
        """Constructor."""
        Parser.__init__(self)
        self._chars = ' \t'
        
    def clone(self):
        """Implements cloning."""
        return ParagraphSpaces()

    def _test(self, s, start, end):
        """Implements the match test."""
        for i in range(start,end):
            c = s[i]
            if c not in self._chars:
                if c != '\n':
                    return (True, i - start)
                elif i+1 < end and s[i+1] == '\n' :
                    return (False, 0)
        return (True, end - start)

#---------------------------------------------------------------------------------
class ParagraphParser(LatexParser):
    """Parses a paragraph"""
    def __init__(self, mode = 'body', paragraph = Paragraph):
        """Constructor."""
        LatexParser.__init__(self, mode)
        parsers = (ParagraphItemParser(), ParagraphSpaces())
        self.parser = ListParser( parsers )
        self.paragraph = paragraph

    def clone(self):
        """Implement cloning"""
        p = ParagraphParser(self.mode)
        return p

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        
        para = self.paragraph()
        for i in range(0,len(self.parser),2):
            p = self.parser[i]
            para.appendItem(p.docItem)
        self.docItem = para
            
        return (True, self.parser.getEnd() - start)

#def DocumentItemCreator(cmd_name, arg1 = None):
#    if arg1:
#        if cmd_name in doc_command_names_1:
#            item = 
#            return doc_command_names_0[cmd_name](cmd_name)
#    return None

#---------------------------------------------------------------------------------
class TitleParser(LatexParser):
    """Parsers the \title{...} command."""
    def __init__(self):
        """Constructor."""
        LatexParser.__init__(self)
        self.parser = SeqParser()
        self.parser.addParser( CharParser('\\') )
        self.parser.addParser( AlphaParser() ) 
        self.parser.addParser( ZeroOrMoreSpaces() ) 
        self.textParser = ParagraphParser('body',Title)
        innerParser = SeqParser()
        innerParser.addParser(ZeroOrMoreSpaces())
        innerParser.addParser(self.textParser)
        self.parser.addParser( BracketsParser('{','}', innerParser) )
         
    def clone(self):
        """Implement cloning"""
        return TitleParser()

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
    
        if not isinstance(self.textParser.docItem, Title):
            raise Exception("Wrong doc item in title")
        
        self.docItem = self.textParser.docItem
        
        for item in self.docItem.items:
            if not item:
                del item
        
        return (True, self.parser.getEnd() - start)
        
#---------------------------------------------------------------------------------
class DocumentItemParser(LatexParser):
    """Parser for an item in a paragraph: a word or a command."""
    def __init__(self, mode = 'body'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.parser = AltParser()
        self.parser.addParser( TitleParser() )
        self.parser.addParser( ParagraphParser() )
        
    def clone(self):
        """Implement cloning"""
        return DocumentItemParser(self.mode)

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        good = self.parser.goodParser()
        if isinstance( good, LatexParser ):
            self.docItem = good.docItem
        else:
            return (False, 0)
        return (True, self.parser.getEnd() - start)
    
#---------------------------------------------------------------------------------
class DocumentParser(LatexParser):
    """Parse the whole document"""
    def __init__(self):
        """Constructor."""
        LatexParser.__init__(self)
        self.parser = SeqParser()
        self.parser.addParser( ZeroOrMoreSpaces() )
        self.itemParser = ListParser( (DocumentItemParser(), ZeroOrMoreSpaces()) )
        self.parser.addParser( self.itemParser )

    def clone(self):
        """Implement cloning"""
        return DocumentParser()

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        
        doc = Document()
        n = len(self.itemParser)
        for i in range(0,n,2):
            p = self.itemParser[i]
            if p.docItem:
                doc.appendParagraph(p.docItem)
        self.docItem = doc
            
        return (True, self.parser.getEnd() - start)
        
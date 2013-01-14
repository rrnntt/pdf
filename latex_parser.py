"""Simple latex parser"""
from string_parser import *
import rect
from rect import Rect

class DocItem:
    """An item of a document. Can be simple or complex. Complex items contain other items."""
    def __init__(self):
        self.items = []
        self.name = ''
    
symbols = {'alpha': u'\u03b1',
           'beta': u'\u03b2',
           'gamma': u'\u03b3',
           'delta': u'\u03b3',
           'epsilon': u'\u03b4',
           'zeta': u'\u03b5',
           'eta': u'\u03b6',
           'theta': u'\u03b7',
           'iiii': u'\u03b8',
           'kappa': u'\u03b9',
           'lambda': u'\u03ba',
           'mu': u'\u03bb',
           'nu': u'\u03bc',
           'xi': u'\u03bd',
           'oooo': u'\u03be',
           'pi': u'\u03bf',
           'rho': u'\u03c0',
           '?': u'\u03c1',
           'tau': u'\u03c2',
           'u': u'\u03c3',
           'phi': u'\u03c4',
           'chi': u'\u03c5',
           'psi': u'\u03c6',
          }

textAlignments = {'j': rect.justifyX,
                  'l': rect.alignLeft,
                  'r': rect.alignRight,
                  'c': rect.center,
                 }

class TextItem(DocItem):
    """Prints some form of text"""
    def __init__(self):
        DocItem.__init__(self)

    def writePDF(self, pdf = None):
        """Write itself to a FPDF object.
        
        Args:
            pdf (FPDF): the FPDF object to write to.
        """
        return self.getText()
    
    def resizePDF(self, pdf):
        """Resize internal Rect according to current settings of pdf"""
        width = pdf.get_string_width( self.getText() )
        height = pdf.font_size_pt / pdf.k
        self.rect = Rect( 0, 0, width, height )
    
    def cellPDF(self, pdf):
        r = self.rect
        pdf.set_y( r.y0() )
        pdf.set_x( r.x0() )
        pdf.cell( r.width(), r.height(), self.getText() )
        
class Word(TextItem):
    """Prints a word"""
    def __init__(self, name):
        TextItem.__init__(self)
        self.name = name
        
    def getText(self):
        """'Virtual' method returning text of this item."""
        return self.name
        
class Symbol(TextItem):
    """Prints a symbol or word wich can be output as a unicode string"""
    def __init__(self, name):
        TextItem.__init__(self)
        self.name = name
        
    def getText(self):
        """'Virtual' method returning text of this item."""
        return symbols[self.name]
        
class Paragraph(DocItem):
    """Paragraph of a documant."""
    def __init__(self, width = -1):
        DocItem.__init__(self)
        self.width = width
        # possible alignments: j (justify), l (left), r (right), c (center)
        self.textAlignment = 'j'
        
        
    def appendItem(self, item):
        """Append a document item to the paragraph."""
        self.items.append(item)
        
    def writePDF(self, pdf = None):
        """Write itself to a FPDF object."""
        res = ''
        for item in self.items:
            if item:
                res += item.writePDF(pdf) + ' '
        return res
    
    def resizePDF(self, pdf):
        if self.width <= 0:
            self.width = pdf.fw - pdf.l_margin - pdf.r_margin
        self.space = pdf.get_string_width(' ')
        self.lineHeight = pdf.font_size_pt / pdf.k * 1.2
            
        rectList = []
        for item in self.items:
            if item:
                item.resizePDF(pdf)
                rectList.append( item.rect )
            
        for r in rectList:
            r.translate(rect.Point(0,pdf.t_margin))
            
        alignFunction = textAlignments[self.textAlignment]
        
        onFirstLine = True
        while len( rectList ) > 0:
            n = alignFunction(rectList, pdf.l_margin, self.width, self.space)
            if n == len( rectList ) and self.textAlignment == 'j':
                rect.alignLeft(rectList, pdf.l_margin, self.width, self.space)
            if not onFirstLine:
                for r in rectList:
                    r.translate(rect.Point(0,self.lineHeight))
            onFirstLine = False
            del rectList[:n]
            
    def cellPDF(self, pdf):
        """Output the paragraph to PDF"""
        for item in self.items:
            if item:
                item.cellPDF(pdf)
                
        

""" commands without arguments """
command_names_0 = {'alpha':Symbol, 'beta':Symbol, 'gamma': Symbol}


class LatexParser(Parser):
    """Base class for latex parsers."""
    docItem = None
    def __init__(self, mode = 'text'):
        """Constructor.
    
        Args:
            mode (str): a latex mode: 'text' or 'math'
        """
        Parser.__init__(self)
        self._mode = mode

class CommandParser(LatexParser):
    """Parses a latex command of the form: \command_name ."""
    def __init__(self, mode = 'text'):
        """Constructor."""
        LatexParser.__init__(self, mode)
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

        name = self._nameParser[1].getMatch(s)        
        if name in command_names_0:
            self.docItem = command_names_0[name](name)
            return (True, self._nameParser.getEnd() - start)
        
        return (False, 0)

class WordParser(LatexParser):
    """Parses a normal word."""
    def __init__(self, mode = 'text'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.parser = AllNotCharParser(' \t\n\\')
        
    def clone(self):
        """Implement cloning"""
        return WordParser(self._mode)
    
    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        self.docItem = Word(self.parser.getMatch(s))
        return (True, self.parser.getEnd() - start)
    
    
class ParagraphItemParser(LatexParser):
    """Parser for an item in a paragraph: a word or a command."""
    def __init__(self, mode = 'text'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        self.parser = AltParser()
        self.parser.addParser( CommandParser(mode) )
        self.parser.addParser( WordParser(mode) )
        
    def clone(self):
        """Implement cloning"""
        p = ParagraphItemParser(self._mode)
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
    
class ParagraphParser(LatexParser):
    """Parses a paragraph"""
    def __init__(self, mode = 'text'):
        """Constructor."""
        LatexParser.__init__(self, mode)
        parsers = (ParagraphItemParser(), ZeroOrMoreSpaces())
        self.parser = ListParser( parsers )

    def clone(self):
        """Implement cloning"""
        p = ParagraphParser(self._mode)
        return p

    def _test(self, s, start, end):
        """Implements the match test."""
        self.parser.match(s, start, end)
        if not self.parser.hasMatch():
            return (False, 0)
        
        para = Paragraph()
        for i in range(0,len(self.parser),2):
            p = self.parser[i]
            para.appendItem(p.docItem)
        self.docItem = para
            
        return (True, self.parser.getEnd() - start)

"""Simple latex parser"""
from string_parser import *
import rect
from rect import Rect

######################################################################################
#     Document items
######################################################################################
class DocItem:
    """An item of a document. Can be simple or complex. Complex items contain other items."""
    def __init__(self):
        self.items = []
        self.name = ''
    
symbols = {'alpha': u'\u03b1',
           'beta': u'\u03b2',
           'gamma': u'\u03b3',
           'delta': u'\u03b4',
           'epsilon': u'\u03b5',
           'zeta': u'\u03b6',
           'eta': u'\u03b7',
           'theta': u'\u03b8',
           'iota': u'\u03b9',
           'kappa': u'\u03ba',
           'lambda': u'\u03bb',
           'mu': u'\u03bc',
           'nu': u'\u03bd',
           'xi': u'\u03be',
           'omicron': u'\u03bf',
           'pi': u'\u03c0',
           'rho': u'\u03c1',
           'varsigma': u'\u03c2',
           'sigma': u'\u03c3',
           'tau': u'\u03c4',
           'upsilon': u'\u03c5',
           'varphi': u'\u03c6',
           'chi': u'\u03c7',
           'psi': u'\u03c8',
           'omega': u'\u03c9',
           'phi': u'\u03d5',
           
           'Alpha': u'\u0391',
           'Beta': u'\u0392',
           'Gamma': u'\u0393',
           'Delta': u'\u0394',
           'Epsilon': u'\u0395',
           'Zeta': u'\u0396',
           'Eta': u'\u0397',
           'Theta': u'\u0398',
           'Iota': u'\u0399',
           'Kappa': u'\u039a',
           'Lambda': u'\u039b',
           'Mu': u'\u039c',
           'Nu': u'\u039d',
           'Xi': u'\u039e',
           'Omicron': u'\u039f',
           'Pi': u'\u03a0',
           'Rho': u'\u03a1',
           'Sigma': u'\u03a3',
           'Tau': u'\u03a4',
           'Upsilon': u'\u03a5',
           'Phi': u'\u03a6',
           'Chi': u'\u03a7',
           'Psi': u'\u03a8',
           'Omega': u'\u03a9',          
           }

textAlignments = {'j': rect.justifyX,
                  'l': rect.alignLeft,
                  'r': rect.alignRight,
                  'c': rect.center,
                 }

styles = {'body': ('times', '', 12),
          'title': ('times', 'B', 16),
          'symbol': ('DejaVu','', 12),
         }

def initPDF(pdf):
    """Set up a FPDF object to work with latex parsers"""
    pdf.add_page()
    pdf.add_font('DejaVu','','font/DejaVuSansCondensed.ttf',uni=True)


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
    
    def resizePDF(self, pdf, x = 0, y = 0):
        """Resize internal Rect according to current settings of pdf"""
        width = pdf.get_string_width( self.getText() )
        height = pdf.font_size_pt / pdf.k
        self.rect = Rect( x, y, x + width, y + height )
    
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
        self.style = 'body'
        
    def getText(self):
        """'Virtual' method returning text of this item."""
        return self.name
        
class Symbol(TextItem):
    """Prints a symbol or word wich can be output as a unicode string"""
    def __init__(self, name):
        TextItem.__init__(self)
        self.name = name
        self.style = 'symbol'
        
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
    
    def resizePDF(self, pdf, x = 0, y = 0):
        """Calculate the sizes of all items in the paragraph.
        
        Args:
            pdf (FPDF): the pdf object.
            x, y (float): coordinates of the top-left corner of the paragraph relative to the page's
                margins.
        """
        style = 'body'
        f = styles[style]
        pdf.set_font(f[0],f[1],f[2])
        if self.width <= 0:
            self.width = pdf.fw - pdf.l_margin - pdf.r_margin - x
        self.space = pdf.get_string_width(' ')
        self.lineHeight = pdf.font_size_pt / pdf.k * 1.2
        self.rect = Rect()
        
        y += pdf.t_margin
        rectList = []
        # resize individual items and collect their Rects
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    f = styles[style]
                    pdf.set_font(f[0],f[1],f[2])
                item.resizePDF(pdf, 0, y)
                rectList.append( item.rect )
            
        # position the items on the page
            
        alignFunction = textAlignments[self.textAlignment]
        
        xstart = pdf.l_margin + x
        xend = pdf.l_margin + x + self.width
        onFirstLine = True
        while len( rectList ) > 0:
            n = alignFunction(rectList, xstart, xend, self.space)
            if n == len( rectList ) and self.textAlignment == 'j':
                rect.alignLeft(rectList, xstart, xend, self.space)
            if not onFirstLine:
                for r in rectList:
                    r.translate(rect.Point(0,self.lineHeight))
            for r in rectList[:n]:
                self.rect.unite(r)
            onFirstLine = False
            del rectList[:n]
            
    def cellPDF(self, pdf):
        """Output the paragraph to PDF"""
        style = ''
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    f = styles[style]
                    pdf.set_font(f[0],f[1],f[2])
                item.cellPDF(pdf)
                
        pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')
                
                
class Title(Paragraph):
    """Print a document title."""
    def __init__(self, width = -1):
        Paragraph.__init__(self, width)
        self.textAlignment = 'c'
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if self.width <= 0:
            self.width = pdf.fw - pdf.l_margin - pdf.r_margin - x
            self.width *= 0.8
        for item in self.items:
            item.style = 'title'
        Paragraph.resizePDF(self, pdf, x, y)
        
        
######################################################################################
#        Parsers
######################################################################################
""" commands without arguments """
command_names_0 = {}

for name,code in symbols.iteritems():
    command_names_0[name] = Symbol

#command_names_1 = {'title': Title,
#                  }

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

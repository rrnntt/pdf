import rect
from rect import Rect

######################################################################################
#     Document items
######################################################################################
class DocItem:
    """An item of a document."""
    def __init__(self):
        self.text = ''
    
#---------------------------------------------------------------------------------
class MultiItem:
    """A complex item containing other items."""
    def __init__(self):
        self.items = []
        
    def appendItem(self, item):
        """Append a child document item."""
        self.items.append(item)
        
    def refit(self):
        """Refit all the children items so that they are all inside (if possible) of this MultiItem's rect.
        
        This method is supposed to be called after rect of this item has been moved by an outside object
        (a parent of this item for example). Other objects mustn't (shouldn't?) resize this rect however.
        Although I don't know how to enforce it in python.
        
        This method moves children's rects and refits them. 
        """
        old_rect = self.getUnionRect()
        dp = self.rect.p0() - old_rect.p0()
        for item in self.items:
            if item:
                item.rect.translate(dp)
                item.refit()
                
    def getUnionRect(self):
        """Create a union of all children's rects."""
        rect = Rect()
        for item in self.items:
            if item:
                rect.unite(item.rect)
        return rect
        
#---------------------------------------------------------------------------------
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

default_styles = {'body': ('times', '', 12),
          'title': ('times', 'B', 16),
          'symbol': ('symbol','', 12),
          'math-var': ('times', 'I', 12),
          'math-symbol': ('symbol', '', 12),
         }

#---------------------------------------------------------------------------------
def initPDF(pdf):
    """Set up a FPDF object to work with latex parsers"""
    pdf.add_page()
    pdf.add_font('symbol','','font/DejaVuSansCondensed.ttf',uni=True)
    #pdf.add_font('math-var','','font/lmroman7-italic.otf',uni=True)
    f = default_styles['body']
    pdf.set_font(f[0],f[1],f[2])

#---------------------------------------------------------------------------------
def setFontPDF(pdf,style, styles = default_styles):
    """Set font of a pdf object based on the styles in a style list"""
    f = styles[style]
    pdf.set_font(f[0],f[1],f[2])

#---------------------------------------------------------------------------------
class TextItem(DocItem):
    """Prints some form of text"""
    def __init__(self, text = '', style = 'body'):
        DocItem.__init__(self)
        self.text = text
        self.style = style

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
        
    def refit(self):
        """Doesn't need to do anything as cellPDF uses self.rect to output the content"""
        pass
        
#---------------------------------------------------------------------------------
class Word(TextItem):
    """Prints a word"""
    def __init__(self, name, style = 'body'):
        TextItem.__init__(self,name,style)
        
    def getText(self):
        """'Virtual' method returning text of this item."""
        return self.text
        
#---------------------------------------------------------------------------------
class Symbol(TextItem):
    """Prints a symbol or word wich can be output as a unicode string"""
    def __init__(self, name, style = 'symbol'):
        TextItem.__init__(self, name, style)
        
    def getText(self):
        """'Virtual' method returning text of this item."""
        return symbols[self.text]
        
#---------------------------------------------------------------------------------
class MathVariable(Word):
    """Prints some form of text"""
    def __init__(self, text):
        Word.__init__(self,text,'math-var')

#---------------------------------------------------------------------------------
class MathSign(Word):
    """Prints some form of text"""
    def __init__(self, text):
        Word.__init__(self,text,'math-symbol')
        if text == '-':
            self.text = u'\u2212'

#---------------------------------------------------------------------------------
class InlineMathBlock(DocItem):
    """Container for inline maths"""
    def __init__(self):
        DocItem.__init__(self)
        self.style = 'math-var'
        # pointer to the local styles dict
        self.styles = default_styles
        
    def resizePDF(self, pdf, x = 0, y = 0):
        self.rect = Rect(x,y,x,y)
        dx = pdf.get_string_width(' ')
        rectList = []
        width = 0.0
        for item in self.items:
            if item:
                item.resizePDF(pdf,x,y)
                rectList.append(item.rect)
                width += item.rect.width()
                
        rect.alignLeft(rectList, x, x+width, dx)
        for r in rectList:
            self.rect.unite(r)

    def cellPDF(self, pdf):
        """Output the paragraph to PDF"""
        style = ''
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    f = self.styles[style]
                    pdf.set_font(f[0],f[1],f[2])
                item.cellPDF(pdf)

#---------------------------------------------------------------------------------
class Paragraph(DocItem):
    """Paragraph of a document."""
    def __init__(self, width = -1):
        DocItem.__init__(self)
        self.width = width
        # possible alignments: j (justify), l (left), r (right), c (center)
        self.textAlignment = 'j'
        # parent Document
        self.doc = None
        # pointerr to the local styles dict
        self.styles = default_styles
        # spaces added before and after the paragraph. negative values mean to be set to defaults in resizePDF
        self.t_margin = -1
        self.b_margin = -1
        
    def setDocument(self, doc):
        """Re-parent this paragraph"""
        self.doc = doc
        self.styles = doc.styles
        
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
        f = self.styles[style]
        pdf.set_font(f[0],f[1],f[2])
        if self.width <= 0:
            self.width = pdf.fw - pdf.l_margin - pdf.r_margin - x
        self.space = pdf.get_string_width(' ')
        self.lineHeight = pdf.font_size_pt / pdf.k * 1.2
        if self.t_margin < 0:
            self.t_margin = self.lineHeight * 0.5
        if self.b_margin < 0:
            self.b_margin = self.lineHeight
            
        
        y += pdf.t_margin
        xstart = pdf.l_margin + x
        xend = pdf.l_margin + x + self.width
        self.rect = Rect( xstart, y, xend, y )
        y += self.t_margin

        rectList = []
        # resize individual items and collect their Rects
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    f = self.styles[style]
                    pdf.set_font(f[0],f[1],f[2])
                item.resizePDF(pdf, 0, y)
                rectList.append( item.rect )
            
        # position the items on the page
            
        alignFunction = textAlignments[self.textAlignment]
        
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
        # add the bottom margin
        self.rect.adjust(rect.Point(0,0), rect.Point(0,self.b_margin))
            
    def cellPDF(self, pdf):
        """Output the paragraph to PDF"""
        style = ''
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    f = self.styles[style]
                    pdf.set_font(f[0],f[1],f[2])
                item.cellPDF(pdf)
                
        #pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')
                
                
#---------------------------------------------------------------------------------
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
            if item:
                item.style = 'title'
        Paragraph.resizePDF(self, pdf, x + self.width * 0.1, y)
        
#---------------------------------------------------------------------------------
class Document(DocItem):
    """Entire document"""
    def __init__(self):
        DocItem.__init__(self)
        self.styles = {'body': ('times', '', 12),
                      'title': ('times', 'B', 16),
                      'symbol': ('symbol','', 12),
                       }
        
    def appendItem(self, item):
        """Append a child document item."""
        self.items.append(item)
        item.setDocument( self )
        
    def setPDF(self, pdf):
        """Set a FPDF object to output the document to"""
        self.pdf = pdf
        pdf.add_page()
        pdf.add_font('symbol','','font/DejaVuSansCondensed.ttf',uni=True)
        # resize the child items
        y = 0
        for item in self.items:
            if item:
                item.resizePDF(pdf, 0, y)
                y += item.rect.height() 
    
    def outputPDF(self, destName, destType = 'F'):
        """Output this document to a PDF object.
        
        Args:
            destName (str): name of the destination (eg filename);
            destType (str): type of the destination: 'F' for file, 'S' for string
        """
        for item in self.items:
            if item:
                item.cellPDF(self.pdf)
                
        self.pdf.output(destName, destType)

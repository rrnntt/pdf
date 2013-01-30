import rect
from rect import Rect

######################################################################################
#     Document items
######################################################################################
default_styles = {'body': ('times', '', 12),
          'title': ('times', 'B', 16),
          'symbol': ('symbol','', 12),
          'math-var': ('times', 'I', 12),
          'math-symbol': ('symbol', '', 12),
          'math-fun': ('times', '', 12),
         }

textAlignments = {'j': rect.justifyX,
                  'l': rect.alignLeft,
                  'r': rect.alignRight,
                  'c': rect.center,
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
    if isinstance(style,tuple):
        style_name = style[0]
        factor = style[1]
    else:
        style_name = style
        factor = 1
    f = styles[style_name]
    font_size = f[2] * factor
    pdf.set_font(f[0],f[1],font_size)

#---------------------------------------------------------------------------------
class DocItem:
    """An item of a document."""
    def __init__(self):
        self.text = ''
    
    def scaleFont(self,factor):
        """Scale font size by a factor"""
        if hasattr(self,'style'):
            if isinstance(self.style,tuple):
                self.style = self.style[0],factor
            else:
                self.style = (self.style,factor)
                
    def showRect(self,pdf):
        pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')

#---------------------------------------------------------------------------------
class MultiItem(DocItem):
    """A complex item containing other items."""
    def __init__(self):
        DocItem.__init__(self)
        self.items = []
        # pointer to the local styles dict
        self.styles = default_styles
        self.style = ('body',1)
        
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
                
    def moveTo(self,x,y):
        """Moves this multi-item to point with coordinates x,y."""
        self.rect.moveTo(rect.Point(x,y))
        self.refit()
                
    def getUnionRect(self):
        """Create a union of all children's rects."""
        rect = Rect()
        for item in self.items:
            if item:
                rect.unite(item.rect)
        return rect
    
    def cellPDF(self, pdf):
        """Output the item to PDF"""
        style = ''
        for item in self.items:
            if item:
                if hasattr(item,'style') and item.style != style:
                    setFontPDF(pdf, item.style, self.styles)
                item.cellPDF(pdf)
                
    def scaleFont(self,factor):
        """Scale font size by a factor"""
        self.style = self.style[0],factor
        for item in self.items:
            if item:
                item.scaleFont(factor)
                
    def setFontPDF(self,pdf,item):
        setFontPDF(pdf,item.style, self.styles)

    def resizeItemsPDF(self,pdf, x, y):
        """Resize all items with origin at x,y"""
        for item in self.items:
            if item:
                self.setFontPDF(pdf, item)
                item.resizePDF(pdf, x, y)
                
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
class MathFunction(Word):
    """Prints name of math function such as sin or log"""
    def __init__(self, text):
        Word.__init__(self,text,'math-fun')

#---------------------------------------------------------------------------------
class InlineMathBlock(MultiItem):
    """Container for inline maths"""
    def __init__(self, *items):
        MultiItem.__init__(self)
        self.style = ('math-var',1)
        for item in items:
            self.appendItem(item)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        self.rect = Rect(x,y,x,y)
        dx = pdf.get_string_width(' ')
        dx *= self.style[1]
        rectList = []
        width = 0.0
        style = ''
        for item in self.items:
            if item:
                if hasattr(item,'style') and item.style != style:
                    setFontPDF(pdf, item.style, self.styles)
                item.resizePDF(pdf,x,y)
                rectList.append(item.rect)
                width += item.rect.width() + dx
                
        rect.alignLeft(rectList, x, x+width, dx)
        for r in rectList:
            self.rect.unite(r)
        self.refit()

#---------------------------------------------------------------------------------
class MathPower(MultiItem):
    """Container for inline maths"""
    def __init__(self):
        MultiItem.__init__(self)
        self.style = 'math-var', 1
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if len(self.items) < 2 or not self.items[0] or not self.items[1]:
            raise Exception('MathPower must have two items.')

        self.rect = Rect(x,y,x,y)
        dx = pdf.get_string_width(' ') * self.style[1]
        
        base = self.items[0] 
        if hasattr(base,'style'):
            setFontPDF(pdf, base.style, self.styles)
        base.resizePDF(pdf,x,y)

        index = self.items[1] 
        index.scaleFont(0.8)
        if hasattr(index,'style'):
            setFontPDF(pdf, index.style, self.styles)
        index.resizePDF(pdf, base.rect.x1() + dx, y - base.rect.height() * 0.4)

        self.rect.unite(base.rect)
        self.rect.unite(index.rect)
        self.refit()

#---------------------------------------------------------------------------------
class MathBrackets(InlineMathBlock):
    """Container for inline maths"""
    def __init__(self):
        InlineMathBlock.__init__(self)
        
    def appendItem(self, item):
        """Override append a child item. There can only be one item"""
        self.items = []
        self.items.append(MathSign('('))
        self.items.append(item)
        self.items.append(MathSign(')'))
        
#---------------------------------------------------------------------------------
class MathFrac(MultiItem):
    """Container for inline maths"""
    def __init__(self):
        MultiItem.__init__(self)
        self.style = 'math-var', 1
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if len(self.items) < 2 or not self.items[0] or not self.items[1]:
            raise Exception('MathFrac must have two items.')

        self.rect = Rect(x,y,x,y)
        dx = pdf.get_string_width(' ') * self.style[1]
        setFontPDF(pdf, self.style, self.styles)
        lineHeight = pdf.font_size_pt / pdf.k
        
        numerator = self.items[0] 
        if hasattr(numerator,'style'):
            setFontPDF(pdf, numerator.style, self.styles)
        numerator.resizePDF(pdf,x, y - lineHeight * 0.5)

        denominator = self.items[1] 
        if hasattr(denominator,'style'):
            setFontPDF(pdf, denominator.style, self.styles)
        denominator.resizePDF(pdf, x, numerator.rect.y1())
        
        if numerator.rect.width() > denominator.rect.width():
            denominator.rect.alignXCenter(numerator.rect)
        else:
            numerator.rect.alignXCenter(denominator.rect)

        self.rect.unite(numerator.rect)
        self.rect.unite(denominator.rect)
        self.refit()
        self.rect.adjust(rect.Point(0,0),rect.Point(2*dx,0))

    def cellPDF(self, pdf):
        MultiItem.cellPDF(self, pdf)
        y = self.items[0].rect.y1()
        pdf.line(self.rect.x0(), y, self.rect.x1(), y)
        #pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')

#---------------------------------------------------------------------------------
class MathBigBrackets(InlineMathBlock):
    """Container for inline maths"""
    def __init__(self, bra = '(', ket = ')'):
        InlineMathBlock.__init__(self)
        if bra != '':
            self.bra = MathSign(bra)
        else:
            self.bra = None
        if ket != '':
            self.ket = MathSign(ket)
        else:
            self.ket = None
        self.data = None
        
    def appendItem(self, item):
        """Override append a child item. There can only be one item"""
        self.items = []
        if self.bra:
            self.items.append(self.bra)
        self.items.append(item)
        self.data = item
        if self.ket:
            self.items.append(self.ket)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        InlineMathBlock.resizePDF(self, pdf, x, y)
        scale = None
        if self.bra:
            scale = self.data.rect.height() / self.bra.rect.height()
            self.bra.scaleFont(scale)
        if self.ket:
            if not scale:
                scale = self.data.rect.height() / self.ket.rect.height()
            self.ket.scaleFont(scale)
        InlineMathBlock.resizePDF(self, pdf, x, y)
        #self.showRect(pdf)
        
#---------------------------------------------------------------------------------
class MathBelowAndAbove(MultiItem):
    """Can have up to 3 items: first is placed inline with the text,
    if there is a second item it's placed below the first,
    if there is a third item it's placed above the first.
    """
    def __init__(self,base = None, below = None, above = None):
        MultiItem.__init__(self)
        self.style = 'math-var', 1
        if base:
            self.appendItem(base)
            if below:
                self.appendItem(below)
                if above:
                    self.appendItem(above)
            else:
                if above:
                    self.appendItem(None)
                    self.appendItem(above)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if len(self.items) == 0:
            raise Exception('MathAboveAndBelow must have at least one item.')
        self.rect = Rect(x,y,x,y)
        base = self.items[0]
        self.setFontPDF(pdf, base)
        base.resizePDF(pdf,x,y)
        self.rect.unite(base.rect)

        if len(self.items) > 1 and self.items[1]:
            below = self.items[1]
            self.setFontPDF(pdf, below)
            below.resizePDF(pdf,x,y)
            below.rect.translate(0, base.rect.height())
            below.rect.alignXCenter( base.rect )
            self.rect.unite(below.rect)
            
        if len(self.items) > 2 and self.items[2]:
            above = self.items[2]
            self.setFontPDF(pdf, above)
            above.resizePDF(pdf,x,y)
            above.rect.translate(0, - above.rect.height())
            above.rect.alignXCenter( base.rect )
            self.rect.unite(above.rect)
            
        self.refit()
        #pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')

#---------------------------------------------------------------------------------
class MathColumn(MultiItem):
    """Container for inline maths"""
    def __init__(self, *items):
        MultiItem.__init__(self)
        self.style = ('math-var',1)
        for item in items:
            self.appendItem(item)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        self.rect = Rect(x,y,x,y)
        for item in self.items:
            self.setFontPDF(pdf, item)
            item.resizePDF(pdf,x,y)
            item.rect.translate(0,self.rect.height())
            self.rect.unite(item.rect)
                
        self.refit()

#---------------------------------------------------------------------------------
class MathSum(MathBelowAndAbove):
    """"""
    def __init__(self, below = None, above = None):
        if below:
            below.scaleFont(0.8)
        if above:
            above.scaleFont(0.8)
        sigma = Symbol('Sigma')
        sigma.scaleFont(2.0)
        MathBelowAndAbove.__init__(self, sigma, below, above)

#---------------------------------------------------------------------------------
class MathProd(MathBelowAndAbove):
    """"""
    def __init__(self, below = None, above = None):
        if below:
            below.scaleFont(0.8)
        if above:
            above.scaleFont(0.8)
        sigma = Symbol('Pi')
        sigma.scaleFont(2.0)
        MathBelowAndAbove.__init__(self, sigma, below, above)

#---------------------------------------------------------------------------------
class MathSubSuperscript(MultiItem):
    """An item with a subscript"""
    def __init__(self, base, subscript = None, superscript = None):
        MultiItem.__init__(self)
        self.appendItem(base)
        self.base = base  
        self.subscript = subscript
        self.superscript = superscript
        if subscript:
            subscript.scaleFont(0.8)
            self.appendItem(subscript)
        if superscript:
            superscript.scaleFont(0.8)
            self.appendItem(superscript)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        self.resizeItemsPDF(pdf, x, y)
        dx = pdf.get_string_width(' ') * self.style[1]
        self.rect = Rect(x,y,x,y)
         
        h = self.base.rect.height()
        w = self.base.rect.width() + dx
        
        if self.subscript:
            self.subscript.rect.translate(w, h*0.5)
            self.rect.unite(self.subscript.rect)
        if self.superscript:
            self.superscript.rect.translate(w, - h*0.5)
            self.rect.unite(self.superscript.rect)
        
        self.refit()
    
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

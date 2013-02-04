import rect
from rect import Rect

######################################################################################
#     Document items
######################################################################################
default_styles = {'body': ('times', '', 12),
          'title': ('times', 'B', 16),
          'symbol': ('math-symbol','', 12),
          'math-var': ('math-var', '', 12),
          'math-symbol': ('math-symbol', '', 12),
          'math-fun': ('math-symbol', '', 12),
         }

textAlignments = {'j': rect.justifyX,
                  'l': rect.alignLeft,
                  'r': rect.alignRight,
                  'c': rect.center,
                 }

""""Empirically found fraction of font's height from the top which defines
character's baseline"""
pdf_baseline = 0.81

#---------------------------------------------------------------------------------
def initPDF(pdf):
    """Set up a FPDF object to work with latex parsers"""
    pdf.c_margin = 0.0 # inner cell margin
    pdf.add_page()
    pdf.add_font('math-var','','font/lmroman7-italic.ttf',uni=True)
    pdf.add_font('math-symbol','','font/GFSDidot-Regular.ttf',uni=True)
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
        # left and top inner margins
        self.margins = rect.Point(0,0)
        
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
        dp = self.rect.p0() - old_rect.p0() + self.margins
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
    
    def cellPDF(self, pdf, r = None):
        """Output the item to PDF"""
        style = self.style
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    self.setFontPDF(pdf, item)
                item.cellPDF(pdf, r)
                
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
                
    def getLineHeight(self, pdf):
        return pdf.font_size_pt / pdf.k
    
    def addItems(self, *items):
        for item in items:
            self.appendItem(item)
                
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

funs = ['sin', 'cos', 'log']

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
    
    def cellPDF(self, pdf, r = None):
        if r:
            x_shift = r.x0()
            y_shift = r.y0()
        else:
            x_shift = 0.0
            y_shift = 0.0
        pdf.set_y( self.rect.y0() - y_shift )
        pdf.set_x( self.rect.x0() - x_shift )
        pdf.cell( self.rect.width(), self.rect.height(), self.getText() )
        
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
class MathNumber(Word):
    """Prints some form of text"""
    def __init__(self, text):
        Word.__init__(self,text)

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
    def __init__(self, num = None, denom = None):
        MultiItem.__init__(self)
        self.style = 'math-var', 1
        if num:
            if not denom:
                denom = MathNumber('1')
            self.appendItem(num)
            self.appendItem(denom)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if len(self.items) < 2 or not self.items[0] or not self.items[1]:
            raise Exception('MathFrac must have two items.')

        self.rect = Rect(x,y,x,y)
        dx = pdf.get_string_width(' ') * self.style[1]
        self.margins.set(dx, 0.0)
        setFontPDF(pdf, self.style, self.styles)
        lineHeight = pdf.font_size_pt / pdf.k
        
        numerator = self.items[0] 
        if hasattr(numerator,'style'):
            setFontPDF(pdf, numerator.style, self.styles)
        numerator.resizePDF(pdf,x + dx, y - lineHeight * 0.5)

        denominator = self.items[1] 
        if hasattr(denominator,'style'):
            setFontPDF(pdf, denominator.style, self.styles)
        denominator.resizePDF(pdf, x + dx, numerator.rect.y1())
        
        if numerator.rect.width() > denominator.rect.width():
            denominator.rect.alignXCenter(numerator.rect)
        else:
            numerator.rect.alignXCenter(denominator.rect)

        self.rect.unite(numerator.rect)
        self.rect.unite(denominator.rect)
        self.rect.adjust(rect.Point(0,0),rect.Point(dx,0))

    def cellPDF(self, pdf, r = None):
        MultiItem.cellPDF(self, pdf, r)
        y = self.items[0].rect.y1()
        pdf.set_line_width(0.2)
        if r:
            x_shift = r.x0()
            y_shift = r.y0()
        else:
            x_shift = 0.0
            y_shift = 0.0
        pdf.line(self.rect.x0() - x_shift, y - y_shift, self.rect.x1() - x_shift, y - y_shift)
        #self.showRect(pdf)

#---------------------------------------------------------------------------------
class MathBigBrackets(InlineMathBlock):
    """Container for inline maths"""
    def __init__(self, bra = '(', ket = ')', items = None):
        InlineMathBlock.__init__(self)
        if bra != '':
            self.bra = MathSign(bra)
        else:
            self.bra = None
        if ket != '':
            self.ket = MathSign(ket)
        else:
            self.ket = None
        
        if items:
            self.data = items
            self.appendItem(items)
        else:
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
        h = self.data.rect.height()
        if self.bra:
            scale = h / self.bra.rect.height()
            self.bra.scaleFont(scale)
        if self.ket:
            if not scale:
                scale = h / self.ket.rect.height()
            self.ket.scaleFont(scale)
        InlineMathBlock.resizePDF(self, pdf, x, y)
        if scale > 1.0:
            dy = h * ( 1.0 - pdf_baseline )
            self.data.rect.translate(0,dy)
            self.data.refit()
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
class MathSumLike(MathBelowAndAbove):
    """"""
    def __init__(self, symbol, below = None, above = None):
        if below:
            below.scaleFont(0.8)
        if above:
            above.scaleFont(0.8)
        sigma = Symbol(symbol)
        sigma.scaleFont(2.0)
        MathBelowAndAbove.__init__(self, sigma, below, above)
        
    def resizePDF(self, pdf, x = 0, y = 0):
        self.setFontPDF(pdf, self)
        lineHeight = self.getLineHeight(pdf)
        MathBelowAndAbove.resizePDF(self, pdf, x, y)
        dy = self.items[0].rect.height() * pdf_baseline - lineHeight
        self.rect.translate(0, - dy)
        self.refit()
        
#    def cellPDF(self, pdf):
#        MathBelowAndAbove.cellPDF(self, pdf)
#        self.items[0].showRect(pdf)
#        self.showRect(pdf)

#---------------------------------------------------------------------------------
class MathSum(MathSumLike):
    """"""
    def __init__(self, below = None, above = None):
        MathSumLike.__init__(self, 'Sigma', below, above)
        
#---------------------------------------------------------------------------------
class MathProd(MathSumLike):
    """"""
    def __init__(self, below = None, above = None):
        MathSumLike.__init__(self, 'Pi', below, above)

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
class Paragraph(MultiItem):
    """Paragraph of a document. 
    
    If width isn't set the box is positioned relative the pdf's page margins. 
    """
    def __init__(self, width = -1):
        MultiItem.__init__(self)
        self.style = ('body',1)
        self.width = width
        # possible alignments: j (justify), l (left), r (right), c (center)
        self.textAlignment = 'j'
        # parent Document
        self.doc = None
        # pointer to the local styles dict
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
        style = self.style
        setFontPDF(pdf, style, self.styles)

        if self.width <= 0:
            self.width = pdf.fw - pdf.l_margin - pdf.r_margin - x
            y += pdf.t_margin
            xstart = pdf.l_margin + x
            xend = pdf.l_margin + x + self.width
        else:
            xstart = x
            xend = x + self.width
        
        self.space = pdf.get_string_width(' ')
        self.lineHeight = self.getLineHeight(pdf) * 1.2
        if self.t_margin < 0:
            self.t_margin = self.lineHeight * 0.5
        if self.b_margin < 0:
            self.b_margin = self.lineHeight
            
        y += self.t_margin

        rectList = []
        # resize individual items and collect their Rects
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    self.setFontPDF(pdf, item)
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
#            for r in rectList[:n]:
#                self.rect.unite(r)
            onFirstLine = False
            del rectList[:n]
        #self.rect = Rect( xstart, y, xend, y )
        self.rect = self.getUnionRect()
        # add top and bottom margins
        self.margins = rect.Point(0,self.t_margin)
        self.rect.adjust(rect.Point(0,-self.t_margin), rect.Point(0,self.b_margin))
        self.refit()
            
    def outputPDF(self, pdf, r):
        """Output the paragraph to PDF"""
        style = self.style
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    self.setFontPDF(pdf, item)
                if item.rect.y1() > r.y0() + r.height():# - self.doc.pdf.t_margin:
                    self.doc.addPage()
                    dy = item.rect.y0() - r.y0() - self.doc.pdf.t_margin
                    r.translate(0, dy)
                item.cellPDF(pdf, r)
                
#---------------------------------------------------------------------------------
class Title(Paragraph):
    """Print a document title."""
    def __init__(self, width = -1):
        Paragraph.__init__(self, width)
        self.textAlignment = 'c'
        
    def resizePDF(self, pdf, x = 0, y = 0):
        if self.width <= 0:
            self.width = pdf.fw - pdf.r_margin - x - pdf.l_margin
            self.width *= 0.8
            x_start = x + pdf.l_margin
            y_start = y + pdf.t_margin
        else:
            x_start = x
            y_start = y
            
        for item in self.items:
            if item:
                item.style = 'title'
        Paragraph.resizePDF(self, pdf, x_start + self.width * 0.1, y_start)
        
#---------------------------------------------------------------------------------
class Document:
    """Entire document"""
    def __init__(self):
        self.styles = {'body': ('times', '', 12),
                      'title': ('times', 'B', 16),
                      'symbol': ('symbol','', 12),
                       }
        self.paragraphs = []
        
    def appendParagraph(self, para):
        """Append a child document item."""
        self.paragraphs.append(para)
        para.setDocument( self )
        
    def setPDF(self, pdf):
        """Set a FPDF object to output the document to"""
        self.pdf = pdf
        initPDF(pdf)
        pdf.set_auto_page_break(False)
        self.page_height = pdf.fh - pdf.t_margin
        # resize the child items
        y = 0
        for para in self.paragraphs:
            para.resizePDF(pdf, 0, y)
            y += para.rect.height() 
    
    def addPage(self):
        self.pdf.add_page()
    
    def outputPDF(self, destName, destType = 'F'):
        """Output this document to a PDF object.
        
        Args:
            destName (str): name of the destination (eg filename);
            destType (str): type of the destination: 'F' for file, 'S' for string
        """
        r = Rect(0,0,self.pdf.fw, self.page_height)
        for para in self.paragraphs:
            para.outputPDF(self.pdf, r)
                
        self.pdf.output(destName, destType)

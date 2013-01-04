# try all ttf fonts 

from fpdf import FPDF
import fpdf
import sys
import os
import time

pdf = FPDF()
pdf.add_page()

#font_dir = fpdf.FPDF_FONT_DIR
font_dir = '../fpdf/font'

txt = open('HelloWorld.txt').read()

# Add a Unicode font (uses UTF-8)
for font in os.listdir(font_dir):
    if font.lower().endswith('.ttf'):
        fontpath = os.path.join(font_dir, font)
        print fontpath
        t0 = time.time()
        pdf.add_font(font,'', fontpath, uni=True)
        t1 = time.time()
        pdf.set_font(font,'',14)
        t2 = time.time()
        pdf.write(8, font)
        pdf.ln()
        pdf.write(8, txt)
        pdf.ln()
        t3 = time.time()
        print "ttf loading time", t1-t0
        print "ttf total time", t3-t0
        print

fn = 'unifonts.pdf'
pdf.output(fn,'F')
import os
try:
    os.startfile(fn)
except:
    os.system("evince %s" % fn)

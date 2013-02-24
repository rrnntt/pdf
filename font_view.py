from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.add_font('jax','','font/mathjax_amsregular.ttf',uni=True)
pdf.set_font('jax','',12)


for i in range(0x03b1,0x0400):
    pdf.write(10, unichr(i))
    #print unichr(i)
pdf.output('out/latex/font_view.pdf', 'F')

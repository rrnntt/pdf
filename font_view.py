from fpdf import FPDF

#font_file_name = 'font/mathjax_amsregular.ttf'
font_file_name = 'font/MathJax/ttf/mathjax_size4regular.ttf'

size = 10
pdf = FPDF()
pdf.add_page()
pdf.add_font('jax','',font_file_name,uni=True)

lb = 0
for n in range(0xeffc):
    c = unichr(n)
    pdf.set_font('jax','',size)
    w = pdf.get_string_width(c)
    if w > 0:
        pdf.set_font('times','',size)
        pdf.cell(13, 10, hex(n) + ': ' )
        pdf.set_font('jax','',size)
        pdf.cell(10, 10, c)
        if lb == 6: 
            pdf.ln(10)
            lb = 0
        else:
            lb += 1
    #print unichr(i)
pdf.output('out/latex/font_view.pdf', 'F')
print 'done'
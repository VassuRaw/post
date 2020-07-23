import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
def write_pdf():
    page = canvas.Canvas("sanction.pdf", bottomup=0, pagesize=A4)
    width, height = A4
    print(width, height, A4)
    page.drawCentredString(125,40, "Department Of Posts, India")
    page.showPage()
    page.save()
    os.system("sanction.pdf")

write_pdf()

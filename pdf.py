import os
from fpdf import FPDF
from datetime import datetime, date
from num2words import num2words

def write_pdf(data, amount): 
    pdf = FPDF()
    pdf.add_page()

    epw = pdf.w - 2*pdf.l_margin
     
    pdf.set_font("Arial", 'B', size = 15) 
    pdf.cell(epw, 10, txt = "Department Of Posts, India", 
                    ln=1, align = 'C') 
    pdf.cell(epw, 5, txt = "O/o Sr. Supdt. Of Post Offices, Dehradun Division, Dehradun - 248001", 
                    ln=1, align = 'C')

    pdf.ln()
    pdf.set_font("Courier",'B', size = 13)
    pdf.cell(epw, 10, txt = f"Memo No. J-2/Tech/Sanction/2020-21 Dated at Dehradun {date.today()}", ln=1)

    amount_words = num2words(amount, lang="en_In")
    pdf.set_font("Courier", size = 11)
    pdf.multi_cell(epw, 5, txt = f"Sanction of the undersigned is hereby accorded for payment of Rs. {amount}/- \n(Rs. {amount_words} Only)")
    pdf.ln()

    pdf.set_font("Courier", size = 9)
    width_list = [0,0,0,0,0]
    for row in data:
        for i in range(len(row)):
            width = pdf.get_string_width(str(row[i]))
            if width > width_list[i]:
                width_list[i] = width + 3
    for i in range(len(data)):
        for j in range(len(data[i])):
            if i == 0:
                pdf.set_font("Courier",'B', size = 9)
                pdf.set_fill_color(192,192,192)
                pdf.cell(width_list[j],10, fill=True, txt=str(data[i][j]), border=1)
            else:
                pdf.set_font("Courier", size = 9)
                pdf.cell(width_list[j],10, txt=str(data[i][j]), border=1)
                
        pdf.ln()
       
    pdf.output("Sanction.pdf", 'F')
    os.startfile("Sanction.pdf")



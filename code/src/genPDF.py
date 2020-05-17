from fpdf import FPDF 

def init_pdf(title):
    pdf = FPDF(orientation='P', unit='mm', format='A4') 
    pdf.set_font("Arial", size = 15) 
    pdf.add_page() 
    add_title(pdf, title)
    add_image(pdf, "static/images/logo.jpg")
    return pdf

def add_image(pdf, image_path):
    pdf.image(image_path, x=10, y=5, w=50)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, ln=1)

def add_title(pdf, title):
    pdf.cell(200, 10, txt = title, ln = 1, align='C') 
    pdf.set_line_width(1)
    pdf.set_draw_color(0, 0, 255)
    #point1 (x,y), point2(x,y)
    pdf.line(10, 30, 200, 30)

def write_file(pdf, file_path):
    pdf.ln(5)  
    f = open(file_path, "r")
    for line in f.readlines():
        pdf.write(8, line)

def createPDF(title, file_path):
    # title = "Knowledge management"
    pdf = init_pdf(title)
  
    # file_path = "paragraphs.txt"
    write_file(pdf, file_path)

    pdf.output("notes.pdf") 
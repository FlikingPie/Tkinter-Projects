from fpdf import FPDF

def create_invoice(customer_name, items):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 16)
    pdf.cell(40, 10, "Invoice")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(40, 10, f'Customer: {customer_name}')
    pdf.line(10, 30, 200, 30)
    total=0

    for item,price in items.items():
        pdf.cell(40, 10, f'item: {item}: S/{price}')
        pdf.ln(8)
        total+=price
    pdf.ln(10)
    pdf.cell(40,10, f'Total: {total}')
    pdf.output("invoice.pdf")
    print("PDF GENERADO!")

create_invoice("Angel", {"laptop":100, "Teclado":50, "Audifonos":30})
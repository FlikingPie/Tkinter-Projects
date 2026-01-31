from fpdf import FPDF

def create_invoice(customer_name, items):
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")

    pdf.ln(5)

    # Datos del cliente
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Customer: {customer_name}", ln=True)

    # Línea separadora (corregido)
    pdf.line(10, 30, 200, 30)

    pdf.ln(10)

    total = 0

    # Lista de productos
    for item, price in items.items():
        pdf.cell(0, 10, f"{item}: S/ {price}", ln=True)
        total += price

    pdf.ln(5)

    # Total
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total: S/ {total}", ln=True)

    pdf.output("invoice.pdf")
    print("¡PDF GENERADO!")

create_invoice("Angel", {"Laptop": 100, "Teclado": 50, "Audífonos": 30})

import tkinter as tk
from tkinter import messagebox, ttk

ventana = tk.Tk()
ventana.title("Convertidor de monedas")
ventana.geometry("400x350")
ventana.config(bg="white")
ventana.resizable(False, False)

tema_oscuro = False


titulo = tk.Label(
    ventana,
    text="Convertidor de monedas",
    font=("Arial", 16),
    bg="white",
    fg="black"
)
titulo.pack(pady=10)

label_origen = tk.Label(ventana, text="Seleccione su moneda", bg="white", fg="black")
label_origen.pack(pady=5)


monedas_usd = {
    "DOLAR": 1.0,
    "PEN": 3.36,
    "EUR": 0.92,
    "JPY": 155,
    "GBP": 0.78,
    "MXN": 17.0,
    "ARS": 850,
    "BRL": 5.0,
    "CLP": 930,
    "COP": 3900,
    "PAB": 1.00,
    "CRC": 520,
    "PYG": 7400,
    "UYU": 39,
    "BOB": 6.90,
    "VND": 24500,
    "INR": 83,
    "KRW": 1350,
    "RUB": 90,
    "TRY": 30
}

combobox_1 = ttk.Combobox(ventana, width=30, values=list(monedas_usd.keys()), state="readonly")
combobox_1.pack(pady=5)

label_dinero = tk.Label(ventana, text="Ingrese su dinero", bg="white", fg="black")
label_dinero.pack(pady=5)

dinero_entry = tk.Entry(ventana, width=20)
dinero_entry.pack(pady=5)

label_destino = tk.Label(ventana, text="Convertir a...", bg="white", fg="black")
label_destino.pack(pady=5)

combobox_2 = ttk.Combobox(ventana, width=30, values=list(monedas_usd.keys()), state="readonly")
combobox_2.pack(pady=5)


def conversion_dinero():
    dinero = dinero_entry.get()
    opcion_1 = combobox_1.get()
    opcion_2 = combobox_2.get()

    if not dinero or not opcion_1 or not opcion_2:
        messagebox.showwarning("Advertencia", "Ingrese todos los campos.")
        return

    try:
        dinero = float(dinero)
        if dinero <= 0:
            messagebox.showwarning("Advertencia", "Ingrese un valor mayor a 0.")
            return
    except ValueError:
        messagebox.showerror("Error", "Ingrese un monto válido.")
        dinero_entry.delete(0, tk.END)
        return

    if opcion_1 == opcion_2:
        messagebox.showwarning("Advertencia", "Seleccione monedas diferentes.")
        return

    conversion = (dinero / monedas_usd[opcion_1]) * monedas_usd[opcion_2]
    messagebox.showinfo("Conversión", f"Resultado: {conversion:.2f} {opcion_2}")


tk.Button(
    ventana,
    text="Convertir",
    width=25,
    command=conversion_dinero
).pack(pady=10)

def cambiar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro

    if tema_oscuro:
        ventana.config(bg="black")
        titulo.config(bg="black", fg="white")
        label_origen.config(bg="black", fg="white")
        label_dinero.config(bg="black", fg="white")
        label_destino.config(bg="black", fg="white")
    else:
        ventana.config(bg="white")
        titulo.config(bg="white", fg="black")
        label_origen.config(bg="white", fg="black")
        label_dinero.config(bg="white", fg="black")
        label_destino.config(bg="white", fg="black")

tk.Button(
    ventana,
    text="🌙 Cambiar tema",
    width=25,
    command=cambiar_tema
).pack(pady=5)

ventana.mainloop()

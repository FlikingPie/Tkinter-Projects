import tkinter as tk
import time
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Tiempo :)")
ventana.geometry("200x200")
ventana.resizable(False, False)

tk.Label(ventana, text="Ingrese una fecha (DD/MM/YYYY)").pack(pady=5)

fecha_string = tk.Entry(ventana, width=25)
fecha_string.pack(pady=5)

def convertir_date():
    try:
        fecha = fecha_string.get()
        t = time.strptime(fecha, "%d/%m/%Y")
        fecha_formateada = time.strftime("%d/%m/%Y", t)
        messagebox.showinfo("Fecha", f"La fecha es {fecha_formateada}")
    except ValueError:
        messagebox.showerror("Error", "Formato incorrecto. Use DD/MM/YYYY")

boton = tk.Button(
    ventana,
    width=20,
    text="Convertir a date",
    command=convertir_date
)
boton.pack(pady=10)

ventana.mainloop()

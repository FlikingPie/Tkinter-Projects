import tkinter as tk
from tkinter import simpledialog, messagebox

ventana = tk.Tk()
ventana.withdraw()  # Oculta la ventana principal (opcional)

nombre = simpledialog.askstring("Entrada", "Ingrese su nombre:")
if len(nombre)==0:
    messagebox.showerror("Error", "Ingrese el nombre.")


print(nombre)

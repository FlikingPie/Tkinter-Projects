import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import *

ventana = tk.Tk()
ventana.title("Convertidor de grados")
ventana.geometry("400x400")

titulo = tk.Label(ventana, text="Convertidor", font=("Arial", 18, "bold italic"))
titulo.pack(pady=20)

convertir = tk.Label(ventana, text="Ingrese los grados que desea convertir", font=("Arial", 12, "italic"))
convertir.pack(pady=10)

entrada = tk.Entry(ventana, width=20)
entrada.pack(pady=10)

elige_opcion_label = tk.Label(ventana, text="Selecciona una opción", font=("Arial", 12, "italic"))
elige_opcion_label.pack(pady=10)

#Selecciona una opccion en un listcombobox
combobox=ttk.Combobox(ventana, width=30, height=10, font=("Arial", 12, "italic"))
combobox.pack()
grados_lista=["Celcius (°C) - Kelvin(K)", "Celcius(°C) - Fahrenheit (°F)", "Kelvin(K) - Celcius(°C)", "Kelvin(K) - Fahrenheit (°F)", "Fahrenheit (°F) - Celcius(°C)", "Fahrenheit (°F) - Kelvin(K)"]
combobox["values"] =grados_lista

espacio_label=tk.Label(ventana, text=" ")
espacio_label.pack()
resultado_label=tk.Label(ventana, text="Resultado", font=("Arial", 12, "italic"))
resultado_label.pack()

resultado=tk.Entry(ventana)
resultado.pack()


#Ingresar los grados

def ingresar_grados(event):
    grados_vacio=entrada.get()
    if len(grados_vacio)==0:
        messagebox.showinfo("Info", "Ingrese los grados!!")
    try:
        grados=float(entrada.get())
        messagebox.showinfo("Info", f'Grados : {grados}')
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor válido!!")    
entrada.bind("<Return>", ingresar_grados)

#Seleccionar conversión...

def celcius_kelvin(event):
    try:
        valor_seleccionado = combobox.get()

        if valor_seleccionado == grados_lista[0]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            celcius = float(entrada.get())
            kelvin = celcius + 273.5
            resultado.delete(0, "end")
            resultado.insert(0, f'{kelvin:.2f}')
            messagebox.showinfo("Info", f'Kelvin: {kelvin:.2f} K')

        elif valor_seleccionado == grados_lista[1]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            celcius = float(entrada.get())
            fahrenheit = (1.8 * celcius) + 32
            resultado.delete(0, "end")
            resultado.insert(0, f'{fahrenheit:.2f}')
            messagebox.showinfo("Info", f'Fahrenheit: {fahrenheit:.2f} °F')

        elif valor_seleccionado == grados_lista[2]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            kelvin = float(entrada.get())
            celcius = kelvin - 273.5
            resultado.delete(0, "end")
            resultado.insert(0, f'{celcius:.2f}')
            messagebox.showinfo("Info", f'Celcius: {celcius:.2f}')

        elif valor_seleccionado == grados_lista[3]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            kelvin = float(entrada.get())
            fahrenheit = (kelvin - 273.5) * 1.8 + 32
            resultado.delete(0, "end")
            resultado.insert(0, f'{fahrenheit:.2f}')
            messagebox.showinfo("Info", f'Fahrenheit: {fahrenheit:.2f} °F')

        elif valor_seleccionado == grados_lista[4]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            fahrenheit = float(entrada.get())
            celcius = (fahrenheit - 32) / 1.8
            resultado.delete(0, "end")
            resultado.insert(0, f'{celcius:.2f}')
            messagebox.showinfo("Info", f'Celcius: {celcius:.2f}')

        elif valor_seleccionado == grados_lista[5]:
            print(f'Se ha seleccionado: {valor_seleccionado}')
            fahrenheit = float(entrada.get())
            kelvin = ((fahrenheit - 32) / 1.8) + 273.5
            resultado.delete(0, "end")
            resultado.insert(0, f'{kelvin:.2f}')
            messagebox.showinfo("Info", f'Kelvin: {kelvin:.2f} K')

        else:
            messagebox.showwarning("Info", "Seleccione una opción válida.")

    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor numérico válido.")
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))


combobox.bind("<<ComboboxSelected>>", celcius_kelvin)


ventana.mainloop()

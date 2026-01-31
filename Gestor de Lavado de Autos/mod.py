import tkinter as tk 
from tkinter import ttk, messagebox, simpledialog #Modulos de tkinter
import os
from datetime import datetime

# Archivos de texto, Define nombre de los archivos que se guardaran al momento de abrir el programa
archivo_cliente = "cliente.txt"
archivo_producto = "producto.txt"
archivo_venta = "venta.txt"

# Crear archivos si no existen
for archivo in [archivo_cliente, archivo_producto, archivo_venta]:
    if not os.path.exists(archivo):
        open(archivo, 'w').close()

# Leer archivo
def leer(archivo):
    with open(archivo, 'r') as f:
        return [linea.strip().split(',') for linea in f if linea.strip()]

# Escribir archivo completo
def escribir(archivo, datos):
    with open(archivo, 'w') as f:
        for fila in datos:
            f.write(','.join(fila) + '\n')

# Agregar nueva línea
def agregar_linea(archivo, datos):
    with open(archivo, 'a') as f:
        f.write(','.join(datos) + '\n')

# Interfaz principal
class App:
    def __init__(self, root):  # Corregido __init__
        self.root = root
        self.root.title("Gestión de Clientes, Productos y Ventas")
        self.root.geometry("800x400")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill="both") #Define el tamaño de la ventana de pixeles

        self.menu()

    def menu(self):
        barra = tk.Menu(self.root) #Crea la barra : Cliente/Producto/Venta

        # Menú Cliente
        menu_cliente = tk.Menu(barra, tearoff=0)
        menu_cliente.add_command(label="Registrar", command=self.registrar_cliente)
        menu_cliente.add_command(label="Modificar", command=self.modificar_cliente)
        menu_cliente.add_command(label="Mostrar", command=lambda: self.mostrar(archivo_cliente, ["ID", "Nombre", "Dirección"]))
        barra.add_cascade(label="Cliente", menu=menu_cliente)

        # Menú Producto
        menu_producto = tk.Menu(barra, tearoff=0)
        menu_producto.add_command(label="Registrar", command=self.registrar_producto)
        menu_producto.add_command(label="Modificar", command=self.modificar_producto)
        menu_producto.add_command(label="Mostrar", command=lambda: self.mostrar(archivo_producto, ["ID", "Nombre", "Precio"]))
        barra.add_cascade(label="Producto", menu=menu_producto)

        # Menú Venta
        menu_venta = tk.Menu(barra, tearoff=0)
        menu_venta.add_command(label="Registrar", command=self.registrar_venta)
        menu_venta.add_command(label="Eliminar", command=self.eliminar_venta)
        menu_venta.add_command(label="Mostrar", command=lambda: self.mostrar(archivo_venta, ["ID Venta", "ID Producto", "ID Cliente", "Fecha", "Cantidad"]))
        barra.add_cascade(label="Venta", menu=menu_venta)

        self.root.config(menu=barra) #Configura la ventana principal y muestra las opciones de cada menu 

    def mostrar(self, archivo, encabezados):    #Mostrar cuantas columnas tendra la tabla
        self.tree.delete(*self.tree.get_children())
        datos = leer(archivo)
        columnas = [f"col{i}" for i in range(len(encabezados))]
        self.tree.config(columns=columnas, show="headings")

        for i, col in enumerate(columnas):
            self.tree.heading(col, text=encabezados[i])
            self.tree.column(col, width=150, anchor="center")

        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def registrar_cliente(self):
        idc = simpledialog.askstring("ID Cliente", "Ingrese el ID del cliente:")
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del cliente:")
        direccion = simpledialog.askstring("Dirección", "Ingrese la dirección del cliente:")
        if idc and nombre and direccion:
            agregar_linea(archivo_cliente, [idc, nombre, direccion])
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.mostrar(archivo_cliente, ["ID", "Nombre", "Dirección"])

    def registrar_producto(self):
        idp = simpledialog.askstring("ID Producto", "Ingrese el ID del producto:")
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del producto:")
        precio = simpledialog.askstring("Precio", "Ingrese el precio del producto:")
        if idp and nombre and precio:
            agregar_linea(archivo_producto, [idp, nombre, precio])
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            self.mostrar(archivo_producto, ["ID", "Nombre", "Precio"])

    def registrar_venta(self):
        idv = simpledialog.askstring("ID Venta", "Ingrese el ID de la venta:")
        idp = simpledialog.askstring("ID Producto", "Ingrese el ID del producto:")
        idc = simpledialog.askstring("ID Cliente", "Ingrese el ID del cliente:")
        fecha = datetime.now().strftime("%Y-%m-%d")
        cantidad = simpledialog.askstring("Cantidad", "Ingrese la cantidad:")

        productos = leer(archivo_producto)
        clientes = leer(archivo_cliente)

        if not any(p[0] == idp for p in productos):
            messagebox.showerror("Error", "El ID del producto no existe.")
            return
        if not any(c[0] == idc for c in clientes):
            messagebox.showerror("Error", "El ID del cliente no existe.")
            return

        agregar_linea(archivo_venta, [idv, idp, idc, fecha, cantidad])
        messagebox.showinfo("Éxito", "Venta registrada correctamente.")
        self.mostrar(archivo_venta, ["ID Venta", "ID Producto", "ID Cliente", "Fecha", "Cantidad"])

    def modificar_cliente(self):
        datos = leer(archivo_cliente)
        id_mod = simpledialog.askstring("Modificar Cliente", "Ingrese el ID del cliente a modificar:")
        for cliente in datos:
            if cliente[0] == id_mod:
                nuevo_nombre = simpledialog.askstring("Nuevo nombre", "Ingrese nuevo nombre:")
                nueva_direccion = simpledialog.askstring("Nueva dirección", "Ingrese nueva dirección:")
                cliente[1] = nuevo_nombre
                cliente[2] = nueva_direccion
                escribir(archivo_cliente, datos)
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                self.mostrar(archivo_cliente, ["ID", "Nombre", "Dirección"])
                return
        messagebox.showerror("Error", "Cliente no encontrado.") #Si escribo un ID que no he añadido

    def modificar_producto(self):
        datos = leer(archivo_producto)
        id_mod = simpledialog.askstring("Modificar Producto", "Ingrese el ID del producto a modificar:")
        for producto in datos:
            if producto[0] == id_mod:
                nuevo_nombre = simpledialog.askstring("Nuevo nombre", "Ingrese nuevo nombre:")
                nuevo_precio = simpledialog.askstring("Nuevo precio", "Ingrese nuevo precio:")
                producto[1] = nuevo_nombre
                producto[2] = nuevo_precio
                escribir(archivo_producto, datos)
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.mostrar(archivo_producto, ["ID", "Nombre", "Precio"])
                return
        messagebox.showerror("Error", "Producto no encontrado.")

    def eliminar_venta(self):
        datos = leer(archivo_venta)
        id_venta = simpledialog.askstring("Eliminar Venta", "Ingrese el ID de la venta a eliminar:")
        nuevos_datos = [fila for fila in datos if fila[0] != id_venta]
        if len(nuevos_datos) < len(datos):
            escribir(archivo_venta, nuevos_datos)
            messagebox.showinfo("Éxito", "Venta eliminada correctamente.")
            self.mostrar(archivo_venta, ["ID Venta", "ID Producto", "ID Cliente", "Fecha", "Cantidad"])
        else:
            messagebox.showerror("Error", "ID de venta no encontrado.")

# ------------------------------
if __name__ == "__main__":  
    root = tk.Tk()
    app = App(root)
    root.mainloop()

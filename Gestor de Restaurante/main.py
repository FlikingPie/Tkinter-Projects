import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tabulate import tabulate
import sqlite3,time,datetime
from datetime import datetime, timedelta, time
from rich import print
from rich.progress import track
from rich.panel import Panel
from rich.console import Console
from rich.theme import Theme

ventana=tk.Tk()
ventana.title("Gestor de Restaurante")
ventana.geometry("1015x400+400+300")

#CREAR TABLA SQL
conexion=sqlite3.connect("restaurante2026.db")
cursor=conexion.cursor()

try:
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Restaurante_tabla2026 (
                   Cliente TEXT,
                   Nro_orden INT,
                   DNI INT,
                   Nro_mesa INT,
                   Nombre_plato TEXT,
                   Precio DOUBLE)
                   """)
    print("Tabla creada correctamente")
except sqlite3.OperationalError:
    print("Error al crear la tabla.")




#Variables globales
cliente=""
nro_orden=0
dni=0 
nro_mesa=0
nombre_platos=""
precio=0.0
total=0.0
ultimo_dia = datetime.now().date()

#Agregar estilos y colores al terminal
console=Console()

custom_theme=Theme({"succes":"green", "error":"red"})
console=Console(theme=custom_theme)


#MENÚ
barra_menu=tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_clientes=tk.Menu(barra_menu, tearoff=0)
menu_ordenes=tk.Menu(barra_menu, tearoff=0)
menu_ventas=tk.Menu(barra_menu, tearoff=0)
menu_estadisticas=tk.Menu(barra_menu, tearoff=0)

barra_menu.add_cascade(label="Opciones Clientes", menu=menu_clientes)
barra_menu.add_cascade(label="Opciones Ordenes",menu=menu_ordenes)
barra_menu.add_cascade(label="Opciones Ventas", menu=menu_ventas)
barra_menu.add_cascade(label="Estadísticas", menu=menu_estadisticas)


#Tablas: Clientes, Ordenes, Ventas
headings_cliente=["Cliente", "Nro Órden", "DNI"]
tree_clientes=ttk.Treeview(ventana, show="headings", columns=headings_cliente)

for col in headings_cliente:
    tree_clientes.heading(col, text=col)
    tree_clientes.column(col, width=150, anchor="center")
tree_clientes.pack(expand=True, fill="both")

headings_ordenes=["Nro Mesa", "Plato", "Precio S/"]
tree_ordenes=ttk.Treeview(ventana, show="headings", columns=headings_ordenes)

for col in headings_ordenes:
    tree_ordenes.heading(col, text=col)
    tree_ordenes.column(col, width=150, anchor="center")

headings_ventas=["Cliente", "Nro Órden", "DNI", "Nro Mesa", "Nro Platos", "Precio S/"]
tree_ventas=ttk.Treeview(ventana, show="headings", columns=headings_ventas)

for col in headings_ventas:
    tree_ventas.heading(col, text=col)
    tree_ventas.column(col, width=150, anchor="center")


#Platos - Precios
platos={
    "Lomo saltado":30,
    "Ají de gallina":26,
    "Arroz con pollo":25.45,
    "Pollo a la brasa":35.50,
    "Ceviche":30,
    "Tallarines rojos":21.72
}

#Funciones clientes:
def mostrar_clientes():
    tree_ordenes.forget()
    tree_ventas.forget()
    tree_clientes.pack(expand=True, fill="both")


def agregar_cliente():
    top=tk.Toplevel()
    top.title("Agregar cliente")
    top.geometry("300x300+400+300")
    top.resizable(False, False)

    tk.Label(top, text="Nombre del cliente").pack(pady=5)
    cliente_entry=tk.Entry(top, width=15)
    cliente_entry.pack(pady=5)

    tk.Label(top, text="DNI").pack(pady=5)
    dni_entry=tk.Entry(top, width=15)
    dni_entry.pack(pady=5)

    def guardar_cliente():
        global cliente, nro_orden, dni
        cliente=cliente_entry.get().capitalize()
        dni=dni_entry.get().strip()

        if not cliente or not dni:
            messagebox.showwarning("Advertencia", "Debe ingresar todos los campos!")
            return
        
        elif len(dni)!=8:
            messagebox.showerror("Error", "El DNI debe contener 8 dígitos.")
            return

        try:
            dni=int(dni_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "DNI INVÁLIDO.")
            dni_entry.delete(0,tk.END)
            return

        else:
            nro_orden+=1
            tree_clientes.insert("","end", values=(cliente, nro_orden,dni ))
            cursor.execute("""
                           
                           """)
            cliente_entry.delete(0,tk.END)
            dni_entry.delete(0,tk.END)

    tk.Button(top, text="Agregar", width=20, command=guardar_cliente).pack(pady=5)


def eliminar_cliente():
    item=tree_clientes.selection()
    if not tree_clientes:
        messagebox.showwarning("Error", "Lista de clientes vacía!")
    elif not item:
        messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
    else:
        confirmar=messagebox.askyesno("Connfirmar", "Eliminar?")
        if confirmar:
            tree_clientes.delete(item)
        else:
            return

def modificar_cliente():
    item = tree_clientes.selection() 

    if not tree_clientes.get_children():
        messagebox.showerror("Error", "Lista de clientes vacía!")
        return

    if not item:
        messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
        return

    item = item[0]  # ID del item seleccionado
    datos = tree_clientes.item(item, "values") #Fila seleccionada y su datos

    nombre = datos[0]

    new_orden = simpledialog.askinteger("Nro Orden", "Ingrese el nuevo número de orden")
    if new_orden is None:
        return

    new_dni = simpledialog.askinteger("DNI", "Ingrese el nuevo DNI")
    if new_dni is None:
        return


    # MODIFICAR la fila seleccionada
    tree_clientes.item(item, values=(nombre, new_orden, new_dni))

def archivo_cliente():
    if not tree_clientes.get_children():
        messagebox.showerror("Error", "La lista de clientes esta vacía!")
        return
    else:
        with open("Clientes_restaurante2026.txt", "w") as archivo:
            clientes=[]
            for item in tree_clientes.get_children():
                clientes.append(tree_clientes.item(item, "values"))
            archivo.write(tabulate(clientes, headers=["Cliente", "Nro Orden", "DNI"]))

        try:
            with open("Clientes_restaurante2026.txt", "r") as ver_archivo:
                contenido=ver_archivo.read()
                if len(contenido) ==0:
                    messagebox.showerror("Error", "Archivo vacío!!")
                else:
                    print(contenido)
        except FileExistsError:
            messagebox.showerror("Error", "el archivo NO existe.")
            return
                


menu_clientes.add_command(label="Ver clientes", command=mostrar_clientes)
menu_clientes.add_command(label="Agregar cliente", command=agregar_cliente)
menu_clientes.add_command(label="Eliminar cliente", command=eliminar_cliente)
menu_clientes.add_command(label="Modificar cliente", command=modificar_cliente)
menu_clientes.add_command(label="Archivo cliente",command=archivo_cliente )


#Funciones ordenes

def mostrar_ordenes():
    tree_clientes.forget()
    tree_ventas.forget()
    tree_ordenes.pack(expand=True, fill="both")


def agregar_orden():
    top=tk.Toplevel()
    top.title("Agregar orden")
    top.geometry("300x300+400+300")
    top.resizable(False, False)

    tk.Label(top, text="Nro Mesa").pack(pady=5)
    nro_mesas_entry=tk.Entry(top, width=15)
    nro_mesas_entry.pack(pady=5)

    tk.Label(top, text="Plato").pack(pady=5)
    nombre_platos_entry=tk.Entry(top, width=15)
    nombre_platos_entry.pack(pady=5)

    def guardar():
        global nro_mesa, nombre_platos,precio
        nro_mesa=nro_mesas_entry.get()
        nombre_platos=nombre_platos_entry.get().capitalize()

        if not nro_mesa or not nombre_platos:
            messagebox.showwarning("Advertencia", "Complete todos los campos!")
            return 
        
        try:
            nro_mesa=int((nro_mesas_entry).get())
        except ValueError:
            messagebox.showerror("Error", "Número de mesa no válido.")
        else:
            if nombre_platos not in list(platos.keys()):
                messagebox.showerror("Error", "Plato no disponible.")
                nombre_platos_entry.delete(0,tk.END)
                return
            else:
                precio=platos[nombre_platos]
                tree_ordenes.insert("","end", values=(nro_mesa, nombre_platos, precio))
                nro_mesas_entry.delete(0, tk.END)
                nombre_platos_entry.delete(0, tk.END)

    tk.Button(top, text="Agregar orden", width=15, command=guardar).pack(pady=5)


def eliminar_orden():
    item=tree_ordenes.selection()
    if not tree_ordenes.get_children():
        messagebox.showerror("Error", "Lista de ordenes vacía!")
        return
    elif not item:
        messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
        return
    else:
        confirmar=messagebox.askyesno("Eliminar", "Confirmar eliminación?")
        if confirmar:
            tree_ordenes.delete(item)


def modificar_orden():
    item=tree_ordenes.selection()

    if not tree_ordenes.get_children():
        messagebox.showerror("Error", "Lista de ordenes vacía!")
        return
    elif not item:
        messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
        return
    else:
        item=item[0]
        datos=tree_ordenes.item(item, "values")

        nro_mesa=datos[0]

        new_plato=simpledialog.askstring("Nuevo plato", "Ingrese el nombre del nuevo plato")
        if new_plato is None or new_plato not in list(platos.keys()) or new_plato.isnumeric():
            messagebox.showerror("Error", "Plato no identificado.")
            return
        
        new_precio=platos[new_plato]
        tree_ordenes.item(item, values=(nro_mesa, new_plato,new_precio)) #En el item seleccionado, Modifica

        #Recuerda: 0j0
        #Insert -> agrega
        #Item -> Modifica
        #Delete -> elimina uno o varios ID´s


    

def archivo_orden():
    if not tree_ordenes.get_children():
        messagebox.showerror("Error", "Lisra de ordenes vacía")
    else:
        with open("Ordenes_clientes2026.txt", "w") as archivo:
            ordenes=[]
            for item in tree_ordenes.get_children():
                ordenes.append(tree_ordenes.item(item,"values"))
            archivo.write(tabulate(ordenes, headers=["Nro mesa", "Plato", "Precio S/"]))

        try:
            with open("Ordenes_clientes2026.txt", "r") as ver_archivo:
                contenido=ver_archivo.read()
                if len(contenido)==0:
                    messagebox.showerror("Error", "Archivo vacío.")
                else:
                    print(contenido)
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo NO existe!")


menu_ordenes.add_command(label="Ver ordenes", command=mostrar_ordenes)
menu_ordenes.add_command(label="Agregar orden", command=agregar_orden)
menu_ordenes.add_command(label="Eliminar orden", command=eliminar_orden)
menu_ordenes.add_command(label="Modificar orden", command=modificar_orden)
menu_ordenes.add_command(label="Archivo ordenes", command=archivo_orden)





def mostrar_ventas():
    tree_clientes.forget()
    tree_ordenes.forget()
    tree_ventas.pack(expand=True, fill="both")


def agregar_venta():
    global cliente, nro_orden, nro_mesa, dni, nombre_platos,precio,total
    if not cliente or not nro_orden or not dni or not nro_mesa or not nombre_platos:
        messagebox.showwarning("Advertencia", "Debe ingresar todos los datos del cliente para agregar una venta.")
        return
    else:
        tree_ventas.insert("","end", values=(cliente, nro_orden, dni, nro_mesa, nombre_platos, precio))
        cursor.execute("""
                       INSERT INTO Restaurante_tabla2026
                       (Cliente, Nro_orden, DNI, Nro_mesa, Nombre_plato, Precio)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (cliente, nro_orden, dni, nro_mesa, nombre_platos, precio))
        
        total+=precio
        conexion.commit()


def eliminar_venta():
    item=tree_ventas.selection()
    if not tree_ventas.get_children():
        messagebox.showerror("Error", "Lista de ventas vacía!")
        return
    elif not item:
        messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
        return
    else:
        item=item[0]
        confirmar=messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar la fila seleccionada?")
        datos=tree_ventas.item(item, "values")
        v1, v2, v3, v4, v5, v6= datos
        if confirmar:
            cursor.execute("""
                           DELETE FROM Restaurante_tabla2026
                           WHERE Cliente = ? AND
                           Nro_orden = ? AND
                           DNI = ? AND
                           Nro_mesa = ? AND
                           Nombre_plato = ? AND
                           Precio = ? 
                           """, (v1, v2, v3, v4, v5, v6))
            
            conexion.commit()
            tree_ventas.delete(item)



def archivo_ventas():
    if not tree_ventas.get_children():
        messagebox.showerror("Error", "Lista de ventas vacía!")
        return
    else:
        with open("Ventas_restaurante2026.txt", "w") as archivo:
            ventas=[]
            for item in tree_ventas.get_children():
                ventas.append(tree_ventas.item(item, "values"))
            archivo.write(tabulate(ventas, headers=["Cliente", "Nro orden", "DNI", "Nro mesa", "Plato", "Precio S/"]))

        try:
            with open("Ventas_restaurante2026.txt", "r") as ver_archivo:
                contenido=ver_archivo.read()
                if len(contenido)==0:
                    messagebox.showerror("Error", "Archivo vacío.")
                else:
                    print(contenido)
        except FileNotFoundError:
            messagebox.showerror("Error", "el archivo NO existe.")


menu_ventas.add_command(label="Ver ventas", command=mostrar_ventas)
menu_ventas.add_command(label="Agregar venta", command=agregar_venta)
menu_ventas.add_command(label="Eliminar venta", command=eliminar_venta)
menu_ventas.add_command(label="Archivo ventas", command=archivo_ventas)


#Estadísticas
def ver_platos():
    print(Panel("[bold blue]1) [bold red]Lomo saltado[bold green] --> S/30 \n"
                "[bold blue]2) [bold red]Ají de gallina[bold green] --> S/26 \n"
                "[bold blue]2) [bold red]Arroz con pollo[bold green] --> S/25.45 \n"
                "[bold blue]3) [bold red]Pollo a la brasa[bold green] --> S/35.50 \n"
                "[bold blue]4) [bold red]Ceviche[bold green] -->S/30 \n"
                "[bold blue]5) [bold red]Tallarines rojos[bold green] --> S/21.72 \n", title="MENÚ DE ALMUERZOS"))
    
def lista_platos():
    top=tk.Toplevel()
    top.title("Ver clientes")
    top.geometry("200x200+400+300")
    top.resizable(False,False)
    tk.Label(top, text="Seleccione un plato").pack(side="top")
    
    menu_platos=[plato for plato in list(platos.keys())]
    combox=ttk.Combobox(top, values=(menu_platos))
    combox.pack(pady=5)

    def seleccionar():
        opcion=combox.get()
        if not opcion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una opción!")
            return
        else:
            cursor.execute("SELECT * FROM Restaurante_tabla2026 WHERE Nombre_plato = ?",(opcion,))
            datos=cursor.fetchall()

            if not datos:
                console.print(f'De momento no se encuentran clientes que hayan ordenado {opcion}', style="error")
            else:
                for _ in track(range(10), description="CARGANDO..."):
                    time.sleep(0.5)
                
                console.print("Mostrando resultados", style="succes")
                print(" ")
                for fila in datos:
                    print(fila)


        conexion.commit()
    tk.Button(top, text="Visualizar", command=seleccionar, width=15).pack(pady=10)


def plato_mas_vendido():
    cont_1=cont_2=cont_3=cont_4=cont_5=cont_6=0

    nombres_platos = [
        "Lomo saltado",
        "Ají de gallina",
        "Arroz con pollo",
        "Pollo a la brasa",
        "Ceviche",
        "Tallarines rojos"
    ]

    cursor.execute("SELECT * FROM Restaurante_tabla2026")
    datos = cursor.fetchall()

    for fila in datos:
        if fila[4] == "Lomo saltado":
            cont_1 += 1
        elif fila[4] == "Ají de gallina":
            cont_2 += 1
        elif fila[4] == "Arroz con pollo":
            cont_3 += 1
        elif fila[4] == "Pollo a la brasa":
            cont_4 += 1
        elif fila[4] == "Ceviche":
            cont_5 += 1
        elif fila[4] == "Tallarines rojos":
            cont_6 += 1

    cont_platos = [cont_1, cont_2, cont_3, cont_4, cont_5, cont_6]
    ventas = dict(zip(nombres_platos, cont_platos))

    for _ in track(range(10), description="CARGANDO RESULTADOS..."):
        time.sleep(0.3)

    print()
    for plato, total in ventas.items():
        print(f"{plato}: {total}")

    plato_top = max(ventas, key=ventas.get)
    cantidad = ventas[plato_top]

    print()
    print(f"🥇 Plato más vendido: {plato_top} ({cantidad} ventas)")


def total_generado_dia():
    global total, ultimo_dia

    ahora = datetime.now()

    if ahora.date() != ultimo_dia:
        total = 0
        ultimo_dia = ahora.date()
        print("🔄 Nuevo día detectado → total reiniciado")

    print(f"Fecha actual: {ahora.strftime('%d/%m/%Y')}")
    print(f"Total generado: {total}")
    print("")

menu_estadisticas.add_command(label="Ver Menú de platos", command=ver_platos)
menu_estadisticas.add_command(label="Lista de platos", command=lista_platos)
menu_estadisticas.add_command(label="Plato más vendido", command=plato_mas_vendido)
menu_estadisticas.add_command(label="Total generado por día", command=total_generado_dia)

def salir(event):
    ventana.destroy()
ventana.bind("<Escape>", salir )

ventana.mainloop()

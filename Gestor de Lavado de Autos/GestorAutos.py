import tkinter as tk,sqlite3,os
from tkinter import ttk
from tkinter import messagebox, filedialog, simpledialog
from tabulate import tabulate
from fpdf import FPDF


print(os.getcwd())

ventana=tk.Tk()
ventana.title("Gestor de lavado de autos")
ventana.geometry("1035x400+460+200")

lavados = {
    "Básico": 10,
    "Exterior": 15,
    "Motor": 25,
    "Premium": 45,
    "Vapor": 25
}



conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
cursor=conexion.cursor()

#CREAR LA TABLA EN SQL...
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS Lavado_de_Autos (
#            Cliente TEXT,
#            DNI INTEGER,
#            Telefono INTEGER,
#            Placa TEXT,
#            Nro_Autos INTEGER,
#            Lavado TEXT,
#            Precio REAL
#        )
#    """)
#    conexion.commit()
#    print("Tabla generada con éxito.")
#except sqlite3.OperationalError as e:
#    print("Error al generar la tabla:", e)


# ---------- TREE CLIENTES ----------
headings_clientes=["Nombre", "DNI", "Teléfono"]
tree_clientes=ttk.Treeview(ventana, columns=headings_clientes, show="headings")

for col in headings_clientes:
    tree_clientes.heading(col, text=col)
    tree_clientes.column(col, width=150, anchor="center")

# ---------- TREE AUTOS ----------
headings_autos=["Placa", "Nro° autos", "Tipo de Lavado", "Precio S/"]
tree_autos=ttk.Treeview(ventana, columns=headings_autos, show="headings")

for col in headings_autos:
    tree_autos.heading(col, text=col)
    tree_autos.column(col, width=150, anchor="center")

tree_clientes.pack(expand=True, fill="both")

headings_ventas=["Cliente", "DNI", "Telefono", "Placa", "Nro° de autos", "Lavado", "Precio S/"]
tree_ventas=ttk.Treeview(ventana, show="headings", columns=headings_ventas)

for col in headings_ventas:
    tree_ventas.heading(col, text=col)
    tree_ventas.column(col, width=150 ,anchor="center")


# ---------- FUNCIONES MOSTRAR ----------
def mostrar_clientes():
    tree_autos.pack_forget() #el pack.forget() permite ocultar widgets en la memoria del sistema pero sin ser eliminados( si quiero ver los clientes,oculto autos)
    tree_ventas.pack_forget()
    tree_clientes.pack(expand=True, fill="both")

def mostrar_autos():
    tree_clientes.pack_forget() #Si quiero ver los autos, oculto los clientes
    tree_ventas.pack_forget()
    tree_autos.pack(expand=True, fill="both")

# ---------- MENÚ ----------
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_cliente = tk.Menu(barra_menu, tearoff=0)
menu_auto = tk.Menu(barra_menu, tearoff=0)
menu_ventas=tk.Menu(barra_menu, tearoff=0)
menu_buscar=tk.Menu(barra_menu, tearoff=0)
menu_datos=tk.Menu(barra_menu, tearoff=0)
menu_archivos=tk.Menu(barra_menu, tearoff=0)

barra_menu.add_cascade(label="Opciones Cliente", menu=menu_cliente)
barra_menu.add_cascade(label="Opciones Auto", menu=menu_auto)
barra_menu.add_cascade(label="Ver Ventas", menu=menu_ventas)
barra_menu.add_cascade(label="Buscar Clientes", menu=menu_buscar)
barra_menu.add_cascade(label="Datos", menu=menu_datos)
barra_menu.add_cascade(label="Visor Archivos", menu=menu_archivos)

# ---------- CLIENTES ----------
def agregar_cliente():
    top=tk.Toplevel()
    top.title("Agregar Cliente")
    top.geometry("300x200")

    tk.Label(top,text="Nombre").pack()
    e_nombre=tk.Entry(top); e_nombre.pack()

    tk.Label(top,text="DNI").pack()
    e_dni=tk.Entry(top); e_dni.pack()

    tk.Label(top,text="Teléfono").pack()
    e_tel=tk.Entry(top); e_tel.pack()

    def guardar():
        global nombre, dni,tel
        nombre=e_nombre.get()
        dni=e_dni.get()
        tel=e_tel.get()

        if not nombre or not dni or not tel:
            messagebox.showwarning("Advertencia","Complete todo")
            return

        tree_clientes.insert("", "end", values=(nombre,dni,tel))
        top.destroy()

    tk.Button(top,text="Agregar",command=guardar).pack(pady=10)

def archivo_clientes(): 
    with open("ClientesAutos.txt", "w") as archivo:
        clientes=[]
        
        for item in tree_clientes.get_children(): #El get_children permite recorrer cada item de una fila sin repetir
            clientes.append(tree_clientes.item(item, "values"))
        archivo.write(tabulate(clientes, headers=["Nombre", "DNI", "Telefono"]))
        
def eliminar_cliente():
    item=tree_clientes.selection()
    confirmar=messagebox.askyesno("Eliminar", "¿Desea eliminar?")
    
    if confirmar:
        tree_clientes.delete(item)


def modificar_cliente():
    if not tree_clientes.get_children():
        messagebox.showerror("Error", "No hay clientes por modificar")
        return
    else:
        seleccionado = tree_clientes.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar una fila.")
            return
        else:
            item = seleccionado[0]
            valores = tree_clientes.item(item, "values")

            new_nombre = simpledialog.askstring("Nuevo nombre", "Ingrese nuevo nombre")
            if new_nombre is None or new_nombre.strip() == "":
                return

            new_dni = simpledialog.askstring("Nuevo DNI", "Ingrese un nuevo DNI")
            if new_dni is None or new_dni.strip() == "":
                return

            new_tel = simpledialog.askstring("Nuevo Teléfono", "Ingrese el nuevo teléfono")
            if new_tel is None or new_tel.strip() == "":
                return

            confirmar = messagebox.askyesno("Guardar cambios", "Desea guardar cambios?")
            if confirmar:
                tree_clientes.delete(item)  # usar el ID correcto
                tree_clientes.insert("", "end", values=(new_nombre, new_dni, new_tel))


       
menu_cliente.add_command(label="Agregar Cliente", command=agregar_cliente)
menu_cliente.add_command(label="Mostrar Clientes", command=mostrar_clientes)
menu_cliente.add_command(label="Crear Archivo", command=archivo_clientes)
menu_cliente.add_command(label="Eliminar Cliente", command=eliminar_cliente)
menu_cliente.add_command(label="Modificar cliente", command=modificar_cliente)

# ---------- AUTOS ----------
def agregar_auto():
    top=tk.Toplevel()
    top.title("Agregar Auto")
    top.geometry("300x200")

    tk.Label(top,text="Placa").pack()
    e_placa=tk.Entry(top); e_placa.pack()

    tk.Label(top,text="Nro° Autos").pack()
    e_num=tk.Entry(top); e_num.pack()

    tk.Label(top,text="Tipo Lavado").pack()
    t_lavado=tk.Entry(top); t_lavado.pack()


    def guardar():
        global placa, num, precio, lavado,precio
        placa=e_placa.get()
        num=e_num.get()
        lavado=t_lavado.get()


        if not placa or not num or not lavado :
            messagebox.showwarning("Advertencia","Complete todo")
            return
        
        try:
            num=int(e_num.get())

        except ValueError:
            messagebox.showerror("Error", "Ingrese un número de autos válido.")
            return 
        
        if lavado not in lavados.keys():
            messagebox.showwarning("Advertencia", "Ingrese un tipo de lavado válido.")
            return
        
        precio=lavados[lavado] * int(num)
        tree_autos.insert("", "end", values=(placa,num,lavado,precio))
        top.destroy()
    tk.Button(top,text="Agregar",command=guardar).pack(pady=10)

def archivo_autos():
    with open("AutosLavados.txt", "w") as archivo:
        if not tree_autos.get_children():
            messagebox.showerror("Error", "No hay datos por guardar.")
        else:
            autos=[]
            for item in tree_autos.get_children():
                autos.append(tree_autos.item(item, "values"))
            archivo.write(tabulate(autos, headers=["Placa", "Nro°", "Lavado", "Precio"]))
        

def eliminar_auto():
    if not tree_autos.get_children():
        messagebox.showerror("Error", "Lista de autos vacía.")
    else:
        item=tree_autos.selection()
        confirmar=messagebox.askyesno("Eliminar", "Confirmar eliminación?")

        if confirmar:
            tree_autos.delete(item)


def modificar_auto():
    if not tree_autos.get_children():
        messagebox.showerror("Error", "No se encuentran autos por modificar.")
        return
    else:
        seleccionado=tree_autos.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar una fila")
            return
        else:
            item=seleccionado[0]
            new_placa=simpledialog.askstring("Nueva Placa", "Ingrese el número de Placa")
            if new_placa is None or new_placa =="".strip():
                return
            
            new_num=simpledialog.askinteger("Numero de autos", "Ingrese el nuevo número de autos")
            if new_num is None or new_num =="".strip():
                return
            
            new_lavado=simpledialog.askstring("Nuevo lavado", "Ingrese el nuevo Lavado")
            if new_lavado is None or new_lavado =="".strip():
                return
            
            new_precio=lavados[new_lavado]*new_num
            confirmar=messagebox.askyesno("Guardar cambios", "¿Desea guardar cambios?")
            if confirmar:
                tree_autos.delete(item)
                tree_autos.insert("","end", values=(new_placa, new_num, new_lavado, new_precio))


menu_auto.add_command(label="Agregar Auto", command=agregar_auto)
menu_auto.add_command(label="Mostrar Autos", command=mostrar_autos)
menu_auto.add_command(label="Crear Archivo", command=archivo_autos)
menu_auto.add_command(label="Eliminar Auto", command=eliminar_auto)
menu_auto.add_command(label="Modificar Auto", command=modificar_auto)


#---VENTAS----

def mostar_ventas():
    tree_autos.pack_forget()
    tree_clientes.pack_forget()
    tree_ventas.pack(expand=True, fill="both")
    
def agregar_venta():
    global nombre, dni, tel, placa, num, lavado, precio
    tree_ventas.insert("", "end", values=(nombre, dni, tel, placa, num, lavado, precio))
    cursor.execute("""
        INSERT INTO Lavado_de_Autos
        (Cliente, DNI, Telefono, Placa, Nro_Autos, Lavado, Precio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, dni, tel, placa, num, lavado, precio))

    conexion.commit()


def eliminar_venta():
    if not tree_ventas.get_children():
        messagebox.showwarning("Error", "Lista de ventas vacía.")
        return

    seleccionado = tree_ventas.selection()
    if not seleccionado:
        messagebox.showwarning("Error", "Seleccione una venta para eliminar.")
        return

    item = seleccionado[0]
    valores = tree_ventas.item(item, "values")
    v0, v1, v2, v3, v4, v5, v6 = valores 

    confirmar = messagebox.askyesno(
        "Eliminar", 
        f"¿Desea eliminar al cliente {v0} con placa {v3}?"
    )

    if confirmar:
        cursor.execute("""
            DELETE FROM Lavado_de_Autos
            WHERE Cliente = ? AND
                  DNI = ? AND
                  Telefono = ? AND
                  Placa = ? AND
                  Nro_Autos = ? AND
                  Lavado = ? AND
                  Precio = ?
        """, (v0, v1, v2, v3, v4, v5, v6))

        conexion.commit()
        tree_ventas.delete(item)
        messagebox.showinfo("Info", "Venta eliminada exitosamente ✔")

def archivo_ventas():
    with open("VentasLavados.txt", "w", encoding="utf-8") as archivo:
        if not tree_ventas.get_children():
            messagebox.showerror("Error", "No hay datos por guardar.")
        else:
            datos = []

            for item in tree_ventas.get_children():
               datos.append(tree_ventas.item(item, "values"))
            archivo.write(tabulate(datos,headers=["Cliente", "DNI", "Telefono", "Placa", "Nro°", "Lavado", "Precio S/"]))


def ordenar_precio():
    top=tk.Toplevel()
    top.geometry("880x300+400+200")
    top.title("Orden por precio.")

    headings_orden=("Cliente","DNI", "Telefono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_orden_precio=ttk.Treeview(top, show="headings", columns=headings_orden)
    
    for col in headings_orden:
        tree_orden_precio.heading(col, text=col)
        tree_orden_precio.column(col, width=150, anchor="center")
    tree_orden_precio.pack(expand=True, fill="both")

    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    cursor.execute("""
        SELECT Cliente, DNI, Telefono, Placa, Nro_Autos, Lavado, Precio
        FROM Lavado_de_Autos
        ORDER BY Precio ASC
        """)
    
    ventas_ordenadas=cursor.fetchall()

    for fila in ventas_ordenadas:
        tree_orden_precio.insert("","end", values=fila)

    conexion.close()


def generar_boleta_venta():
    seleccionado = tree_ventas.selection()

    if not seleccionado:
        messagebox.showwarning("Error", "Seleccione una venta para generar la boleta.")
        return

    item = seleccionado[0]
    nombre, dni, tel, placa, num, lavado, precio = tree_ventas.item(item, "values")
    # tree_ventas.item --> Es un método que devuelve la información de una fila específica.

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "BOLETA DE VENTA", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    pdf.cell(0, 8, f"Cliente: {nombre}", ln=True)
    pdf.cell(0, 8, f"DNI: {dni}", ln=True)
    pdf.cell(0, 8, f"Teléfono: {tel}", ln=True)
    pdf.cell(0, 8, f"Placa: {placa}", ln=True)
    pdf.cell(0, 8, f"Nro. Autos: {num}", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "DETALLE DEL SERVICIO", ln=True)
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 8, f"Tipo de lavado: {lavado}", ln=True)
    pdf.cell(0, 8, f"Precio: S/ {precio}", ln=True)

    pdf.ln(10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(5)
    pdf.cell(0, 8, "Gracias por su preferencia", ln=True, align="C")

    pdf.output("boleta_lavado.pdf")

    messagebox.showinfo("Éxito", "Boleta generada como 'boleta_lavado.pdf'")

def lavado_mas_vendido():
    lavados = []

    conexion = sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Lavado_de_Autos")
    datos = cursor.fetchall()

    for row in datos:
        lavados.append(row[5])  # columna del tipo de lavado

    basico = lavados.count("Básico")
    exterior = lavados.count("Exterior")
    motor = lavados.count("Motor")
    vapor = lavados.count("Vapor")
    premium = lavados.count("Premium")

    cantidades = [basico, exterior, motor, vapor, premium]
    nombres = ["Básico", "Exterior", "Motor", "Vapor", "Premium"]

    mayor = max(cantidades)
    indice = cantidades.index(mayor)

    mensaje = (
        f"Lavado Básico: {basico}\n"
        f"Lavado Exterior: {exterior}\n"
        f"Lavado Motor: {motor}\n"
        f"Lavado Vapor: {vapor}\n"
        f"Lavado Premium: {premium}\n\n"
        f"El lavado más vendido es: {nombres[indice]} ({mayor} ventas)"
    )

    messagebox.showinfo("Reporte de Ventas", mensaje)

    conexion.close()



menu_ventas.add_command(label="Ver ventas", command=mostar_ventas)
menu_ventas.add_command(label="Agregar venta", command=agregar_venta)  
menu_ventas.add_command(label="Eliminar venta", command=eliminar_venta)  
menu_ventas.add_command(label="Crear Archivo", command=archivo_ventas)
menu_ventas.add_command(label="Ordenar por precio", command=ordenar_precio)
menu_ventas.add_command(label="Generar Boleta PDF", command=generar_boleta_venta)
menu_ventas.add_command(label="Lavado más vendido", command=lavado_mas_vendido)



#Buscar clientes, placas, dni

def buscar_cliente_nombre():
    conexion = sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM Lavado_de_Autos")
    datos = cursor.fetchall()

    nombre_search = simpledialog.askstring("Nombre", "Ingrese el nombre del cliente: ")

    if not nombre_search:
        messagebox.showwarning("Advertencia", "Debe ingresar el nombre del cliente.")
        conexion.close()
        return

    for row in datos:
        if nombre_search.lower() in row[0].lower():
            messagebox.showinfo(
                "Cliente encontrado",
                f"Cliente: {row[0]}\n"
                f"DNI: {row[1]}\n"
                f"Teléfono: {row[2]}\n"
                f"Placa: {row[3]}\n"
                f"Nro_autos: {row[4]}\n"
                f"Lavado: {row[5]}\n"
                f'Precio: S/{row[6]} \n'
                "----------------------\n"
            )
            break
    else:
        # 👇 Este else pertenece al FOR, no al IF
        messagebox.showerror("Error", f"No se encontró al cliente {nombre_search}.")

    conexion.close()

def buscar_cliente_dni():
    conexion = sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT* FROM Lavado_de_Autos")
    datos=cursor.fetchall()

    dni_search=simpledialog.askinteger("DNI", "Ingrese el DNI del cliente:")
    
    if dni_search is None:  #“Solo entra aquí si el usuario canceló o no escribió nada”
        messagebox.showwarning("Advertencia", "Debe ingresar el DNI del cliente.")
        conexion.close()
        return
    else:
        for row in datos:
            if str(dni_search) in str(row[1]):
                messagebox.showinfo("Cliente encontrado", 
                                    f"Cliente: {row[0]}\n"
                                    f"DNI: {row[1]}\n"
                                    f"Teléfono: {row[2]}\n"
                                    f"Placa: {row[3]}\n"
                                    f"Nro_autos: {row[4]}\n"
                                    f"Lavado: {row[5]}\n"
                                    f'Precio: S/{row[6]} \n'
                                   "----------------------\n")
                break
        else:
            messagebox.showerror("Error", f'No se encontro el DNI {dni_search}')

        conexion.close()
        #None = no existe
        #not = existe pero está vacío o es 0


def buscar_cliente_placa():
    conexion = sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor = conexion.cursor()

    placa_search = simpledialog.askstring("Placa", "Ingrese la placa del cliente:")

    if not placa_search:
        messagebox.showwarning("Advertencia", "Debe ingresar la placa.")
        conexion.close()
        return

    placa_search = placa_search.upper().strip()

    cursor.execute("""
        SELECT Cliente, DNI, Telefono, Placa, Lavado, Precio
        FROM Lavado_de_Autos
        WHERE UPPER(Placa) = ?
    """, (placa_search,))

    resultados = cursor.fetchall()

    if resultados:
        mensaje = ""
        for row in resultados:
            mensaje += (
                f"Cliente: {row[0]}\n"
                f"DNI: {row[1]}\n"
                f"Teléfono: {row[2]}\n"
                f"Placa: {row[3]}\n"
                f"Lavado: {row[4]}\n"
                f"Precio: S/ {row[5]}\n"
                "----------------------\n"
            )

        messagebox.showinfo("Vehículo encontrado", mensaje)
    else:
        messagebox.showerror("Error", f"No se encontró la placa {placa_search}")

    conexion.close()




menu_buscar.add_command(label="Por Nombre", command=buscar_cliente_nombre)
menu_buscar.add_command(label="Por DNI", command=buscar_cliente_dni)
menu_buscar.add_command(label="Por Placa", command=buscar_cliente_placa)


#Datos de los clientes:
def lavados_basicos():
    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    top=tk.Toplevel()
    top.title("Clientes Lavado Básico")
    top.geometry("800x300")
    
    headings_basicos=("Cliente", "DNI", "Teléfono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_basicos=ttk.Treeview(top,show="headings", columns=headings_basicos)

    for col in headings_basicos:
        tree_basicos.heading(col, text=col)
        tree_basicos.column(col, width=150, anchor="center")
    tree_basicos.pack(expand=True, fill="both")

    cursor.execute("SELECT* FROM Lavado_de_Autos WHERE Lavado == 'Básico'")
    datos=cursor.fetchall()

    for fila in datos:
        tree_basicos.insert("","end", values=fila)
    
    conexion.close()


def lavados_exterior():
    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    top=tk.Toplevel()
    top.title("Clientes Lavado Exterior")
    top.geometry("800x300")
    
    headings_ext=("Cliente", "DNI", "Teléfono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_basicos=ttk.Treeview(top,show="headings", columns=headings_ext)

    for col in headings_ext:
        tree_basicos.heading(col, text=col)
        tree_basicos.column(col, width=150, anchor="center")
    tree_basicos.pack(expand=True, fill="both")

    cursor.execute("SELECT* FROM Lavado_de_Autos WHERE Lavado == 'Exterior'")
    datos=cursor.fetchall()

    for fila in datos:
        tree_basicos.insert("","end", values=fila)
    
    conexion.close()

def lavados_motor():
    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    top=tk.Toplevel()
    top.title("Clientes Lavado Motor")
    top.geometry("800x300")
    
    headings_motor=("Cliente", "DNI", "Teléfono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_basicos=ttk.Treeview(top,show="headings", columns=headings_motor)

    for col in headings_motor:
        tree_basicos.heading(col, text=col)
        tree_basicos.column(col, width=150, anchor="center")
    tree_basicos.pack(expand=True, fill="both")

    cursor.execute("SELECT* FROM Lavado_de_Autos WHERE Lavado == 'Motor'")
    datos=cursor.fetchall()

    for fila in datos:
        tree_basicos.insert("","end", values=fila)
    
    conexion.close()

def lavados_premium():
    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    top=tk.Toplevel()
    top.title("Clientes Lavado Premium")
    top.geometry("800x300")
    
    headings_premium=("Cliente", "DNI", "Teléfono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_basicos=ttk.Treeview(top,show="headings", columns=headings_premium)

    for col in headings_premium:
        tree_basicos.heading(col, text=col)
        tree_basicos.column(col, width=150, anchor="center")
    tree_basicos.pack(expand=True, fill="both")

    cursor.execute("SELECT* FROM Lavado_de_Autos WHERE Lavado == 'Premium'")
    datos=cursor.fetchall()

    for fila in datos:
        tree_basicos.insert("","end", values=fila)
    
    conexion.close()


def lavados_vapor():
    conexion=sqlite3.connect("Gestor de Lavado_de_Autos.db")
    cursor=conexion.cursor()

    top=tk.Toplevel()
    top.title("Clientes Lavado Vapor")
    top.geometry("800x300")
    
    headings_vapor=("Cliente", "DNI", "Teléfono", "Placa", "Nro_autos", "Lavado", "Precio S/")
    tree_vapor=ttk.Treeview(top,show="headings", columns=headings_vapor)

    for col in headings_vapor:
        tree_vapor.heading(col, text=col)
        tree_vapor.column(col, width=150, anchor="center")
    tree_vapor.pack(expand=True, fill="both")

    cursor.execute("SELECT* FROM Lavado_de_Autos WHERE Lavado == 'Vapor'")
    datos=cursor.fetchall()

    for fila in datos:
        tree_vapor.insert("","end", values=fila)
    
    conexion.close()


menu_datos.add_command(label="Clientes de lavado básico", command=lavados_basicos)
menu_datos.add_command(label="Clientes de Lavado exterior", command=lavados_exterior)
menu_datos.add_command(label="Clientes de Lavado motor", command=lavados_motor)
menu_datos.add_command(label="Clientes de Lavado premium", command=lavados_premium)
menu_datos.add_command(label="Clientes de Lavado Vapor", command=lavados_vapor)


#ver archivos

def visor_archivos():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

    if not ruta:
        return

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    messagebox.showinfo("Contenido del archivo", contenido)

    
menu_archivos.add_command(label="Buscar archivos", command=visor_archivos)


#Salir de la App
def exit_app(event):
    ventana.destroy()
ventana.bind("<Escape>", exit_app)


if __name__=="__main__":
    ventana.mainloop()
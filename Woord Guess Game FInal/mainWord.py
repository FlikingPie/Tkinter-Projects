import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime



palabras = {
    "FUTBOL": "El deporte más famoso del mundo",
    "CEREBRO": "Órgano que controla todo el cuerpo",
    "VISTA": "Sentido que nos permite apreciar objetos",
    "LAPTOP": "Dispositivo portátil con batería",
    "AURORA": "Fenómeno luminoso natural en el cielo",
    "BRUJULA": "Instrumento para orientarse",
    "CELULA": "Unidad básica de los seres vivos",
    "ECLIPSE": "Ocultación de un cuerpo celeste",
    "GALAXIA": "Conjunto enorme de estrellas",
    "LABERINTO": "Lugar con caminos confusos",
    "UNIVERSO": "Conjunto de todo lo que existe"
}


usuario = ""
palabra_correcta = ""
pista_actual = ""
racha = 0
vidas = 3



def registrar_usuario(event=None):
    global usuario
    usuario = entry_usuario.get().strip()
    if not usuario:
        messagebox.showwarning("Aviso", "Ingrese un nombre de usuario")
    else:
        messagebox.showinfo("Bienvenido", f"Usuario {usuario} registrado correctamente")

def nueva_palabra():
    global palabra_correcta, pista_actual
    palabra_correcta, pista_actual = random.choice(list(palabras.items()))

def mostrar_pista():
    messagebox.showinfo("Pista", pista_actual)

def borrar_texto():
    pantalla.config(state="normal")
    pantalla.delete(0, tk.END)
    pantalla.config(state="disabled")

def presionar_letra(event):
    letra = event.widget["text"]
    pantalla.config(state="normal")
    pantalla.insert(tk.END, letra)
    pantalla.config(state="disabled")
    event.widget.config(state="disabled")

def verificar_palabra():
    global vidas, racha
    intento = pantalla.get().upper()

    if intento == palabra_correcta:
        racha += 1
        messagebox.showinfo("Correcto", f"¡Bien hecho! 🔥 Racha: {racha}")
        reiniciar_ronda()
    else:
        vidas -= 1
        messagebox.showerror("Incorrecto", f"Te quedan {vidas} vidas")

        if vidas == 0:
            messagebox.showinfo("Fin del juego", f"Perdiste 😢 La palabra era: {palabra_correcta}")
            guardar_registro()
            ventana_juego.destroy()

def reiniciar_ronda():
    borrar_texto()
    nueva_palabra()
    for boton in botones_letras:
        boton.config(state="normal")

def guardar_registro():
    with open("jugadores_word_guessing.txt", "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        f.write(f"{fecha} - Usuario: {usuario} - Racha máxima: {racha}\n")

# ------------------ VENTANA PRINCIPAL ------------------

ventana_principal = tk.Tk()
ventana_principal.title("Registrar Usuario")
ventana_principal.geometry("300x250")
ventana_principal.resizable(False, False)

tk.Label(ventana_principal, text="Ingrese su nombre", font=("Arial", 12)).pack(pady=20)

entry_usuario = tk.Entry(ventana_principal, width=25)
entry_usuario.pack()
entry_usuario.bind("<Return>", registrar_usuario)

tk.Button(ventana_principal, text="ACEPTAR", command=lambda: abrir_juego()).pack(pady=20)



def abrir_juego():
    if not usuario:
        messagebox.showwarning("Error", "Primero registre un usuario")
        return

    global ventana_juego, pantalla, botones_letras

    nueva_palabra()

    ventana_juego = tk.Toplevel()
    ventana_juego.title("Word Guessing Game")
    ventana_juego.geometry("800x500")
    ventana_juego.resizable(False, False)

    tk.Label(ventana_juego, text="Adivina la palabra", font=("Arial", 18)).pack(pady=15)

    pantalla = tk.Entry(ventana_juego, width=40, justify="center", font=("Arial", 14), state="disabled")
    pantalla.pack(pady=10)

    frame = tk.Frame(ventana_juego)
    frame.pack()

    botones_letras = []
    letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

    fila = columna = 0
    for letra in letras:
        btn = tk.Button(frame, text=letra, width=4, height=2)
        btn.grid(row=fila, column=columna, padx=5, pady=5)
        btn.bind("<Button-1>", presionar_letra)
        botones_letras.append(btn)

        columna += 1
        if columna == 7:
            columna = 0
            fila += 1

    tk.Button(ventana_juego, text="BORRAR", width=15, command=borrar_texto).pack(pady=5)
    tk.Button(ventana_juego, text="INGRESAR", width=15, command=verificar_palabra).pack(pady=5)

    menu = tk.Menu(ventana_juego)
    ventana_juego.config(menu=menu)
    menu.add_command(label="Ver pista", command=mostrar_pista)
    menu.add_command(label="Nueva palabra", command=reiniciar_ronda)

ventana_principal.mainloop()

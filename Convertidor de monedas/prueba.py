import tkinter as tk

ventana = tk.Tk()
ventana.title("Cambio de color")
ventana.geometry("300x300+400+300")
ventana.resizable(False, False)

titulo = tk.Label(
    ventana,
    text="Título",
    font=("Arial", 16, "italic"),
    fg="black",
    bg="white"
)
titulo.pack(pady=20)

tema_oscuro = False  # estado del tema

def cambiar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro

    if tema_oscuro:
        ventana.config(bg="black")
        titulo.config(fg="white", bg="black")
    else:
        ventana.config(bg="white")
        titulo.config(fg="black", bg="white")

tk.Button(
    ventana,
    text="Cambiar tema",
    command=cambiar_tema,
    width=13
).pack(pady=10)

ventana.mainloop()

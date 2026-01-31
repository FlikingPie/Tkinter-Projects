from tkinter import filedialog


def abrir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt")])
        if not ruta:
            return
        # abrir el archivo en modo lectura
        with open (ruta, "r", encoding='utf-8') as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 4:
                    id = int(partes[0])
                    nombre = partes[1]
                    cantidad = int(partes[2])
                    precio = float(partes[3])
                    self.datos.append((id,nombre, cantidad, precio))
        self.ruta_archivo = ruta
        self.actualizar_grilla()
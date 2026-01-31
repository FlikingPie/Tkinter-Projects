import time

# Fecha elegida
fecha = "15/03/2026"

# Convertir string a estructura de tiempo
t = time.strptime(fecha, "%d/%m/%Y")

# Convertir a timestamp
timestamp = time.mktime(t)

print("Timestamp:", timestamp)
print("Fecha:", time.strftime("%d/%m/%Y", time.localtime(timestamp)))

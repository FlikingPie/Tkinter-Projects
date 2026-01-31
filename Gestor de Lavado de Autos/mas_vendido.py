import sqlite3

conexion=sqlite3.connect("Series_animadas.db")
cursor=conexion.cursor()

try:
    cursor.execute("""
                   CREATE TABLE Series_animadas (
                   Año INT,
                   Nombre TEXT,
                   Creador TEXT)
                   """)
    print("Tabla creada con éxito")
except sqlite3.OperationalError:
   print("Error al generar la tabla")


#Series animadas:

series=(
    (2006, "Ben 10", "Man of Action Studios"),
    (2010, "Un Show más", "J.G Quintel"),
    (2009, "Hora de Aventura", "Pendleton Ward"),
    (2011, "El Increible mundo de Gumball", "Ben Bocquelet "),
    (2014, "Escandalosos", "Daniel Chong")
)


#cursor.executemany("""
#                  INSERT INTO Series_animadas(Año, Nombre, Creador)
#                   VALUES (?, ?, ?)
#                   """, series)

cursor.execute("""
        SELECT COUNT(*) 
        FROM Series_animadas
        WHERE Año >= 2010
    """)

cantidad = cursor.fetchone()[0]
print(f"\nSeries desde 2010 en adelante: {cantidad}\n")

    # ---- MOSTRAR CUÁLES SON ----
cursor.execute("""
        SELECT Nombre, Año 
        FROM Series_animadas
        WHERE Año >= 2010
        ORDER BY Año
    """)

print("Listado de series encontradas:")
for nombre, año in cursor.fetchall():
    print(f"- {nombre} ({año})")


conexion.commit()
conexion.close()
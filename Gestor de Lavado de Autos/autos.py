lavados={
        "Básico":10,
        "Exterior":15,
        "Motor":25,
        "Premium":45,
        "Vapor":25
    }

unidades=int(input("Ingrese el numero de autos = "))
lavado=input("Ingrese el tipo de lavado = ")

if lavado not in lavados.keys():
    print(f'El lavado {lavado} no existe.')
else:
    print(f'Tipo de lavado : {lavado}'"\n"
          f'Precio total : {unidades*lavados[lavado]}')
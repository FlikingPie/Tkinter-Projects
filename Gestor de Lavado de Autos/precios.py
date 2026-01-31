lavados={
    "basico":15,
    "exterior":20,
    "interior":25,
    "lavado completo":40,
    "lavado premium":45
}


select=input("Seleccione un tipo de lavado = ")

if select in lavados.keys():
    print(f'Lavado: {select}, precio: {lavados[select]}')
else:
    print("No se encuentra ese tipo de lavado :(")
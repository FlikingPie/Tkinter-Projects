"conversion de soles a dolares y viseversa"

def soles_dolares(soles):
    if soles<=0:
        return "Debe ingresar una cantidad válida."
    else:
        return soles/3.75
soles=float(input("Ingrese la cantidad de soles = S/"))
print(soles_dolares(soles))

print("")
def dolares_soles(dolares):
    if dolares<=0:
        return "Debe ingresar una cantidad válida."
    else:
        return dolares*3.75
dolares=float(input("Ingrese la cantidad de dolares = $"))
print(dolares_soles(dolares))

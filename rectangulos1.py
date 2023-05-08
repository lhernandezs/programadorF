ancho = 10
alto = 8

listaX = [x for x in range(ancho)]
listaY = [y for y in range(alto)]

matrizDeRectangulos = []
matrizHorasProgramadas = [[" "  for y in listaY] for x in listaX]

matrizHorasProgramadas[4][3] = "X"
matrizHorasProgramadas[5][5] = "X"
matrizHorasProgramadas[2][6] = "X"

print("   ", end="")
for x in range(len(listaX)):
    print(f"|{x}", end = "")
print("|")
for y in range(len(listaY)):
    print(f" {y:2d}", end = "")
    for x in range(len(listaX)):
         print(f"|{matrizHorasProgramadas[x][y]}", end = "")
    print("|")

def encontrarRectangulo():
    ban = False
    if len(pila) > 0:
        (xIni, yIni, xFin, yFin) = pila.pop()
        for y in range(yIni, yFin+1):
            for x in range(xIni, xFin+1):
                if matrizHorasProgramadas[x][y] != " ":
                    matrizDeRectangulos.append(["Dentro", xIni, yIni, xFin, y-1])
                    pila.append((xIni, yIni, x-1, yFin))
                    pila.append((x+1, yIni, xFin, yFin))
                    pila.append((xIni, y+1, xFin, yFin))
                    yFin = y
                    encontrarRectangulo()
                    ban = True
                    break
            if ban:
                break
        else:
            matrizDeRectangulos.append(["Fuera ", xIni, yIni, xFin, yFin])
            if len(pila)>0:
#                (xIni, yIni, xFin, yFin) = pila.pop()
                encontrarRectangulo()
    else:
        return


pila = [(0,0,9,7)]
encontrarRectangulo()
for x in range(len(matrizDeRectangulos)):
    print(f"Lugar: {matrizDeRectangulos[x][0]} -- coordenada Inicial: ({matrizDeRectangulos[x][1]:2d} , {matrizDeRectangulos[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulos[x][3]:2d}, {matrizDeRectangulos[x][4]:2d})")

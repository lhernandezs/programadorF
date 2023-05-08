listaX = [x for x in range(10)]
listaY = [y for y in range(8)]

matrizDeRectangulos = []
matrizHorasProgramadas = [[" "  for y in listaY] for x in listaX]

#matrizHorasProgramadas[4][3] = "X"
matrizHorasProgramadas[5][5] = "X"
# matrizHorasProgramadas[2][6] = "X"


print("   ", end="")
for i in range(len(listaX)):
        print(f"|{i}", end = "")
print("|")
for j in range(len(listaY)):
    print(f" {j:2d}", end = "")
    for i in range(len(listaX)):
         print(f"|{matrizHorasProgramadas[i][j]}", end = "")
    print("|")

def encontrarRectangulo():
    global pila
    global ban
    if len(pila) > 0:
        (xIni, yIni, xFin, yFin) = pila.pop()
    else:
        return

    for y in range(yIni, yFin+1):
        for x in range(xIni, xFin+1):
            if ban:
                if matrizHorasProgramadas[x][y] != " ":
                    matrizDeRectangulos.append(["Dentro", xIni, yIni, xFin, y-1])
                    pila.append((xIni, yIni, x-1, yFin))
                    pila.append((x+1, yIni, xFin, yFin))
                    pila.append((xIni, y+1, xFin, yFin))
                    # pila.append((x, y+1, xFin, yFin))
                    # pila.append((x+1, y, xFin, yFin))
                    encontrarRectangulo()
    else:
        if ban:
            matrizDeRectangulos.append(["Fuera ", xIni, yIni, xFin, yFin])
            if len(pila)>0:
                (xIni, yIni, xFin, yFin) = pila.pop()
                encontrarRectangulo()
            else:
                ban = False

ban = True                        
pila = [(0,0,9,7)]
encontrarRectangulo()
for x in range(len(matrizDeRectangulos)):
    print(f"Lugar: {matrizDeRectangulos[x][0]} -- coordenada Inicial: ({matrizDeRectangulos[x][1]:2d} , {matrizDeRectangulos[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulos[x][3]:2d}, {matrizDeRectangulos[x][4]:2d})")
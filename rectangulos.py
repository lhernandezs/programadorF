listaX = [x for x in range(10)]
listaY = [y for y in range(8)]

matrizDeRectangulos = []
matrizHorasProgramadas = [[" "  for y in listaY] for x in listaX]

matrizHorasProgramadas[4][3] = "X"

print("   ", end="")
for i in range(len(listaX)):
        print(f"|{i}", end = "")
print("|")
for j in range(len(listaY)):
    print(f" {j:2d}", end = "")
    for i in range(len(listaX)):
         print(f"|{matrizHorasProgramadas[i][j]}", end = "")
    print("|")

def encontrarRectangulo(xFin, yFin):
    global xAnt
    global yAnt
    global pila
    if len(pila)> 0:
        (xIni, yIni) = pila.pop()
    else:
        (xIni, yIni) = (10, 8)


    for i in range(xIni, xFin):
        for j in range(yIni, yFin):
            if matrizHorasProgramadas[i][j] != " ":
                matrizDeRectangulos.append(["Dentro", "R", xIni, j-1, yIni, yFin])
                pila.append((i + 1, j))
                pila.append((i, j + 1))
                encontrarRectangulo(i-1, yFin)
    else:
        matrizDeRectangulos.append(["Fuera", "T", xIni, xFin, yIni, yFin])
        if len(pila)>0:
            (xIni,yIni) = pila.pop()
            encontrarRectangulo(10, 8)
        else:
            return
                        
pila = [(0,0)]
encontrarRectangulo(10, 8)
for x in range(len(matrizDeRectangulos)):
    print(f"sentido: {matrizDeRectangulos[x][0]}, marca: {matrizDeRectangulos[x][1]} -- horas: {matrizDeRectangulos[x][2]:2d} a {matrizDeRectangulos[x][3]:2d} -- dias: {matrizDeRectangulos[x][4]:2d} a {matrizDeRectangulos[x][5]:2d}")
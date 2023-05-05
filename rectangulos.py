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

def encontrarRectangulo():
    global xAnt
    global yAnt
    global pila
    if len(pila)> 0:
        (xIni, yIni, xFin, yFin) = pila.pop()
    else:
        (xIni, yIni, yFin, xFin) = (10, 8, 10, 8)


    for i in range(xIni, xFin):
        for j in range(yIni, yFin):
            if matrizHorasProgramadas[i][j] != " ":
                matrizDeRectangulos.append(["Dentro", "R", xIni, j-1, yIni, yFin])
                pila.append((i + 1, j, xFin, yFin))
                pila.append((i, j + 1, xFin, yFin))
                encontrarRectangulo()
    else:
        matrizDeRectangulos.append(["Fuera", "T", xIni, xFin, yIni, yFin])
        if len(pila)>0:
            (xIni, yIni, xFin, yFin) = pila.pop()
            encontrarRectangulo()
        else:
            return
                        
pila = [(0,0,10,8)]
encontrarRectangulo()
for x in range(len(matrizDeRectangulos)):
    print(f"sentido: {matrizDeRectangulos[x][0]}, marca: {matrizDeRectangulos[x][1]} -- horas: {matrizDeRectangulos[x][2]:2d} a {matrizDeRectangulos[x][3]:2d} -- dias: {matrizDeRectangulos[x][4]:2d} a {matrizDeRectangulos[x][5]:2d}")
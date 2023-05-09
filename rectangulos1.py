ancho = 20
alto = 14

listaX = [x for x in range(ancho)]
listaY = [y for y in range(alto)]

matrizDeRectangulos = []
matrizHorasProgramadas = [[" "  for y in listaY] for x in listaX]

matrizHorasProgramadas[4][3] = "X"
matrizHorasProgramadas[5][5] = "X"
matrizHorasProgramadas[6][5] = "X"
matrizHorasProgramadas[7][5] = "X"
matrizHorasProgramadas[8][5] = "X"
matrizHorasProgramadas[9][5] = "X"
matrizHorasProgramadas[2][6] = "X"
matrizHorasProgramadas[2][7] = "X"
matrizHorasProgramadas[2][8] = "X"
matrizHorasProgramadas[2][9] = "X"
matrizHorasProgramadas[15][12] = "X"
matrizHorasProgramadas[16][12] = "X"
matrizHorasProgramadas[17][12] = "X"

# print("   ", end="")
# for x in range(len(listaX)):
#     print(f"|{x}", end = "")
# print("|")
# for y in range(len(listaY)):
#     print(f" {y:2d}", end = "")
#     for x in range(len(listaX)):
#          print(f"|{matrizHorasProgramadas[x][y]}", end = "")
#     print("|")

def encontrarRectangulo():
    ban = False
    if len(pila) > 0:
        (xIni, yIni, xFin, yFin) = pila.pop()
        for y in range(yIni, yFin+1):
            for x in range(xIni, xFin+1):
                if matrizHorasProgramadas[x][y] != " ":
                    if xIni <= xFin and yIni <= y-1:
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
            if xIni <= xFin and yIni <= yFin:
                matrizDeRectangulos.append(["Fuera ", xIni, yIni, xFin, yFin])
            if len(pila)>0:
#                (xIni, yIni, xFin, yFin) = pila.pop()
                encontrarRectangulo()
    else:
        return


pila = [(0,0,ancho-1,alto-1)]
encontrarRectangulo()
print("*********************************************")
print("************* c o m e n z o *****************")
print("*********************************************")

matrizDeRectangulosNew = []
while len(matrizDeRectangulos)>0:
    (indicador,xIni, yIni, xFin, yFin) = matrizDeRectangulos.pop()
    xEIni, yEIni, xEFin, yEFin = xIni, yIni, xFin, yFin
    ban = False
    for rn in range(len(matrizDeRectangulosNew)):
        if len(matrizDeRectangulosNew)>0:
            (indicador, xnIni, ynIni, xnFin, ynFin) = matrizDeRectangulosNew[rn]
            if   xIni != xnIni and xFin == xnFin and yIni == ynIni and yFin == ynFin:
                xEIni = xIni if xIni <= xnIni else xnIni
                ban = True
            elif xIni == xnIni and xFin != xnFin and yIni == ynIni and yFin == ynFin:
                xEFin = xFin if xFin >= xnFin else xnFin
                ban = True
            elif xIni == xnIni and xFin == xnFin and yIni != ynIni and yFin == ynFin:
                yEIni = yIni if yIni <= ynIni else ynIni
                ban = True
            elif xIni == xnIni and xFin == xnFin and yIni == ynIni and yFin != ynFin:
                yEFin = yFin if yFin >= ynFin else ynFin
                ban = True        
    if not ban:
        matrizDeRectangulosNew.append([indicador, xEIni, yEIni, xEFin, yEFin])


# for x in range(len(matrizDeRectangulosNew)):
#     print(f"Lugar: {matrizDeRectangulosNew[x][0]} -- coordenada Inicial: ({matrizDeRectangulosNew[x][1]:2d} , {matrizDeRectangulosNew[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulosNew[x][3]:2d}, {matrizDeRectangulosNew[x][4]:2d})")
#     print("   ", end="")
#     for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
#         for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
#             matrizHorasProgramadas[a][b] = "O" 

#     for i in range(len(listaX)):
#         print(f"|{i:2d}", end = "")
#     print("|")
#     for j in range(len(listaY)):
#         print(f" {j:2d}", end = "")
#         for i in range(len(listaX)):
#             print(f"|{(matrizHorasProgramadas[i][j]).rjust(2)}", end = "")
#         print("|")

#     for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
#         for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
#             matrizHorasProgramadas[a][b] = " " 

with open("text.txt","w") as file:

    for x in range(len(matrizDeRectangulosNew)):
        file.write(f"Lugar: {matrizDeRectangulosNew[x][0]} -- coordenada Inicial: ({matrizDeRectangulosNew[x][1]:2d} , {matrizDeRectangulosNew[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulosNew[x][3]:2d}, {matrizDeRectangulosNew[x][4]:2d})\n")
        file.write("   ")
        for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
            for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
                matrizHorasProgramadas[a][b] = "O" 

        for i in range(len(listaX)):
            file.write(f"|{i:2d}")
        file.write("|\n")
        for j in range(len(listaY)):
            file.write(f" {j:2d}")
            for i in range(len(listaX)):
                file.write(f"|{(matrizHorasProgramadas[i][j]).rjust(2)}")
            file.write("|\n")

        for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
            for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
                matrizHorasProgramadas[a][b] = " " 

file.close()

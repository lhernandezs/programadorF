import sys as sys

ancho = 31
alto = 24

recursividad = recursividadIz= recursividadDe = recursividadIn = 0

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
matrizHorasProgramadas[1][6] = 'X'
matrizHorasProgramadas[2][6] = 'X'
matrizHorasProgramadas[3][6] = 'X'
matrizHorasProgramadas[4][6] = 'X'
matrizHorasProgramadas[5][6] = 'X'
matrizHorasProgramadas[6][6] = 'X'
matrizHorasProgramadas[7][6] = 'X'
matrizHorasProgramadas[8][6] = 'X'
matrizHorasProgramadas[9][6] = 'X'
matrizHorasProgramadas[10][6] = 'X'
matrizHorasProgramadas[11][6] = 'X'
matrizHorasProgramadas[12][6] = 'X'
matrizHorasProgramadas[13][6] = 'X'
matrizHorasProgramadas[14][6] = 'X'
matrizHorasProgramadas[15][6] = 'X'
matrizHorasProgramadas[16][6] = 'X'
matrizHorasProgramadas[17][6] = 'X'
matrizHorasProgramadas[18][6] = 'X'
matrizHorasProgramadas[19][6] = 'X'
matrizHorasProgramadas[20][6] = 'X'
matrizHorasProgramadas[21][6] = 'X'
matrizHorasProgramadas[22][6] = 'X'
matrizHorasProgramadas[23][6] = 'X'
matrizHorasProgramadas[24][6] = 'X'
matrizHorasProgramadas[25][6] = 'X'
matrizHorasProgramadas[26][6] = 'X'
matrizHorasProgramadas[27][6] = 'X'
matrizHorasProgramadas[28][6] = 'X'
matrizHorasProgramadas[1][7] = 'X'
matrizHorasProgramadas[2][7] = 'X'
matrizHorasProgramadas[3][7] = 'X'
matrizHorasProgramadas[4][7] = 'X'
matrizHorasProgramadas[5][7] = 'X'
matrizHorasProgramadas[6][7] = 'X'
matrizHorasProgramadas[7][7] = 'X'
matrizHorasProgramadas[8][7] = 'X'
matrizHorasProgramadas[9][7] = 'X'
matrizHorasProgramadas[10][7] = 'X'
matrizHorasProgramadas[11][7] = 'X'
matrizHorasProgramadas[12][7] = 'X'
matrizHorasProgramadas[13][7] = 'X'
matrizHorasProgramadas[14][7] = 'X'
matrizHorasProgramadas[15][7] = 'X'
matrizHorasProgramadas[16][7] = 'X'
matrizHorasProgramadas[17][7] = 'X'
matrizHorasProgramadas[18][7] = 'X'
matrizHorasProgramadas[19][7] = 'X'
matrizHorasProgramadas[20][7] = 'X'
matrizHorasProgramadas[21][7] = 'X'
matrizHorasProgramadas[22][7] = 'X'
matrizHorasProgramadas[23][7] = 'X'
matrizHorasProgramadas[24][7] = 'X'
matrizHorasProgramadas[25][7] = 'X'
matrizHorasProgramadas[26][7] = 'X'
matrizHorasProgramadas[27][7] = 'X'
matrizHorasProgramadas[28][7] = 'X'
matrizHorasProgramadas[3][10] = 'X'
matrizHorasProgramadas[4][10] = 'X'
matrizHorasProgramadas[5][10] = 'X'
matrizHorasProgramadas[6][10] = 'X'
matrizHorasProgramadas[7][10] = 'X'
matrizHorasProgramadas[8][10] = 'X'
matrizHorasProgramadas[9][10] = 'X'
matrizHorasProgramadas[10][10] = 'X'
matrizHorasProgramadas[11][10] = 'X'
matrizHorasProgramadas[12][10] = 'X'
matrizHorasProgramadas[13][10] = 'X'
matrizHorasProgramadas[14][10] = 'X'
matrizHorasProgramadas[15][10] = 'X'
matrizHorasProgramadas[16][10] = 'X'
# matrizHorasProgramadas[17][10] = 'X'
# matrizHorasProgramadas[18][10] = 'X'
# matrizHorasProgramadas[19][10] = 'X'
# matrizHorasProgramadas[20][10] = 'X'
# matrizHorasProgramadas[21][10] = 'X'
# matrizHorasProgramadas[22][10] = 'X'
# matrizHorasProgramadas[23][10] = 'X'
# matrizHorasProgramadas[24][10] = 'X'
# matrizHorasProgramadas[6][13] = 'X'
# matrizHorasProgramadas[7][13] = 'X'
# matrizHorasProgramadas[8][13] = 'X'
# matrizHorasProgramadas[9][13] = 'X'
# matrizHorasProgramadas[10][13] = 'X'
# matrizHorasProgramadas[11][13] = 'X'
# matrizHorasProgramadas[12][13] = 'X'
# matrizHorasProgramadas[13][13] = 'X'
# matrizHorasProgramadas[14][13] = 'X'
# matrizHorasProgramadas[15][13] = 'X'
# matrizHorasProgramadas[16][13] = 'X'
# matrizHorasProgramadas[17][13] = 'X'
# matrizHorasProgramadas[18][13] = 'X'
# matrizHorasProgramadas[19][13] = 'X'
# matrizHorasProgramadas[20][13] = 'X'
# matrizHorasProgramadas[6][14] = 'X'
# matrizHorasProgramadas[7][14] = 'X'
# matrizHorasProgramadas[8][14] = 'X'
# matrizHorasProgramadas[9][14] = 'X'
# matrizHorasProgramadas[10][14] = 'X'
# matrizHorasProgramadas[11][14] = 'X'
# matrizHorasProgramadas[12][14] = 'X'
# matrizHorasProgramadas[13][14] = 'X'
# matrizHorasProgramadas[14][14] = 'X'
# matrizHorasProgramadas[15][14] = 'X'
# matrizHorasProgramadas[16][14] = 'X'
# matrizHorasProgramadas[17][14] = 'X'
# matrizHorasProgramadas[18][14] = 'X'
# matrizHorasProgramadas[19][14] = 'X'
# matrizHorasProgramadas[20][14] = 'X'
# matrizHorasProgramadas[6][15] = 'X'
# matrizHorasProgramadas[7][15] = 'X'
# matrizHorasProgramadas[8][15] = 'X'
# matrizHorasProgramadas[9][15] = 'X'
# matrizHorasProgramadas[10][15] = 'X'
# matrizHorasProgramadas[11][15] = 'X'
# matrizHorasProgramadas[12][15] = 'X'
# matrizHorasProgramadas[13][15] = 'X'
# matrizHorasProgramadas[14][15] = 'X'
# matrizHorasProgramadas[15][15] = 'X'
# matrizHorasProgramadas[16][15] = 'X'
# matrizHorasProgramadas[17][15] = 'X'
# matrizHorasProgramadas[18][15] = 'X'
# matrizHorasProgramadas[19][15] = 'X'
# matrizHorasProgramadas[20][15] = 'X'


def encontrarRectangulo():
    global recursividad
    global recursividadIz
    global recursividadDe
    global recursividadIn
    
    recursividad += 1
    ban = False
    if len(pila) > 0:
        (xIni, yIni, xFin, yFin) = pila.pop()
        superior = izquierdo = derecho = inferior = False
        for y in range(yIni, yFin+1):
            for x in range(xIni, xFin+1):
                if matrizHorasProgramadas[x][y] != " ":              # NO                       APUNTA                          ENTRA
                    if   x == 0 and y == 0                         : # izquierdo superior       derecho inferior    
                        derecho = inferior = True
                    elif x == 0 and y in range(1,  alto-1)         : # izquierdo                derecho inferior                superior
                        derecho = inferior = superior = True
                    elif y == 0 and x in range(1, ancho-1)         : # superior                 derecho inferior izquierdo
                        derecho = inferior = izquierdo = True
                    elif x == (ancho-1) and y == (alto-1)          : # derecho inferior         izquierdo                       superior
                        izquierdo = superior = True
                    elif x == (ancho-1) and y in range(1, alto-1)  : # derecho                  izquierdo inferior              superior
                        izquierdo = inferior = superior = True
                    elif y == (alto-1)  and x in range (1, ancho-1): # inferior                 izquierdo derecho               superior
                        izquierdo = derecho = superior = True
                    elif x == 0 and y == (alto-1)                  : # izquierdo inferior       derecho                         superior
                        derecho = superior = True
                    elif x == (ancho-1) and y == 0                 : # derecho superior         izquierdo inferior
                        izquierdo =  inferior = True
                    else:     
                        if   xIni == x and yIni == y               : # izquierdo superior       derecho inferior
                            derecho = inferior = True
                        elif xIni == x and yIni != y               : # superior                 izquierdo derecho inferior      
                            izquierdo = derecho = inferior = True
                        elif yIni == y and xIni != x               : # izquierdo                derecho inferior                superior
                            derecho = inferior = True
                        else                                       : #                          izquierdo derecho inferior      superior
                            izquierdo = derecho = inferior = superior = True

                    if superior:
                        matrizDeRectangulos.append(["Dentro", xIni, yIni, xFin, y-1, (xFin - xIni)*((y-1) - yIni)]) # ENTRA superior
                    if izquierdo and matrizHorasProgramadas[x-1][y] == " ":
                        pila.append((xIni, yIni, x-1, yFin))                          # apunta a rectangulo izquierdo
                        recursividadIz += 1
#                    if derecho and matrizHorasProgramadas[x+1][y] == " ":  
                    if derecho:
                        pila.append((x+1, yIni, xFin, yFin))                          # apunta a rectangulo derecho
                        recursividadDe += 1
#                    if inferior and matrizHorasProgramadas[x][y+1] == " ":
                    if inferior:
                        pila.append((xIni, y+1, xFin, yFin))                          # apunta a rectangulo inferior
                        recursividadIn += 1

#                    yFin = y
                    encontrarRectangulo()
                    ban = True
                    break
            if ban:
                break
        else:
            if xIni <= xFin and yIni <= yFin:
                matrizDeRectangulos.append(["Fuera ", xIni, yIni, xFin, yFin, (xFin - xIni)*(yFin - yIni)])
            if len(pila)>0:
                encontrarRectangulo()
    else:
        return

print(sys.getrecursionlimit())
sys.setrecursionlimit(5000000)
print(sys.getrecursionlimit())
pila = [(0,0,ancho-1,alto-1)]
encontrarRectangulo()
print("*********************************************")
print("************* c o m e n z o *****************")
print("*********************************************")
print(f"recursividad = {recursividad} Izquierdo = {recursividadIz} Derecho = {recursividadDe} Inferior = {recursividadIn}")

relleno = str(chr(35))  
relleno = "0"

arregloMatrizRectangulos = True

if arregloMatrizRectangulos:
    matrizDeRectangulosOrd = sorted(matrizDeRectangulos, key=lambda x: x[5])
    matrizDeRectangulosNew = []
    while len(matrizDeRectangulosOrd)>0:
        (indicador, xOIni, yOIni, xOFin, yOFin, capacidad) = matrizDeRectangulosOrd.pop()
        interno = False
        for rn in range(len(matrizDeRectangulosNew)):
            if len(matrizDeRectangulosNew)>0:
                (indicador, xNIni, yNIni, xNFin, yNFin) = matrizDeRectangulosNew[rn]
                if xOIni >= xNIni and xOFin <= xNFin and yOIni >= yNIni and yOFin <= yNFin:
                    interno = True        
        if not interno:
            matrizDeRectangulosNew.append([indicador, xOIni, yOIni, xOFin, yOFin])
else:
    matrizDeRectangulosNew = sorted(matrizDeRectangulos, key=lambda x: x[5])


terminal = False

if terminal:
    for x in range(len(matrizDeRectangulosNew)):
        print(f"Lugar: {matrizDeRectangulosNew[x][0]} -- coordenada Inicial: ({matrizDeRectangulosNew[x][1]:2d} , {matrizDeRectangulosNew[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulosNew[x][3]:2d}, {matrizDeRectangulosNew[x][4]:2d})")
        print("   ", end="")
        for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
            for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
                matrizHorasProgramadas[a][b] = relleno 
        for i in range(len(listaX)):
            print(f"|{i:2d}", end = "")
        print("|")
        for j in range(len(listaY)):
            print(f" {j:2d}", end = "")
            for i in range(len(listaX)):
                print(f"|{(matrizHorasProgramadas[i][j]).rjust(2)}", end = "")
            print("|")
        for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
            for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
                matrizHorasProgramadas[a][b] = " " 
else:
    with open("text.txt","w") as file:
        for x in range(len(matrizDeRectangulosNew)):
            file.write(f"Lugar: {matrizDeRectangulosNew[x][0]} -- coordenada Inicial: ({matrizDeRectangulosNew[x][1]:2d} , {matrizDeRectangulosNew[x][2]:2d}) -- coordenada Final: ({matrizDeRectangulosNew[x][3]:2d}, {matrizDeRectangulosNew[x][4]:2d})\n")
            file.write("   ")
            for a in range(matrizDeRectangulosNew[x][1], matrizDeRectangulosNew[x][3] +1 ):
                for b in range(matrizDeRectangulosNew[x][2], matrizDeRectangulosNew[x][4] +1 ):
                    matrizHorasProgramadas[a][b] = relleno 

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

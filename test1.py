# eventosPorDiaHora = self.eventosPorDiaHora()
# for i in range(Mes(mes).ultimoDia().day):
#     for j in range(24):
#         if len(eventosPorDiaHora[i][j]) > 1:
#             print(f"[dia: {i+1:2d}, horas: {j:2d} a {j+1:2d}]...Eventos:", eventosPorDiaHora[i][j])
# print("****************")


# lista =[x for x in range(1,32)]
# for i in range(1,32):
#     print(i, " - ", lista[i-1], ";", end="")
# print("********************")
# lista1 = [[j for j in range(24)] for i in range(1, 31)]
# print(lista1)
# print("********************")
# class prueba:
#     def __init__(self):
#         _cedula
#         _nombre
#         _apellido

#     @property
#     def cedula(self):
#         return _cedula

#     @cedula.setter
#     def cedula(self, cedula):
#         _cedula = cedula

#     @property
#     def nombre(self):
#         return _nombre

#     @nombre.setter
#     def nombre(self, nombre):
#         _nombre = nombre

#     @property
#     def apellido(self):
#         return _apellido

#     @apellido.setter
#     def apellido(self, apellido):
#         _apellido = apellido


# number = 0
# for number in range(10):
#     if number == 5:
#         break    # break here

#     print('Number is ' + str(number))

# print('Out of loop')

# number = 0
# for number in range(10):
#     if number == 5:
#         continue    # continue here

#     print('Number is ' + str(number))

# print('Out of loop')

# datos = [ (3, 1, 2), (2, 3, 1), (3, 2, 0), (1, 2, 3), (4, 1, 4), (4, 2, 1), (3, 3, 0)]
# print(sorted(sorted(datos, key=lambda x: x[2]), key=lambda x: -x[1]))
# datos =[]
# print(sorted(datos, key=lambda x: -x[1]))

# from collections import Counter

# a = [[[1],[1,1],[2],[2,2],[3,1]], [[1,1],[1,1],[1],[2,2],[3]], [[1,1],[1,1],[2,1],[2,2],[3,1]]]

# print(list(filter(lambda item: len(item) == 1, [a[i][j] for j in range(5) for i in range(3)])))

# counter = Counter(a)
# print(max(a, key=a.count),"repetido ",a.count(max(a, key=a.count)))

# first, second, *_, last = counter.most_common()

# print(first, second, last)
# print(counter.most_common(1))

# class Prueba:
#     def __init__(self):
#         a = 0
#         b = 1

#     def mandaTupla(self):
#         datos = ( 1, 2, 3 )
#         return datos

#     def utilizaTupla(self):
#         ( x, y , z) = self.mandaTupla()
#         print(z)

# prueba = Prueba()
# prueba.utilizaTupla()

# lista = (3,2,1)
# lista1 = sorted(lista)
# print(lista1)

# print("SI" if 3 > None else None)

# declare our own string class
# class String:

#     # magic method to initiate object
#     def __init__(self, string):
#         self.string = string

# # Driver Code
# if __name__ == '__main__':

#     # object creation
#     string1 = String('Hello')

#     # print object location
#     print(string1)

# lista = [1,2,3]
# if len(lista) > 2:
#     print("la lista tiene mas de 2 elementos y su longitud es:", len(lista))
# else:
#     print("la lista tiene dos o menos elementos y su longitud es:", len(lista))

# lista = [1,2,3]
# if (long:= len(lista)) > 2:
#     print("la lista tiene mas de 2 elementos y su longitud es:", long)
# else:
#     print("la lista tiene dos o menos elementos y su longitud es:", long)

# class Decorador:
#     def __init__(self):
#         _var = False

#     @property
#     def var(self):
#         return _var

#     @var.setter
#     def var(self, var):
#         _var = var

# lista = True
# dec = Decorador()
# dec.var =lista 
# print(dec.var)

# class Prueba:
#     def imprimir():
#         print("hola")
#     a = 3
#     def __init__(self):
#         self.b = Prueba.a +3

# Prueba.imprimir()
# print(Prueba.a)
# o = Prueba()
# print(o.b)

# lista = [1, 3, 5, 6, 1, 5, 1]
# print(max(lista, key=lista.count))
# print(sorted(lista, key=lista.count))
# 
# lista = [[1,2,5],[2,4,4],[3,6,2],[4,5,7]]
# orden2 = [5,6,2,4]
# listaO = sorted(lista, key=lambda l: -l[2])
# lista.sort(key=lambda l: -l[2])
# lista.sort(orden2)
# print("original ordenada:", lista)
# print("copia ordinada   :", listaO)

# l  = [ x for x in range(10)]
# i = l[len(l)-1]
# print(i)
# print(l)
# l.pop(-1)
# l.pop(-1)
# print(l)

# dias = [3, 4, 5, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28 ]

# v = 11
# i = dias.index(v)
# c = 6
# r = i+c-1
# print(dias[r])
# print(dias[dias.index(v)+c -1])

# dias = [1,2,3,4,5]
# horas = [10,11,12,13]

# matriz = []
# i = 0
# for h in horas:
#     matriz.append([h,[]])
#     for d in dias:
#         matriz[i][1].append(d)
#     i += 1
# print(matriz)
# print(len(matriz))
# print(len(matriz[0][1]))



# lista = [1,2,3,4,65]
# print(lista.index(65))
# print(lista[-1])
# lista = lista[:2]
# print(lista)
# print

# listaDiasNoLaborables = [1,2,6,7,8,9,15,16,22,23,29,30]
# listaDiasLaborables = [3,4,5,10,11,12,13,14,17,18,19,20,21,24,25,26,27,28]
# matrizDeRectangulos = []
# matrizHorasNoProgramadas = [[(" " if d+1 in listaDiasLaborables else "F") for d in range(31)] for h in range(24)]

# matrizHorasNoProgramadas[12][19] = "X"
# matrizHorasNoProgramadas[9][12] = "X"

# for i in range(24):
#     print(f" {i:2d}", end = "")
#     for j in range(30):
#          print(f"|{matrizHorasNoProgramadas[i][j]}|", end = "")
#     print()

# def encontrarRectangulo(hIni, hFin, dIni, dFin):
#     global vertical
#     global hAnt
#     global dAnt
#     if hIni == 24 or dIni == 28:
#         return
#     banPorTerminaciónBucled = True
#     for h in range(hIni, hFin):
#         for d in listaDiasLaborables[listaDiasLaborables.index(dIni):listaDiasLaborables.index(dFin)]:
#             if matrizHorasNoProgramadas[h][d-1] != " ":
#                 banPorTerminaciónBucled = False
#                 matrizDeRectangulos.append([vertical, "R", hIni, h-1, dIni, dFin])
#                 if not vertical:
#                     # d = listaDiasLaborables[listaDiasLaborables.index(d)-1]
#                     # hAnt = h
#                     # dIni = dAnt
#                     hIni = hAnt
#                     hFin = hAnt
#                     dIni = dIni
#                     dFin = listaDiasLaborables[listaDiasLaborables.index(d)-1]
#                     hAnt = hIni
#                     dAnt = dIni
#                 else:
#                     hIni = hAnt
#                     hFin = hAnt
#                     dIni = listaDiasLaborables[listaDiasLaborables.index(d)+ 1]
#                     dFin = dFin
#                     hAnt = hIni
#                     dAnt = dIni
#                     # dAnt = d + 1
#                     # hIni = hAnt + 1
#                     # dIni = listaDiasLaborables[listaDiasLaborables.index(d)+ 1]
#                 vertical = not vertical
#                 encontrarRectangulo(hIni, hFin, dIni, dFin)
#     if banPorTerminaciónBucled:
# #        contador += 1
#         matrizDeRectangulos.append([vertical, "T", hIni, hFin, dIni, dFin])

# hAnt = 0
# dAnt = 3
# vertical = False
# encontrarRectangulo(0, 24, 3, 28)
# for x in range(len(matrizDeRectangulos)):
#     print(f"contador: {matrizDeRectangulos[x][0]:2d}, marca: {matrizDeRectangulos[x][1]} -- horas: {matrizDeRectangulos[x][2]:2d} a {matrizDeRectangulos[x][3]:2d} -- dias: {matrizDeRectangulos[x][4]:2d} a {matrizDeRectangulos[x][5]:2d}")

# listaDias = [d for d in range(10)]
# listaHoras = [h for h in range(12)]

# matrizDeRectangulos = []
# matrizHorasProgramadas = [[" "  for d in listaDias] for h in listaHoras]

# matrizHorasProgramadas[4][5] = "X"

# print("   ", end="")
# for j in range(10):
#         print(f"|{j}", end = "")
# print("|")
# for i in range(12):
#     print(f" {i:2d}", end = "")
#     for j in range(10):
#          print(f"|{matrizHorasProgramadas[i][j]}", end = "")
#     print("|")

# def encontrarRectangulo(hIni, hFin, dIni, dFin):
#     global hAnt
#     global dAnt
#     if hIni > 10 and dIni > 9:
#         return
#     for h in range(hIni, hFin):
#         for d in range(dIni, dFin):
#             if matrizHorasProgramadas[h][d] != " ":
#                 banPorTerminaciónBucled = False
#                 matrizDeRectangulos.append(["Dentro", "R", hIni, h-1, dIni, dFin])
#                 hAnt = h + 1
#                 dAnt = d + 1
#                 encontrarRectangulo(hIni, hFin, dIni, d-1)
#     else:
#         matrizDeRectangulos.append(["Fuera", "T", hIni, hFin, dIni, dFin])
#         encontrarRectangulo(hAnt, hFin, dAnt, dFin)
                        
# hAnt = 0
# dAnt = 0
# encontrarRectangulo(0, 11, 0, 9)
# for x in range(len(matrizDeRectangulos)):
#     print(f"sentido: {matrizDeRectangulos[x][0]:2d}, marca: {matrizDeRectangulos[x][1]} -- horas: {matrizDeRectangulos[x][2]:2d} a {matrizDeRectangulos[x][3]:2d} -- dias: {matrizDeRectangulos[x][4]:2d} a {matrizDeRectangulos[x][5]:2d}")


# lista = [[1,3],[2,2],[1,6]]
# lista1 = sorted(lista, key=lambda x: x[1])
# print(lista.sort(key=lambda x: x[1]))
# print(lista1)

# lista = [x for x in range(5)]
# print(lista)
# print(lista.index(0))
# print(lista.index(len(lista)-1))
# print(sorted(lista, reverse=True))
# print(lista[-1])
# print(list(filter(lambda x: x%2 == 0, lista)))

# diccionario = {10:1, 11:2, 12: 2, 13:2}
#print(list(filter(lambda value: value == 2 for value in diccionario.values)))
# print(list(filter(lambda x: diccionario[x]== 2, diccionario.keys())))
# print(30//4)

# class Prueba:
#     a = 3
#     b = 5

# print(Prueba.b)

# for i in range(3,3+1):
#     print(i)

# lista = list(filter(lambda x: x>10, range(3)))
# print(lista)
# l1 = [[1,2],[3],["nd"]]
# for i in range(len(l1)):
#     if len(l1[i]) > 1 or l1[i] == ["nd"]:
#         print(l1[i])

lista = [[1,2],[3,1],[2,1],[2,2],[1,1],[1],[1,2],[2,2],[1,1],[1],[2,2],[1,1]]
resultado={}
for l in lista:
    il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
    resultado[il] = 0

for l in lista:
    il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
    resultado[il] += 1

print(resultado)

for id in resultado.keys():
    print(id.split("_"))

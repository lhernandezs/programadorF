
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
# print(list(filter(lambda value: value == 2 for value in diccionario.values)))
# print(list(filter(lambda x: diccionario[x]== 2, diccionario.keys())))
# print(30//4)

# lista = list(filter(lambda x: x>10, range(3)))
# print(lista)
# l1 = [[1,2],[3],["nd"]]
# for i in range(len(l1)):
#     if len(l1[i]) > 1 or l1[i] == ["nd"]:
#         print(l1[i])

# lista = [[1,2],[3,1],[2,1],[2,2],[1,1],[1],[1,2],[2,2],[1,1],[1],[2,2],[1,1]]
# resultado={}
# for l in lista:
#     il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
#     resultado[il] = 0

# for l in lista:
#     il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
#     resultado[il] += 1

# print(resultado)

# for id in resultado.keys():
#     print(id.split("_"))

# lista = [d for d in range(10)]
# a = [1,2]
# b = [5,8,9]
# print(list(set(lista) - set(a)- set(b)))

# lista = [d for d in range(10,20)]
# menor = 13
# mayor = 15
# listaAbajo = lista[:lista.index(menor)]
# listaArriba = lista[lista.index(mayor):]
# lista2 = lista[lista.index(menor):lista.index(mayor)]
# diferencia = lista.index(mayor) - lista.index(menor)
# print(listaAbajo)
# print(listaArriba)
# print(lista2)
# print(diferencia)

# print([d for d in range(31,0)])

# lista = [d for d in range(10)]
# listaA = [d for d in [0,1]]
# listaL = [d for d in [8,9]]

# print(list(set(lista) & set(listaA)))

# cadena = "Perdon"
# if cadena[0] == "J":
#     print("listo")

# lista = [x*2 for x in range(10)]
# print(lista)
# indice3 = lista.index(6)
# indice5 = lista.index(12)
# print(indice3)
# print(indice5)
# print(lista[indice3:indice5])

# lista = [[1,2,3],[1,2],[1,2,3,4]]
# l1 = sorted(lista, key=lambda x: -len(x))
# print(l1)

for i in sorted([1,2,3], reverse=True):
    print(i)
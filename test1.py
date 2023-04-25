# eventosPorDiaHora = self.eventosPorDiaHora()
# for i in range(Mes(self._mes).ultimoDia().day):
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
#         self.__cedula
#         self.__nombre
#         self.__apellido

#     @property
#     def cedula(self):
#         return self.__cedula

#     @cedula.setter
#     def cedula(self, cedula):
#         self.__cedula = cedula

#     @property
#     def nombre(self):
#         return self.__nombre

#     @nombre.setter
#     def nombre(self, nombre):
#         self.__nombre = nombre

#     @property
#     def apellido(self):
#         return self.__apellido

#     @apellido.setter
#     def apellido(self, apellido):
#         self.__apellido = apellido


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
#         self._a = 0
#         self._b = 1

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
#         self.__var = False

#     @property
#     def var(self):
#         return self.__var

#     @var.setter
#     def var(self, var):
#         self.__var = var

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
dic = {1: "a", 2: "b", 3: "c"}
print(list(dic.keys()))
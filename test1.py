
lista =[x for x in range(1,32)]
for i in range(1,32):
    print(i, " - ", lista[i-1], ";", end="")
print("********************")
lista1 = [[j for j in range(24)] for i in range(1, 31)]
print(lista1)
print("********************")
class prueba:
    def __init__(self):
        self.__cedula
        self.__nombre
        self.__apellido

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, cedula):
        self.__cedula = cedula
        
    @property 
    def nombre(self): 
        return self.__nombre 
    
    @nombre.setter 
    def nombre(self, nombre): 
        self.__nombre = nombre 

    @property 
    def apellido(self): 
        return self.__apellido 

    @apellido.setter 
    def apellido(self, apellido): 
        self.__apellido = apellido

def decorador(f):
    def funcion_nueva():
        print("Funcionalidad extra")
        f()
    return funcion_nueva
print("********************")
@decorador
def funcion_inicial():
    print("Funcionalidad inicial")

funcion_inicial()
print("********************")
for i in range(28,30):
    print(i)
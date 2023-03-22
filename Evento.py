import datetime

class Evento:
    def __init__(self, ficha, horaI, horaF, fechaI, fechaF):
        self.__ficha = ficha
        self.__horaI = horaI
        self.__horaF = horaF
        self.__fechaI = fechaI
        self.__fechaF = fechaF

    def setFicha(self, ficha):
        self.__ficha = ficha
    
    def getFicha(self):
        return self.__ficha

    def setHoraI(self, horaI):
        self.__horaI = horaI
    
    def getHoraI(self):
        return self.__horaI

    def setHoraF(self, horaF):
        self.__horaF = horaF
    
    def getHoraF(self):
        return self.__horaF

    def setFechaI(self, fechaI):
        self.__fechaI = fechaI
    
    def getFechaI(self):
        return self.__fechaI

    def setFechaF(self, fechaF):
        self.__fechaF = fechaF
    
    def getFechaF(self):
        return self.__fechaF

    def __str__(self):
        return str(self.__ficha) + ", " + str(self.__horaI) + ", " + str(self.__horaF) + ", " + str(self.__fechaI) + ", " + str(self.__fechaF)

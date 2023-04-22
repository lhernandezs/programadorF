from datetime import datetime

class Evento:
    def __init__(self):
        self.__id = 0
        self.__ficha = 0
        self.__horaI = 0
        self.__horaF = 0
        self.__fechaI = None   
        self.__fechaF = None
        self.__listaDiasLaborables = None
        self.__listaDiasAntesCruce = None
        self.__listaDiasLuegoCruce = None
        self.__listaDiasAProgramar = None
        self.__listaDiasPorProgram = None
        self.__fichaYaProgramada = False

    def __init__(self, id, ficha, horaI, horaF, fechaI, fechaF):
        self.__id = id
        self.__ficha = ficha
        self.__horaI = horaI
        self.__horaF = horaF
        self.__fechaI = fechaI
        self.__fechaF = fechaF
        self.__listaDiasLaborables = None
        self.__listaDiasAntesCruce = None
        self.__listaDiasLuegoCruce = None
        self.__listaDiasAProgramar = None
        self.__listaDiasPorProgram = None        
        self.__fichaYaProgramada = False

    @property
    def id(self):
        return self.__id
    @id.setter
    def evento(self, id):
        self.__id = id
        
    @property 
    def ficha(self): 
        return self.__ficha 
    @ficha.setter 
    def ficha(self, ficha): 
        self.__ficha = ficha 

    @property 
    def horaI(self): 
        return self.__horaI 
    @horaI.setter 
    def horaI(self, horaI): 
        self.__horaI = horaI

    @property 
    def horaF(self): 
        return self.__horaF 
    @horaF.setter 
    def horaF(self, horaF): 
        self.__horaF = horaF

    @property 
    def fechaI(self): 
        return self.__fechaI 
    @fechaI.setter 
    def fechaI(self, fechaI): 
        self.__fechaI = fechaI

    @property 
    def fechaF(self): 
        return self.__fechaF 
    @fechaF.setter 
    def fecahF(self, fechaF): 
        self.__fechaF = fechaF

    @property 
    def listaDiasLaborables(self): 
        return self.__listaDiasLaborables 
    @listaDiasLaborables.setter 
    def listaDiasLaborables(self, listaDiasLaborables): 
        self.__listaDiasLaborables = listaDiasLaborables

    @property 
    def listaDiasAntesCruce(self): 
        return self.__listaDiasAntesCruce 
    @listaDiasAntesCruce.setter 
    def listaDiasAntesCruce(self, listaDiasAntesCruce): 
        self.__listaDiasAntesCruce = listaDiasAntesCruce

    @property 
    def listaDiasLuegoCruce(self): 
        return self.__listaDiasLuegoCruce 
    @listaDiasLuegoCruce.setter 
    def listaDiasLuegoCruce(self, listaDiasLuegoCruce): 
        self.__listaDiasLuegoCruce = listaDiasLuegoCruce

    @property 
    def listaDiasAProgramar(self): 
        return self.__listaDiasAProgramar
    @listaDiasAProgramar.setter 
    def listaDiasAProgramar(self, listaDiasAProgramar): 
        self.__listaDiasAProgramar = listaDiasAProgramar

    @property 
    def listaDiasPorProgram(self): 
        return self.__listaDiasPorProgram
    @listaDiasPorProgram.setter 
    def listaDiasPorProgram(self, listaDiasPorProgram): 
        self.__listaDiasPorProgram = listaDiasPorProgram

    @property 
    def fichaYaProgramada(self): 
        return self.__fichaYaProgramada 
    @fichaYaProgramada.setter 
    def fichaYaProgramada(self, fichaYaProgramada): 
        self.__fichaYaProgramada = fichaYaProgramada

    def __str__(self):
        return f"evento: {self.id}, ficha: {self.ficha}, horas: [{self.horaI:2d} a {self.horaF:2d}] fechas: [{self.fechaI.day:2d} a {self.fechaF.day:2d}], \n dias laborables     : {self.listaDiasLaborables}, \n dias antes del cruce: {self.listaDiasAntesCruce}, \n dias luego del cruce: {self.listaDiasLuegoCruce}, \n dias a programar: {self.listaDiasAProgramar}, \n dias Por programar: {self.listaDiasPorProgram},\n la ficha ya esta programada: {self.fichaYaProgramada}"


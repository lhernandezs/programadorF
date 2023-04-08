from datetime import datetime

class Evento:
    def __init__(self):
        self._id = 0
        self._ficha = 0
        self._horaI = 0
        self._horaF = 0
        self._fechaI = None   
        self._fechaF = None
        self._listaDiasLaborables = None
        self._listaDiasAntesCruce = None
        self._listaDiasLuegoCruce = None
        self._listaDiasAProgramar = None
        self._fichaYaProgramada = False

    def __init__(self, id, ficha, horaI, horaF, fechaI, fechaF):
        self._id = id
        self._ficha = ficha
        self._horaI = horaI
        self._horaF = horaF
        self._fechaI = fechaI
        self._fechaF = fechaF
        self._listaDiasLaborables = None
        self._listaDiasAntesCruce = None
        self._listaDiasLuegoCruce = None
        self._listaDiasAProgramar = None
        self._fichaYaProgramada = False

    @property
    def id(self):
        return self._id
    @id.setter
    def evento(self, id):
        self._id = id
        
    @property 
    def ficha(self): 
        return self._ficha 
    @ficha.setter 
    def ficha(self, ficha): 
        self._ficha = ficha 

    @property 
    def horaI(self): 
        return self._horaI 
    @horaI.setter 
    def horaI(self, horaI): 
        self._horaI = horaI

    @property 
    def horaF(self): 
        return self._horaF 
    @horaF.setter 
    def horaF(self, horaF): 
        self._horaF = horaF

    @property 
    def fechaI(self): 
        return self._fechaI 
    @fechaI.setter 
    def fechaI(self, fechaI): 
        self._fechaI = fechaI

    @property 
    def fechaF(self): 
        return self._fechaF 
    @fechaF.setter 
    def fecahF(self, fechaF): 
        self._fechaF = fechaF

    @property 
    def listaDiasLaborables(self): 
        return self._listaDiasLaborables 
    @listaDiasLaborables.setter 
    def listaDiasLaborables(self, listaDiasLaborables): 
        self._listaDiasLaborables = listaDiasLaborables

    @property 
    def listaDiasAntesCruce(self): 
        return self._listaDiasAntesCruce 
    @listaDiasAntesCruce.setter 
    def listaDiasAntesCruce(self, listaDiasAntesCruce): 
        self._listaDiasAntesCruce = listaDiasAntesCruce

    @property 
    def listaDiasLuegoCruce(self): 
        return self._listaDiasLuegoCruce 
    @listaDiasLuegoCruce.setter 
    def listaDiasLuegoCruce(self, listaDiasLuegoCruce): 
        self._listaDiasLuegoCruce = listaDiasLuegoCruce

    @property 
    def listaDiasAProgramar(self): 
        return self._listaDiasAProgramar
    @listaDiasAProgramar.setter 
    def listaDiasAProgramar(self, listaDiasAProgramar): 
        self._listaDiasAProgramar = listaDiasAProgramar

    @property 
    def fichaYaProgramada(self): 
        return self._fichaYaProgramada 
    @fichaYaProgramada.setter 
    def fichaYaProgramada(self, fichaYaProgramada): 
        self._fichaYaProgramada = fichaYaProgramada

    def __str__(self):
        return f"evento: {self.id}, ficha: {self.ficha}, horas: [{self.horaI:2d} a {self.horaF:2d}] fechas: [{self.fechaI.day:2d} a {self.fechaF.day:2d}], \n dias laborables     : {self.listaDiasLaborables}, \n dias antes del cruce: {self.listaDiasAntesCruce}, \n dias luego del cruce: {self.listaDiasLuegoCruce}, \n dias a programar: {self.listaDiasAProgramar},\n la ficha ya esta programada: {self.fichaYaProgramada}"


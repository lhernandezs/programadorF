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
        dLa = self.listaDiasLaborables
        dAc = self.listaDiasAntesCruce
        dLc = self.listaDiasLuegoCruce
        dAp = self.listaDiasAProgramar if not self.listaDiasAProgramar is None else []
        dPp = self.listaDiasPorProgram if not self.listaDiasPorProgram is None else []
        diasLaborables = f"  {dLa[0]:2d} a {dLa[len(dLa)-1]:2d} " if len(dLa)> 0 else f"          "
        diasAntesCruce = f"  {dAc[0]:2d} a {dAc[len(dAc)-1]:2d} " if len(dAc)> 0 else f"          "
        diasLuegoCruce = f"  {dLc[0]:2d} a {dLc[len(dLc)-1]:2d} " if len(dLc)> 0 else f"          "
        diasAProgramar = f"  {dAp[0]:2d} a {dAp[len(dAp)-1]:2d} " if len(dAp)> 0 else f"          "
        diasPorProgram = f"  {dPp[0]:2d} a {dPp[len(dPp)-1]:2d} " if len(dPp)> 0 else f"          "

        return f"|    {self.id:2d}    |  {self.ficha:7d} |  {self.horaI:2d} - {self.horaF:2d} |  {self.fechaI.day:2d} a {self.fechaF.day:2d} |{diasLaborables}| {diasAntesCruce}|{diasLuegoCruce}|{diasAProgramar}|{diasPorProgram}|{'    Si    ' if self.fichaYaProgramada else '    No    '}|"


from datetime import datetime

class Evento:

    @classmethod
    def encabezado(cls):
        columnas = ["Evento", "Ficha", "Horas", "D In Fi", "D Labor", "D A NoD", "D L NoD", "D A Cruc", "D D Cruc", "D A Prog", "D P Prog", "Ya Prog", "H Programa"]
        encabez = "|"
        for nombreCol in columnas:
            encabez += nombreCol.center(10) + "|"
        return encabez

    def __init__(self, id, ficha, horaI, horaF, fechaI, fechaF):
        self.__id = id
        self.__ficha = ficha
        self.__horaI = horaI
        self.__horaF = horaF
        self.__fechaI = fechaI
        self.__fechaF = fechaF
        self.__listaDiasLaborables = []        
        self.__listaDiasAntesNoDis = []
        self.__listaDiasLuegoNoDis = []
        self.__listaDiasAntesCruce = []
        self.__listaDiasLuegoCruce = []
        self.__listaDiasAProgramar = []
        self.__listaDiasPorProgram = []  
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
    def listaDiasAntesNoDis(self): 
        return self.__listaDiasAntesNoDis 
    @listaDiasAntesNoDis.setter 
    def listaDiasAntesNoDis(self, listaDiasAntesNoDis): 
        self.__listaDiasAntesNoDis = listaDiasAntesNoDis

    @property 
    def listaDiasLuegoNoDis(self): 
        return self.__listaDiasLuegoNoDis 
    @listaDiasLuegoNoDis.setter 
    def listaDiasLuegoNoDis(self, listaDiasLuegoNoDis): 
        self.__listaDiasLuegoNoDis = listaDiasLuegoNoDis

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
        horas = (f"{self.horaI:2d} - {self.horaF:2d}").center(10)
        fechas = (f"{self.fechaI.day:2d} a {self.fechaF.day:2d}").center(10)

        cadenaVacia = " " * 10
        
        dLa = self.listaDiasLaborables
        dAn = self.listaDiasAntesNoDis
        dLn = self.listaDiasLuegoNoDis
        dAc = self.listaDiasAntesCruce
        dLc = self.listaDiasLuegoCruce
        dAp = self.listaDiasAProgramar
        dPp = self.listaDiasPorProgram

        diasLaborables = (f"{dLa[0]:2d} a {dLa[-1]:2d}").center(10) if dLa != [] else cadenaVacia
        diasAntesNoDis = (f"{dAn[0]:2d} a {dAn[-1]:2d}").center(10) if dAn != [] else cadenaVacia
        diasLuegoNoDis = (f"{dLn[0]:2d} a {dLn[-1]:2d}").center(10) if dLn != [] else cadenaVacia
        diasAntesCruce = (f"{dAc[0]:2d} a {dAc[-1]:2d}").center(10) if dAc != [] else cadenaVacia
        diasLuegoCruce = (f"{dLc[0]:2d} a {dLc[-1]:2d}").center(10) if dLc != [] else cadenaVacia
        diasAProgramar = (f"{dAp[0]:2d} a {dAp[-1]:2d}").center(10) if dAp != [] else cadenaVacia
        diasPorProgram = (f"{dPp[0]:2d} a {dPp[-1]:2d}").center(10) if dPp != [] else cadenaVacia

        si = "Si".center(10)
        no = "No".center(10)

        horasProgramadas = (self.horaF - self.horaI + 1) * len(dAp)

        return f"|{str(self.id).center(10)}|{str(self.ficha).center(10)}|{horas}|{fechas}|{diasLaborables}|{diasAntesNoDis}|{diasLuegoNoDis}|{diasAntesCruce}|{diasLuegoCruce}|{diasAProgramar}|{diasPorProgram}|{si if self.fichaYaProgramada else no}|{str(horasProgramadas).center(10)}|"
    


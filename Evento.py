from datetime import datetime, date   

class Evento:
    def __init__(self):
        self._ficha = 00000
        self._horaI = 0
        self._horaF = 0
        self._fechaI = None   
        self._fechaF = None
        self._fechaICruce = None
        self._fechaFCruce = None

    def __init__(self, ficha, horaI, horaF, fechaI, fechaF):
        self._ficha = ficha
        self._horaI = horaI
        self._horaF = horaF
        self._fechaI = fechaI
        self._fechaF = fechaF

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
    def fechaF(self, fechaF): 
        self._fechaF = fechaF  
    
    @property 
    def fechaICruce(self): 
        return self._fechaICruce  

    @fechaICruce.setter 
    def fechaICruce(self, fechaICruce): 
        self._fechaICruce = fechaICruce  

    @property 
    def fechaFCruce(self): 
        return self._fechaFCruce  

    @fechaFCruce.setter 
    def fechaFCruce(self, fechaFCruce): 
        self._fechaFCruce = fechaFCruce   
    
    def __str__(self):
        return f"ficha: {self._ficha}, horaI: {self._horaI:2d}, horaF: {self._horaF:2d}, fechaI: {self._fechaI}, fechaF: {self._fechaF}, fechaICruce: {str(self._fechaICruce).ljust(10, ' ')}, fechaFCruce: {str(self._fechaFCruce).ljust(10,' ')}"
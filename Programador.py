from Mes import Mes
from Evento import Evento
from datetime import date

class Programador:
    # constructor de la clase
    def __init__(self, listaEventos, mes, horasAProgramar, tolerancia):
        self._listaEventos = listaEventos
        self._mes = mes
        self._horasAProgramar = horasAProgramar
        self._tolerancia = tolerancia
        self._promedioHorasPorFicha = self._horasAProgramar // len (self.listaFichas())
        self._minimoHorasAProgramarPorFicha = self._promedioHorasPorFicha * (1-(self._tolerancia/100))
        self._maximoHorasAProgramarPorFicha = self._promedioHorasPorFicha * (1+(self._tolerancia/100))
        self._matrizDeEventosPorDiaHora = None
        self._saldoDeHorasAProgramar = horasAProgramar
        self._ultimaFecMes = Mes(self._mes).ultimoDia()
        self._diasDelMes = self._ultimaFecMes.day
        self._listaDiasLaborablesMes = Mes(self._mes).listaDiasLaborables()

    # retorna True si el evento está en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, x, y):
        fecha = date(2023, self._mes, x)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= y and y < evento.horaF else False
    
    # devuelve una lista de eventos sin programar
    def listaEventosSinProgramar(self):
        return list(filter(lambda e: not e._fichaYaProgramada ,self._listaEventos))

    # setea la matriz de los eventos sin programar por cada dia y la hora del mes  
    def matrizEventosPorDiaHora(self):
        matrizDeEventosPorDiaHora = [[[] for j in range(24)] for i in range(self._diasDelMes)]
        for evento in self.listaEventosSinProgramar():
            for i in range(self._diasDelMes):
                for j in range(24):
                    if self.estaElEventoEnDiaHora(evento, i+1, j) and i+1 in self._listaDiasLaborablesMes:
                        matrizDeEventosPorDiaHora[i][j].append(evento.id)
        self._matrizDeEventosPorDiaHora = matrizDeEventosPorDiaHora  

    # setea las listas de dias laborables, dias antes de cruce y dias luego de cruce de los eventos sin programar   
    def analisisDiasEventos(self):
        self.matrizEventosPorDiaHora()
        conjuntoDiasLaborablesMes = set(self._listaDiasLaborablesMes)
        for evento in self.listaEventosSinProgramar():
            diaIniEvento = 1 if (evento.fechaI < date(2023, self._mes, 1)) else evento.fechaI.day
            diaFinEvento = self._diasDelMes if (self._ultimaFecMes < evento.fechaF) else evento.fechaF.day
            listaDiasIniFinEvento = [dia for dia in range(diaIniEvento, diaFinEvento+1)]
            fecIniCruce = fecFinCruce = None
            for i in range(self._diasDelMes):
                for j in range(24):
                    if len(self._matrizDeEventosPorDiaHora[i][j]) > 1 and evento.id in self._matrizDeEventosPorDiaHora[i][j]:
                        if fecIniCruce is None or date(2023, self._mes, i+1) < fecIniCruce: fecIniCruce = date(2023, self._mes, i+1)
                        if fecFinCruce is None or date(2023, self._mes, i+1) > fecFinCruce: fecFinCruce = date(2023, self._mes, i+1)
            listaDiasAntesDeCruce = listaDiasIniFinEvento if fecIniCruce is None else [x for x in range(diaIniEvento, fecIniCruce.day)] 
            listaDiasLuegoDeCruce = [] if fecFinCruce is None else [x for x in range(fecFinCruce.day+1, diaFinEvento)]

            self._listaEventos[evento.id].listaDiasLaborables = list(set(listaDiasIniFinEvento) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasAntesCruce = list(set(listaDiasAntesDeCruce) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasLuegoCruce = list(set(listaDiasLuegoDeCruce) & conjuntoDiasLaborablesMes)
    
    # retorna la lista de las fichas
    def listaFichas(self):        
        return list(set([evento.ficha for evento in self._listaEventos]))

    # 1. iterar
    #   se asigna horas en los eventos que tengan dias antes o luego del cruce suficientes para cumplir entre el -x% y +x% del promedio de horas por ficha
    #   si es posible el paso anterior, la ficha queda programada, se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
    #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas 
    def programarEventosSinCruces(self):
        bandera = True
        while bandera:
            bandera = False
            self.analisisDiasEventos()
            for evento in self.listaEventosSinProgramar():
                horasEvento = evento.horaF - evento.horaI 
                listaDiasMasLarga =  evento.listaDiasAntesCruce if len(evento.listaDiasAntesCruce) > len(evento.listaDiasLuegoCruce) else evento.listaDiasLuegoCruce
                if (horasEvento * len(listaDiasMasLarga)) > self._minimoHorasAProgramarPorFicha:
                    bandera = True
                    listaDiasAProgramar = []
                    horasCargadasEnEvento = 0
                    for dia in listaDiasMasLarga:
                        if horasCargadasEnEvento < self._maximoHorasAProgramarPorFicha and self._saldoDeHorasAProgramar > 0:
                            listaDiasAProgramar.append(dia)
                            horasCargadasEnEvento += horasEvento
                            self._saldoDeHorasAProgramar -= horasEvento
                        else:
                            break
                    for eve in self._listaEventos:
                        if evento.ficha == eve.ficha:
                            self._listaEventos[eve.id].fichaYaProgramada = True
                    self._listaEventos[evento.id].listaDiasAProgramar = listaDiasAProgramar

        # 2. iterar
        #   se resuelven los cruces priorizando los eventos en que se pueda asignar entre el -20% y +20% del promedio de horas por ficha. 
        #   se retiran todos los eventos de la ficha en la matriz y se baja el numero de horas a programar
        #   se ejecuta toda el ciclo 2.
        #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas
        
# principal 
listaEventos = [ \
Evento(0, 1, 6, 8, date(2023,4,1), date(2023,4,30)), \
Evento(1, 1, 10, 11, date(2023,4,9), date(2023,4,20)), \
Evento(2, 2, 6, 7, date(2023,4,10), date(2023,4,26)), \
Evento(3, 2, 8, 9, date(2023,4,1), date(2023,4,28)), \
Evento(4, 3, 9, 11, date(2023,4,1), date(2023,4,23)), \
Evento(5, 3, 12, 13, date(2023,4,10), date(2023,4,28)), \
]

programador = Programador(listaEventos, 4, 60, 50)
programador.programarEventosSinCruces()

for evento in programador._listaEventos:
    print(evento)
print(programador._saldoDeHorasAProgramar)
#print(programador.listaFichas())
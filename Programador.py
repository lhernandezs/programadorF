from Mes import Mes
from Evento import Evento
from datetime import date

class Programador:
    # constructor de la clase
    def __init__(self, listaEventos, mes, horasAProgramar, tolerancia):
        self._listaEventos = listaEventos
        self._diccionarioFichas = dict.fromkeys([evento.ficha for evento in self._listaEventos], 0)
        self._mes = mes
        self._horasAProgramar = horasAProgramar
        self._tolerancia = tolerancia
        self._promedioHorasPorFicha = self._horasAProgramar // len(self._diccionarioFichas)
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
        return list(filter(lambda e: e.listaDiasAProgramar is None and not e.fichaYaProgramada ,self._listaEventos))

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
    
    # filtra los todos los eventos que tiene la misma ficha y coloca en True el atributo fichaYaProgramada
    def marcarEventosDeLaFichaYaProgramada(self, evento):
        todosLosEventosDeLaFicha = list(filter(lambda e: evento.ficha == e.ficha, [e for e in self._listaEventos]))
        for e in todosLosEventosDeLaFicha:
            self._listaEventos[e.id]._fichaYaProgramada = True

    # El mejor evento programable es: 1. tiene la capacidad mas grande descontando los cruces 2. en caso de empate, tiene horas mas temprano. 3. 
    # Si se acaban los eventos programables sin cruce se revisan los eventos que tengan dos cruces solamente...... - en contruccion ---    
    # Todos los eventos programables deben tener capacidad de al menos el 50% del monimo de horas a programar por ficha
    def buscarMejorEventoProgramable(self):
        eventosProgramables = []
        listaEventosSinProgramar = list(filter(lambda e: not e.fichaYaProgramada and e.listaDiasAProgramar is None, [e for e in self._listaEventos]))
        for evento in listaEventosSinProgramar:
            horasEvento = evento.horaF - evento.horaI 
            listaDiasMasLarga =  evento.listaDiasAntesCruce if len(evento.listaDiasAntesCruce) > len(evento.listaDiasLuegoCruce) else evento.listaDiasLuegoCruce
            capacidad = horasEvento * len(listaDiasMasLarga)
            if capacidad >= self._minimoHorasAProgramarPorFicha // 2:
                eventosProgramables.append((evento.id, capacidad, evento.horaI, listaDiasMasLarga, horasEvento))
        if len(eventosProgramables) > 0:
            return (self._listaEventos[sorted(sorted(eventosProgramables, key=lambda x: x[2]), key=lambda x: -x[1])[0][0]], eventosProgramables[0][1], eventosProgramables[0][2], eventosProgramables[0][3], eventosProgramables[0][4])
        else:
            # se procesan los eventos que comparten con solo otro evento en el cruce. -- en construcion
            return None

    # 1. iterar
    #   se asigna horas al mejor evento programable
    #   si la ficha queda programada ( al menos el minimo de horas a progrmara por ficha), se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
    #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas 
    def programarEventos(self):
        # Eventos Programables son los que tienen capacidad de al menos el 50% de las horas a Programar por Ficha de las Fichas No Programadas.
        self.analisisDiasEventos()
        mejorEventoProgramable = self.buscarMejorEventoProgramable()
        while mejorEventoProgramable:
            listaDiasAProgramar = []
            for dia in mejorEventoProgramable[3]:
                if  self._saldoDeHorasAProgramar in range(mejorEventoProgramable[4]) or \
                    (self._maximoHorasAProgramarPorFicha - self._diccionarioFichas[mejorEventoProgramable[0].ficha]) in range(mejorEventoProgramable[4]):
                    self.marcarEventosDeLaFichaYaProgramada(mejorEventoProgramable)
                    break                        
                else:                        
                    listaDiasAProgramar.append(dia)
                    self._saldoDeHorasAProgramar -= mejorEventoProgramable[4]
                    self._diccionarioFichas[mejorEventoProgramable[0].ficha] += mejorEventoProgramable[4]              
            self._listaEventos[mejorEventoProgramable[0].id].listaDiasAProgramar = listaDiasAProgramar
            self.analisisDiasEventos()
            mejorEventoProgramable = self.buscarMejorEventoProgramable()
        # bandera = True
        # while bandera:
        #     bandera = False
        #     self.analisisDiasEventos()
        #     for evento in self.listaEventosSinProgramar():
        #         horasEvento = evento.horaF - evento.horaI 
        #         listaDiasMasLarga =  evento.listaDiasAntesCruce if len(evento.listaDiasAntesCruce) > len(evento.listaDiasLuegoCruce) else evento.listaDiasLuegoCruce
        #         # caso donde con un solo evento se puede programar la ficha dentro del rago de tolerancia de horas a programar por ficha
        #         if (horasEvento * len(listaDiasMasLarga)) > self._minimoHorasAProgramarPorFicha:
        #             bandera = True
        #             listaDiasAProgramar = []
        #             horasProgramadasEnEvento = 0
        #             for dia in listaDiasMasLarga:
        #                 if horasProgramadasEnEvento < self._maximoHorasAProgramarPorFicha and self._saldoDeHorasAProgramar > 0:
        #                     listaDiasAProgramar.append(dia)
        #                     horasProgramadasEnEvento += horasEvento
        #                     self._saldoDeHorasAProgramar -= horasEvento
        #                 else:
        #                     break
        #             self._listaEventos[evento.id].listaDiasAProgramar = listaDiasAProgramar
        #             self.marcarEventosDeLaFichaYaProgramada(evento)

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
programador.programarEventos()

for evento in programador._listaEventos:
    print(evento)
print(programador._saldoDeHorasAProgramar)
print(programador._diccionarioFichas)
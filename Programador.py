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
        self._matrizDeEventos = None
        self._saldoDeHorasAProgramar = horasAProgramar
        self._ultimaFecMes = Mes(self._mes).ultimoDia()
        self._diasDelMes = self._ultimaFecMes.day
        self._listaDiasLaborablesMes = Mes(self._mes).listaDiasLaborables()

    # retorna True si el evento está en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, dia, hora):
        fecha = date(2023, self._mes, dia)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= hora and hora < evento.horaF else False
    
    # devuelve la lista de eventos sin programar
    def listaEventosSinProgramar(self):
        return list(filter(lambda evento: evento.listaDiasAProgramar is None and not evento.fichaYaProgramada ,self._listaEventos))

    # setea la matriz de los eventos sin programar por cada dia y la hora del mes  
    def matrizDeEventos(self):
        matrizDeEventos = [[[] for h in range(24)] for d in range(self._diasDelMes)]
        for evento in self.listaEventosSinProgramar():
            for d in range(self._diasDelMes):
                for h in range(24):
                    if self.estaElEventoEnDiaHora(evento, d+1, h) and d+1 in self._listaDiasLaborablesMes:
                        matrizDeEventos[d][h].append(evento.id)
        self._matrizDeEventos = matrizDeEventos  

    # setea las listas de dias laborables, dias antes de cruce y dias luego de cruce de los eventos sin programar   
    def analisisDiasEventos(self):
        self.matrizDeEventos()
        conjuntoDiasLaborablesMes = set(self._listaDiasLaborablesMes)
        for evento in self.listaEventosSinProgramar():
            diaIniEvento = 1 if (evento.fechaI < date(2023, self._mes, 1)) else evento.fechaI.day
            diaFinEvento = self._diasDelMes if (self._ultimaFecMes < evento.fechaF) else evento.fechaF.day
            listaDiasIniFinEvento = [dia for dia in range(diaIniEvento, diaFinEvento+1)]
            fecIniCruce = fecFinCruce = None
            for d in range(self._diasDelMes):
                for h in range(24):
                    if len(self._matrizDeEventos[d][h]) > 1 and evento.id in self._matrizDeEventos[d][h]:
                        if fecIniCruce is None or date(2023, self._mes, d+1) < fecIniCruce: fecIniCruce = date(2023, self._mes, d+1)
                        if fecFinCruce is None or date(2023, self._mes, d+1) > fecFinCruce: fecFinCruce = date(2023, self._mes, d+1)
            listaDiasAntesDeCruce = listaDiasIniFinEvento if fecIniCruce is None else [x for x in range(diaIniEvento, fecIniCruce.day)] 
            listaDiasLuegoDeCruce = [] if fecFinCruce is None else [x for x in range(fecFinCruce.day+1, diaFinEvento)]

            self._listaEventos[evento.id].listaDiasLaborables = list(set(listaDiasIniFinEvento) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasAntesCruce = list(set(listaDiasAntesDeCruce) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasLuegoCruce = list(set(listaDiasLuegoDeCruce) & conjuntoDiasLaborablesMes)
    
    # filtra los todos los eventos que tiene la misma ficha y coloca en True el atributo fichaYaProgramada
    def marcarEventosDeLaFichaProgramada(self, evento):
        todosLosEventosDeLaFicha = list(filter(lambda even: evento.ficha == even.ficha, self._listaEventos))
        for e in todosLosEventosDeLaFicha:
            self._listaEventos[e.id]._fichaYaProgramada = True

    # El mejor evento programable es: 1. tiene la capacidad mas grande descontando los cruces 2. en caso de empate, tiene la hora de inicio mas temprano. 3. 
    # Si se acaban los eventos programables sin cruce se revisan los eventos que tengan dos cruces solamente...... - en contruccion ---    
    # Nota: todos los eventos programables deben tener capacidad de al menos el 50% del monimo de horas a programar por ficha
    def buscarMejorEventoProgramable(self):
        eventosProgramables = []
        for evento in self.listaEventosSinProgramar():
            horasEvento = evento.horaF - evento.horaI 
            listaDiasMasLarga = evento.listaDiasAntesCruce if len(evento.listaDiasAntesCruce) > len(evento.listaDiasLuegoCruce) else evento.listaDiasLuegoCruce
            capacidad = horasEvento * len(listaDiasMasLarga)
            if capacidad >= self._minimoHorasAProgramarPorFicha // 2:
                eventosProgramables.append((evento, capacidad, evento.horaI, listaDiasMasLarga, horasEvento))
        if len(eventosProgramables) > 0:
            eventosProgramablesOrdenados = sorted(sorted(eventosProgramables, key=lambda x: x[2]), key=lambda x: -x[1])
            return eventosProgramables[0] 
        else:
            # se procesan los eventos que comparten con solo otro evento en el cruce. -- en construcion
            return None

    # 1. iterar
    #   se asignan horas al mejor evento programable
    #   si la ficha queda programada (al menos el minimo de horas a programar por ficha), se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
    #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas 
    def programarEventos(self):
        # Eventos Programables son los que tienen capacidad de al menos el 50% de las horas a Programar por Ficha de las Fichas No Programadas.
        self.analisisDiasEventos()
        mejorEventoProgramable = self.buscarMejorEventoProgramable()
        while mejorEventoProgramable:
            listaDiasAProgramar = []
            for dia in mejorEventoProgramable[3]:
                saldoDeHorasAProgramarDeLaFicha = self._minimoHorasAProgramarPorFicha - self._diccionarioFichas[mejorEventoProgramable[0].ficha]
                if  self._saldoDeHorasAProgramar < mejorEventoProgramable[4] or saldoDeHorasAProgramarDeLaFicha < mejorEventoProgramable[4]:
                    self.marcarEventosDeLaFichaProgramada(mejorEventoProgramable[0])
                    break                        
                else:                        
                    listaDiasAProgramar.append(dia)
                    self._saldoDeHorasAProgramar -= mejorEventoProgramable[4]
                    self._diccionarioFichas[mejorEventoProgramable[0].ficha] += mejorEventoProgramable[4]              
            self._listaEventos[mejorEventoProgramable[0].id].listaDiasAProgramar = listaDiasAProgramar
            self.analisisDiasEventos()
            mejorEventoProgramable = self.buscarMejorEventoProgramable()

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

programador = Programador(listaEventos, 4, 60, 15)
programador.programarEventos()

for evento in programador._listaEventos:
    print(evento)
print(programador._saldoDeHorasAProgramar)
print(programador._diccionarioFichas)
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
        self._ultimaFecMes = Mes(self._mes).ultimoDia()
        self._diasDelMes = self._ultimaFecMes.day
        self._listaDiasLaborablesMes = Mes(self._mes).listaDiasLaborables()
        self._matrizDeEventos = self.matrizDeEventos()
        self._saldoDeHorasAProgramar = horasAProgramar

    # retorna True si el evento está en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, dia, hora):
        fecha = date(2023, self._mes, dia)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= hora and hora < evento.horaF else False
    
    # devuelve la lista de eventos sin programar
    def listaEventosSinProgramar(self):
        return list(filter(lambda evento: evento.listaDiasAProgramar is None and not evento.fichaYaProgramada, self._listaEventos))

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
    
    # setea en True el atributo fichaYaProgramada de todos los eventos que tiene la misma ficha el evento
    def marcarEventosDeLaFichaProgramada(self, evento):
        lista = list(filter(lambda e: evento.ficha == e.ficha, self._listaEventos))
    #    map(lambda e: e.fichaYaProgramada(True), lista)
        for e in lista:
            e.fichaYaProgramada = True

    # recibe un evento y un boleano que indica si el evento esta cruzado o no
    # devuelve una tupla con el evento, la capacidad de horas a programar en el evento, la lista mas larga de dias programables y la duracion en horas
    def capacidadEvento(self, evento, cruzado):
        horasEvento = evento.horaF - evento.horaI
        if cruzado:
            listaDias = evento.listaDiasLaborables
            capacidad = horasEvento * len(evento.listaDiasLaborables)
            return (evento, capacidad, listaDias, horasEvento)
        else:
            listaDias = lA if len(lA := evento.listaDiasAntesCruce) > len(lL := evento.listaDiasLuegoCruce) else lL
            capacidad = horasEvento * len(listaDias)
            return (capacidad, listaDias, horasEvento)
    
    # devuelve True si la capacidad del evento es al menos el 50% del mínimo de horas a programar por ficha o False en caso contrario
    def tieneCapacidadMinima(self, capacidad):
        return True if capacidad >= self._minimoHorasAProgramarPorFicha // 2 else False
    
    # devuelve el evento, la lista de dias a programar y las horas del mejor evento programable, que se define: 
    # 1. Tiene la capacidad mas grande revisando las lista de dias que no se cruzan; en caso de empate, tiene la hora de inicio mas temprano. 
    # 2. Si se acaban los eventos anteriores, se revisan los eventos cruzados de menos a mas cardinalidad.   
    def buscarMejorEventoProgramable(self):
        eventosProgramables = [] # 1.
        for evento in self.listaEventosSinProgramar():
            (capacidad, listaDias, horasEvento) = self.capacidadEvento(evento, False)
            eventosProgramables.append((evento, capacidad, evento.horaI, listaDias, horasEvento)) if self.tieneCapacidadMinima(capacidad) else None                
        if len(eventosProgramables) > 0:
            (evento, capacidad, horaI, listaDias, horasEvento) = (list(sorted(sorted(eventosProgramables, key=lambda x: x[2]), key=lambda x: -x[1])))[0]
            return (evento, listaDias, horasEvento)
        else:
            # 2.
            for l in range(2, len(self._listaEventos)):
                listaDeEventosCruzados = list(filter(lambda item: len(item) == l, [self._matrizDeEventos[i][j] for j in range(24) for i in range(self._diasDelMes)]))
                if listaDeEventosCruzados:
                    cruceMasRepetido = max(listaDeEventosCruzados, key=listaDeEventosCruzados.count)
                    listaTuplas = []
                    for id in cruceMasRepetido:
                        listaTuplas.append(self.capacidadEvento(self._listaEventos[id], True))
                    (evento, capacidad, listaDias, horasEvento)= (list(sorted(listaTuplas, key=lambda t: -t[1])))[0]
                    return (evento, listaDias, horasEvento)
                else:
                    return (None, None, None)

    # 1. iterar
    #   se asignan horas al mejor evento programable
    #   si la ficha queda programada (al menos el minimo de horas a programar por ficha), se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
    #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas 
    # 2.
    def programarEventos(self):
        self.analisisDiasEventos() # 1.
        (evento, listaDias, horasEvento) = self.buscarMejorEventoProgramable()
        while evento:
            listaDiasAProgramar = []
            for dia in listaDias:
                saldoDeHorasAProgramarDeLaFicha = self._minimoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                if  self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento:
                    self.marcarEventosDeLaFichaProgramada(evento)
                    break                        
                else:                        
                    listaDiasAProgramar.append(dia)
                    self._saldoDeHorasAProgramar -= horasEvento
                    self._diccionarioFichas[evento.ficha] += horasEvento
                    saldoDeHorasAProgramarDeLaFicha = self._minimoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                    if  self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento:
                        self.marcarEventosDeLaFichaProgramada(evento)           
            evento.listaDiasAProgramar = listaDiasAProgramar
            evento.listaDiasPorProgram = list(set(listaDias) - set(listaDiasAProgramar)) if len(listaDias) != len(listaDiasAProgramar) else []
            self.analisisDiasEventos()
            (evento, listaDias, horasEvento) = self.buscarMejorEventoProgramable()
        for evento in list(filter(lambda e: not e.listaDiasPorProgram is None, self._listaEventos)):
            listaDiasPorProgramar = evento.listaDiasPorProgram[:]
            for dia in listaDiasPorProgramar:
                horasEvento = evento.horaF - evento.horaI
                saldoDeHorasAProgramarDeLaFicha = self._maximoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                if  not (self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento):
                    evento.listaDiasAProgramar.append(dia)
                    evento.listaDiasPorProgram.remove(dia)
                    self._saldoDeHorasAProgramar -= horasEvento
                    self._diccionarioFichas[evento.ficha] += horasEvento
        
# principal 
listaEventos = [ \
Evento(0, 1, 6, 8, date(2023,4,1), date(2023,4,30)), \
Evento(1, 1, 10, 11, date(2023,4,9), date(2023,4,20)), \
Evento(2, 2, 6, 7, date(2023,4,10), date(2023,4,26)), \
Evento(3, 2, 8, 9, date(2023,4,1), date(2023,4,28)), \
Evento(4, 3, 9, 11, date(2023,4,1), date(2023,4,23)), \
Evento(5, 3, 12, 13, date(2023,4,10), date(2023,4,28)), \
]

programador = Programador(listaEventos, 4, 160, 30)
programador.programarEventos()
print()
print(f"  H a programar: {programador._horasAProgramar} - H por Programar:{programador._saldoDeHorasAProgramar:3d} - Dicionario: {programador._diccionarioFichas}  - Mes: {programador._mes}  - Tolerancia: {programador._tolerancia}%" )
print(" -------------------------------------------------------------------------------------------------------------- ")
print("|  Evento  |   Ficha  |   Horas   |  D In Fi | D labor  | D A Cruz | D L Cruz | D A Prog | D P Prog | Ya Progr | ")
print(" -------------------------------------------------------------------------------------------------------------- ")
for evento in programador._listaEventos:
    print(evento)
    print(" -------------------------------------------------------------------------------------------------------------- ")
print()
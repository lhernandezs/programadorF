from Evento import Evento
from Mes import Mes
from datetime import datetime, timedelta, date

class Programador:
    # constructor de la clase
    def __init__(self, listaEventos, mes, horasAProgramar):
        self._listaEventos = listaEventos
        self._mes = mes
        self._horasAProgramar = horasAProgramar

    # retorna True si el evento está en el Dia y la Hora pasado como parametros o False en caso contrario
    def eventoEnDiaHora(self, evento, x, y):
        fecha = date(2023, self._mes, x)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= y and y < evento.horaF else False

    # retorna una Matriz de los eventos en cada dia y la hora del mes    
    def eventosPorDiaHora(self):
        diasDelMes = Mes(self._mes).ultimoDia().day
        eventosPorDiaHora = [[[] for j in range(24)] for i in range(diasDelMes)]
        for e in range(len(self._listaEventos)):
            for i in range(diasDelMes):
                for j in range(24):
                    if self.eventoEnDiaHora(self._listaEventos[e], i+1, j) and i+1 in Mes(self._mes).listaDiasLaborables():
                        eventosPorDiaHora[i][j].append(e)
        return eventosPorDiaHora

    # retorna una arreglo con tres listas: [0]dias Laborales del evento, [1]dias laborables evento antes de cruce
    #[2]dias laboralbes eventos despues de cruce
    def listaDiasLaborablesEvento(self, evento):
        diaInicio = 1 if (evento.fechaI < Mes(self._mes).primerDia()) else evento.fechaI.day
        diaFin = Mes(self._mes).ultimoDia().day if (Mes(self._mes).ultimoDia() < evento.fechaF) else evento.fechaF.day
        return [list(set([x for x in range(diaInicio, diaFin+1)]) & set(Mes(self._mes).listaDiasLaborables())),
                list(set([] if evento.fechaICruce is None else [x for x in range(diaInicio, evento.fechaICruce.day)]) & set(Mes(self._mes).listaDiasLaborables())),
                list(set([] if evento.fechaFCruce is None else [x for x in range(evento.fechaFCruce.day, diaFin)]) & set(Mes(self._mes).listaDiasLaborables()))]
    
    # retorna la capacidad en horas brutas y horas cruzadas de un evento y setea la fecha Inicial y Final de cruces del evento   
    def horasProgramablesEvento(self, e):
        horasCruzadasBrutas = horasCruzadasNetas = horasCruzadasNetasIniciales = horasCruzadasNetasFinales = 0
        eventosPorDiaHora = self.eventosPorDiaHora()
        diaMinCruce = diaMaxCruce = None
        for i in range(Mes(self._mes).ultimoDia().day):
            for j in range(24):
                if e in eventosPorDiaHora[i][j] and len(eventosPorDiaHora[i][j]) > 1:
                    horasCruzadasBrutas += 1
                    if diaMinCruce is None or date(2023, self._mes, i+1) < diaMinCruce: diaMinCruce = date(2023, self._mes, i+1)
                    if diaMaxCruce is None or date(2023, self._mes, i+1) > diaMaxCruce: diaMaxCruce = date(2023, self._mes, i+1)
        self._listaEventos[e].fechaICruce = diaMinCruce
        self._listaEventos[e].fechaFCruce = diaMaxCruce
        horasDelEvento = self._listaEventos[e].horaF - self._listaEventos[e].horaI
        return { \
            "ficha": (self._listaEventos[e].ficha), \
            "horasBrutas" : horasDelEvento * len(self.listaDiasLaborablesEvento(self._listaEventos[e])[0]), \
            "horasCruzadasBrutas" : horasCruzadasBrutas, \
            "horasNoCruzadasNetasIniciales" : horasDelEvento * len(self.listaDiasLaborablesEvento(self._listaEventos[e])[1]), \
            "horasNoCruzadasNetasFinales" : horasDelEvento * len(self.listaDiasLaborablesEvento(self._listaEventos[e])[2]) \
        }
    
    # retorna un diccionario de las fichas con sus respectivos datos de horas brutas y horas cruzadas 
    def horasProgramablesFicha(self):        
        listaFichas = list(set([evento.ficha for evento in self._listaEventos]))
        horasPorFicha = {}
        for ficha in listaFichas:
            horasPorFicha[ficha] = [0,0,0,0]
        for e in range(len(self._listaEventos)):            
            horasEvento = self.horasProgramablesEvento(e)
            print(f"evento {e:2d}: horas brutas: {horasEvento['horasBrutas']:2d}, horas cruzadas brutas: {horasEvento['horasCruzadasBrutas']:2d}, horas no cruzadas netas iniciales : {horasEvento['horasNoCruzadasNetasIniciales']:2d}, horas no cruzadas netas finales : {horasEvento['horasNoCruzadasNetasFinales']:2d},")
            horasPorFicha[horasEvento['ficha']][0] += horasEvento['horasBrutas']  
            horasPorFicha[horasEvento['ficha']][1] += horasEvento['horasCruzadasBrutas']
            horasPorFicha[horasEvento['ficha']][2] += horasEvento['horasNoCruzadasNetasIniciales']
            horasPorFicha[horasEvento['ficha']][3] += horasEvento['horasNoCruzadasNetasFinales']
        return horasPorFicha

    # Presenta en consola el resultado de la programacion    
    def resultado(self):
        eventosPorDiaHora = self.eventosPorDiaHora()    
        for i in range(Mes(self._mes).ultimoDia().day):
            for j in range(24):
                if len(eventosPorDiaHora[i][j]) > 0:
                    print(f"[dia: {i+1:2d}, horas: {j:2d} a {j+1:2d}]...Eventos:", eventosPorDiaHora[i][j])
        print("****************")
        print(self.horasProgramablesFicha())
        for evento in listaEventos:
            print(evento)
        
# principal       
evento0 = Evento(2675758, 6, 7, date(2023,4,1), date(2023,4,30))
evento1 = Evento(2675759, 7, 8, date(2023,4,1), date(2023,4,30))
evento2 = Evento(2626937, 12, 14, date(2023,4,1), date(2023,4,30))
evento3 = Evento(2626938, 7, 9, date(2023,4,1), date(2023,4,30))
evento4 = Evento(2626939, 9, 11, date(2023,4,1), date(2023,4,30))
evento5 = Evento(2626940, 7, 8, date(2023,4,1), date(2023,4,30))
evento6 = Evento(2675911, 12, 13, date(2023,4,1), date(2023,4,30))
evento7 = Evento(2675912, 20, 22, date(2023,4,1), date(2023,4,30))
evento8 = Evento(2675758, 13, 16, date(2023,4,1), date(2023,4,30))
evento9 = Evento(2675759, 0, 0, date(2023,4,1), date(2023,4,30))
evento10 = Evento(2626937, 22, 23, date(2023,4,1), date(2023,4,30))
evento11 = Evento(2626938, 6, 7, date(2023,4,1), date(2023,4,30))
evento12 = Evento(2626939, 8, 9, date(2023,4,1), date(2023,4,30))
evento13 = Evento(2626940, 8, 10, date(2023,4,1), date(2023,4,30))
evento14 = Evento(2675911, 6, 7, date(2023,4,1), date(2023,4,30))
evento15 = Evento(2675912, 0, 0, date(2023,4,1), date(2023,4,30))

#listaEventos = [evento0]
#listaEventos = [evento0, evento1, evento2]
#listaEventos = [evento0, evento1, evento2, evento3]
listaEventos = [evento0, evento1, evento2, evento3, evento4, evento5, evento6, evento7, evento8, evento9, evento10, evento11, evento12, evento13, evento14, evento15]

programador = Programador(listaEventos, 4, 160)
programador.resultado()
from Evento import Evento
from Mes import Mes
from datetime import datetime, timedelta, date
import pprint

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

    # retorna una arreglo con tres listas: [0] dias Laborales del evento, [1] dias laborables del evento antes de cruce
    #[2] dias laborables del evento despues de cruce
    def listaDiasLaborablesEvento(self, evento):
        diaInicio = 1 if (evento.fechaI < Mes(self._mes).primerDia()) else evento.fechaI.day
        diaFin = Mes(self._mes).ultimoDia().day if (Mes(self._mes).ultimoDia() < evento.fechaF) else evento.fechaF.day
        listaDiasInicioFinEvento = [x for x in range(diaInicio, diaFin+1)]
        listaDiasAntesDeCruce = listaDiasInicioFinEvento if evento.fechaICruce is None else [x for x in range(diaInicio, evento.fechaICruce.day)] 
        listaDiasDespuesDeCruce = [] if evento.fechaFCruce is None else [x for x in range(evento.fechaFCruce.day+1, diaFin)]
        return [list(set(listaDiasInicioFinEvento) & set(Mes(self._mes).listaDiasLaborables())),
                list(set(listaDiasAntesDeCruce) & set(Mes(self._mes).listaDiasLaborables())),
                list(set(listaDiasDespuesDeCruce) & set(Mes(self._mes).listaDiasLaborables()))]
    
    # retorna la capacidad en horas brutas y horas cruzadas de un evento y setea la fecha Inicial y Final de cruces del evento   
    def horasProgramablesEvento(self, e):
        horasCruzadasBrutas = 0
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
            "horasNoCruzadasNetasI" : horasDelEvento * len(self.listaDiasLaborablesEvento(self._listaEventos[e])[1]), \
            "horasNoCruzadasNetasF" : horasDelEvento * len(self.listaDiasLaborablesEvento(self._listaEventos[e])[2]) \
        }
    
    # retorna un diccionario de las fichas con sus respectivos datos de horas brutas y horas cruzadas 
    def horasProgramablesFicha(self):        
        listaFichas = list(set([evento.ficha for evento in self._listaEventos]))
        horasPorFicha = {}
        for ficha in listaFichas:
            horasPorFicha[ficha] = [0,0,0,0]
        for e in range(len(self._listaEventos)):            
            horasEvento = self.horasProgramablesEvento(e)
            horasPorFicha[horasEvento['ficha']][0] += horasEvento['horasBrutas']  
            horasPorFicha[horasEvento['ficha']][1] += horasEvento['horasCruzadasBrutas']
            horasPorFicha[horasEvento['ficha']][2] += horasEvento['horasNoCruzadasNetasI']
            horasPorFicha[horasEvento['ficha']][3] += horasEvento['horasNoCruzadasNetasF']
        return horasPorFicha

    # Presenta en consola el resultado de la programacion    
    def resultado(self):
        eventosPorDiaHora = self.eventosPorDiaHora()   
        for i in range(Mes(self._mes).ultimoDia().day):
            for j in range(24):
                if len(eventosPorDiaHora[i][j]) > 1:
                    print(f"[dia: {i+1:2d}, horas: {j:2d} a {j+1:2d}]...Eventos:", eventosPorDiaHora[i][j])
        print("****************")
        
        dhpf = self.horasProgramablesFicha() 
        for e in  dhpf:
            print(f"ficha: {e}, H_brutas: {dhpf[e][0]:2d}, H_N_C_I: {dhpf[e][1]:2d}, H_N_C_F: {dhpf[e][2]:2d}")
        print("****************")

        self.horasProgramablesFicha() 
        i = 0
        for evento in self._listaEventos:
            print(f"evento: {i:2d}, {evento}")
            i += 1
        
        
# principal       
evento0 = Evento(1, 6, 8, date(2023,4,1), date(2023,4,30))
evento1 = Evento(1, 10, 11, date(2023,4,9), date(2023,4,20))
evento2 = Evento(2, 6, 7, date(2023,4,10), date(2023,4,26))
evento3 = Evento(2, 8, 9, date(2023,4,1), date(2023,4,28))
evento4 = Evento(3, 9, 11, date(2023,4,1), date(2023,4,23))
evento5 = Evento(3, 12, 13, date(2023,4,10), date(2023,4,28))

#listaEventos = [evento0]
#listaEventos = [evento0, evento1, evento2]
#listaEventos = [evento0, evento1, evento2, evento3]
listaEventos = [evento0, evento1, evento2, evento3, evento4, evento5]

programador = Programador(listaEventos, 4, 160)
programador.resultado()
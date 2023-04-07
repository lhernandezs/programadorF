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
        self._promedioHorasPorFicha = None
        self._matrizDeEventosPorDiaHora = None
        self._saldoDeHorasAProgramar = horasAProgramar

    # retorna True si el evento está en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, x, y):
        fecha = date(2023, self._mes, x)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= y and y < evento.horaF else False

    # setea la matriz de los eventos por cada dia y la hora del mes    
    def matrizEventosPorDiaHora(self):
        diasDelMes = Mes(self._mes).ultimoDia().day
        listaDiasLaborables = Mes(self._mes).listaDiasLaborables()
        matrizDeEventosPorDiaHora = [[[] for j in range(24)] for i in range(diasDelMes)]
        for e in range(len(self._listaEventos)):
            for i in range(diasDelMes):
                for j in range(24):
                    if self.estaElEventoEnDiaHora(self._listaEventos[e], i+1, j) and i+1 in listaDiasLaborables:
                        matrizDeEventosPorDiaHora[i][j].append(e)
        self._matrizDeEventosPorDiaHora = matrizDeEventosPorDiaHora  

    # setea las listas de dias laborables, dias antes de cruce y dias luego de cruce de Evento   
    def analisisDiasEventos(self):
        setDiasLaborablesMes = set(Mes(self._mes).listaDiasLaborables())
        ultimaFecMes = Mes(self._mes).ultimoDia()

        for evento in self._listaEventos:
            diaIniEvento = 1 if (evento.fechaI < Mes(self._mes).primerDia()) else evento.fechaI.day
            diaFinEvento = ultimaFecMes.day if (ultimaFecMes < evento.fechaF) else evento.fechaF.day
            listaDiasIniFinEvento = [x for x in range(diaIniEvento, diaFinEvento+1)]

            fecIniCruce = fecFinCruce = None
            for i in range(ultimaFecMes.day):
                for j in range(24):
                    if len(self._matrizDeEventosPorDiaHora[i][j]) > 1 and evento.id in self._matrizDeEventosPorDiaHora[i][j]:
                        if fecIniCruce is None or date(2023, self._mes, i+1) < fecIniCruce: fecIniCruce = date(2023, self._mes, i+1)
                        if fecFinCruce is None or date(2023, self._mes, i+1) > fecFinCruce: fecFinCruce = date(2023, self._mes, i+1)

            listaDiasAntesDeCruce = listaDiasIniFinEvento if fecIniCruce is None else [x for x in range(diaIniEvento, fecIniCruce.day)] 
            listaDiasLuegoDeCruce = [] if fecFinCruce is None else [x for x in range(fecFinCruce.day+1, diaFinEvento)]

            self._listaEventos[evento.id].listaDiasLaborables = list(set(listaDiasIniFinEvento) & setDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasAntesCruce = list(set(listaDiasAntesDeCruce) & setDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasLuegoCruce = list(set(listaDiasLuegoDeCruce) & setDiasLaborablesMes)
    
    # retorna la lista de las fichas
    def listaFichas(self):        
        return list(set([evento.ficha for evento in self._listaEventos]))

    # Presenta en consola el resultado de la programacion    
    def resultado(self):
        self.matrizEventosPorDiaHora()
        self.analisisDiasEventos()

        # 1. calcular y setear el promedio de horas por ficha
        self._promedioHorasPorFicha = self._horasAProgramar // len (self.listaFichas())

        for evento in self._listaEventos:
            if not evento.fichaYaProgramada:
                horasEvento = evento.horaF - evento.horaI 
                listaDiasMasLarga =  evento.listaDiasAntesCruce if len(evento.listaDiasAntesCruce) > len(evento.listaDiasLuegoCruce) else evento.listaDiasLuegoCruce
                if (horasEvento * len(listaDiasMasLarga)) > self._promedioHorasPorFicha * (1-(self._tolerancia/100)):
                    limiteHorasAProgramar = self._promedioHorasPorFicha * (1+(self._tolerancia/100))
                    horasAcumuladas = 0
                    for dia in listaDiasMasLarga:
                        if horasAcumuladas < limiteHorasAProgramar:
                            self._listaEventos[evento.id].listaDiasAProgramar.append(dia)
                            horasAcumuladas += horasEvento
                        else:
                            break
                    for eve in self._listaEventos:
                        if evento.ficha == eve.ficha:
                            self._listaEventos[eve.id].fichaYaProgramada = True
                    self._saldoDeHorasAProgramar -= horasEvento * len(self._listaEventos[evento.id].listaDiasAProgramar)
                    # retirar los eventos de la matriz

        for evento in self._listaEventos:
            print(evento)
        print(self._saldoDeHorasAProgramar)
                    


        # 2. iterar
        #   se asigna horas en el primer evento que tenga dias antes o luego del cruce suficientes para cumplir entre el -x% y +x% del promedio de horas por ficha
        #   si es posible el paso anterior, la ficha queda programada, se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
        #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas
        # 3. iterar
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
programador.resultado()
#print(programador.listaFichas())
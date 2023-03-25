from Evento import Evento
from DiasLaborables import DiasLaborables
from dateutil.relativedelta import relativedelta
import datetime


class Programador:
    def __init__(self, listaEventos, mes, horasAProgramar):
        self.__listaEventos = listaEventos
        self.__mes = mes
        self.__horasAProgramar = horasAProgramar
 
    def horasEvento(self, evento):
        # verifica que horaF sea entero mayor que hora    
        # verifica que diaF sea entero mayor que diaI
        # Cuenta el numero de horas en el rango
        # Cuenta el numero de dias en el rango descontando sabados, domingos y festivos
        # retorn la multiplicacion de horas x dias
        pass

    #Devuelve una lista con el diaI y el diaF propuesto de acuerdo a las horas estimadas y el los dias laborables
    #Debe verificar que no se crucen los horarios y los dias, para ello deber ordenar la lista de eventos por la horaI
    #Utiliza los dias laborales
    def proponerDias(self):
        pass

    # Construye una lista de horas equitativas por cada evento
    def promediarHorasEvento(self):
        #calcula la cantidad de fichas
        #calcula la cantidad de horas en los n eventos de la ficha
        #distribuye horas por cada evento tratando de ser equitativo segun las horas a programar
        #setea las horas estimadas n
        pass

    def diasHabilesPorEvento(self, mes, fechaI, fechaF):
        rangoDiasHabiles = []
        if (fechaI < datetime.date(2023, mes, 1)):
            rangoDiasHabiles.append(1)
        else:
            rangoDiasHabiles.append(fechaI.day)
        if ((datetime.date(2023, mes, 1) + relativedelta(day=31)) < fechaF):
            rangoDiasHabiles.append((datetime.date(2023, mes, 1) + relativedelta(day=31)).day)
        else:
            rangoDiasHabiles.append(fechaF.day)
        print(rangoDiasHabiles)
        return rangoDiasHabiles
    
    def capacidadBrutaHoras(self):
        capacidadBrutaHoras = 0
        for i in range(0,len(self.__listaEventos)):
            horasEvento = self.__listaEventos[i].getHoraF()-self.__listaEventos[i].getHoraI()
            rangoDiasHabiles = self.diasHabilesPorEvento(self.__mes, self.__listaEventos[i].getFechaI(), self.__listaEventos[i].getFechaF())
            diasCorrientesEvento = [x for x in range(rangoDiasHabiles[0],rangoDiasHabiles[1]+1)]
            diasLaborales = DiasLaborables(self.__mes)
            diasLaborablesEvento = list(set(diasCorrientesEvento) & set(diasLaborales.diasLaborables()))
            capacidadBrutaHoras += horasEvento * len(diasLaborablesEvento)
        return capacidadBrutaHoras
    
    # Presenta en consola el resultado de la programacion    
    def resultado(self):
        promedioHorasPorFicha = self.__horasAProgramar // len(self.__listaEventos) 
        capacidadBrutaHoras = self.capacidadBrutaHoras()
        print(capacidadBrutaHoras)
       

evento1 = Evento(123456, 6, 8, datetime.date(2023,3,1), datetime.date(2023,3,31))
evento2 = Evento(123456, 8, 10, datetime.date(2023,1,12), datetime.date(2023,3,15))
evento3 = Evento(123457, 10, 12, datetime.date(2023,3,11), datetime.date(2023,3,20))
evento4 = Evento(123458, 12, 13, datetime.date(2023,3,1), datetime.date(2023,3,31))
                
listaEventos = [evento1, evento2, evento3, evento4]
programador = Programador(listaEventos, 3, 160)
programador.resultado()
        

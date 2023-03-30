from Evento import Evento
from DiasLaborables import DiasLaborables
from dateutil.relativedelta import relativedelta
import datetime

class Programador:
    def __init__(self, listaEventos, mes, horasAProgramar):
        self.__listaEventos = listaEventos
        self.__mes = mes
        self.__horasAProgramar = horasAProgramar

    # este metodo retorna True si el evento está en el Dia y la Hora pasado como parametros

    def eventoEnDiaHora(self, evento, i, j):
#      print(evento.getFechaI(), " ", evento.getFechaF(), " ", i, " ", j)
        dia = i
        if (datetime.date(2023,self.__mes,1) + relativedelta(day=31)).day >= dia:
#            print("Entro", datetime.date(2023,self.__mes,1) + relativedelta(31))
            if evento.getFechaI() <= datetime.date(2023, self.__mes, dia) and datetime.date(2023, self.__mes, dia) <= evento.getFechaF() \
                and evento.getHoraI() <= j and j < evento.getHoraF(): 
#                print(" Adicionar .....", evento.getFechaI(), " ", evento.getFechaF(), " ", i, " ", j )
                return True
        return False
            
    # este metodo retorna una lista de igual longitud a la lista de eventos, con tuplas (horaI, horaF, diaI, diaF) de los eventos depurando que los cruces. Los cruces se resolveran tratando de colocar horas "similares" a todas
    def cruceDeEventos(self):
        programacionBruta = [[[] for j in range(24)] for i in range(1,32)]
        for e in range(len(self.__listaEventos)):
            for i in range(1,32):
                for j in range(24):
                    if self.eventoEnDiaHora(self.__listaEventos[e], i, j) and i in DiasLaborables(self.__mes).diasLaborablesMes():
                        programacionBruta[i][j].append(e)

        for i in range(31):
            for j in range(24):
                print("[",i,",",j,"]...", programacionBruta[i][j])

    def diasLaborablesEvento(self, fechaI, fechaF):
        rangoDiasCorrientes = []
        if (fechaI < datetime.date(2023, self.__mes, 1)):
            rangoDiasCorrientes.append(1)
        else:
            rangoDiasCorrientes.append(fechaI.day)
        if ((datetime.date(2023, self.__mes, 1) + relativedelta(day=31)) < fechaF):
            rangoDiasCorrientes.append((datetime.date(2023, self.__mes, 1) + relativedelta(day=31)).day)
        else:
            rangoDiasCorrientes.append(fechaF.day)
        diasCorrientesEvento = [x for x in range(rangoDiasCorrientes[0],rangoDiasCorrientes[1]+1)]
        diasLaborablesEvento = list(set(diasCorrientesEvento) & set(DiasLaborables(self.__mes).diasLaborablesMes()))
        print(diasLaborablesEvento)       
        return diasLaborablesEvento
    
    def capacidadBrutaHoras(self):
        capacidadBrutaHoras = 0
        for evento in self.__listaEventos:
            horasEvento = evento.getHoraF() - evento.getHoraI()
            diasLaborablesEvento = self.diasLaborablesEvento(evento.getFechaI(), evento.getFechaF())
            capacidadBrutaHoras += horasEvento * len(diasLaborablesEvento)      
        if capacidadBrutaHoras < self.__horasAProgramar:
            print("hay que crear eventos")
        else:
            print("en teoria los eventos actuales alcanzan pero hay que revisar que no se crucen")
        return capacidadBrutaHoras
    
    # Presenta en consola el resultado de la programacion    
    def resultado(self):
#        capacidadBrutaHoras = self.capacidadBrutaHoras()
        self.cruceDeEventos()
       
evento1 = Evento(123456, 6, 9, datetime.date(2023,3,1), datetime.date(2023,3,3))
evento2 = Evento(123456, 8, 10, datetime.date(2023,3,12), datetime.date(2023,3,15))
evento3 = Evento(123457, 8, 12, datetime.date(2023,3,11), datetime.date(2023,3,20))
evento4 = Evento(123458, 11, 13, datetime.date(2023,3,1), datetime.date(2023,3,5))
                
#listaEventos = [evento1]
listaEventos = [evento1, evento2, evento3]
#listaEventos = [evento1, evento2, evento3, evento4]
programador = Programador(listaEventos, 3, 80)
programador.resultado()
        

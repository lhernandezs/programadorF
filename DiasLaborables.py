# Comentario de esta clase
import calendar

class DiasLaborables:

    FESTIVOS = {1: [9],
                    2 : [],
                    3 : [20],
                    4 : [6, 7],
                    5 : [1, 22],
                    6 : [12, 19],
                    7 : [3, 20],
                    8 : [7, 21],
                    9 : [],
                    10 : [16],
                    11 : [6, 13],
                    12 : [8, 25]
                    }
    
    def __init__(self, mes):
        self.mes = mes

    #Devuelve la lista de los dias laborables del mes
    def diasLaborables(self):

        # se crea un obejto de la Clase Calendar
        calendario = calendar.Calendar()

        # se crean las tuplas de (dia mes, dia semana) del mes
        listDiasMes = [x for x in calendario.itermonthdays2(2023, self.mes)]

        #se elminan los sabados y domingos y se crea la lista de dias --eliminando los ceros de relleno
        listTuplasMes = list(filter(lambda x: x[1] not in [5,6] and x[0]!= 0, listDiasMes))
       
        #return listaDiasLaborables eliminando los festivos del mes
        return list(filter(lambda y: y not in DiasLaborables.FESTIVOS[self.mes], [x[0] for x in listTuplasMes]))



import calendar
import datetime
from dateutil.relativedelta import relativedelta

class Mes:
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
        self._mes = mes

    # devuelve la lista de los dias laborables del mes
    def listaDiasLaborables(self):
        calendario = calendar.Calendar()
        listaDiasMes = [x for x in calendario.itermonthdays2(2023, self._mes)] # se crean las tuplas (dia mes, dia semana)
        listaTuplasMes = list(filter(lambda x: x[1] not in [5,6] and x[0]!= 0, listaDiasMes)) # se elminan los sabados y domingos y se crea la lista de dias. tambien elimina los ceros de relleno en listaDiasMes
        return list(filter(lambda x: x not in Mes.FESTIVOS[self._mes], [x[0] for x in listaTuplasMes])) # retorna la lista de dias laborables del mes eliminando los festivos

    # devuelve la fecha del ultimo dia del mes ..
    def ultimoDia(self):
        return datetime.date(2023, self._mes, 1) + relativedelta(day=31)
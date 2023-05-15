import sys as sys
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
        self._diccionarioFichas = dict.fromkeys([evento.ficha for evento in self._listaEventos], 0) # crea el diccionario de fichas en ceros
        self._promedioHorasPorFicha = self._horasAProgramar // len(self._diccionarioFichas) # valor entero de la division
        self._minimoHorasAProgramarPorFicha = int(self._promedioHorasPorFicha * (1-(self._tolerancia/100))) # valor entero
        self._maximoHorasAProgramarPorFicha = int(self._promedioHorasPorFicha * (1+(self._tolerancia/100))) # valor entero
        self._ultimaFecMes = Mes(self._mes).ultimoDia() # contiene la fecha del ultimo dia del mes
        self._diasDelMes = self._ultimaFecMes.day # contiene el entero del ultimo dia del mes
        self._listaDiasLaborablesMes = Mes(self._mes).listaDiasLaborables() # contiene la lista de los dias laborables del mes
        self._matrizDeEventos = self.matrizDeEventos() # contiene una matriz de 24 horas x los dias del mes con los eventos -- sin programar
        self._saldoDeHorasAProgramar = horasAProgramar # representa el saldo de horas aún sin programar
        self._matrizHorasProgramadas = None # contiene la horas proramadas y no laborables del mes
        self._matrizDeRectangulos = None # contiene los "rectangulos" disponibles - sin programacion -
        self._pila = None # contiene la pila de llamadas recursivas para el metodo encontrar rectangulos

    # retorna True si el evento exite en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, dia, hora):
        fecha = date(2023, self._mes, dia)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= hora and hora < evento.horaF else False
    
    # devuelve la lista de eventos sin ningun dia programado de las fichas que aú no han sido programadas
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
            capacidad = horasEvento * len(listaDias)
            return (evento, capacidad, listaDias, horasEvento)
        else:
            listaDias = lA if len(lA := evento.listaDiasAntesCruce) > len(lL := evento.listaDiasLuegoCruce) else lL
            capacidad = horasEvento * len(listaDias)
            return (capacidad, listaDias, horasEvento)
    
    # devuelve True si la capacidad es al menos la mitdas del mínimo de horas a programar por ficha o False en caso contrario
    def tieneCapacidadMinima(self, capacidad):
        return True if capacidad >= self._minimoHorasAProgramarPorFicha // 2 else False
    
    # del mejor evento programable devuelve el evento, la lista de dias a programar y las horas, que se define asi: 
    # 1. Tiene la capacidad mas grande revisando las listas de dias de los eventos sin programar; en caso de empate, tiene la hora de inicio mas temprano. 
    # 2. Si se acaban los eventos anteriores, se revisan los eventos cruzados de menos a mas "cardinalidad" -- número de eventos que se cruzan en un dia y hora-.   
    def buscarMejorEventoProgramable(self):
        eventosProgramables = [] 
        # 1.
        for evento in self.listaEventosSinProgramar():
            (capacidad, listaDias, horasEvento) = self.capacidadEvento(evento, False)
            eventosProgramables.append((evento, capacidad, evento.horaI, listaDias, horasEvento)) if self.tieneCapacidadMinima(capacidad) else None                
        if len(eventosProgramables) > 0:
            (evento, capacidad, horaI, listaDias, horasEvento) = (list(sorted(sorted(eventosProgramables, key=lambda x: x[2]), key=lambda x: -x[1])))[0]
            return (evento, listaDias, horasEvento)
        else:
            # 2.
            for longitud in range(2, len(self._listaEventos)):
                listaDeEventosCruzados = list(filter(lambda item: len(item) == longitud, [self._matrizDeEventos[i][j] for j in range(24) for i in range(self._diasDelMes)]))
                if listaDeEventosCruzados:
                    cruceMasRepetido = max(listaDeEventosCruzados, key=listaDeEventosCruzados.count)
                    listaTuplas = []
                    for id in cruceMasRepetido:
                        listaTuplas.append(self.capacidadEvento(self._listaEventos[id], True))
                    (evento, capacidad, listaDias, horasEvento)= (list(sorted(listaTuplas, key=lambda t: -t[1])))[0]
                    return (evento, listaDias, horasEvento)
                else:
                    return (None, None, None)
    
    # retorna True si el evento "está programado" en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaProgramadoElEventoEnDiaHora(self, evento, dia, hora):
        return True if not evento.listaDiasAProgramar is None and dia in evento.listaDiasAProgramar and evento.horaI <= hora and hora < evento.horaF else False

    # ---- replantear con la nueva funcion -----
    def encontrarRectangulo(self):

        global recursividad
        global recursividadIz
        global recursividadDe
        global recursividadIn
        
        alto = 24
        ancho = self._diasDelMes

        recursividad += 1

        ban = False
        if len(self._pila) > 0:
            (xIni, yIni, xFin, yFin) = self._pila.pop()
            superior = izquierdo = derecho = inferior = False
            for y in range(yIni, yFin+1):
                for x in range(xIni, xFin+1):
                    if self._matrizHorasProgramadas[x][y] != " ":        # NO                       APUNTA                          ENTRA
                        if   x == 0 and y == 0                         : # izquierdo superior       derecho inferior    
                            derecho = inferior = True
                        elif x == 0 and y in range(1,  alto-1)         : # izquierdo                derecho inferior                superior
                            derecho = inferior = superior = True
                        elif y == 0 and x in range(1, ancho-1)         : # superior                 derecho inferior izquierdo
                            derecho = inferior = izquierdo = True
                        elif x == (ancho-1) and y == (alto-1)          : # derecho inferior         izquierdo                       superior
                            izquierdo = superior = True
                        elif x == (ancho-1) and y in range(1, alto-1)  : # derecho                  izquierdo inferior              superior
                            izquierdo = inferior = superior = True
                        elif y == (alto-1)  and x in range (1, ancho-1): # inferior                 izquierdo derecho               superior
                            izquierdo = derecho = superior = True
                        elif x == 0 and y == (alto-1)                  : # izquierdo inferior       derecho                         superior
                            derecho = superior = True
                        elif x == (ancho-1) and y == 0                 : # derecho superior         izquierdo inferior
                            izquierdo =  inferior = True
                        else:     
                            if   xIni == x and yIni == y               : # izquierdo superior       derecho inferior
                                derecho = inferior = True
                            elif xIni == x and yIni != y               : # superior                 izquierdo derecho inferior      
                                izquierdo = derecho = inferior = True
                            elif yIni == y and xIni != x               : # izquierdo                derecho inferior                superior
                                derecho = inferior = True
                            else                                       : #                          izquierdo derecho inferior      superior
                                izquierdo = derecho = inferior = superior = True

                        if superior:
                            self._matrizDeRectangulos.append(["Dentro", xIni, yIni, xFin, y-1, (xFin - xIni)*((y-1) - yIni)]) # ENTRA superior
                        if izquierdo:
                            for i in range (x-1, xIni, -1):
                                if self._matrizHorasProgramadas[i][yIni] == " ":                        
                                    self._pila.append((xIni, yIni, i, yFin))                          # apunta a rectangulo izquierdo
                                    recursividadIz += 1
                                    break
                        if derecho:
                            for i in range (x+1, xFin):
                                if self._matrizHorasProgramadas[i][yIni] == " ":
                                    self._pila.append((i, yIni, xFin, yFin))                          # apunta a rectangulo derecho
                                    recursividadDe += 1
                                    break
                        if inferior:
                            for j in range (y+1, yFin):
                                if self._matrizHorasProgramadas[xIni][j] == " ":
                                    self._pila.append((xIni, j, xFin, yFin))                          # apunta a rectangulo inferior
                                    recursividadIn += 1
                                    break
                        self.encontrarRectangulo()
                        ban = True
                        break
                if ban:
                    break
            else:
                if xIni <= xFin and yIni <= yFin:
                    self._matrizDeRectangulos.append(["Fuera ", xIni, yIni, xFin, yFin, (xFin - xIni)*(yFin - yIni)])
                if len(self._pila)>0:
                    self.encontrarRectangulo()
        else:
            return

    # setea una matriz que tiene las 24 horas del dia y en cada hora uno o varios rangos de dias (disyuntos) que no tienen programación. POR MEJORAR: Tener eventos de 2 o mas horas seguidas....
    def mejoresEspaciosNoProgramados(self):
        #  construir la matriz marcando los dias no laborables con "NL"
        self._matrizHorasProgramadas = [[(" " if d+1 in self._listaDiasLaborablesMes else "NL") for h in range(24)] for d in range(self._diasDelMes)]
        # colocar en la matriz anterior los eventos programados
        for evento in self._listaEventos:
            for d in self._listaDiasLaborablesMes:
                for h in range(24):
                    if self.estaProgramadoElEventoEnDiaHora(evento, d, h):
                        self._matrizHorasProgramadas[d][h] = str(f"{evento.id:2d}")
          
        self._pila = [(0, 0, programador._diasDelMes, 24)]
        self.encontrarRectangulo()

        ropc = sorted(self._matrizDeRectangulos, key=lambda c: -l[5]) # OJO: ordenar la matriz de rectangulos de mayor a menor capacidad
        rectangulosOrdenadosPorHora = []
        for h in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 4, 5, 6, 7, 19, 20, 21, 2, 3, 22, 0, 23]:
            for r in ropc:
                if r[1] == h:
                    rectangulosOrdenadosPorHora.append(r)
        return rectangulosOrdenadosPorHora
    
    # 1. iterar
    #   se asignan horas al mejor evento programable
    #   si la ficha queda programada (al menos el minimo de horas a programar por ficha), se retiran los eventos de la ficha en la matriz y se baja el numero de horas a programar
    #   se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas 
    # 2. para todos los eventos que tengan dias por programar se tratan de asignar horas en los dias
    # 3. se revisan las fichas no programadas para hacer los siguientes ajustes --se da por hecho que se han acabado los eventos originales-:
    #   si hay horas por programar, se buscar un horario y dias que no se crucen con lo ya programado para programar el mínimo de horas por ficha
    #   si se acaban las horas por programar, hay que quitar dias de las fichas que tienen mayor número de horas para dejar programación a las fichas
   
    def programarEventos(self):
        # 1.
        self.analisisDiasEventos() 
        (evento, listaDias, horasEvento) = self.buscarMejorEventoProgramable() if not self.buscarMejorEventoProgramable() is None else (None, None, None)
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
        # 2.
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
        # 3. POR MEJORAR ... tener en cuenta que en el mejor hueco "sin progrmar" no alcance a programarse la ficha
        for item in list(filter(lambda item: item[1] < self._minimoHorasAProgramarPorFicha, self._diccionarioFichas.items())): # devulve tuplas ficha - horas programadas del diccionario de fichas cuando la ficha este progamada por debajo del minimo de horas a programar
            ficha = item[0] # obtine la ficha que aun no está programada
            if (horasAReducir := (self._minimoHorasAProgramarPorFicha - self._saldoDeHorasAProgramar)) > 0: # se deben quitar horas a otra ficha
                fichaADesprogramar = max(self._diccionarioFichas, key=self._diccionarioFichas.get) # se consigue la ficha con mayor numero de horas programadas
                eventoADesprogramar = sorted(list(filter(lambda e: e.ficha == fichaADesprogramar and not e.listaDiasAProgramar is None, self._listaEventos)), key =lambda e: len(e.listaDiasAProgramar))[0] # se consigue el evento con mas programacion de la ficha a desprogramar
                horasEventoADesprogramar = eventoADesprogramar.horaF - eventoADesprogramar.horaI
                diasAReducir = (horasAReducir // horasEventoADesprogramar) + 1 
                for x in range(diasAReducir): 
                    d = eventoADesprogramar.listaDiasAProgramar.pop() # reducir los dias programados en el evento
                    eventoADesprogramar.listaDiasPorProgram.append(d) # aumentar los dias por programar en el evento  
                    eventoADesprogramar.listaDiasPorProgram.sort() # ordenar la lista de dias dado que el nuevo dia programado queda al final
                self._diccionarioFichas[fichaADesprogramar] -= horasEventoADesprogramar * diasAReducir # disminuir las horas en el diccionario para la ficha
                self._saldoDeHorasAProgramar += horasEventoADesprogramar * diasAReducir # aumentar el saldo de horas a Programar
            # crear un evento para la ficha si no lo tiene en la mejor Capacidad de Dias No programados - incluir este evento en self._listaEventos-- OJO: no se puede cruzar con los eventos de la ficha
            ban = True
            mejores = self.mejoresEspaciosNoProgramados()
            while ban:
                (horaI, diaI, diaF, capacidad) = mejores.pop(0) # OJO: 
                for e in list(filter(lambda eve: eve.ficha == ficha, self._listaEventos)):
                    if e.horaI in range(horaI, horaI+1) or e.horaF in range(horaI, horaI+1):
                        continue
                    id = len(self._listaEventos)
                    diaFin = self._listaDiasLaborablesMes[self._listaDiasLaborablesMes.index(diaI) + self._minimoHorasAProgramarPorFicha - 1]
                    nuevoEvento = Evento(id, ficha, horaI, horaI+1, date(2023, self._mes, diaI), date(2023, self._mes, diaFin)) 
                    self._listaEventos.append(nuevoEvento)        
                    # setear los dias programados hasta el minimo de horas a programar por ficha
                    nuevoEvento.listaDiasAProgramar = list(set(self._listaDiasLaborablesMes) & set(range(diaI, diaFin+1)))
                    self.analisisDiasEventos() # esto para inicializar la lista de dias a programar
                    # POR MEJORAR .. puede ser que la ficha no quede programar en un solo evento por que no le alcance el hueco para cumplir sus horas minimas
                    self.marcarEventosDeLaFichaProgramada(nuevoEvento)
                    self._diccionarioFichas[ficha] += self._minimoHorasAProgramarPorFicha # aumentar las horas programadas en el diccionario para la ficha
                    self._saldoDeHorasAProgramar -= self._minimoHorasAProgramarPorFicha # disminuir el saldo de horas totales a Programar
                    mejores = self.mejoresEspaciosNoProgramados()
                    ban = False
                    break
                
# principal 
sys.setrecursionlimit(5000000)
print(sys.getrecursionlimit())

listaEventos = [ \
# Evento(0, 1, 6, 8, date(2023,4,1), date(2023,4,30)), \
# Evento(1, 1, 10, 11, date(2023,4,9), date(2023,4,20)), \
# Evento(2, 2, 6, 7, date(2023,4,10), date(2023,4,26)), \
# Evento(3, 2, 8, 9, date(2023,4,1), date(2023,4,28)), \
# Evento(4, 3, 9, 11, date(2023,4,1), date(2023,4,23)), \
# Evento(5, 3, 12, 13, date(2023,4,10), date(2023,4,28)), \

# Evento(0, 2675758, 6, 7, date(2023,4,1), date(2023,4,30)), \
# Evento(1, 2675759, 7, 8, date(2023,4,1), date(2023,4,30)), \
# Evento(2, 2626937, 12, 14, date(2023,4,1), date(2023,4,30)), \
# Evento(3, 2626938, 7, 9, date(2023,4,1), date(2023,4,30)), \
# Evento(4, 2626939, 9, 11, date(2023,4,1), date(2023,4,30)), \
# Evento(5, 2626940, 7, 8, date(2023,4,1), date(2023,4,30)), \
# Evento(6, 2675911, 12, 13, date(2023,4,1), date(2023,4,30)), \
# Evento(7, 2675912, 20, 22, date(2023,4,1), date(2023,4,30)), \
# Evento(8, 2675758, 6, 7, date(2023,4,1), date(2023,4,30)), \
# Evento(9, 2675759, 7, 8, date(2023,4,1), date(2023,4,30)), \
# Evento(10, 2626937, 12, 14, date(2023,4,1), date(2023,4,30)), \
# Evento(11, 2626938, 7, 9, date(2023,4,1), date(2023,4,30)), \
# Evento(12, 2626939, 9, 11, date(2023,4,1), date(2023,4,30)), \
# Evento(13, 2626940, 7, 8, date(2023,4,1), date(2023,4,30)), \
# Evento(14, 2675911, 12, 13, date(2023,4,1), date(2023,4,30)), \
# Evento(15, 2675912, 20, 22, date(2023,4,1), date(2023,4,30)), \
Evento(0, 2600000, 0, 0, date(2023,4,1), date(2023,4,30)), \
Evento(1, 2700000, 0, 0, date(2023,4,1), date(2023,4,30)), \
]

programador = Programador(listaEventos, 4, 160, 10)

programador.programarEventos()
print("*********************************************")
print("************* c o m e n z o *****************")
print("*********************************************")
print(f"recursividad = {recursividad} Izquierdo = {recursividadIz} Derecho = {recursividadDe} Inferior = {recursividadIn}")

print()

print(f"  H a programar: {programador._horasAProgramar} - H por Programar:{programador._saldoDeHorasAProgramar:3d} - Dicionario: {programador._diccionarioFichas}  - Mes: {programador._mes}  - Tolerancia: {programador._tolerancia}%" )
# print(" -------------------------------------------------------------------------------------------------------------- ")
# print("|  Evento  |   Ficha  |   Horas   |  D In Fi | D labor  | D A Cruz | D L Cruz | D A Prog | D P Prog | Ya Progr | ")
# print(" -------------------------------------------------------------------------------------------------------------- ")
# for evento in programador._listaEventos:
#     print(evento)
#     print(" -------------------------------------------------------------------------------------------------------------- ")
# print()

print("| hora |", end="")
for i in range(programador._diasDelMes):
    print((f"{i+1}").center(4), end="|")
print()
hora = 0
for h in range(24):
    print(f"|  {hora:2d}  |", end="")
    for d in range(programador._diasDelMes):
        print((f"{programador._matrizHorasNoProgramadas[d][h]}").center(4), end="|")
    print()
    hora += 1

#print(programador._matrizHorasNoProgramadas)
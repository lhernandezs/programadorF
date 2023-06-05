import sys as sys
from Mes import Mes
from Evento import Evento
from datetime import date

class Programador:
    # constructor de la clase
    def __init__(self, listaEventos, mes, horasAProgramar, tolerancia):
        self._listaEventos = listaEventos # recibe la lista de eventos
        self._mes = mes # recibe el mes que se quiere programar
        self._horasAProgramar = horasAProgramar # recibe la cantidad de horas a programar
        self._tolerancia = tolerancia # determina que porcentaje de horas por encima o por debajo se puede programar una ficha respecto al promedio
        self._diccionarioFichas = dict.fromkeys([evento.ficha for evento in self._listaEventos], 0) # crea el diccionario de fichas en ceros
        self._promedioHorasPorFicha = self._horasAProgramar // len(self._diccionarioFichas) # valor entero de la division
        self._minimoHorasAProgramarPorFicha = int(self._promedioHorasPorFicha * (1-(self._tolerancia/100))) # valor entero
        self._maximoHorasAProgramarPorFicha = int(self._promedioHorasPorFicha * (1+(self._tolerancia/100))) # valor entero
        self._ultimaFecMes = Mes(self._mes).ultimoDia() # contiene la fecha del ultimo dia del mes
        self._diasDelMes = self._ultimaFecMes.day # contiene el entero del ultimo dia del mes
        self._listaDiasLaborablesMes = Mes(self._mes).listaDiasLaborables() # contiene la lista de los dias laborables del mes
        self._matrizDeEventosSinProgramar = self.matrizDeEventosSinProgramar() # contiene una matriz de 24 horas x los dias del mes con los eventos -- sin programar
        self._saldoDeHorasAProgramar = horasAProgramar # contiene el saldo de horas aún sin programar
        self._matrizHorasProgramadas = None # contiene la horas programadas del mes marcando los dias no laborables
        self._matrizDeRectangulos = [] # contiene los "rectangulos" disponibles - sin programacion -
        self._pila = [] # contiene la pila de llamadas recursivas para el metodo encontrarRectangulo

    # retorna True si el evento exite en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, dia, hora):
        fecha = date(2023, self._mes, dia)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= hora and hora <= evento.horaF else False
    
    # devuelve la lista de eventos sin ningun dia programado de las fichas que aún no han sido programadas
    def listaEventosSinProgramar(self):
        return list(filter(lambda evento: len(evento.listaDiasAProgramar) == 0 and not evento.fichaYaProgramada, self._listaEventos))

    # setea la matriz de los eventos sin programar de las fichas que aun no han sido programadas por cada dia y la hora del mes
    def matrizDeEventosSinProgramar(self):
        matrizDeEventosSinProgramar = [[[] for h in range(24)] for d in range(self._diasDelMes)]
        for evento in self.listaEventosSinProgramar():
            for i in range(self._diasDelMes):
                dia = i+1
                for h in range(24):
                    if self.estaElEventoEnDiaHora(evento, dia, h) and dia in self._listaDiasLaborablesMes:
                        matrizDeEventosSinProgramar[i][h].append(evento.id)
        self._matrizDeEventosSinProgramar = matrizDeEventosSinProgramar  

    # setea las listas de dias laborables, dias antes de cruce y dias luego de cruce de los eventos sin programar   
    def analisisDiasEventos(self):
        self.matrizDeEventosSinProgramar()
        conjuntoDiasLaborablesMes = set(self._listaDiasLaborablesMes)
        for evento in self.listaEventosSinProgramar():
            diaIniEvento = 1 if (evento.fechaI < date(2023, self._mes, 1)) else evento.fechaI.day # controla si el inicio del evento es antes del 1er dia del mes
            diaFinEvento = self._diasDelMes if (self._ultimaFecMes < evento.fechaF) else evento.fechaF.day # controla si el fin del evento es despues del ultimo dia del mes
            listaDiasIniFinEvento = [dia for dia in range(diaIniEvento, diaFinEvento+1)]  # tener en cuenta que en los rangos el valor final no se incluye
            fecIniCruce = fecFinCruce = None
            for i in range(self._diasDelMes):
                dia = i+1
                for h in range(24):
                    if len(self._matrizDeEventosSinProgramar[i][h]) > 1 and evento.id in self._matrizDeEventosSinProgramar[i][h]: # si hay cruce del evento
                        if fecIniCruce is None or date(2023, self._mes, dia) < fecIniCruce: fecIniCruce = date(2023, self._mes, dia) # encuentro la menor fecha inicial de cruce
                        if fecFinCruce is None or date(2023, self._mes, dia) > fecFinCruce: fecFinCruce = date(2023, self._mes, dia) # encuentro la mayor fecha final de cruce
            listaDiasAntesDeCruce = listaDiasIniFinEvento if fecIniCruce is None else [x for x in range(diaIniEvento, fecIniCruce.day)] 
            listaDiasLuegoDeCruce = [] if fecFinCruce is None else [x for x in range(fecFinCruce.day+1, diaFinEvento)]

            self._listaEventos[evento.id].listaDiasLaborables = list(set(listaDiasIniFinEvento) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasAntesCruce = list(set(listaDiasAntesDeCruce) & conjuntoDiasLaborablesMes)
            self._listaEventos[evento.id].listaDiasLuegoCruce = list(set(listaDiasLuegoDeCruce) & conjuntoDiasLaborablesMes)
    
    # setea en True el atributo fichaYaProgramada de todos los eventos que tiene la misma ficha el evento
    def marcarEventosDeLaFichaProgramada(self, evento):
        lista = list(filter(lambda e: evento.ficha == e.ficha, self._listaEventos))
        for e in lista: e.fichaYaProgramada = True

    # recibe un evento y un boleano que indica si el evento esta cruzado o no dependiendo desde donde se llama este metodo
    # devuelve una tupla con el evento - depende -, la capacidad de horas a programar en el evento, la lista mas larga de dias programables y la duracion en horas
    def capacidadEvento(self, evento, cruzado):
        horasEvento = evento.horaF - evento.horaI + 1 # se parte que si un evento tiene la misma hora de inicio y de fin, el evento dura una hora
        if cruzado:
            listaDias = evento.listaDiasLaborables  # se toman todos los dias laborables del evento sin importar los cruces
            capacidad = horasEvento * len(listaDias)
            return (evento, capacidad, listaDias, horasEvento)
        else:
            listaDias = lA if len(lA := evento.listaDiasAntesCruce) > len(lL := evento.listaDiasLuegoCruce) else lL  # se toman la lista mayor de los dias que no se cruzan con otros eventos
            capacidad = horasEvento * len(listaDias)
            return (capacidad, listaDias, horasEvento)
    
    # devuelve True si la capacidad es al menos la mitad del mínimo de horas a programar por ficha o False en caso contrario
    def tieneCapacidadMinima(self, capacidad):
        return True if capacidad >= self._minimoHorasAProgramarPorFicha // 2 else False
    
    # Busca el mejor evento programable que se define asi: 
    # 1. Tiene la capacidad mas grande entre los eventos sin programar ; en caso de empate, tiene la hora de inicio mas temprano. 
    # 2. Si se acaban los eventos anteriores, se revisan los eventos cruzados de menos a mas "cardinalidad" - número de eventos que se cruzan el mismo dia y hora -.
    # Devuelve el evento, la lista de dias a programar y las horas
    def buscarMejorEventoProgramable(self):
        eventosProgramables = [] 
        # 1.
        for evento in self.listaEventosSinProgramar():
            (capacidad, listaDias, horasEvento) = self.capacidadEvento(evento, False)
            eventosProgramables.append((evento, capacidad, evento.horaI, listaDias, horasEvento))  # en lugar de None deberia ser un "pass" pero no funciona   
            # eventosProgramables.append((evento, capacidad, evento.horaI, listaDias, horasEvento)) if self.tieneCapacidadMinima(capacidad) else None  # en lugar de None deberia ser un "pass" pero no funciona            
        if len(eventosProgramables) > 0:
            (evento, capacidad, horaI, listaDias, horasEvento) = (list(sorted(sorted(eventosProgramables, key=lambda x: x[2]), key=lambda x: -x[1])))[0] # capacidad y horaI se utilizan en el ordenamiento
            return (evento, listaDias, horasEvento)
        else:
            # 2.
            for cardinalidad in range(2, len(self._listaEventos)): # se procesan los eventos de cardinalidad 2, luego 3, luego 4, etc.
                listaDeEventosCruzados = list(filter(lambda item: len(item) == cardinalidad, [self._matrizDeEventosSinProgramar[i][j] for j in range(24) for i in range(self._diasDelMes)]))
                if listaDeEventosCruzados:
                    cruceMasRepetido = max(listaDeEventosCruzados, key=listaDeEventosCruzados.count) 
                    listaTuplas = []
                    for id in cruceMasRepetido:
                        listaTuplas.append(self.capacidadEvento(self._listaEventos[id], True))
                    (evento, capacidad, listaDias, horasEvento)= (list(sorted(listaTuplas, key=lambda tupla: -tupla[1])))[0] # escoje el evento de mayor capacidad
                    return (evento, listaDias, horasEvento)
            else:
                return (None, None, None) # si no hay eventos sin cruzar ni tampoco eventos cruzados devuelve una tupla de None

    # retorna True si el evento "está programado" en el Dia y la Hora pasado como parametros o False en caso contrario
    def estaProgramadoElEventoEnDiaHora(self, evento, dia, hora):
        return True if not evento.listaDiasAProgramar is None and dia in evento.listaDiasAProgramar and evento.horaI <= hora and hora <= evento.horaF else False

    # metodo que encuentra los "rectangulos" que estan disponibles
    def encontrarRectangulo(self):

        global recursividad
        global recursividadIz
        global recursividadDe
        global recursividadIn
        
        recursividad += 1

        primerDia    = self._listaDiasLaborablesMes[0]
        ultimoDia    = self._listaDiasLaborablesMes[-1]
        penultimoIndice = len(self._listaDiasLaborablesMes)-2

        ban = False

        if len(self._pila) > 0:
            (dIni, hIni, dFin, hFin) = self._pila.pop()
            indiceDIni = self._listaDiasLaborablesMes.index(dIni)
            indiceDFin = self._listaDiasLaborablesMes.index(dFin)
            superior = izquierdo = derecho = inferior = False
            for h in range(hIni, hFin+1):
                for dia in self._listaDiasLaborablesMes[indiceDIni:indiceDFin]:
                    indiceD = self._listaDiasLaborablesMes.index(dia) # indice en la lista de dias laborables del mes
                    indiceDMatriz = dia-1 # indice en la matrizHorasProgramadas
                    if self._matrizHorasProgramadas[indiceDMatriz][h] != "  ":                    # NO                       APUNTA                          ENTRA
                        if   dia == primerDia and h == 0                                        : # izquierdo superior       derecho inferior    
                            derecho = inferior = True
                        elif dia in self._listaDiasLaborablesMes[1:penultimoIndice] and h == 0  : # superior                 derecho inferior izquierdo
                            derecho = inferior = izquierdo = True
                        elif dia == ultimoDia and h == 0                                        : # derecho superior         izquierdo inferior
                            izquierdo =  inferior = True
                        elif dia == ultimoDia and h in range(1, 23)                             : # derecho                  izquierdo inferior              superior
                            izquierdo = inferior = superior = True
                        elif dia == ultimoDia and h == 23                                       : # derecho inferior         izquierdo                       superior
                            izquierdo = superior = True
                        elif dia in self._listaDiasLaborablesMes[1:penultimoIndice] and h == 23 : # inferior                 izquierdo derecho               superior
                            izquierdo = derecho = superior = True
                        elif dia == primerDia and h == 23                                       : # izquierdo inferior       derecho                         superior
                            derecho = superior = True
                        elif dia == primerDia and h in range(1, 23)                             : # izquierdo                derecho inferior                superior
                            derecho = inferior = superior = True
                        else:     
                            if   indiceDIni == indiceD and hIni == h                            : # izquierdo superior       derecho inferior
                                derecho = inferior = True
                            elif indiceDIni == indiceD and hIni != h                            : # izquierdo                derecho inferior                superior
                                derecho = inferior = superior = True
                            elif indiceDIni != indiceD and hIni == h                            : # superior                 derecho izquierdo inferior
                                derecho = izquierdo = inferior = True
                            else                                                                : #                          izquierdo derecho inferior      superior
                                izquierdo = derecho = inferior = superior = True

                        if superior:
                            capacidad = (self._listaDiasLaborablesMes.index(dFin) - self._listaDiasLaborablesMes.index(dIni)) * (h - hIni)
                            self._matrizDeRectangulos.append(["Dentro", dIni, hIni, dFin, h-1, capacidad])    # ENTRA superior a la matriz de rectangulos
                        if izquierdo:
                            for dl in sorted(self._listaDiasLaborablesMes[indiceD-1: indiceDIni], reverse = True):
                                if self._matrizHorasProgramadas[dl][hIni] == "  ":                        
                                    self._pila.append((dIni, hIni, dl, hFin))                                 # apunta a rectangulo izquierdo
                                    recursividadIz += 1
                                    break
                        if derecho:
                            for dl in self._listaDiasLaborablesMes[indiceD+1: indiceDFin]: 
                                if self._matrizHorasProgramadas[dl][hIni] == "  ":
                                    self._pila.append((dl, hIni, dFin, hFin))                                 # apunta a rectangulo derecho
                                    recursividadDe += 1
                                    break
                        if inferior:
                            for j in range (h+1, hFin):
                                if self._matrizHorasProgramadas[indiceDIni][j] == "  ":
                                    self._pila.append((dIni, j, dFin, hFin))                                  # apunta a rectangulo inferior
                                    recursividadIn += 1
                                    break
                        self.encontrarRectangulo()
                        ban = True
                        break
                if ban:
                    break
            else:
                if indiceDIni <= indiceDFin and hIni <= hFin:
                    capacidad = (self._listaDiasLaborablesMes.index(dFin) - self._listaDiasLaborablesMes.index(dIni)) * (hFin -hIni + 1 )
                    self._matrizDeRectangulos.append(["Fuera ", dIni, hIni, dFin, hFin, capacidad])
                if len(self._pila)>0:
                    self.encontrarRectangulo()
        else:
            return

    # setea la matriz que tiene los dias del mes y las 24 horas del dia, marca fines de semana y festivos como NL -no laborables y establece los evetos programados
    def setMatrizHorasProgramadas(self):
        #  construir la matriz marcando los dias no laborables con "NL"
        self._matrizHorasProgramadas = [[("  " if d+1 in self._listaDiasLaborablesMes else "NL") for h in range(24)] for d in range(self._diasDelMes)]
        # colocar en la matriz anterior los eventos programados
        for evento in self._listaEventos:
            for dia in self._listaDiasLaborablesMes:
                indiceDMatriz = dia-1
                for h in range(24):
                    if self.estaProgramadoElEventoEnDiaHora(evento, dia, h):
                        self._matrizHorasProgramadas[indiceDMatriz][h] = str(f"{evento.id:2d}")

    # Devuelve la matriz de rectangulos disponibles llamado a los metodos setMatrizHorasProgramdas y encontraRectangulos
    def mejoresRectangulosNoProgramados(self):
        self.setMatrizHorasProgramadas() # parte de la matriz de horas programadas
        self._pila = [(self._listaDiasLaborablesMes[0], 0, self._listaDiasLaborablesMes[-1], 23)] # el rectangulo inicial que se sopone libre es todo el mes todas las horas
        self.encontrarRectangulo() 
        rectangulosOrdenadosPorHora = []
        for h in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 4, 5, 6, 7, 19, 20, 21, 2, 3, 22, 0, 23]:
            for r in self._matrizDeRectangulos:
                if  h == r[2] and self._minimoHorasAProgramarPorFicha <= r[5]: # programo los rectangulos que tiene capacidad mayor o igual al minimo de horas a programar por ficha
                     rectangulosOrdenadosPorHora.append(r)
        return rectangulosOrdenadosPorHora

    # Devuelve True si hay fichas con cero programación o si el saldo de horas -generales- por programar es mayor que cero
    def finDeLaProgramacion(self):
        False if len(list(filter(lambda x: self._diccionarioFichas[x] == 0,self._diccionarioFichas.keys()))) > 0 or self._saldoDeHorasAProgramar > 0 else True

    # Para programar los eventos sigo la siguiente logica:
    # 1. Para utilizar los eventos actuales: 
    #   iterar
    #       se asignan horas al mejor evento programable
    #       si la ficha queda programada (al menos el minimo de horas a programar por ficha), se retiran los eventos de la ficha en la lista y se baja el numero de horas a programar
    #       se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas
    # 2. Si hay saldo de horas por programar o fichas programar: 
    #       en todos los eventos que tengan dias por programar que pertenezcan a fichas sin programar se tratará de asignar horas en esos dias
    # 3. se revisan las fichas no programadas para hacer los siguientes ajustes - dando por hecho que se han acabado los eventos originales -:
    #       si hay horas -generales- por programar no hay que quitar programación, 
    #       si se acaban las horas -generales- por programar, hay que quitar dias de las fichas que tienen mayor número de horas para dejar programación a las fichas
    #       se buscar un rectangulo libre de programacion para programar el mínimo de horas por ficha
   
    def programarEventos(self):
        while not self.finDeLaProgramacion():
            # 1.
            self.analisisDiasEventos() 
            (evento, listaDias, horasEvento) = self.buscarMejorEventoProgramable() if not self.buscarMejorEventoProgramable() is None else (None, None, None)
            if evento:
                listaDiasAProgramar = []
                while True:
                    if len(listaDias) > 0:
                        dia = listaDias.pop(0)
                        saldoDeHorasAProgramarDeLaFicha = self._maximoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                        if  self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento:
                            self.marcarEventosDeLaFichaProgramada(evento)
                            break
                        evento.listaDiasAProgramar.append(dia) # programo un dia mas
                        self._saldoDeHorasAProgramar -= horasEvento # disminuyo las horas -generales- a programar
                        self._diccionarioFichas[evento.ficha] += horasEvento # aumento el numero de horas programadas de la ficha                                                       
                    else:
                        saldoDeHorasAProgramarDeLaFicha = self._minimoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                        if  self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento:
                            self.marcarEventosDeLaFichaProgramada(evento)
                        break                                     
                evento.listaDiasAProgramar = listaDiasAProgramar
                evento.listaDiasPorProgram = list(set(listaDias) - set(listaDiasAProgramar)) if len(listaDias) != len(listaDiasAProgramar) else []
            else:       
                # 2.
                for evento in list(filter(lambda e: not e.listaDiasPorProgram is None, self._listaEventos)): # eventos con lista de dias por programar
                    listaDiasPorProgramar = evento.listaDiasPorProgram[:] # copia la lista en otra lista para que se recorran los dias sin las modificacion del cuerpo del for
                    for dia in listaDiasPorProgramar:
                        horasEvento = evento.horaF - evento.horaI
                        saldoDeHorasAProgramarDeLaFicha = self._maximoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]
                        if  not (self._saldoDeHorasAProgramar < horasEvento or saldoDeHorasAProgramarDeLaFicha < horasEvento):
                            evento.listaDiasAProgramar.append(dia)
                            evento.listaDiasPorProgram.remove(dia)
                            self._saldoDeHorasAProgramar -= horasEvento
                            self._diccionarioFichas[evento.ficha] += horasEvento
                # 3. 
                for (ficha, horasProgramadas) in list(filter(lambda item: item[1] < self._minimoHorasAProgramarPorFicha, self._diccionarioFichas.items())): # devuelve tuplas ficha - horas programadas del diccionario de fichas cuando la ficha este programada por debajo del minimo de horas a programar
                    horasAProgramar = self._minimoHorasAProgramarPorFicha - horasProgramadas # calcula el mínimo de horas que le faltan por programar para alcanzar el minimo de horas por Ficha
                    if horasAProgramar > self._saldoDeHorasAProgramar: # si las hora que hacen falta por programar a la ficha son mas que el saldo de horas a programar se deben quitar horas a otra ficha
                        fichaADesprogramar = max(self._diccionarioFichas, key=self._diccionarioFichas.get) # se consigue la ficha con mayor numero de horas programadas
                        eventoADesprogramar = sorted(list(filter(lambda e: e.ficha == fichaADesprogramar and not e.listaDiasAProgramar is None, self._listaEventos)), key =lambda e: len(e.listaDiasAProgramar))[0] # se consigue el evento con mas programacion de la ficha a desprogramar
                        horasEventoADesprogramar = eventoADesprogramar.horaF - eventoADesprogramar.horaI + 1
                        diasMaxAReducir = (horasAProgramar // horasEventoADesprogramar) + 1 
                        diasAReducir = 0
                        for x in range(diasMaxAReducir): 
                            if len(eventoADesprogramar.listaDiasAProgramar) > 0:
                                d = eventoADesprogramar.listaDiasAProgramar.pop() # reducir los dias programados en el evento
                                eventoADesprogramar.listaDiasPorProgram.append(d) # aumentar los dias por programar en el evento  
                                eventoADesprogramar.listaDiasPorProgram.sort() # ordenar la lista de dias dado que el nuevo dia programado queda al final
                                diasAReducir += 1
                        self._diccionarioFichas[fichaADesprogramar] -= horasEventoADesprogramar * diasAReducir # disminuir las horas en el diccionario para la ficha
                        self._saldoDeHorasAProgramar += horasEventoADesprogramar * diasAReducir # aumentar el saldo de horas a Programar
                    # crea un evento para la ficha en el mejor rectangula No programados - incluir este evento en self._listaEventos
                    mejores = self.mejoresRectangulosNoProgramados()
                    while True:
                        if len(mejores) > 0:
                            (indicador, dIni, hIni, dFin, hFin, capacidad) = mejores.pop(0) # extrae el rectangulo de mayor capacidad
                            for e in list(filter(lambda eve: eve.ficha == ficha, self._listaEventos)): # filtra los eventos de la ficha que aun no está programada
                                id = len(self._listaEventos) 
                                #OJO: revisar los diasAProgramar
                                diasAProgramarTentativo = horasAProgramar // (hFin - hIni + 1) # dias que le faltan por programar a la ficha segun las horas del rectangulo que se encontro
                                if  self._saldoDeHorasAProgramar >= self._maximoHorasAProgramarPorFicha: # en este caso se tratará de programar todos los dias del rectangulo
                                    if ((self._listaDiasLaborablesMes.index(dFin) - self._listaDiasLaborablesMes.index(dIni)) + 1) >= diasAProgramarTentativo: # si hay dias suficientes en el rectangulo
                                        diasAProgramar = diasAProgramarTentativo # se toma solo los dias necesarios
                                    else:
                                        diasAProgramar = (self._listaDiasLaborablesMes.index(dFin) - self._listaDiasLaborablesMes.index(dIni)) + 1 # se toman todos los dias del rectangulo
                                else:
                                    diasAProgramar = self._saldoDeHorasAProgramar // (hFin-hIni + 1) # todos las horas faltantes por programar se programan en el rectangulo
                                diaFin = self._listaDiasLaborablesMes[self._listaDiasLaborablesMes.index(dIni) + diasAProgramar]
                                listaDiasLaborables = sorted(list(set(self._listaDiasLaborablesMes) & set(range(dIni, diaFin))))  # setear los dias laborables del evento
                                listaDiasAProgramar = sorted(list(set(self._listaDiasLaborablesMes) & set(range(dIni, diaFin)))) # setear los dias programados hasta el minimo de horas a programar por ficha
        
                                nuevoEvento = Evento(id, ficha, hIni, hFin, date(2023, self._mes, dIni), date(2023, self._mes, diaFin)) 
                                self._listaEventos.append(nuevoEvento) 
                                self._listaEventos[id].listaDiasLaborables = listaDiasLaborables
                                self._listaEventos[id].listaDiasAProgramar = listaDiasAProgramar

                                self.analisisDiasEventos() # esto para inicializar la matriz de eventos de los eventos sin programar

                                horasProgramadas = diasAProgramar * (hFin-hIni+1)
                                if horasProgramadas >= self._minimoHorasAProgramarPorFicha:
                                    self.marcarEventosDeLaFichaProgramada(nuevoEvento)
                                self._diccionarioFichas[ficha] += horasProgramadas # aumentar las horas programadas en el diccionario para la ficha
                                self._saldoDeHorasAProgramar -= horasProgramadas # disminuir el saldo de horas totales a Programar
                                self._matrizDeRectangulos = []
                                mejores = self.mejoresRectangulosNoProgramados()
                                break
            # 4. si no hubo que encontrar rectangulos tambien hay que setea la matriz de horas programaas.
            self.setMatrizHorasProgramadas()
                
# principal 
sys.setrecursionlimit(500000)
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
# Evento(16, 2600000, 9,15, date(2023,4,4), date(2023,4,30)), \
# Evento(17, 2700000, 0, 0, date(2023,4,1), date(2023,4,30)), \

Evento(0, 2674886, 7, 7 , date(2023,5,2), date(2023,5,31)) , \
Evento(1, 2675815, 8, 8 , date(2023,5,2), date(2023,5,31)) , \
Evento(2, 2675816, 9, 9 , date(2023,5,2), date(2023,5,31)) , \
Evento(3, 2675817, 10, 10 , date(2023,5,2), date(2023,5,31)) , \
Evento(4, 2675818, 11, 11 , date(2023,5,2), date(2023,5,31)) , \
Evento(5, 2675819, 12, 12 , date(2023,5,2), date(2023,5,31)) , \
Evento(6, 2675820, 13, 13 , date(2023,5,2), date(2023,5,31)) , \
Evento(7, 2675821, 14, 14 , date(2023,5,2), date(2023,5,31)) , \

]

recursividad = recursividadIz = recursividadDe = recursividadIn = 0

programador = Programador(listaEventos, 5, 160, 10)
programador.programarEventos()

print("*********************************************")
print("************* c o m e n z o *****************")
print("*********************************************")
print(f"recursividad = {recursividad} Izquierdo = {recursividadIz} Derecho = {recursividadDe} Inferior = {recursividadIn}")
print()

print(f"  H a programar: {programador._horasAProgramar} - H por Programar:{programador._saldoDeHorasAProgramar:3d} - Dicionario: {programador._diccionarioFichas}  - Mes: {programador._mes}  - Tolerancia: {programador._tolerancia}%" )
print(" -------------------------------------------------------------------------------------------------------------- ")
print("|  Evento  |   Ficha  |   Horas   |  D In Fi | D labor  | D A Cruz | D L Cruz | D A Prog | D P Prog | Ya Progr | ")
print(" -------------------------------------------------------------------------------------------------------------- ")

for evento in programador._listaEventos:
    print(evento)
    print(" -------------------------------------------------------------------------------------------------------------- ")
print()

print("| hora |", end="")
for i in range(programador._diasDelMes):
    print((f"{i+1}").center(4), end="|")
print()

for h in range(24):
    print(f"|  {h:2d}  |", end="")
    for indiceDMatriz in range(programador._diasDelMes):
        print((f"{programador._matrizHorasProgramadas[indiceDMatriz][h]}").center(4), end="|")
    print()

#print(programador._matrizHorasNoProgramadas)
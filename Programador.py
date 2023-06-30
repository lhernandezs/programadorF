import sys as sys
from Mes import Mes
from Evento import Evento
from Datos import Datos
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
        self._saldoDeHorasAProgramar = horasAProgramar # contiene el saldo de horas aun sin programar
        self._matrizDeEventosSinProgramar = [] # contiene una matriz de 24 horas por cada dia del mes con los eventos sin programar
        self._matrizHorasProgramadas = None # contiene la horas programadas del mes marcando los dias no laborables
        self._matrizDeRectangulos = [] # contiene los "rectangulos" disponibles - horas y dias sin programacion -
        self._pila = [] # contiene la pila de llamadas recursivas para el metodo encontrarRectangulo

    # retorna True si el evento pasa por el dia y la hora pasado como parametros o False en caso contrario
    def estaElEventoEnDiaHora(self, evento, dia, hora):
        fecha = date(2023, self._mes, dia)
        return True if evento.fechaI <= fecha and fecha <= evento.fechaF and evento.horaI <= hora and hora <= evento.horaF else False
    
    # retorna la lista de eventos sin ningun dia programado de las fichas que aún no han sido programadas
    def listaEventosSinProgramar(self):
        return list(filter(lambda evento: len(evento.listaDiasAProgramar) == 0 and not evento.fichaYaProgramada, self._listaEventos))

    # retorna la lista de eventos ya programados de fichas que esten o no totalmente programadas
    def listaEventosProgramados(self):
        return list(filter(lambda evento: len(evento.listaDiasAProgramar) > 0 , self._listaEventos))

    # retorna True si la capacidad es al menos la mitad del mínimo de horas a programar por ficha o False en caso contrario
    def tieneCapacidadMinima(self, capacidad):
        return True if capacidad >= self._minimoHorasAProgramarPorFicha // 2 else False

    # retorna True si el evento esta "programado en el dia y la hora pasado como parametros o False en caso contrario
    def estaProgramadoElEventoEnDiaHora(self, evento, dia, hora):
        return True if not evento.listaDiasAProgramar is None and dia in evento.listaDiasAProgramar and evento.horaI <= hora and hora <= evento.horaF else False

    # setea en True el atributo fichaYaProgramada de todos los eventos que tiene la misma ficha el evento
    def marcarEventosDeLaFichaProgramada(self, evento):
        for e in list(filter(lambda e: evento.ficha == e.ficha, self._listaEventos)): e.fichaYaProgramada = True

    # imprime la matriz de eventos sin programar
    def imprimirMatrizDeEventosSinProgramar(self):
        print("h".center(2), end= "")
        for d in range(self._diasDelMes):
            dia = str(d+1)
            print(dia.center(7),end="")
        print()
        for h in range(24):
            print(str(h).center(2),end="")
            for d in range(self._diasDelMes):
                lista = str(self._matrizDeEventosSinProgramar[d][h]).replace(" ","").replace("[","").replace("]","")
                print(lista.center(7), end="")
            print()
        pass

    # setea la matriz de los eventos sin programar de las fichas que aun no han sido programadas por cada dia y la hora del mes y marca los dias y horas "yp" en los eventos ya programados
    def matrizDeEventosSinProgramar(self):
        matrizDeEventosSinProgramar = [[[] for h in range(24)] for d in range(self._diasDelMes)] # las horas van de 0 a 23 y los dias de 0 al ultimo dia del mes - 1
        if self.listaEventosSinProgramar() != []: 
            for evento in self.listaEventosSinProgramar():
                for h in range(24):
                    for d in range(self._diasDelMes): 
                        dia = d + 1 # el dia es igual al indice d + 1
                        if self.estaElEventoEnDiaHora(evento, dia, h) and dia in self._listaDiasLaborablesMes:
                            matrizDeEventosSinProgramar[d][h].append(evento.id) # añado en cada item -lista - el evento no programado que esta en el dia y la hora 

        if self.listaEventosProgramados() != []:
            for evento in self.listaEventosProgramados():
                for h in range(evento.horaI, evento.horaF + 1):
                    for dia in evento.listaDiasAProgramar:
                        d = dia - 1 # el indice es igual al dia - 1
                        matrizDeEventosSinProgramar[d][h] = ["yp"] # marca los eventos ya programados en su dia y hora como "yp" - ya programado -                    
        self._matrizDeEventosSinProgramar = matrizDeEventosSinProgramar
#        self.imprimirMatrizDeEventosSinProgramar()

    # setea las listas de dias laborables, dias no disponibles, dias antes de cruce y dias luego de cruce de los eventos sin programar   
    def analisisDiasEventos(self):
        self.matrizDeEventosSinProgramar()
        conjuntoDiasLaborablesMes = set(self._listaDiasLaborablesMes) # prepara este conjunto para la intersección
        for evento in self.listaEventosSinProgramar():
            diaIniEvento = 1 if (evento.fechaI < date(2023, self._mes, 1)) else evento.fechaI.day # controla si el inicio del evento es antes del 1er dia del mes
            diaFinEvento = self._diasDelMes if (self._ultimaFecMes < evento.fechaF) else evento.fechaF.day # controla si el fin del evento es despues del ultimo dia del mes

            fecIniCruce = fecFinCruce = fecIniNoDis = fecFinNoDis = None

            for h in range(24):
                for d in range(self._diasDelMes):
                    dia = d + 1 # el dia es igual al indice d + 1
                    if self.estaElEventoEnDiaHora(evento, dia, h):

                        if self._matrizDeEventosSinProgramar[d][h] == ["yp"]: # si el evento cruza con otro evento ya programado
                            if fecIniNoDis is None or date(2023, self._mes, dia) < fecIniNoDis: fecIniNoDis = date(2023, self._mes, dia) # encuentro la menor fecha inicial
                            if fecFinNoDis is None or date(2023, self._mes, dia) > fecFinNoDis: fecFinNoDis = date(2023, self._mes, dia) # encuentro la mayor fecha final

                        if len(self._matrizDeEventosSinProgramar[d][h]) > 1: # si el evento no esta solo, o sea hay mas de un evento sin programar en ese dia y hora
                            if fecIniCruce is None or date(2023, self._mes, dia) < fecIniCruce: fecIniCruce = date(2023, self._mes, dia) # encuentro la menor fecha inicial
                            if fecFinCruce is None or date(2023, self._mes, dia) > fecFinCruce: fecFinCruce = date(2023, self._mes, dia) # encuentro la mayor fecha final

            listaDiasIniFinEven = [dia for dia in range(diaIniEvento, diaFinEvento + 1)] # como en los rangos el valor final no se incluye se suma 1 al final - dias corrientes -

            listaDiasAntesNoDis = listaDiasIniFinEven if fecIniNoDis is None else [dia for dia in range(diaIniEvento, fecIniNoDis.day)] # no se tiene en cuenta el dia inicio cruce - dias corrientes -
            listaDiasLuegoNoDis = [] if fecFinNoDis is None else [dia for dia in range(fecFinNoDis.day + 1, diaFinEvento + 1)] # no se tiene en cuenta el dia final cruce - dias corrientes -

            listaDiasAntesCruce = listaDiasIniFinEven if fecIniCruce is None else [dia for dia in range(diaIniEvento, fecIniCruce.day)] # no se tiene en cuenta el dia inicio cruce - dias corrientes -
            listaDiasLuegoCruce = [] if fecFinCruce is None else [dia for dia in range(fecFinCruce.day + 1, diaFinEvento + 1)] # no se tiene en cuenta el dia final cruce - dias corrientes -

            self._listaEventos[evento.id].listaDiasLaborables = list(set(listaDiasIniFinEven) & conjuntoDiasLaborablesMes) # setea la lista de dias laborables del evento
            self._listaEventos[evento.id].listaDiasAntesNoDis = list(set(listaDiasAntesNoDis) & conjuntoDiasLaborablesMes) # setea la lista de dias antes de no disponible
            self._listaEventos[evento.id].listaDiasLuegoNoDis = list(set(listaDiasLuegoNoDis) & conjuntoDiasLaborablesMes) # setea la lista de dias despues de no disponble
            self._listaEventos[evento.id].listaDiasAntesCruce = list(set(listaDiasAntesCruce) & conjuntoDiasLaborablesMes) # setea la lista de dias antes de cruce
            self._listaEventos[evento.id].listaDiasLuegoCruce = list(set(listaDiasLuegoCruce) & conjuntoDiasLaborablesMes) # setea la lista de dias despues de cruce
   
    # recibe un evento y un booleano que indica si hay que usar toda la lista de dias laborables
    # retorna una tupla con la capacidad de horas a programar en el evento, la lista mas larga de dias programables y la duracion en horas
    def capacidadEvento(self, evento, calcularSolo):
        horasEvento = evento.horaF - evento.horaI + 1 # se parte que si un evento tiene la misma hora de inicio y de fin, el evento dura una hora
        if calcularSolo:
            listaDiasPreliminar = evento.listaDiasLaborables
        else:
            listaDiasPreliminar = lA if len(lA := evento.listaDiasAntesCruce) > len(lL := evento.listaDiasLuegoCruce) else lL  # se toman la lista mayor de los dias que no se cruzan
        
        listaDiasAntes = list((set(listaDiasPreliminar) & set(evento.listaDiasAntesNoDis)))
        listaDiasLuego = list((set(listaDiasPreliminar) & set(evento.listaDiasLuegoNoDis)))

        listaDias = listaDiasAntes if len(listaDiasAntes) > len(listaDiasLuego) else listaDiasLuego

        capacidad = horasEvento * len(listaDias)
        return (capacidad, listaDias, horasEvento)
    
    # busca el mejor evento programable que se define asi: tiene la capacidad mas grande entre los eventos sin programar de fichas sin programar
    # retorna el evento, la lista de dias a programar y las horas
    def buscarMejorEventoProgramable(self):
        self.analisisDiasEventos() # para asegurar que trabajamos con los eventos sin programar y estan bien seteadas las lista de dias antes y luego de cruce 
        for cardinalidad in range(1, len(self._listaEventos)): # se procesan los eventos de cardinalidad 1, luego 2, luego 3, etc.
            items = [self._matrizDeEventosSinProgramar[d][h] for h in range(24) for d in range(self._diasDelMes)] # cada item es una lista de eventos presentes en dia y hora
            listasDeIdsEventos = list(filter(lambda item: len(item) == cardinalidad and item != ["yp"] and item != [], items )) # filtro que la cardinalidad se la del for y que el item no sea "yp" o vacio
            if listasDeIdsEventos != []:
                diccDeIdsEventos={}
                for l in listasDeIdsEventos: # inicializar las claves del diccionario y los valores en cero
                    il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
                    diccDeIdsEventos[il] = 0
                for l in listasDeIdsEventos: # contar las veces que se repite el los id de eventos cruzados
                    il = str(l).replace("[","").replace("]","").replace(",","_").replace(" ","")
                    diccDeIdsEventos[il] += 1
                diccDeIdsEventos_sorted = dict(sorted(diccDeIdsEventos.items(), key=lambda item:item[1], reverse=True))
                for cruceMasRepetido in diccDeIdsEventos_sorted.keys():
                    listaTuplas = []
                    for idStr in cruceMasRepetido.split("_"):
                        id = int(idStr)
                        evento = self._listaEventos[id]
                        if cardinalidad == 1:
                            (capacidad, listaDias, horasEvento) = self.capacidadEvento(evento, False) # se pasa False para calcular capacidad con los dias Antes o Luego del cruce 
                            if  listaDias == []:
                                continue
                        else:
                            (capacidad, listaDias, horasEvento) = self.capacidadEvento(evento, True)# se pasa False para calcular capacidad con todos los dias laborables - simulando que no hay cruces
                        if self.tieneCapacidadMinima(capacidad):
                            listaTuplas.append((evento, capacidad, listaDias, horasEvento))
                        else:
                            continue 
                    if listaTuplas != []:
                        (evento, capacidad, listaDias, horasEvento)= (list(sorted(listaTuplas, key=lambda tupla: -tupla[1])))[0] # escoje el evento de mayor capacidad
                        return (evento, listaDias, horasEvento)                    
        else:
            return (None, None, None)

    # metodo que encuentra los "rectangulos" que estan disponibles y los setea en la matriz de rectangulos
    def encontrarRectangulo(self):
        global recursividadTo 
        global recursividadIz
        global recursividadDe
        global recursividadIn
        
        recursividadTo += 1
        ban = False

        if len(self._pila) > 0:
            (dIni, hIni, dFin, hFin) = self._pila.pop()

            indiceDIni = self._listaDiasLaborablesMes.index(dIni)
            indiceDFin = self._listaDiasLaborablesMes.index(dFin)

            superio = izquier = derecho = inferio = False
          
            for h in range(hIni, hFin + 1): # las horas van desde la inicial hasta la final + 1
                
                for dia in self._listaDiasLaborablesMes[indiceDIni:(indiceDFin + 1)]: # los dias van desde el inicial hasta el final + 1

                    indiceDia = self._listaDiasLaborablesMes.index(dia) # indice del dia en la lista de dias laborables del mes

                    d = dia - 1 # indice en la matrizHorasProgramadas es igual al dia - 1

                    if self._matrizHorasProgramadas[d][h] != "  ": # en la matriz busco los datos correspondiente a d y h
                                                                                                              # NO                       APUNTA                          ENTRA
                        if   dia == dIni and h == hIni                                                      : # izquierdo superior       derecho inferior    
                            derecho = inferio = True
                        elif dia == dFin and h == hIni                                                      : # derecho superior         izquierdo inferior
                            izquier = inferio = True
                        elif dia == dFin and h == hFin                                                      : # derecho inferior         izquierdo                       superior
                            izquier = superio = True
                        elif dia == dIni and h == hFin                                                      : # izquierdo inferior       derecho                         superior
                            derecho = superio = True

                        elif dia in self._listaDiasLaborablesMes[(indiceDIni + 1): indiceDFin] and h == hIni  : # superior                 derecho inferior izquierdo
                            derecho = inferio = izquier = True
                        elif dia in self._listaDiasLaborablesMes[(indiceDIni + 1): indiceDFin] and h == hFin  : # inferior                 izquierdo derecho               superior
                            izquier = derecho = superio = True

                        elif dia == dIni and h in range((hIni + 1), hFin)                                     : # izquierdo                derecho inferior                superior
                            derecho = inferio = superio = True
                        elif dia == dFin and h in range((hIni + 1), hFin)                                     : # derecho                  izquierdo inferior              superior
                            izquier = inferio = superio = True

                        else:     
                            izquier = derecho = inferio = superio = True                                      #                          izquierdo derecho inferior      superior

                        if superio:
                            capacidad = (indiceDFin - indiceDIni + 1) * (h - hIni) # contar dias laborables desde el inicio hasta el fin + 1
                            self._matrizDeRectangulos.append(["Dentr", dIni, hIni, dFin, (h - 1), capacidad])    # ENTRA superior a la matriz de rectangulos
                        if izquier:
                            for dl in sorted(self._listaDiasLaborablesMes[indiceDIni: indiceDia], reverse = True):
                                if self._matrizHorasProgramadas[dl][h] == "  ":                        
                                    self._pila.append((dIni, hIni, dl, hFin))                                 # apunta a rectangulo izquierdo
                                    recursividadIz += 1
                                    break
                        if derecho:
                            for dl in self._listaDiasLaborablesMes[(indiceDia + 1): indiceDFin]: 
                                if self._matrizHorasProgramadas[dl][h] == "  ":
                                    self._pila.append((dl, hIni, dFin, hFin))                                 # apunta a rectangulo derecho
                                    recursividadDe += 1
                                    break
                        if inferio:
                            for hl in range (h+1, hFin):
                                if self._matrizHorasProgramadas[d][hl] == "  ":
                                    self._pila.append((dIni, hl, dFin, hFin))                                 # apunta a rectangulo inferior
                                    recursividadIn += 1
                                    break

                        self.encontrarRectangulo()
                        ban = True
                        break
                if ban:
                    break
            else:
                if indiceDIni <= indiceDFin and hIni <= hFin:
                    capacidad = (indiceDFin - indiceDIni + 1) * (hFin -hIni + 1 )
                    self._matrizDeRectangulos.append(["Fuera", dIni, hIni, dFin, hFin, capacidad])
                
                if len(self._pila)>0:
                    self.encontrarRectangulo()
        else:
            return

    # setea la matriz que tiene los y establece los eventos programados en sus dias y horas, marca fines de semana y festivos como NL - no laborables - 
    def setMatrizHorasProgramadas(self):
        self._matrizHorasProgramadas = [[("  " if d + 1 in self._listaDiasLaborablesMes else "NL") for h in range(24)] for d in range(self._diasDelMes)] # construir la matriz marcando los dias no laborables con "NL"
        for evento in self._listaEventos: # colocar en la matriz anterior los eventos programados
            for h in range(24):
                for dia in self._listaDiasLaborablesMes:
                    d = dia - 1 # el indice d es igual al dia - 1
                    if self.estaProgramadoElEventoEnDiaHora(evento, dia, h):
                        self._matrizHorasProgramadas[d][h] = str(f"{evento.id:2d}")

    # retorna una matriz de rectangulos disponibles llamado a los metodos setMatrizHorasProgramdas y encontraRectangulos
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

    # retorna True si noy hay fichas con cero programación o si el saldo de horas -generales- por programar es mayor que cero
    def finDeLaProgramacion(self):
        return True if len(list(filter(lambda x: self._diccionarioFichas[x] == 0,self._diccionarioFichas.keys()))) == 0 and self._saldoDeHorasAProgramar == 0 else False

    # para programar los eventos sigo la siguiente logica:
    # 1. con el objetivo de utilizar los eventos actuales: 
    #   iterar
    #       se asignan horas al mejor evento programable
    #       si la ficha queda programada (al menos el minimo de horas a programar por ficha), se retiran los eventos de la ficha en la lista y se baja el numero de horas a programar
    #       se vuelve a iterar hasta que no sea posible asignar mas horas a las fichas
    # 2. si hay saldo de horas por programar o fichas programar: 
    #       en todos los eventos que tengan dias por programar que pertenezcan a fichas sin programar se tratará de asignar horas en esos dias
    # 3. se revisan las fichas no programadas para hacer los siguientes ajustes - dando por hecho que se han acabado los eventos originales -:
    #       si hay horas -generales- por programar suficientes no hay que quitar programación, 
    #       si se acaban las horas -generales- por programar, hay que quitar dias de las fichas que tienen mayor número de horas para poder programar las fichas que aun resta,
    #       se buscar un rectangulo libre de programacion para programar las horas por ficha, creando un evento en ese rectangulo
    def programarEventos(self):
        iter = 1
        while not self.finDeLaProgramacion() and iter == 1:
#            iter = 0
            # 1.
            while True:
                (evento, listaDias, horasEvento) = self.buscarMejorEventoProgramable()
                if not evento is None:
                    listaDiasAProgramar = []
                    while True:
                        horasFaltantesDeLaFicha = self._maximoHorasAProgramarPorFicha - self._diccionarioFichas[evento.ficha]

                        if  horasFaltantesDeLaFicha < horasEvento: # termina porque no es posible programar un dia mas en el evento; se deben marcar los eventos de la ficha como programados
                            self.marcarEventosDeLaFichaProgramada(evento) 
                            break

                        if self._saldoDeHorasAProgramar < horasEvento: # termina por que no hay horas en el saldo total por programar 
                            break

                        if len(listaDias) == 0: # termina porque no hay mas dias en la lista de dias para programar; revisar si se deben marcar los evento y la ficha como ya programados
                            if self._minimoHorasAProgramarPorFicha < self._diccionarioFichas[evento.ficha]:
                                self.marcarEventosDeLaFichaProgramada(evento)
                            break

                        else: # si paso hasta aqui, hay horas faltantes en la ficha, hay saldo total de horas y hay dias en la lista; programar un dia mas -- en el proximo ciclo se revisa si la ficha queda programada
                            dia = listaDias.pop(0)
                            evento.listaDiasAProgramar.append(dia) # programo el dia que sigue en la lista
                            self._saldoDeHorasAProgramar -= horasEvento # disminuyo las horas -generales- a programar
                            self._diccionarioFichas[evento.ficha] += horasEvento # aumento el numero de horas programadas                                                      
                    
                    evento.listaDiasPorProgram = list(set(listaDias) - set(listaDiasAProgramar)) if len(listaDias) != len(listaDiasAProgramar) else []     
                else:
                    break

            # 2.
            self.analisisDiasEventos() # para asegurar que trabajamos con los eventos sin programar y estan bien seteadas las lista de dias antes y luego de cruce 
            eventosConListaDiasPorProgramar = list(filter(lambda e: len(e.listaDiasPorProgram)> 0, self._listaEventos)) # eventos con lista de dias por programar de fichas programadas o no
            banHayHoras = True
            while len(eventosConListaDiasPorProgramar) > 0 and banHayHoras:
                evento = eventosConListaDiasPorProgramar.pop()
                ban = True # la bandera me sirve para mirar si la lista de dias por programar del evento esta libre de programación
                self.setMatrizHorasProgramadas() # coloco los eventos programados en la matriz
                for h in range(evento.horaI, (evento.horaF + 1)):
                    for dia in evento.listaDiasPorProgram:
                        d = dia - 1  # el indice en la matriz es igual al dia - 1
                        if self._matrizHorasProgramadas[d][h] != "  ": ban = False # colocamos la bandera en falso porque en las horas del evento hay dias que ya están programados - no utlizaremos la lista

                if ban:
                    listaDiasPorProgramar = evento.listaDiasPorProgram[:] # copia la lista en otra lista para que se recorran los dias sin las modificacion del cuerpo del for
                    for dia in listaDiasPorProgramar:
                        horasEvento = evento.horaF - evento.horaI + 1
                        if  self._saldoDeHorasAProgramar >= horasEvento: # solo controlo que haya saldo de horas totales por programar -- no importa si la ficha se pasa del tope
                            evento.listaDiasAProgramar.append(dia)
                            evento.listaDiasPorProgram.remove(dia)
                            self._saldoDeHorasAProgramar -= horasEvento
                            self._diccionarioFichas[evento.ficha] += horasEvento
                        else:
                            banHayHoras = False
                    
            # 3. 
            for (ficha, horasProgramadas) in list(filter(lambda item: item[1] < self._minimoHorasAProgramarPorFicha, self._diccionarioFichas.items())): # devuelve tuplas ficha - horas programadas del diccionario de fichas cuando la ficha este programada por debajo del minimo de horas a programar
                maxHorasAProgramarEnLaFicha = self._maximoHorasAProgramarPorFicha - horasProgramadas
                maxHorasAProgramar = maxHorasAProgramarEnLaFicha if maxHorasAProgramarEnLaFicha < self._saldoDeHorasAProgramar else self._saldoDeHorasAProgramar # calcula el maximo numero de horas que se podrían programar en la ficha
    
                horasAProgramar = maxHorasAProgramar if maxHorasAProgramar > self._minimoHorasAProgramarPorFicha else self._minimoHorasAProgramarPorFicha

                if horasAProgramar > self._saldoDeHorasAProgramar: # si las horas que hacen falta por programar a la ficha son mas que el saldo de horas a programar se deben quitar horas a otra ficha
                    fichaADesprogramar = max(self._diccionarioFichas, key=self._diccionarioFichas.get) # se consigue la ficha con mayor numero de horas programadas
                    eventoADesprogramar = sorted(list(filter(lambda e: e.ficha == fichaADesprogramar and len(e.listaDiasAProgramar) > 0, self._listaEventos)), key =lambda e: len(e.listaDiasAProgramar))[-1] # se consigue el evento con mas dias programados de la ficha a desprogramar
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

                # crea un evento para la ficha en el mejor rectangulo No programados - incluir este evento en self._listaEventos
                ban = True
                while ban:
                    self._matrizDeRectangulos = [] # reinicio la matriz de rectangulos
                    mejores = self.mejoresRectangulosNoProgramados() # busco los mejores rectangulos
                    if len(mejores) > 0:
                        (indicador, dIni, hIni, dFin, hFin, capacidad) = mejores.pop(0) # extrae el rectangulo de mayor capacidad

                        if capacidad >= horasAProgramar:

                            for h in range (hIni, hFin + 1):
                                listaDias = []
                                horasProgramadas = horasAProgramar
                                if ban:
                                    for dia in self._listaDiasLaborablesMes[self._listaDiasLaborablesMes.index(dIni) : self._listaDiasLaborablesMes.index(dFin) + 1 ]:
                                        listaDias.append(dia)
                                        horasEvento = h - hIni + 1
                                        horasProgramadas -= horasEvento
                                        if horasProgramadas <= horasEvento:
                                            id = len(self._listaEventos) # el id del nuevo evento será el numero de eventos actual - los id de los eventos empiezan en cero -
                                            evento = Evento(id, ficha, hIni, h, date(2023, self._mes, dIni), date(2023, self._mes, dia)) 
                                            self._listaEventos.append(evento) 
                                            evento.listaDiasAProgramar = listaDias # programo el dia que sigue en la lista
                                            evento.listaDiasPorProgram = []     
                                            self._saldoDeHorasAProgramar -= (h - hIni + 1) * len(listaDias) # disminuyo las horas -generales- a programar
                                            self._diccionarioFichas[evento.ficha] += (h - hIni + 1) * len(listaDias) # aumento el numero de horas programadas                                                      
                                            self.analisisDiasEventos() # esto para inicializar la matriz de eventos de los eventos sin programar
                                            self.marcarEventosDeLaFichaProgramada(evento) 
                                            ban = False
                                            break
                                else:
                                    break
                    else:
                        break

            # 4. Si el numero de horas Programadas es menor que cero
            while self._saldoDeHorasAProgramar < 0:
                listaFichasOrdenada = list(dict(sorted(self._diccionarioFichas.items(), key=lambda item:item[1], reverse=True)).items())
                ban= True
                while ban:
                    (ficha, horasProgramadas) = listaFichasOrdenada.pop(0)
                    l= list(filter(lambda e: e.ficha == ficha, self._listaEventos))
                    listaEventosFicha = sorted(list(filter(lambda e: e.ficha == ficha, self._listaEventos)), key=lambda evento: len(evento.listaDiasAProgramar), reverse =True)
                    while True:
                        if len(listaEventosFicha) > 0:
                            evento = listaEventosFicha.pop(0)
                            horasEvento = evento.horaF - evento.horaI + 1
                            if self._saldoDeHorasAProgramar % horasEvento == 0 and (len(evento.listaDiasAProgramar) * horasEvento) >= -self._saldoDeHorasAProgramar:
                                copiaListaDiasAProgramar = evento.listaDiasAProgramar
                                for dia in evento.listaDiasAProgramar:
                                    if self._saldoDeHorasAProgramar < 0:
                                        d = copiaListaDiasAProgramar.pop()
                                        evento.listaDiasPorProgram.append(d)
                                        self._saldoDeHorasAProgramar += horasEvento
                                        self._diccionarioFichas[evento.ficha] -= horasEvento
                                evento.listaDiasAProgramar = copiaListaDiasAProgramar
                                ban = False
                                break
                        else:
                            break


            # 5. si no hubo que encontrar rectangulos tambien hay que setea la matriz de horas programadas para poder mostrar el resultado.
            self.setMatrizHorasProgramadas()
                
# principal 
# establezco la recursividad para el interprete especialmente para el metodo de rectangulos libres
sys.setrecursionlimit(500000)
recursividadTo = recursividadIz = recursividadDe = recursividadIn = 0

# fijo los datos de prueba del programa
mes = 7
listaEventos = Datos(mes).listaEventos8
horasAProgramar = 160
tolerancia = 20
programador = Programador(listaEventos, mes, horasAProgramar, tolerancia)

# llamo al metodo de programar eventos
programador.programarEventos()

# salida en pantalla 

# imprimo la recusividad utilizada
print(f"recursividad = {recursividadTo} Izquierdo = {recursividadIz} Derecho = {recursividadDe} Inferior = {recursividadIn}", end="\n"*2)

# imprimo los datos de entrada y el diccionario de fichas
print(f" H a programar: {horasAProgramar} - H por Programar: {programador._saldoDeHorasAProgramar} - Mes: {mes} - Tolerancia: {tolerancia}%" )
print(f" Dicionario:{programador._diccionarioFichas}"  )

# imprimo los eventos
linea = " " + "-"*142 + " " 
# encabezado
print(linea)
print(Evento.encabezado())
print(linea)
# cuerpo
for evento in programador._listaEventos:
    print(evento)
    print(linea)

print()

# imprimo la matriz de horas programadas
# encabezado
print("|" + "hora".center(6) + "|", end="")
for d in range(programador._diasDelMes):
    dia = d + 1 # el dia es igual al indice d + 1
    print((f"{dia}").center(4), end="|")

print()

# cuerpo
for h in range(24):
    print(f"|" + str(h).center(6) + "|", end="")
    for d in range(programador._diasDelMes):
        print((f"{programador._matrizHorasProgramadas[d][h]}").center(4), end="|")
    print()

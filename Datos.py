from Evento import Evento
from datetime import date

class Datos:

        def __init__(self, mes):

                self.listaEventos1 = [ \
                                Evento(0, 1, 6, 8, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(1, 1, 10, 11, date(2023,mes,9), date(2023,mes,20)), \
                                Evento(2, 2, 6, 7, date(2023,mes,10), date(2023,mes,26)), \
                                Evento(3, 2, 8, 9, date(2023,mes,1), date(2023,mes,28)), \
                                Evento(4, 3, 9, 11, date(2023,mes,1), date(2023,mes,23)), \
                                Evento(5, 3, 12, 13, date(2023,mes,10), date(2023,mes,28)), \
                                ]

                self.listaEventos2 = [ \
                                Evento(0, 2675758, 6, 6, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(1, 2675759, 7, 7, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(2, 2626937, 12, 13, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(3, 2626938, 7, 8, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(4, 2626939, 9, 10, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(5, 2626940, 7, 7, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(6, 2675911, 12, 12, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(7, 2675912, 20, 21, date(2023,mes,1), date(2023,mes,30)), \
                                Evento(8, 2600000, 9, 11, date(2023,mes,5), date(2023,mes,30)), \
                                Evento(9, 2700000, 0, 0, date(2023,mes,1), date(2023,mes,30)), \
                                ]

                self.listaEventos3 = [ \
                                Evento(0, 2674886, 7, 7 , date(2023,mes,2), date(2023,mes,31)) , \
                                Evento(1, 2675815, 8, 8 , date(2023,mes,2), date(2023,mes,31)) , \
                                Evento(2, 2675816, 9, 9 , date(2023,mes,2), date(2023,mes,31)) , \
                                Evento(3, 2675817, 10, 10 , date(2023,mes,2), date(2023,mes,31)) , \
                                ]

                # self.listaEventos4 = [ \
                #                 Evento(0, 2674886, 7, 7 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(1, 2675815, 8, 8 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(2, 2675816, 9, 9 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(3, 2675817, 10, 10 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(4, 2675818, 11, 11 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(5, 2675819, 12, 12 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(6, 2675820, 13, 13 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 Evento(7, 2675821, 14, 14 , date(2023,mes,2), date(2023,mes,31)) , \
                #                 ]

                self.listaEventos5 = [ \
                                Evento(0, 2674886, 7, 7 , date(2023,mes,1), date(2023,mes,31)) , \
                                Evento(1, 2675815, 8, 8 , date(2023,mes,1), date(2023,mes,20)) , \
                                Evento(2, 2675816, 9, 9 , date(2023,mes,2), date(2023,mes,12)) , \
                                ]

                self.listaEventos6 = [ \
                                Evento(0, 2626941, 10, 11 , date(2023,7,1), date(2023,7,31)) , \
                                Evento(1, 2626942, 6, 7 , date(2023,7,1), date(2023,7,31)) , \
                                Evento(2, 2626943, 8, 9 , date(2023,7,1), date(2023,7,31)) , \
                                Evento(3, 2675746, 12, 16 , date(2023,7,1), date(2023,7,31)) , \
                                ]
                
                self.listaEventos7 = [ \
                                Evento(0, 2627073, 8, 8, date(2023,7,1), date(2023,7,31)), \
                                Evento(1, 2675815, 7, 7, date(2023,7,1), date(2023,7,31)), \
                                Evento(2, 2675815, 14, 15, date(2023,7,1), date(2023,7,31)), \
                                Evento(3, 2675815, 10, 10, date(2023,7,1), date(2023,7,31)), \
                                Evento(4, 2675816, 13, 14, date(2023,7,1), date(2023,7,31)), \
                                Evento(5, 2675816, 8, 8, date(2023,7,1), date(2023,7,31)), \
                                Evento(6, 2675817, 9, 9, date(2023,7,1), date(2023,7,31)), \
                                Evento(7, 2675818, 10, 10, date(2023,7,1), date(2023,7,31)), \
                ]

                self.listaEventos8 = [ \
                                Evento(0, 2626895, 6, 7, date(2023,7,1), date(2023,7,31)), \
                                Evento(1, 2626896, 8, 9, date(2023,7,1), date(2023,7,31)), \
                                Evento(2, 2626901, 12, 12, date(2023,7,1), date(2023,7,31)), \
                                Evento(3, 2626902, 7, 7, date(2023,7,1), date(2023,7,31)), \
                                Evento(4, 2626902, 13, 13, date(2023,7,1), date(2023,7,31)), \
                                Evento(5, 2675717, 10, 11, date(2023,7,1), date(2023,7,31)), \
                                Evento(6, 2675717, 6, 6, date(2023,7,1), date(2023,7,31)), \
                ]

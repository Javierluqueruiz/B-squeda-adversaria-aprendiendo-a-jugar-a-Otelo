import copy

class AgenteMinimax: 
    def __init__(self, jugadorIA, profundidad_maxima):
        self.jugadorIA = jugadorIA
        self.profundidad_maxima = profundidad_maxima

    def heuristica(self, partida):

        blancas, negras = partida.calcular_puntuacion()
        if self.jugadorIA == 1:
            puntuacion = blancas - negras
        else:
            puntuacion = negras - blancas

        return puntuacion
    

    def obtener_mejor_movimiento(self, partida):
        alfa = -float('inf')
        beta = float('inf')

        movimientos = partida.obtener_movimientos_validos(self.jugadorIA)
        mejor_puntuacion = -float('inf')
        movimiento_max = None

        for movimiento in movimientos:
            partida_copia = copy.deepcopy(partida)
            f, c = movimiento
            partida_copia.ejecutar_movimiento(f, c, self.jugadorIA)

            evaluacion = self._minimax_alfa_beta(partida_copia, self.profundidad_maxima, alfa, beta, True)
            if evaluacion > mejor_puntuacion:
                mejor_puntuacion = evaluacion
                movimiento_max = movimiento

        return movimiento_max



    def _minimax_alfa_beta(self, partida, profundidad, alfa, beta, maximizando):
 
        if partida.es_fin_de_juego() == True or profundidad == 0:
            return self.heuristica(partida)
        
        if maximizando:
            movimientos = partida.obtener_movimientos_validos(self.jugadorIA)
            if len(movimientos) == 0:
                return self._minimax_alfa_beta(partida, profundidad-1, alfa, beta, False)
            max_eval = -float('inf')
            for movimiento in movimientos:
                partida_copia = copy.deepcopy(partida)
                f, c  = movimiento
                partida_copia.ejecutar_movimiento(f, c, self.jugadorIA)

                evaluacion = self._minimax_alfa_beta(partida_copia, profundidad - 1, alfa, beta, False)

                max_eval = max(max_eval, evaluacion)
                
                alfa = max(alfa, max_eval)
                if beta <= alfa:
                    break

            return max_eval
        else:
            oponente = 1 if self.jugadorIA == 2 else 2
            movimientos = partida.obtener_movimientos_validos(oponente)

            if len(movimientos) == 0:
                return self._minimax_alfa_beta(partida, profundidad-1, alfa, beta, True)
            min_eval = float('inf')

            for movimiento in movimientos:
                f, c = movimiento
                partida_copia = copy.deepcopy(partida)
                partida_copia.ejecutar_movimiento(f, c, oponente)

                evaluacion = self._minimax_alfa_beta(partida_copia, profundidad-1, alfa, beta, True)

                min_eval = min(min_eval, evaluacion)
                beta = min(beta, min_eval)
                if alfa >= beta:
                    break

            return min_eval

import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import copy
import random
import numpy as np
from keras.models import load_model


class AgenteMinimax: 
    def __init__(self, jugadorIA, profundidad_maxima, usar_red=True):

        #Inicializar el agente inteligente. 
        self.jugadorIA = jugadorIA # 1 para fichas blancas, 2 para fichas negras
        self.profundidad_maxima = profundidad_maxima # Límite del árbol de búsqueda
        self.usar_red = usar_red 

        #Posibilidad de elegir entre usar la red neuronal o la heurística clásica
        if self.usar_red:
            self.modelo = load_model("modelos/otelo_B.keras")
        else: 
            self.modelo = None


    def heuristica(self, partida):
        """
        Evalúa el estado actual del tablero y devuelve una puntuación que refleja la ventaja del agente sobre el oponente.
        """
        
        if self.usar_red:   
            # Preparar el tablero para la red neuronal y obtener la predicción
            tablero = np.expand_dims(partida.tablero, axis=0)
            prediccion = self.modelo(tablero, training=False).numpy()
            nota = prediccion[0][0]

            if self.jugadorIA == 1:
                puntuacion = nota
            else:
                puntuacion = -nota

            return puntuacion
        else:
            # Heurística clásica: diferencia de fichas
            blancas, negras = partida.calcular_puntuacion()
            if self.jugadorIA == 1:
                puntuacion =  blancas - negras
            else:
                puntuacion =  negras - blancas
            return puntuacion

    def obtener_mejor_movimiento(self, partida):
        """
        Obtiene el mejor movimiento para el agente basado en el algoritmo Minimax con Poda Alfa-Beta.
        """
        alfa = -float('inf')
        beta = float('inf')

        movimientos = partida.obtener_movimientos_validos(self.jugadorIA)
        mejor_puntuacion = -float('inf')
        mejores_movimientos = []

        # Simulamos cada movimiento posible 
        for movimiento in movimientos:
            # Hacemos una copia para no alterar el tablero que ve el jugador humano
            partida_copia = copy.deepcopy(partida)
            f, c = movimiento
            partida_copia.ejecutar_movimiento(f, c, self.jugadorIA)

            # Evaluamos el movimiento usando Minimax con Poda Alfa-Beta
            evaluacion = self._minimax_alfa_beta(partida_copia, self.profundidad_maxima-1, alfa, beta, False)
            
            #Si encontramos un movimiento mejor, lo guardamos. Si hay empate, lo añadimos a la lista de mejores movimientos
            if evaluacion > mejor_puntuacion:
                mejor_puntuacion = evaluacion
                mejores_movimientos.clear()
                mejores_movimientos.append(movimiento)
            elif evaluacion == mejor_puntuacion:
                mejores_movimientos.append(movimiento)

        # Seleccionamos aleatoriamente uno de los mejores movimientos para evitar patrones repetitivos  
        if len(mejores_movimientos) != 0:
            return random.choice(mejores_movimientos)
        else:
            return None



    def _minimax_alfa_beta(self, partida, profundidad, alfa, beta, maximizando):
        """
        Función recursiva que implementa el algoritmo Minimax con Poda Alfa-Beta para evaluar los posibles movimientos. 
        """
        # Condición de parada
        if partida.es_fin_de_juego() == True or profundidad == 0:
            return self.heuristica(partida)
        
        if maximizando:
            # Turno del agente (MAX)
            movimientos = partida.obtener_movimientos_validos(self.jugadorIA)
            # Si no tiene movimientos, le pasa el turno a MIN 
            if len(movimientos) == 0:
                return self._minimax_alfa_beta(partida, profundidad-1, alfa, beta, False)
            max_eval = -float('inf')
            for movimiento in movimientos:
                partida_copia = copy.deepcopy(partida)
                f, c  = movimiento
                partida_copia.ejecutar_movimiento(f, c, self.jugadorIA)
                
                #Evaluamos el subárbol pasandole el turno al oponente (MIN)
                evaluacion = self._minimax_alfa_beta(partida_copia, profundidad - 1, alfa, beta, False)

                max_eval = max(max_eval, evaluacion)
                alfa = max(alfa, max_eval)

                # Si el peor caso de MIN (beta) es menor o igual al mejor caso 
                # de MAX (alfa), podamos esta rama (break).
                if beta <= alfa:
                    break

            return max_eval
        #Misma lógica pero para el turno del oponente (MIN)
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

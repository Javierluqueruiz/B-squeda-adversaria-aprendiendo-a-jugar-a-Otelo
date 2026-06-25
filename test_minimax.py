import unittest
import numpy as np
from otelo import Otelo
from minimax import AgenteMinimax

class TestMinimax(unittest.TestCase):

    def test_ia_sabe_pasar_turno(self):
        # 1. Preparamos el entorno
        partida = Otelo()
        agente = AgenteMinimax(jugadorIA=1, profundidad_maxima=4)
        
        # 2. TRUCAMOS EL TABLERO (Forzamos un caso límite)
        # Llenamos casi todo el tablero de fichas negras para que las blancas (IA)
        # se queden sin movimientos válidos rápidamente en sus simulaciones.
        partida.tablero = np.ones((8, 8), dtype=int) * 2 
        partida.tablero[0][0] = 0 # Dejamos un hueco
        partida.tablero[0][1] = 1 # Ponemos una blanca acorralada
        
        # 3. Ejecutamos la función (si hay un bucle infinito, el test se quedará colgado aquí)
        movimiento = agente.obtener_mejor_movimiento(partida)
        
        # 4. Comprobamos el resultado (Assert)
        # La IA debería devolver None en la vida real porque ella no tiene movimientos
        # en este tablero trucado, pero lo importante es que devuelva algo rápido y no explote.
        self.assertIsNone(movimiento, "La IA debería devolver None al no tener movimientos, pero sin colgarse.")

if __name__ == '__main__':
    unittest.main()
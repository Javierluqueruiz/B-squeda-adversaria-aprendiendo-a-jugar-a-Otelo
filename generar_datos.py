from otelo import Otelo
from minimax import AgenteMinimax
import time


partida = Otelo()
IA_1 = AgenteMinimax(jugadorIA=1, profundidad_maxima=3)
IA_2 = AgenteMinimax(jugadorIA=2, profundidad_maxima=3)


print("Simulación IA vs IA")
inicio = time.time()

while not partida.es_fin_de_juego():

    if partida.jugador_actual == 1:
        agente_actual = IA_1
    else:
        agente_actual = IA_2

    movimiento = agente_actual.obtener_mejor_movimiento(partida=partida)
    
    if movimiento is not None:
        f, c, = movimiento
        partida.ejecutar_movimiento(f, c, agente_actual.jugadorIA)
    else:
        partida.jugador_actual = 1 if agente_actual.jugadorIA == 2 else 2
    
fin = time.time()

blancas, negras = partida.calcular_puntuacion()
print(f"Partida terminada en {round(fin-inicio, 2)} segundos")
print(f"Resultado final: Blancas (1): {blancas} | Negras (2): {negras}")
partida.imprimir_tablero()




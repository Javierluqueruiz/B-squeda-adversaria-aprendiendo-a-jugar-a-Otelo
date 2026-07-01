from minimax import AgenteMinimax
from otelo import Otelo

import numpy as np

NUM_PARTIDAS = 10
PROFUNDIDAD = 3

def jugar_partida(jugador_red, jugador_clasico):
    partida = Otelo()

    agente_red = AgenteMinimax(jugadorIA=jugador_red, profundidad_maxima=PROFUNDIDAD, usar_red=True)
    agente_clasico = AgenteMinimax(jugadorIA=jugador_clasico, profundidad_maxima=PROFUNDIDAD, usar_red=False)

    jugador_actual = 2 #Negras

    while not partida.es_fin_de_juego():
        movimientos_posibles = partida.obtener_movimientos_validos(jugador_actual)

        if len(movimientos_posibles) > 0:
            if jugador_actual == jugador_red:
                mov = agente_red.obtener_mejor_movimiento(partida)
            else:
                mov = agente_clasico.obtener_mejor_movimiento(partida)

            if mov is not None:
                f, c = mov
                partida.ejecutar_movimiento(f, c, jugador_actual)
        
        jugador_actual = 1 if jugador_actual == 2 else 2

        if len(partida.obtener_movimientos_validos(1)) == 0 and len(partida.obtener_movimientos_validos(2)) == 0:
            break   


    fichas_red = np.sum(partida.tablero == jugador_red)
    fichas_clasico = np.sum(partida.tablero == jugador_clasico)

    if fichas_red > fichas_clasico:
        return "RED"
    elif fichas_clasico > fichas_red:
        return "CLASICO"
    else:
        return "EMPATE"


print(f"INICIANDO TORNEO: RED vs CLASICO ({NUM_PARTIDAS} partidas)")
print(f"Profundidad de búsqueda: {PROFUNDIDAD}")

victorias_red = 0
victorias_clasico = 0
empates = 0

for i in range(1, NUM_PARTIDAS + 1):

    if i <= (NUM_PARTIDAS // 2):
        jugador_red = 2
        jugador_clasico = 1
        print(f"\nPartida {i}: RED (Negras) vs CLASICO (Blancas)")
    else:
        jugador_red = 1
        jugador_clasico = 2
        print(f"\nPartida {i}: CLASICO (Negras) vs RED (Blancas)")

    resultado = jugar_partida(jugador_red, jugador_clasico)

    if resultado == "RED":
        victorias_red += 1
        print("Resultado: RED gana")
    elif resultado == "CLASICO":
        victorias_clasico += 1
        print("Resultado: CLASICO gana")
    else:
        empates += 1
        print("Resultado: Empate")


print("\nRESULTADOS FINALES DEL TORNEO:")
print(f"Victorias RED: {victorias_red}")
print(f"Victorias CLASICO: {victorias_clasico}")
print(f"Empates: {empates}")


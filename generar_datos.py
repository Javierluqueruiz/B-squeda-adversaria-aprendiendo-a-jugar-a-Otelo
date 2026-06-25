from otelo import Otelo
from minimax import AgenteMinimax
import time
import numpy as np
import copy


#CONFIGURACIÓN
NUM_PARTIDAS = 500
IA_1 = AgenteMinimax(jugadorIA=1, profundidad_maxima=3)
IA_2 = AgenteMinimax(jugadorIA=2, profundidad_maxima=3)

#ALMACENAMIENTO
tableros_totales = []
etiquetas_totales = []

print(f"Iniciando generación de {NUM_PARTIDAS} partidas")
inicio_global = time.time()

for i in range(NUM_PARTIDAS):
    print(f"Simulando partida {i+1} de {NUM_PARTIDAS}")
    partida = Otelo()
    historia_partida = []

    while not partida.es_fin_de_juego():

        if partida.jugador_actual == 1:
            agente_actual = IA_1
        else:
            agente_actual = IA_2

        movimiento = agente_actual.obtener_mejor_movimiento(partida=partida)
        
        if movimiento is not None:
            copia_estado = np.copy(partida.tablero)
            historia_partida.append((copia_estado, partida.jugador_actual))
            f, c, = movimiento
            partida.ejecutar_movimiento(f, c, agente_actual.jugadorIA)
        else:
            partida.jugador_actual = 1 if agente_actual.jugadorIA == 2 else 2

    #Ganador
    blancas, negras = partida.calcular_puntuacion()
    ganador = 0 
    if blancas > negras:
        ganador = 1
    elif negras > blancas:
        ganador = 2

    #Etiquetado
    for estado_tablero, jugador in historia_partida:
        if ganador == 0:
            etiqueta = 0
        elif jugador == ganador:
            etiqueta = 1
        else:
            etiqueta = -1

        tableros_totales.append(estado_tablero)
        etiquetas_totales.append(etiqueta)

    
fin_global = time.time()

print(f"\n¡Generación completada en {round(fin_global - inicio_global, 2)} segundos!")
print(f"Total de tableros recolectados: {len(tableros_totales)}")

#Guardar en memoria

np.save("datasets/dataset_tableros.npy", np.array(tableros_totales))
np.save("datasets/dataset_etiquetas.npy", np.array(etiquetas_totales))
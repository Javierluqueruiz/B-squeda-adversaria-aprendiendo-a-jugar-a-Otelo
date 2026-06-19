import pygame
import sys
from otelo import Otelo

TAMAÑO_CASILLA = 80
ANCHO = TAMAÑO_CASILLA * 8
ALTO = TAMAÑO_CASILLA * 8

COLOR_FONDO = (34, 139, 34)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_LINEAS = COLOR_NEGRO


def dibujar_tablero(pantalla, juego):
    pantalla.fill(COLOR_FONDO)

    for i in range(8):
        pygame.draw.line(pantalla, COLOR_LINEAS, (0, i*TAMAÑO_CASILLA), (ANCHO, i*TAMAÑO_CASILLA))
        pygame.draw.line(pantalla, COLOR_LINEAS, (i*TAMAÑO_CASILLA, 0), (i*TAMAÑO_CASILLA, ALTO))

    for f in range(8):
        for c in range(8):
            centro_x = c * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
            centro_y = f * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
            radio = TAMAÑO_CASILLA // 2 - 5

            if juego.tablero[f, c] == 1:
                pygame.draw.circle(pantalla, COLOR_BLANCO, (centro_x, centro_y), radio)
            elif juego.tablero[f, c] == 2:
                pygame.draw.circle(pantalla, COLOR_NEGRO, (centro_x, centro_y), radio)



def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Otelo")

    partida = Otelo()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = evento.pos

                fila = pos_y // 80 
                columna = pos_x // 80
                
                if partida.es_movimiento_valido(fila, columna, partida.jugador_actual):
                    partida.ejecutar_movimiento(fila, columna, partida.jugador_actual)
            
        dibujar_tablero(pantalla, partida)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
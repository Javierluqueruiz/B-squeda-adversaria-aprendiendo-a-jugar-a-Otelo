import pygame
import sys
from otelo import Otelo

# Dimensiones
TAMAÑO_CASILLA = 80
ANCHO = TAMAÑO_CASILLA * 8
ALTO_TABLERO = TAMAÑO_CASILLA * 8
ALTO_PANEL = 80
ALTO = ALTO_TABLERO + ALTO_PANEL

# Colores
COLOR_FONDO = (34, 139, 34)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_LINEAS = COLOR_NEGRO
COLOR_BOTON = (50, 50, 150)
COLOR_BOTON_HOVER = (70, 70, 180)
COLOR_PANEL = (40, 40, 40)
COLOR_TEXTO_TURNO = (255, 215, 0)

# Fuentes
pygame.font.init()
FUENTE_TITULO = pygame.font.SysFont('Arial', 64, bold=True)
FUENTE_BOTON = pygame.font.SysFont('Arial', 32, bold=True)
FUENTE_INFO = pygame.font.SysFont('Arial', 22, bold=True)


def dibujar_menu(pantalla):
    pantalla.fill(COLOR_FONDO)

    texto_titulo = FUENTE_TITULO.render("OTELO", True, COLOR_NEGRO)
    rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO //3))
    pantalla.blit(texto_titulo, rect_titulo)

    ancho_boton, alto_boton = 250, 60
    rect_boton = pygame.Rect(ANCHO // 2- ancho_boton // 2, ALTO // 2, ancho_boton, alto_boton)

    pos_raton = pygame.mouse.get_pos()
    if rect_boton.collidepoint(pos_raton):
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER, rect_boton, border_radius=10)
    else:
        pygame.draw.rect(pantalla, COLOR_BOTON, rect_boton, border_radius=10)

    texto_boton = FUENTE_BOTON.render("Empezar Partida", True, COLOR_BLANCO)
    rect_texto = texto_boton.get_rect(center=rect_boton.center)
    pantalla.blit(texto_boton, rect_texto)


    return rect_boton


def dibujar_tablero(pantalla, juego):
    pantalla.fill(COLOR_FONDO)

    for i in range(8):
        pygame.draw.line(pantalla, COLOR_LINEAS, (0, i*TAMAÑO_CASILLA), (ANCHO, i*TAMAÑO_CASILLA))
        pygame.draw.line(pantalla, COLOR_LINEAS, (i*TAMAÑO_CASILLA, 0), (i*TAMAÑO_CASILLA, ALTO_TABLERO))
    pygame.draw.line(pantalla, COLOR_LINEAS, (0, ALTO_TABLERO), (ANCHO, ALTO_TABLERO))

    for f in range(8):
        for c in range(8):
            centro_x = c * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
            centro_y = f * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
            radio = TAMAÑO_CASILLA // 2 - 5

            if juego.tablero[f, c] == 1:
                pygame.draw.circle(pantalla, COLOR_BLANCO, (centro_x, centro_y), radio)
            elif juego.tablero[f, c] == 2:
                pygame.draw.circle(pantalla, COLOR_NEGRO, (centro_x, centro_y), radio)

    pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO_TABLERO, ANCHO, ALTO_PANEL))
    
    blancas, negras = juego.calcular_puntuacion()

    texto_marcador = FUENTE_INFO.render(f"Blancas (B): {blancas}    |   Negras (N): {negras}", True, COLOR_BLANCO)
    pantalla.blit(texto_marcador, (20, ALTO_TABLERO + 25))

    turno_str = "NEGRAS (N)" if juego.jugador_actual == 2 else "BLANCAS (B)"
    texto_turno = FUENTE_INFO.render(f"Turno: {turno_str}", True, COLOR_TEXTO_TURNO)

    rect_turno = texto_turno.get_rect(right=ANCHO - 20, top=ALTO_TABLERO + 25)
    pantalla.blit(texto_turno, rect_turno)

def dibujar_fin_partida(pantalla, partida):
    dibujar_tablero(pantalla, partida)

    blancas, negras = partida.calcular_puntuacion()

    if blancas > negras:
        texto1 = "¡Ganan las blancas!" 
        texto2 = f"({blancas} - {negras})"
        color_texto = COLOR_BLANCO
    elif negras > blancas:
        texto1 = "¡Ganan las negras!"
        texto2 = f"({negras} - {blancas})"
        color_texto = COLOR_NEGRO
    else:
        texto1 = "¡Empate!" 
        texto2 = f"({blancas} - {negras})"
        color_texto = COLOR_TEXTO_TURNO
    
    superficie_texto1 = FUENTE_TITULO.render(texto1, True, color_texto)
    superficie_texto2 = FUENTE_INFO.render(texto2, True, color_texto)

    ancho_caja = max(superficie_texto1.get_width(), superficie_texto2.get_width()) + 60
    alto_caja = superficie_texto1.get_height() + superficie_texto2.get_height() + 40
    caja_fondo = pygame.Rect(0, 0, ancho_caja, alto_caja)
    caja_fondo.center = (ANCHO // 2, ALTO_TABLERO // 2)

    pygame.draw.rect(pantalla, COLOR_PANEL, caja_fondo, border_radius=15)
    pygame.draw.rect(pantalla, COLOR_BLANCO, caja_fondo, width=3, border_radius=15)

    rect_texto1 = superficie_texto1.get_rect(centerx=caja_fondo.centerx, top=caja_fondo.top + 15)
    rect_texto2 = superficie_texto2.get_rect(centerx = caja_fondo.centerx, top = rect_texto1.bottom+10)

    pantalla.blit(superficie_texto1, rect_texto1)
    pantalla.blit(superficie_texto2, rect_texto2)

def dibujar_pasar_turno(pantalla, partida):
    dibujar_tablero(pantalla, partida)

    texto1 = "No tienes movimientos." 
    texto2 = "Clic para pasar turno"
    superficie_texto1 = FUENTE_BOTON.render(texto1, True, COLOR_BLANCO)
    superficie_texto2 = FUENTE_BOTON.render(texto2, True, COLOR_BLANCO)
    
    ancho_caja = max(superficie_texto1.get_width(), superficie_texto2.get_width()) + 40
    alto_caja = superficie_texto1.get_height() + superficie_texto2.get_height() + 50
    rect_boton = pygame.Rect(ANCHO // 2 - ancho_caja // 2, ALTO_TABLERO // 2 - alto_caja // 2, ancho_caja, alto_caja)

    pos_raton = pygame.mouse.get_pos()
    if rect_boton.collidepoint(pos_raton):
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER, rect_boton, border_radius=15)
    else:
        pygame.draw.rect(pantalla, COLOR_BOTON, rect_boton, border_radius=15)

    pygame.draw.rect(pantalla, COLOR_BLANCO, rect_boton, width=3, border_radius=15)

    y_inicial = rect_boton.y + 15
    rect_texto1 = superficie_texto1.get_rect(centerx=rect_boton.centerx, top=y_inicial)
    rect_texto2 = superficie_texto2.get_rect(centerx=rect_boton.centerx, top=rect_texto1.bottom + 10)
    pantalla.blit(superficie_texto1, rect_texto1)
    pantalla.blit(superficie_texto2, rect_texto2)

    return rect_boton

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Otelo")

    estado = "MENU"
    partida = None
    rect_boton_pasar = None

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado == "MENU":
                    if rect_boton.collidepoint(evento.pos):
                        estado = "JUGANDO"
                        partida = Otelo()
                elif estado == "JUGANDO":
                    pos_x, pos_y = evento.pos

                    if pos_y < ALTO_TABLERO:
                        fila = pos_y // 80 
                        columna = pos_x // 80
                    
                        if partida.es_movimiento_valido(fila, columna, partida.jugador_actual):
                            partida.ejecutar_movimiento(fila, columna, partida.jugador_actual)
                            if partida.es_fin_de_juego():
                                estado = "FIN"   
                            elif len(partida.obtener_movimientos_validos(partida.jugador_actual)) == 0:
                                estado = "PASAR_TURNO"

                elif estado == "PASAR_TURNO":
                    if rect_boton_pasar and rect_boton_pasar.collidepoint(evento.pos):
                        partida.jugador_actual = 1 if partida.jugador_actual == 2 else 2
                        estado = "JUGANDO"

        if estado == "MENU":
            rect_boton = dibujar_menu(pantalla)
        elif estado == "JUGANDO":
            dibujar_tablero(pantalla, partida)
        elif estado == "PASAR_TURNO":
            rect_boton_pasar = dibujar_pasar_turno(pantalla, partida)
        elif estado == "FIN":
            dibujar_fin_partida(pantalla, partida)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
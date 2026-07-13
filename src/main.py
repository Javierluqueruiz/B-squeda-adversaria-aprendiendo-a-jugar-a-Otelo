import os 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Silencia el saludo de PyGame

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import sys
import random
import numpy as np
from src.otelo import Otelo
from src.minimax import AgenteMinimax   

# Dimensiones
TAMAÑO_CASILLA = 80
ANCHO = TAMAÑO_CASILLA * 8
ALTO_TABLERO = TAMAÑO_CASILLA * 8
ALTO_PANEL = 100
ALTO = ALTO_TABLERO + ALTO_PANEL

# Colores
COLOR_FONDO = (34, 139, 34)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_LINEAS = COLOR_NEGRO
COLOR_BOTON = (50, 50, 150)
COLOR_BOTON_HOVER = (100, 170, 255) 
COLOR_PANEL = (40, 40, 40)
COLOR_TEXTO_TURNO = (255, 215, 0)
COLOR_PISTA = (60, 180, 60)

# Fuentes
pygame.font.init()
FUENTE_TITULO = pygame.font.SysFont('Arial', 64, bold=True)
FUENTE_SUBTITULO = pygame.font.SysFont('Arial', 40, bold=True)
FUENTE_BOTON = pygame.font.SysFont('Arial', 32, bold=True)
FUENTE_INFO = pygame.font.SysFont('Arial', 22, bold=True)


def dibujar_menu(pantalla):
    pantalla.fill(COLOR_FONDO)

    texto_titulo = FUENTE_TITULO.render("OTELO", True, COLOR_NEGRO)
    rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 3))
    pantalla.blit(texto_titulo, rect_titulo)

    ancho_boton, alto_boton = 300, 60
    
    rect_pvp = pygame.Rect(ANCHO // 2 - ancho_boton // 2, ALTO // 2 - 40, ancho_boton, alto_boton)
    pygame.draw.rect(pantalla, COLOR_BOTON, rect_pvp, border_radius=10)
    texto_pvp = FUENTE_BOTON.render("Jugar 1 vs 1", True, COLOR_BLANCO)
    pantalla.blit(texto_pvp, texto_pvp.get_rect(center=rect_pvp.center))

    rect_pvia = pygame.Rect(ANCHO // 2 - ancho_boton // 2, ALTO // 2 + 40, ancho_boton, alto_boton)
    pygame.draw.rect(pantalla, COLOR_BOTON, rect_pvia, border_radius=10)
    texto_pvia = FUENTE_BOTON.render("Jugar vs IA", True, COLOR_BLANCO)
    pantalla.blit(texto_pvia, texto_pvia.get_rect(center=rect_pvia.center))

    return rect_pvp, rect_pvia

def dibujar_config_ia(pantalla, tipo_ia, profundidad_ia):
    pantalla.fill(COLOR_FONDO)
    
    # Titulo de la pantalla
    texto_titulo = FUENTE_BOTON.render("CONFIGURAR INTELIGENCIA ARTIFICIAL", True, COLOR_NEGRO)
    pantalla.blit(texto_titulo, texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 8)))
    
    # --- SELECCION DE ALGORITMO ---
    texto_tipo = FUENTE_BOTON.render("Selecciona el motor de evaluacion:", True, COLOR_BLANCO)
    pantalla.blit(texto_tipo, (ANCHO // 2 - 260, ALTO // 4 - 10))
    
    rect_minimax = pygame.Rect(ANCHO // 2 - 180, ALTO // 4 + 35, 180, 45)
    rect_red = pygame.Rect(ANCHO // 2 + 20, ALTO // 4 + 35, 180, 45)
    
    # Resaltamos con un color diferente (COLOR_BOTON_HOVER) el que este seleccionado activo
    col_minimax = COLOR_BOTON_HOVER if tipo_ia == "MINIMAX" else COLOR_BOTON
    col_red = COLOR_BOTON_HOVER if tipo_ia == "RED" else COLOR_BOTON
    
    pygame.draw.rect(pantalla, col_minimax, rect_minimax, border_radius=8)
    pygame.draw.rect(pantalla, col_red, rect_red, border_radius=8)
    
    txt_m = FUENTE_INFO.render("Minimax Clasico", True, COLOR_BLANCO)
    txt_r = FUENTE_INFO.render("Red Neuronal", True, COLOR_BLANCO)
    pantalla.blit(txt_m, txt_m.get_rect(center=rect_minimax.center))
    pantalla.blit(txt_r, txt_r.get_rect(center=rect_red.center))
    
    # --- SELECCION DE PROFUNDIDAD ---
    texto_prof = FUENTE_INFO.render(f"Profundidad de busqueda en el arbol: {profundidad_ia}", True, COLOR_BLANCO)
    pantalla.blit(texto_prof, (ANCHO // 2 - 180, ALTO // 2 - 10))
    
    rect_menos = pygame.Rect(ANCHO // 2 - 65, ALTO // 2 + 25, 55, 45)
    rect_mas = pygame.Rect(ANCHO // 2 + 10, ALTO // 2 + 25, 55, 45)
    
    pygame.draw.rect(pantalla, COLOR_BOTON, rect_menos, border_radius=5)
    pygame.draw.rect(pantalla, COLOR_BOTON, rect_mas, border_radius=5)
    
    txt_menos = FUENTE_BOTON.render("-", True, COLOR_BLANCO)
    txt_mas = FUENTE_BOTON.render("+", True, COLOR_BLANCO)
    pantalla.blit(txt_menos, txt_menos.get_rect(center=rect_menos.center))
    pantalla.blit(txt_mas, txt_mas.get_rect(center=rect_mas.center))
    
    # --- BOTONES DE ACCION ---
    rect_iniciar = pygame.Rect(ANCHO // 2 - 110, ALTO // 2 + 120, 220, 55)
    pygame.draw.rect(pantalla, (50, 150, 50), rect_iniciar, border_radius=10)
    txt_iniciar = FUENTE_BOTON.render("¡JUGAR!", True, COLOR_BLANCO)
    pantalla.blit(txt_iniciar, txt_iniciar.get_rect(center=rect_iniciar.center))
    
    rect_volver = pygame.Rect(ANCHO // 2 - 110, ALTO // 2 + 195, 220, 40)
    pygame.draw.rect(pantalla, (150, 50, 50), rect_volver, border_radius=5)
    txt_volver = FUENTE_INFO.render("Volver al Menu", True, COLOR_BLANCO)
    pantalla.blit(txt_volver, txt_volver.get_rect(center=rect_volver.center))
    
    return rect_minimax, rect_red, rect_menos, rect_mas, rect_iniciar, rect_volver

def dibujar_tablero(pantalla, juego, modo_juego=None, agente=None):
    pantalla.fill(COLOR_FONDO)

    for i in range(8):
        pygame.draw.line(pantalla, COLOR_LINEAS, (0, i*TAMAÑO_CASILLA), (ANCHO, i*TAMAÑO_CASILLA))
        pygame.draw.line(pantalla, COLOR_LINEAS, (i*TAMAÑO_CASILLA, 0), (i*TAMAÑO_CASILLA, ALTO_TABLERO))
    pygame.draw.line(pantalla, COLOR_LINEAS, (0, ALTO_TABLERO), (ANCHO, ALTO_TABLERO))

    movimientos_validos = juego.obtener_movimientos_validos(juego.jugador_actual)
    for mov in movimientos_validos:
        f, c = mov
        centro_x = c * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
        centro_y = f * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
        pygame.draw.circle(pantalla, COLOR_PISTA, (centro_x, centro_y), 12)



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

    # --- NUEVO: TEXTO INFORMATIVO DE LA IA ---
    if modo_juego == "PvIA" and agente is not None:
        tipo_ia = "Red Neuronal" if agente.usar_red else "Minimax"
        color_ia = "Blancas (B)" if agente.jugadorIA == 1 else "Negras (N)"
        
        texto_ia = FUENTE_INFO.render(f"IA: {tipo_ia} jugando con {color_ia}", True, (180, 200, 255))
        pantalla.blit(texto_ia, (20, ALTO_TABLERO + 60))
    # -----------------------------------------

    ancho_boton_salir = 100
    alto_boton_salir = 40
    x_boton = ANCHO - ancho_boton_salir - 20
    y_boton = ALTO_TABLERO + 55

    rect_salir = pygame.Rect(x_boton, y_boton, ancho_boton_salir, alto_boton_salir)

    pygame.draw.rect(pantalla, (200, 50, 50), rect_salir, border_radius=5)
    text_salir = FUENTE_INFO.render("Menú", True, COLOR_BLANCO)
    pantalla.blit(text_salir, text_salir.get_rect(center=rect_salir.center)) 

    return rect_salir

def dibujar_fin_partida(pantalla, partida, modo_juego=None, agente=None):
    rect_salir = dibujar_tablero(pantalla, partida, modo_juego=modo_juego, agente=agente)

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

    return rect_salir

def dibujar_pasar_turno(pantalla, partida, modo_juego=None, agente=None):
    dibujar_tablero(pantalla, partida, modo_juego=modo_juego, agente=agente)

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
    modo_juego = None
    agente = None
    rect_boton_pasar = None
    rect_boton_salir = None

    # Variables para la configuracion de la IA
    tipo_ia_seleccionado = "MINIMAX" 
    profundidad_ia_seleccionada = 3   


    corriendo = True
    while corriendo:

        if estado == "MENU":
            rect_pvp, rect_pvia = dibujar_menu(pantalla)
        elif estado == "CONFIG_IA":
            rect_mm, rect_rd, rect_men, rect_ma, rect_ini, rect_vol = dibujar_config_ia(pantalla, tipo_ia_seleccionado, profundidad_ia_seleccionada)
        elif estado == "JUGANDO":
            rect_boton_salir = dibujar_tablero(pantalla, partida, modo_juego=modo_juego, agente=agente)
        elif estado == "PASAR_TURNO":
            rect_boton_pasar = dibujar_pasar_turno(pantalla, partida, modo_juego=modo_juego, agente=agente)
        elif estado == "FIN":
            rect_boton_salir = dibujar_fin_partida(pantalla, partida, modo_juego=modo_juego, agente=agente)

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado == "MENU":
                    if rect_pvp.collidepoint(evento.pos):
                        modo_juego="PvP"
                        estado = "JUGANDO"
                        partida = Otelo()
                    elif rect_pvia.collidepoint(evento.pos):
                        estado = "CONFIG_IA"
                  

                elif estado == "JUGANDO":
                    if rect_boton_salir is not None and rect_boton_salir.collidepoint(evento.pos):
                        estado="MENU"
                    
                    else:

                        es_turno_humano = (modo_juego=="PvP") or (modo_juego=="PvIA" and partida.jugador_actual != agente.jugadorIA)

                        if es_turno_humano:
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
                
                elif estado == "FIN":
                    if rect_boton_salir and rect_boton_salir.collidepoint(evento.pos):
                        estado = "MENU"
                
                elif estado == "CONFIG_IA":
                    if rect_mm.collidepoint(evento.pos):
                        tipo_ia_seleccionado = "MINIMAX"
                    elif rect_rd.collidepoint(evento.pos):
                        tipo_ia_seleccionado = "RED"
                    elif rect_men.collidepoint(evento.pos):
                        if profundidad_ia_seleccionada > 1:
                            profundidad_ia_seleccionada -= 1
                    elif rect_ma.collidepoint(evento.pos):
                        # Ponemos un tope maximo de 5 para evitar que el algoritmo puro 
                        # colapse el hilo principal de PyGame debido al coste computacional
                        if profundidad_ia_seleccionada < 5:
                            profundidad_ia_seleccionada += 1
                    elif rect_vol.collidepoint(evento.pos):
                        estado = "MENU"
                    elif rect_ini.collidepoint(evento.pos):
                    # ¡Aqui iniciamos la partida con lo elegido por el usuario!
                        modo_juego = "PvIA"
                        estado = "JUGANDO"
                        partida = Otelo()
                    
                        color_ia = random.choice([1, 2])
                        usar_red = True if tipo_ia_seleccionado == "RED" else False
                    
                        # Inyectamos los parametros reales seleccionados por el usuario
                        agente = AgenteMinimax(
                            jugadorIA=color_ia, 
                            profundidad_maxima=profundidad_ia_seleccionada, 
                            usar_red=usar_red
                        )
                

        if estado == "JUGANDO" and modo_juego=="PvIA":
            if partida.jugador_actual == agente.jugadorIA:
                dibujar_tablero(pantalla, partida, modo_juego=modo_juego, agente=agente)
                pygame.display.flip()
                pygame.time.wait(200)

                movimiento = agente.obtener_mejor_movimiento(partida)

                if movimiento is not None:
                    f, c, = movimiento
                    partida.ejecutar_movimiento(f, c, agente.jugadorIA)

                    if partida.es_fin_de_juego():
                        estado = "FIN"
                    elif len(partida.obtener_movimientos_validos(partida.jugador_actual)) == 0:
                                    estado = "PASAR_TURNO"

                else:
                    print("La IA no tiene movimientos. Pasa el turno")
                    partida.jugador_actual = 1 if agente.jugadorIA == 2 else 2

                    if partida.es_fin_de_juego():
                        estado = "FIN"
                    elif len(partida.obtener_movimientos_validos(partida.jugador_actual)) == 0:
                        estado = "PASAR_TURNO"

        

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
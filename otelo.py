import numpy as np 

#Jugador 1: Fichas blancas
#Jugador 2: Fichas negras


class Otelo:
    def __init__(self):
        self.tablero = np.zeros((8, 8), dtype=int)

        self.tablero[3][3] = 1
        self.tablero[3][4] = 2
        self.tablero[4][3] = 2
        self.tablero[4][4] = 1

        self.jugador_actual = 2 #Según las reglas de Otelo, siempre empiezan las fichas negras


    def imprimir_tablero(self):

        for i in range(8):
            fila = []
            for j in range(8):
                if self.tablero[i][j] == 0:
                    fila.append('.')
                elif self.tablero[i][j] == 1:
                    fila.append('B')
                else:
                    fila.append('N')

            print(f"{i} {' '.join(fila)}")


    DIRECCIONES = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    
    def es_movimiento_valido(self, fila, columna, jugador):
        if self.tablero[fila, columna] != 0:
            return False;
        
        oponente = 1 if jugador == 2 else 2

        for df, dc in self.DIRECCIONES:
            f, c = fila + df, columna + dc
            fichas_oponentes_intermedias = 0

            while  0<= f <8 and 0 <= c < 8 and self.tablero[f, c] == oponente:
                fichas_oponentes_intermedias += 1
                f, c = f + df, c + dc

            if 0 <= f < 8 and 0 <= c < 8:
                if self.tablero[f, c] == jugador and fichas_oponentes_intermedias > 0:
                    return True
            
        return False
    
    def ejecutar_movimiento(self, fila, columna, jugador):

        if not self.es_movimiento_valido(fila, columna, jugador): 
            return False
    
        self.tablero[fila, columna] = jugador

        oponente = 1 if jugador == 2 else 2

        for df, dc, in self.DIRECCIONES:
            f, c = fila + df, columna + dc
            fichas_oponente = []

            while 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == oponente:
                fichas_oponente.append((f, c))
                f, c = f + df, c + dc

            if 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == jugador:
                for f_cambiar, c_cambiar in fichas_oponente:
                    self.tablero[f_cambiar, c_cambiar] = jugador
        
        self.jugador_actual = oponente 

        return True
    

    def obtener_movimientos_validos(self, jugador):
        movimientos = []
        for f in range(8):
            for c in range(8):
                if self.es_movimiento_valido(f, c, jugador):
                    movimientos.append((f, c))
        
        return movimientos
    
    def es_fin_de_juego(self):
        movimientos_blancas = self.obtener_movimientos_validos(1)
        movimientos_negras = self.obtener_movimientos_validos(2)

        if len(movimientos_blancas) == 0 and len(movimientos_negras) == 0:
            return True

        if np.count_nonzero(self.tablero) == 64:
            return True
        
        return False
    
    def calcular_puntuacion(self):
        blancas = np.sum(self.tablero == 1)
        negras = np.sum(self.tablero == 2)

        return blancas, negras


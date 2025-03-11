import heapq
import pygame
import sys
import random
import math

# Configuracion de Pygame
pygame.init()
CELDA_TAM = 40  # Tamano de cada celda en pixeles
COLS = 20  # Numero de columnas
FILAS = 15  # Numero de filas
ANCHO = COLS * CELDA_TAM + 300  # Ancho total incluyendo el panel lateral
ALTO = FILAS * CELDA_TAM  # Alto total de la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))  # Creacion de la ventana
pygame.display.set_caption("A* Pathfinding Mejorado")  # Titulo de la ventana
RELOJ = pygame.time.Clock()  # Reloj para controlar la velocidad de actualizacion
FUENTE = pygame.font.Font(None, 22)  # Fuente para el texto

# Definicion de colores utilizados en la interfaz
dic_colores = {
    "fondo": (44, 62, 80),
    "obstaculo": (34, 40, 49),
    "explorado": (0, 168, 255),
    "camino": (46, 204, 113),
    "inicio": (241, 196, 15),
    "objetivo": (231, 76, 60),
    "boton": (155, 89, 182),
    "texto": (236, 240, 241)
}


# Definicion de la clase Nodo para el algoritmo A*
class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion  # Coordenadas del nodo en la cuadricula
        self.padre = padre  # Nodo padre para reconstruir el camino
        self.g = 0  # Costo desde el inicio hasta este nodo
        self.h = 0  # Heuristica (estimacion del costo restante)
        self.f = 0  # Costo total (g + h)

    def __eq__(self, otro):
        return self.posicion == otro.posicion  # Compara dos nodos por posicion

    def __lt__(self, otro):
        return self.f < otro.f  # Compara los costos f para la cola de prioridad

# Funcion heuristica para el algoritmo A* (distancia Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Genera un mapa aleatorio con obstaculos
def generar_mapa_aleatorio(inicio, objetivo):
    while True:
        mapa = [[0 if random.random() > 0.25 else 1 for _ in range(COLS)] for _ in range(FILAS)]
        mapa[inicio[0]][inicio[1]] = 0
        mapa[objetivo[0]][objetivo[1]] = 0
        if a_estrella(mapa, inicio, objetivo, validar=True):
            return mapa

# Funcion para dibujar la interfaz grafica
def dibujar_interfaz(mapa, camino=None, explorados=None):
    VENTANA.fill(dic_colores["fondo"])
    
    for i in range(FILAS):
        for j in range(COLS):
            color = dic_colores["fondo"]
            if mapa[i][j] == 1:
                color = dic_colores["obstaculo"]
            if explorados and (i, j) in explorados:
                color = dic_colores["explorado"]
            if camino and (i, j) in camino:
                color = dic_colores["camino"]
            if (i, j) == inicio:
                color = dic_colores["inicio"]
            if (i, j) == objetivo:
                color = dic_colores["objetivo"]
            pygame.draw.rect(VENTANA, color, (j * CELDA_TAM, i * CELDA_TAM, CELDA_TAM - 1, CELDA_TAM - 1))
    
    pygame.display.update()

# Implementacion del algoritmo A* para encontrar el camino mas corto
def a_estrella(mapa, inicio, objetivo, validar=False):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, Nodo(inicio))
    
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.posicion)
        
        if current_node.posicion == objetivo:
            if validar:
                return True
            path = []
            while current_node:
                path.append(current_node.posicion)
                current_node = current_node.padre
            return path[::-1], closed_set
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current_node.posicion[0] + dx, current_node.posicion[1] + dy
            if 0 <= x < FILAS and 0 <= y < COLS and mapa[x][y] == 0 and (x, y) not in closed_set:
                new_node = Nodo((x, y), current_node)
                new_node.g = current_node.g + 1
                new_node.h = heuristica((x, y), objetivo)
                new_node.f = new_node.g + new_node.h
                
                if not any(nodo == new_node and nodo.f <= new_node.f for nodo in open_list):
                    heapq.heappush(open_list, new_node)
        
        if not validar:
            dibujar_interfaz(mapa, explorados=closed_set)
            RELOJ.tick(20)
    
    return False if validar else ([], closed_set)

# Inicializacion de variables
inicio = (0, 0)
objetivo = (FILAS - 1, COLS - 1)
mapa = generar_mapa_aleatorio(inicio, objetivo)
camino = []
explorados = set()

# Bucle principal de ejecucion del programa
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                camino, explorados = a_estrella(mapa, inicio, objetivo)
            if event.key == pygame.K_RETURN:  # Accion para la tecla Enter
                camino, explorados = a_estrella(mapa, inicio, objetivo)
            if event.key == pygame.K_d:
                mapa = generar_mapa_aleatorio(inicio, objetivo)
                camino = []
                explorados = set()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila, col = y // CELDA_TAM, x // CELDA_TAM
            
            if 0 <= fila < FILAS and 0 <= col < COLS:
                if event.button == 1:
                    inicio = (fila, col)
                    camino = []
                    explorados = set()
                elif event.button == 3:
                    objetivo = (fila, col)
                    camino = []
                    explorados = set()
                elif event.button == 2:
                    mapa[fila][col] = 1 - mapa[fila][col]
    
    dibujar_interfaz(mapa, camino, explorados)
    RELOJ.tick(60)
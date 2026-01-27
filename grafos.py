import heapq
from collections import deque
import math

class GrafoEntregas:
    def __init__(self):
        self.n = 8
        self.matriz_costos = [[math.inf] * self.n for _ in range(self.n)]
        self.nodos = ['Centro', 'La_Florida', 'La_Carolina', 'Cumbaya', 
                     'Tumbaco', 'Pradera', 'El_Inca', 'Quitumbe']
        
    def agregar_ruta(self, origen, destino, km):
        i, j = self.nodos.index(origen), self.nodos.index(destino)
        self.matriz_costos[i][j] = km
        self.matriz_costos[j][i] = km
        
    def cargar_rutas_quito(self):  
        """Carga rutas reales de Quito (km aproximados)"""
        rutas = [
            ('Centro', 'La_Florida', 3), ('Centro', 'La_Carolina', 5),
            ('La_Florida', 'Cumbaya', 8), ('La_Carolina', 'Pradera', 4),
            ('Cumbaya', 'Tumbaco', 6), ('Pradera', 'El_Inca', 7),
            ('Tumbaco', 'Quitumbe', 12), ('El_Inca', 'Quitumbe', 10)
        ]
        for o, d, km in rutas:
            self.agregar_ruta(o, d, km)
            
    def mostrar_matriz(self):
        print("MATRIZ COSTOS ENTREGAS QUITO (km):")
        for i in range(self.n):
            row = [f"{self.matriz_costos[i][j]:.0f}" if self.matriz_costos[i][j] != math.inf else "---" for j in range(self.n)]
            print(f"{self.nodos[i]:10} | {' | '.join(row)}")
    
    def dijkstra_entrega(self, desde, hasta):
        """Dijkstra con heapq para rutas óptimas"""
        dist = [math.inf] * self.n
        dist[desde] = 0
        prev = [-1] * self.n
        pq = [(0, desde)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v in range(self.n):
                if self.matriz_costos[u][v] != math.inf:
                    alt = d + self.matriz_costos[u][v]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        heapq.heappush(pq, (alt, v))
        
        ruta = []
        v = hasta
        while v != -1:
            ruta.append(self.nodos[v])
            v = prev[v]
        return ruta[::-1], dist[hasta]

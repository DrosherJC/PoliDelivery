import heapq

ARCHIVO_RUTAS = "data/rutas.txt"
ARCHIVO_CENTROS = "data/centros.txt"


def cargar_datos():
    adyacencia = {} #{id_origen: [(id_destino, costo)}
    centros = {}    #{id: nombre}

    #Cargar Centros
    try:
        with open(ARCHIVO_CENTROS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) >= 2:
                    id_cen = datos[0]
                    nombre = datos[1]
                    centros[id_cen] = nombre
                    # Inicializamos la lista de vecinos para este centro
                    if id_cen not in adyacencia:
                        adyacencia[id_cen] = []
    except FileNotFoundError:
        print("Archivo centros.txt no encontrado")

    #Cargar Rutas
    try:
        with open(ARCHIVO_RUTAS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) >= 4:
                    origen, destino, distancia, costo = datos
                    costo = float(costo)
                    
                    # Agregar conexión
                    if origen in adyacencia:
                        adyacencia[origen].append((destino, costo))
                    if destino in adyacencia:
                        adyacencia[destino].append((origen, costo)) # Se asume bidireccional
    except FileNotFoundError:
        print("Archivo rutas.txt no encontrado")
        
    return adyacencia, centros

# Algoritmo de Dijkstra
def dijkstra(adyacencia, inicio, fin):
    cola = [(0, inicio, [])] #(costo, nodo_actual, camino_recorrido)
    visitados = set()
    
    while cola:
        (costo, actual, camino) = heapq.heappop(cola)
        
        if actual in visitados:
            continue
        visitados.add(actual)
        
        camino = camino + [actual]
        
        if actual == fin:
            return camino, costo
        
        # Buscar vecinos en el diccionario
        if actual in adyacencia:
            for (vecino, peso) in adyacencia[actual]:
                if vecino not in visitados:
                    heapq.heappush(cola, (costo + peso, vecino, camino))
                    
    return None, float('inf')

def mostrar_mapa(adyacencia, centros):
    print("\n--- MAPA DE CONEXIONES ---")
    for origen, destinos in adyacencia.items():
        nombre_origen = centros.get(origen, "Desconocido")
        print(f"Centro {nombre_origen} ({origen}) conecta con:")
        for destino, costo in destinos:
            nombre_destino = centros.get(destino, "Desconocido")
            print(f"   -> {nombre_destino} ({destino}) [Costo: ${costo}]")
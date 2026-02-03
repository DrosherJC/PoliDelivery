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

def mostrar_mapa(grafo, datos_centros):
    print("\n--- RED DE DISTRIBUCIÓN (CONEXIONES) ---")
    
    for origen_id, conexiones in grafo.items():
        nombre_origen = datos_centros.get(origen_id, f"ID {origen_id}")
        
        print(f"\n📍 {nombre_origen} (ID: {origen_id})")
        
        total_conexiones = len(conexiones)
        for i, (destino_id, costo) in enumerate(conexiones):
            nombre_destino = datos_centros.get(destino_id, f"ID {destino_id}")
            
            if i == total_conexiones - 1:
                prefijo = "   └──"
            else:
                prefijo = "   ├──"
                
            print(f"{prefijo} 🚚 Hacia: {nombre_destino:<15} [${costo}]")
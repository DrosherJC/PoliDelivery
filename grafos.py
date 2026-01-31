import heapq

ARCHIVO_RUTAS = "data/rutas.txt"
ARCHIVO_CENTROS = "data/centros.txt"


def cargar_datos():
    adyacencia = {} # Estructura: {id_origen: [(id_destino, costo), ...]}
    centros = {}    # Estructura: {id: nombre}

    # 1. Cargar Centros
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

    # 2. Cargar Rutas
    try:
        with open(ARCHIVO_RUTAS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) >= 4:
                    origen, destino, distancia, costo = datos
                    costo = float(costo)
                    
                    # Agregamos la conexión (ida y vuelta si es doble vía)
                    if origen in adyacencia:
                        adyacencia[origen].append((destino, costo))
                    if destino in adyacencia:
                        adyacencia[destino].append((origen, costo)) # Asumimos bidireccional
    except FileNotFoundError:
        print("Archivo rutas.txt no encontrado")
        
    return adyacencia, centros
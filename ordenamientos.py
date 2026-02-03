def bubble_sort(lista_centros, key="nombre"):
    # Ordenamiento Burbuja
    n = len(lista_centros)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista_centros[j][key] > lista_centros[j+1][key]:
                lista_centros[j], lista_centros[j+1] = lista_centros[j+1], lista_centros[j]
    return lista_centros

def quick_sort(lista_centros, key="nombre"):
    # Ordenamiento QuickSort
    if len(lista_centros) <= 1:
        return lista_centros
    else:
        pivote = lista_centros[0]
        menores = [x for x in lista_centros[1:] if x[key] <= pivote[key]]
        mayores = [x for x in lista_centros[1:] if x[key] > pivote[key]]
        return quick_sort(menores, key) + [pivote] + quick_sort(mayores, key)

# Helper para cargar centros en una lista de diccionarios
def obtener_lista_centros():
    lista = []
    try:
        with open("data/centros.txt", "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) >= 2:
                    # Guardamos como diccionario para facilitar ordenamiento
                    lista.append({"id": datos[0], "nombre": datos[1], "region": datos[2]})
    except:
        return []
    return lista
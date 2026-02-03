def busqueda_lineal(lista_centros, nombre_buscar):
    for centro in lista_centros:
        if centro["nombre"].lower() == nombre_buscar.lower():
            return centro
    return None

def busqueda_binaria(lista_centros_ordenada, nombre_buscar):
    # Requiere que la lista esté ordenada por nombre
    inicio = 0
    fin = len(lista_centros_ordenada) - 1
    
    while inicio <= fin:
        medio = (inicio + fin) // 2
        valor_medio = lista_centros_ordenada[medio]["nombre"].lower()
        objetivo = nombre_buscar.lower()
        
        if valor_medio == objetivo:
            return lista_centros_ordenada[medio]
        elif valor_medio < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None
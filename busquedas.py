def busqueda_lineal(lista, valor):
    for i in range(len(lista)):
        if lista[i] == valor:
            return i
    return -1


def busqueda_binaria(lista, valor):
    bajo = 0
    alto = len(lista) - 1

    while bajo <= alto:
        medio = (bajo + alto) // 2
        if lista[medio] == valor:
            return medio
        elif lista[medio] < valor:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1

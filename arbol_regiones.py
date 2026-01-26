class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []


class ArbolRegiones:
    def __init__(self, raiz):
        self.raiz = Nodo(raiz)

    def buscar(self, nodo, valor):
        if nodo.valor == valor:
            return nodo
        for hijo in nodo.hijos:
            encontrado = self.buscar(hijo, valor)
            if encontrado:
                return encontrado
        return None

    def agregar(self, padre, hijo):
        nodo_padre = self.buscar(self.raiz, padre)
        if nodo_padre:
            nodo_padre.hijos.append(Nodo(hijo))

    def recorrido_preorden(self, nodo, resultado):
        resultado.append(nodo.valor)
        for hijo in nodo.hijos:
            self.recorrido_preorden(hijo, resultado)

    def recorrido_postorden(self, nodo, resultado):
        for hijo in nodo.hijos:
            self.recorrido_postorden(hijo, resultado)
        resultado.append(nodo.valor)

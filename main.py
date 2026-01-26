import os
from ordenamientos import burbuja
from busquedas import busqueda_lineal, busqueda_binaria
from arbol_regiones import ArbolRegiones

ruta = os.path.dirname(__file__)

archivo = open(os.path.join(ruta, "datos.txt"), "r")
numeros = [int(linea.strip()) for linea in archivo if linea.strip().isdigit()]
archivo.close()

ordenados = burbuja(numeros)
print(ordenados)

print(busqueda_lineal(ordenados, 5))
print(busqueda_binaria(ordenados, 5))

archivo = open(os.path.join(ruta, "regiones.txt"), "r", encoding="latin-1")
lineas = [linea.strip() for linea in archivo if linea.strip()]
archivo.close()

arbol = ArbolRegiones(lineas[0])

for linea in lineas[1:]:
    padre, hijo = linea.split(":")
    arbol.agregar(padre, hijo)

preorden = []
postorden = []

arbol.recorrido_preorden(arbol.raiz, preorden)
arbol.recorrido_postorden(arbol.raiz, postorden)

print(preorden)
print(postorden)

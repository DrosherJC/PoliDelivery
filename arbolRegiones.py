# Crea un nodo con un nombre y una lista vacía de hijos
def crear_nodo(valor):
    return {
        "valor": valor,   
        "hijos": []       
    }


# Construye el árbol de regiones
def construir_arbol():
    #Raíz del árbol
    raiz = crear_nodo("Mundo PoliDelivery")
    
    #Guarda las regiones ya creadas para no repetirlas
    regiones_creadas = {}

    try:
        with open("data/regiones.txt", "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")

                # Verifica que la línea tenga región y subregión
                if len(datos) >= 2:
                    nom_region = datos[0]
                    nom_subregion = datos[1]

                    # Si la región no existe, se crea y se une a la raíz
                    if nom_region not in regiones_creadas:
                        nodo_region = crear_nodo(nom_region)
                        raiz["hijos"].append(nodo_region)
                        regiones_creadas[nom_region] = nodo_region

                    # Crea la subregión y la une a su región
                    nodo_sub = crear_nodo(nom_subregion)
                    regiones_creadas[nom_region]["hijos"].append(nodo_sub)

    except:
        print("Error leyendo regiones.txt")

    return raiz

def mostrar_jerarquia(nodo, prefijo="", es_ultimo=True, es_raiz=True):
    if es_raiz:
        print(f"🌎 {nodo['valor']}")
        nuevo_prefijo = ""
    else:
        conector = "└── " if es_ultimo else "├──"
        icono = "📍 " if not nodo["hijos"] else "🏳️  " 
        print(f"{prefijo}{conector}{icono}{nodo['valor']}")
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

    #Recorrer los hijos
    hijos = nodo["hijos"]
    cantidad_hijos = len(hijos)
    
    for i, hijo in enumerate(hijos):
        # Verificamos si el hijo actual es el último de la lista
        es_ultimo_hijo = (i == cantidad_hijos - 1)
        
        mostrar_jerarquia(hijo, nuevo_prefijo, es_ultimo_hijo, es_raiz=False)
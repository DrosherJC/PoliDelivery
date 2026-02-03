#se importa lo necesario
import usuarios
import grafos
import ordenamientos
import busquedas
import arbolRegiones
import rutas
import sys

# Variables globales para que se carguen los datos una sola vez al inicio
datos_grafo = {}   #guardaran la adyacencia
datos_centros = {} #guardaran los nombres de centros
datos_arbol = {}   #guardara el árbol de regiones

def cargar_todo():
    global datos_grafo, datos_centros, datos_arbol
    datos_grafo, datos_centros = grafos.cargar_datos()
    datos_arbol = arbolRegiones.construir_arbol()

#este es el menu para el administrador
def menu_admin():
    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Listar Centros (Ordenados)")
        print("2. Buscar Centro")
        print("3. Volver")
        opcion = input("Seleccione: ")
        
        lista = ordenamientos.obtener_lista_centros()
        
        if opcion == "1":
            if not lista:
                print("No hay centros registrados.")
                continue

            ordenada = ordenamientos.quick_sort(lista, key="nombre")
            
            print(f"\n{'ID':<5} | {'NOMBRE':<25} | {'REGIÓN'}")
            print("-" * 50)
            
            for c in ordenada:
                print(f"{c['id']:<5} | {c['nombre']:<25} | {c['region']}")
            
            print("-" * 50)
            print(f"Total: {len(ordenada)} centros.\n")
                
        elif opcion == "2":
            nombre = input("Centro a buscar: ")
            ordenada = ordenamientos.quick_sort(lista) 
            res = busquedas.busqueda_binaria(ordenada, nombre)
            if res:
                print(f"\nENCONTRADO:")
                print(f"ID: {res['id']}")
                print(f"Nombre: {res['nombre']}")
                print(f"Región: {res['region']}\n")
            else:
                print(f"\nEl centro '{nombre}' no existe.\n")
        elif opcion == "3":
            break

#este es el menu para el cliente
def menu_cliente(usuario_email):
    while True:
        print(f"\n=== MENÚ CLIENTE ({usuario_email}) ===")
        print("1. Ver mapa")
        print("2. Cotizar envío")
        print("3. Ver regiones")
        print("4. Historial")
        print("5. Volver")
        opcion = input("Seleccione: ")
        
        if opcion == "1":
            # con lo siguiente pasamos los diccionarios a la funcion
            grafos.mostrar_mapa(datos_grafo, datos_centros)
            
        elif opcion == "2":
            origen = input("ID Origen: ")
            destino = input("ID Destino: ")
            
            # despues llamamos a dijkstra pasando el grafo 
            camino, costo = grafos.dijkstra(datos_grafo, origen, destino)
            
            if camino:
                # aqui se van a recuperar nombres usando el diccionario de centros
                nombres = [datos_centros.get(pid, pid) for pid in camino]
                print(f"\nRUTA: {' -> '.join(nombres)}")
                print(f"COSTO: ${costo}")
                
                if input("¿Guardar? (s/n): ") == 's':
                    rutas.guardar_ruta_cliente(usuario_email, nombres, costo)
            else:
                print("Ruta no encontrada.")
                
        elif opcion == "3":
            arbolRegiones.mostrar_jerarquia(datos_arbol)
            
        elif opcion == "4":
            rutas.ver_historial()
            
        elif opcion == "5":
            break

def iniciar_sistema():
    # es importante cargar datos antes de empezar
    cargar_todo()
    
    while True:
        print("\nBIENVENIDO A POLIDELIVERY")
        print("1. Login")
        print("2. Registro")
        print("3. Salir")
        opcion = input("Opción: ")
        
        if opcion == "1":
            nombre, rol = usuarios.iniciar_sesion()
            if nombre:
                if rol == "admin":
                    menu_admin()
                else:
                    menu_cliente(nombre)
        elif opcion == "2":
            usuarios.registrar_usuario()
        elif opcion == "3":
            sys.exit()
def guardar_ruta_cliente(email, ruta, costo_total):
    archivo_cliente = f"data/rutasCliente.txt" # lugar donde se creara el archivo
    try:
        with open(archivo_cliente, "a", encoding="utf-8") as f:
            ruta_str = " -> ".join(ruta)
            f.write(f"Usuario: {email} | Ruta: {ruta_str} | Costo Total: ${costo_total}\n") #forma de escribir los datos en el archivo
        print("✅ Ruta guardada en historial correctamente.")
    except Exception as e:
        print(f"❌ Error guardando ruta: {e}") 


def ver_historial():
    try:
        with open("data/rutasCliente.txt", "r", encoding="utf-8") as f:
            print("\n--- HISTORIAL DE ENVÍOS ---")
            print(f.read())
    except:
        print("No hay historial disponible.")


def ver_reporte_general():
    print("\n--- REPORTE GLOBAL DE ENVÍOS (ADMIN) ---")
    
    try:
        with open("data/rutasCliente.txt", "r", encoding="utf-8") as f:
            print(f"{'USUARIO':<20} | {'COSTO':<10} | {'DETALLE'}")
            print("-" * 60)
            
            total_ingresos = 0.0
            
            for linea in f:
                partes = linea.strip().split(" | ")
                
                if len(partes) >= 3:
                    usuario = partes[0].replace("Usuario: ", "")
                    
                    try:
                        costo_str = partes[2].replace("Costo Total: $", "")
                        costo = float(costo_str)
                    except ValueError:
                        costo = 0.0

                    ruta = partes[1].replace("Ruta: ", "")
                    
                    print(f"{usuario:<20} | ${costo:<9.2f} | {ruta}")
                    total_ingresos += costo
            
            print("-" * 60)
            print(f"INGRESOS TOTALES: ${total_ingresos:.2f}")

    except FileNotFoundError:
        print("No hay historial de envíos aún.")


def ver_envios_por_centro(nombre_centro):
    print(f"\n--- ENVÍOS RELACIONADOS CON: {nombre_centro.upper()} ---")
    
    encontrado = False
    try:
        with open("data/rutasCliente.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if "Ruta: " in linea:
                    partes = linea.strip().split(" | ")
                    
                    # Buscamos la parte de la ruta
                    parte_ruta = next((p for p in partes if p.startswith("Ruta: ")), None)
                    
                    if parte_ruta:
                        # Limpiamos el string para obtener solo los nombres "A -> B -> C"
                        ruta_limpia = parte_ruta.replace("Ruta: ", "")
                        nodos = ruta_limpia.split(" -> ")
                        
                        origen = nodos[0]
                        destino = nodos[-1]
                        
                        if nombre_centro.lower() == origen.lower():
                            print(f"📤 SALIDA (Origen): {linea.strip()}")
                            encontrado = True
                        elif nombre_centro.lower() == destino.lower():
                            print(f"📥 LLEGADA (Destino): {linea.strip()}")
                            encontrado = True
                            
        if not encontrado:
            print(f"No se encontraron envíos registrados que salgan o lleguen a '{nombre_centro}'.")
            
    except FileNotFoundError:
        print("No hay historial de envíos para buscar.")
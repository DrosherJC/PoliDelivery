def guardar_ruta_cliente(email, ruta, costo_total):
    archivo_cliente = f"data/rutasCliente.txt" # lugar donde se creara el archivo
    try:
        with open(archivo_cliente, "a", encoding="utf-8") as f:
            ruta_str = " -> ".join(ruta)
            f.write(f"Usuario: {email} | Ruta: {ruta_str} | Costo Total: ${costo_total}\n") #forma de escribir los datos en el archivo
        print("Ruta guardada en historial correctamente.")
    except Exception as e:
        print(f"Error guardando ruta: {e}") 

def ver_historial():
    try:
        with open("data/rutasCliente.txt", "r", encoding="utf-8") as f:
            print("\n--- HISTORIAL DE ENVÍOS ---")
            print(f.read())
    except:
        print("No hay historial disponible.")

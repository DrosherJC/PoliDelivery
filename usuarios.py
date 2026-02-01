import os

ARCHIVO_USUARIOS = "data/usuarios.txt" #lugar donde se creara el archivo

def validar_contrasena(password):
    # Requisitos de contraseña: Minúsculas, 1 mayúscula, 1 número
    tiene_mayuscula = False
    tiene_numero = False
    
    for letra in password: #revisamos q se cumplan los requerimientos de la contraseña
        if letra.isupper():
            tiene_mayuscula = True
        if letra.isdigit():
            tiene_numero = True
            
    return tiene_mayuscula and tiene_numero

def registrar_usuario():
    print("\n--- REGISTRO DE USUARIO ---")
    nombre = input("Nombre y Apellido: ")
    identificacion = input("Identificación: ")
    edad = input("Edad: ")
    email = input("Usuario (email): ")
    
    while True:
        password = input("Contraseña: ")
        if validar_contrasena(password):
            break
        else:
            print("Error: La contraseña debe tener al menos una mayúscula y un número.")
            
    # Guardar en archivo
    try:
        with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
            linea = f"{email},{password},{nombre},{identificacion},{edad}\n"
            f.write(linea)
        print("¡Usuario registrado con éxito!")
    except Exception as e:
        print(f"Error al guardar usuario: {e}")

def iniciar_sesion():
    print("\n--- INICIAR SESIÓN ---")
    email_input = input("Email: ")
    pass_input = input("Contraseña: ")
    
    if not os.path.exists(ARCHIVO_USUARIOS):
        print("No hay usuarios registrados.")
        return None, None

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) >= 5:
                    email, password, nombre, _, _ = datos
                    if email == email_input and password == pass_input:
                        # Retorna el nombre y el rol (simple lógica para demo)
                        rol = "admin" if "admin" in email else "cliente"
                        return nombre, rol
        print("Credenciales incorrectas.")
        return None, None
    except Exception as e:
        print(f"Error al leer usuarios: {e}")
        return None, None

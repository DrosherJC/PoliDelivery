import os

ARCHIVO_USUARIOS = "data/usuarios.txt" #lugar donde se creara el archivo
CODIGO_ADMIN = "e2tru25b"

MAX_CARACTERES_NOMBRE = 50
MAX_CARACTERES_EMAIL = 50

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
    while True:
        nombre = input(f"Nombre y Apellido (máx {MAX_CARACTERES_NOMBRE}): ")
        if len(nombre) > MAX_CARACTERES_NOMBRE:
            print(f"Error: El nombre es muy largo. Máximo {MAX_CARACTERES_NOMBRE} caracteres.")
        elif len(nombre) < 1:
            print("Error: El nombre no puede estar vacío.")
        else:
            break # El nombre es válido

    #Validación de Identificación 
    while True:
        identificacion = input("Identificación (10 dígitos): ")
        if len(identificacion) == 10 and identificacion.isdigit():
            break # Es válido
        else:
            print("Error: La identificación debe tener exactamente 10 números y sin letras.")

    edad = input("Edad: ")

    #Validación de Email 
    while True:
        email = input(f"Usuario (email) (máx {MAX_CARACTERES_EMAIL}): ")
        
        if len(email) > MAX_CARACTERES_EMAIL:
            print(f"Error: El correo es muy largo. Máximo {MAX_CARACTERES_EMAIL} caracteres.")
        elif len(email) < 5:
            print("Error: Correo demasiado corto.")
        elif "@" not in email:
            print("Error: El correo electrónico debe contener una arroba (@).")
        else:
            break #Es válido

    if "admin" in email:
        print("AVISO: Se ha detectado un intento de registro como ADMINISTRADOR.")
        codigo_ingresado = input("Ingrese el código de autorización: ")
        
        if codigo_ingresado != CODIGO_ADMIN:
            print("Error: Código de autorización incorrecto. Registro cancelado.")
            return 

    while True:
        password = input("Contraseña: ")
        if validar_contrasena(password):
            break
        else:
            print("Error: La contraseña debe tener al menos una mayúscula y un número.")
            
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
                        # Retorna el nombre y el rol 
                        rol = "admin" if "admin" in email else "cliente"
                        return nombre, rol
        print("Credenciales incorrectas.")
        return None, None
    except Exception as e:
        print(f"Error al leer usuarios: {e}")
        return None, None

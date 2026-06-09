# 🛵 PoliDelivery — Sistema de Gestión de Entregas Basado en Algoritmos y Estructuras de Datos

**PoliDelivery** es una aplicación de consola desarrollada en Python puro enfocada en la gestión de logística y entregas a domicilio. A diferencia de las aproximaciones convencionales, este sistema no utiliza Programación Orientada a Objetos (POO), sino que está construido bajo el paradigma de **Programación Estructurada**, empleando algoritmos avanzados de búsqueda, ordenamiento, y estructuras de datos complejas (Grafos y Árboles Jerárquicos) con persistencia de datos en archivos planos (`.txt`).

---

## 🚀 Componentes y Arquitectura del Sistema

El proyecto está modularizado en funciones específicas divididas por su rol algorítmico:

* **`main.py`:** Punto de entrada del programa que coordina el flujo general de la aplicación.
* **`menu.py`:** Gestiona los menús interactivos de la terminal, incluyendo vistas específicas para la administración.
* **`grafos.py` & `rutas.py`:** Implementación de mapas y optimización de caminos mediante modelos de Grafos para calcular las rutas de entrega eficientemente.
* **`arbolRegiones.py`:** Estructura de datos en forma de árbol para organizar jerárquicamente las regiones y zonas geográficas de cobertura.
* **`ordenamientos.py`:** Contiene la lógica de algoritmos de ordenamiento para organizar datos (como pedidos por prioridad, usuarios, o rutas por distancia).
* **`busquedas.py`:** Algoritmos de búsqueda optimizados para localizar elementos específicos de manera rápida dentro de las estructuras en memoria.
* **`usuarios.py`:** Funciones de control, login y validaciones de seguridad para los accesos al sistema.

---

## 💾 Persistencia de Datos (`/data`)

El sistema utiliza archivos de texto plano para mantener la información persistente entre ejecuciones, simulando una base de datos relacional mediante parsing de archivos:

```text
└── data/
    ├── centros.txt       # Centros de distribución o despacho logístico
    ├── regiones.txt      # Jerarquía de zonas y regiones geográficas
    ├── rutas.txt         # Conexiones de la red vial (Aristas del Grafo)
    ├── rutasCliente.txt  # Asignaciones de rutas específicas por cliente
    └── usuarios.txt      # Credenciales y datos de control validados

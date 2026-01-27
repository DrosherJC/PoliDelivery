import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from grafos import GrafoEntregas
import os
from datetime import datetime

class SistemaEntregasTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("🚚 Sistema Entregas Quito - Tkinter + Dijkstra")
        self.root.geometry("900x650")

        self.grafo = GrafoEntregas()
        self.grafo.cargar_rutas_quito()
        self.contador_id = 1
        self.entregas = [] 

        self.inicializar_archivo_facturas()
        
        self.crear_interfaz()
        
    def inicializar_archivo_facturas(self):
        """Crea/abre rutas-cliente.txt en modo APPEND"""
        try:
            with open('rutas-cliente.txt', 'a', encoding='utf-8') as f:
                f.seek(0, 2)  
                if f.tell() == 0:  
                    f.write("🚚 FACTURAS DE ENTREGAS QUITO\n")
                    f.write(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    f.write("="*60 + "\n\n")
            print("rutas-cliente.txt inicializado")
        except:
            print("No se pudo inicializar archivo")
    
    def crear_interfaz(self):
        titulo = tk.Label(self.root, text="🚚 SISTEMA DE ENTREGAS QUITO", 
                         font=("Arial", 20, "bold"), bg="#2c3e50", fg="white")
        titulo.pack(pady=10, fill="x")
     
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
        left_panel = ttk.LabelFrame(main_frame, text="📦 Nuevo Pedido")
        main_frame.add(left_panel, weight=1)

        ttk.Label(left_panel, text="Nombre Cliente:", font=("Arial", 12, "bold")).pack(pady=10)
        self.nombre_entry = ttk.Entry(left_panel, width=25, font=("Arial", 12))
        self.nombre_entry.pack(pady=5)
        self.nombre_entry.insert(0, "Juan Pérez")
        self.nombre_entry.focus()

        barrios_populares = ['Centro', 'La_Florida', 'Quitumbe', 'Cumbaya']
        ttk.Label(left_panel, text="Origen:", font=("Arial", 12, "bold")).pack(pady=(20,5))
        self.origen_var = tk.StringVar(value="Centro")
        ttk.Combobox(left_panel, textvariable=self.origen_var, 
                    values=barrios_populares, state="readonly").pack(pady=5)
        
        ttk.Label(left_panel, text="Destino:", font=("Arial", 12, "bold")).pack(pady=(10,5))
        self.destino_var = tk.StringVar(value="Quitumbe")
        ttk.Combobox(left_panel, textvariable=self.destino_var, 
                    values=barrios_populares, state="readonly").pack(pady=5)
    
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="➕ PROCESAR Pedido", 
                  command=self.procesar_pedido, width=20).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="📁 CARGAR centros.txt", 
                  command=self.cargar_centros, width=20).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="📋 VER rutas-cliente.txt", 
                  command=self.ver_facturas, width=20).pack(pady=5, fill="x")
      
        right_panel = ttk.LabelFrame(main_frame, text="📊 Historial Entregas")
        main_frame.add(right_panel, weight=2)
        
        self.historial_text = scrolledtext.ScrolledText(right_panel, height=28, font=("Consolas", 10))
        self.historial_text.pack(fill="both", expand=True, padx=10, pady=10)
  
        self.status_var = tk.StringVar(value=f"Listo - ID Siguiente: {self.contador_id}")
        ttk.Label(self.root, textvariable=self.status_var, relief="sunken").pack(side="bottom", fill="x")
    
    def procesar_pedido(self):
        """➕ NUEVO: Procesa pedido + Dijkstra AUTO + Guarda en archivo"""
        nombre = self.nombre_entry.get().strip()
        origen = self.origen_var.get()
        destino = self.destino_var.get()
        
        if not nombre:
            messagebox.showwarning("Error", "Ingresa nombre del cliente")
            return
        
        try:
            i = self.grafo.nodos.index(origen)
            f = self.grafo.nodos.index(destino)
            ruta, km = self.grafo.dijkstra_entrega(i, f)
            costo = km * 0.50
          
            id_envio = self.contador_id
            self.contador_id += 1
         
            with open('rutas-cliente.txt', 'a', encoding='utf-8') as f:
                f.write(f"ID: {id_envio:03d} | {nombre:<20} | ")
                f.write(f"{origen:<12} → {destino:<12} | ")
                f.write(f"Ruta: {' → '.join(ruta)} | {km:.1f}km | ${costo:.2f}\n")
        
            self.entregas.append({
                'id': id_envio, 'nombre': nombre, 'origen': origen, 
                'destino': destino, 'ruta': ruta, 'km': km, 'costo': costo
            })
         
            linea = f"ID:{id_envio:03d} {nombre:<20} "
            linea += f"{origen} → {destino} = {km:.1f}km → ${costo:.2f}"
            self.historial_text.insert(tk.END, linea + "\n")
            self.historial_text.see(tk.END)
        
            self.nombre_entry.delete(0, tk.END)
            self.status_var.set(f"Procesado ID:{id_envio} - Siguiente: {self.contador_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No hay ruta entre {origen} y {destino}")
    
    def cargar_centros(self):
        """Carga centros.txt y PROCESA AUTOMÁTICO todos"""
        filename = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not filename: return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        parts = linea.strip().split(',')
                        if len(parts) >= 3:
                            nombre, origen, destino = parts[0], parts[1], parts[2]
                            self.nombre_entry.delete(0, tk.END)
                            self.nombre_entry.insert(0, nombre)
                            self.origen_var.set(origen)
                            self.destino_var.set(destino)
                            self.procesar_pedido()  
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando: {str(e)}")
    
    def ver_facturas(self):
        """Muestra contenido actual de rutas-cliente.txt"""
        try:
            with open('rutas-cliente.txt', 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.historial_text.delete(1.0, tk.END)
            self.historial_text.insert(tk.END, contenido)
        except:
            messagebox.showerror("Error", "No se pudo leer rutas-cliente.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEntregasTkinter(root)
    root.mainloop()


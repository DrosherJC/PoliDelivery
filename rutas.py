import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from grafos import GrafoEntregas
import os
from datetime import datetime

class SistemaEntregasTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Entregas Quito - Tkinter + Dijkstra")
        self.root.geometry("1000x700")

        self.grafo = GrafoEntregas()
        self.grafo.cargar_rutas_quito()
        self.clientes_procesados = []
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        titulo = tk.Label(self.root, text="SISTEMA DE ENTREGAS QUITO", 
                         font=("Arial", 22, "bold"), bg="#2c3e50", fg="white")
        titulo.pack(pady=10, fill="x")
 
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
     
        left_panel = ttk.LabelFrame(main_frame, text="Gestión de Clientes")
        main_frame.add(left_panel, weight=1)

        ttk.Label(left_panel, text="Origen:", font=("Arial", 12, "bold")).pack(pady=5)
        self.origen_var = tk.StringVar(value="Centro")
        self.cb_origen = ttk.Combobox(left_panel, textvariable=self.origen_var,
                                     values=self.grafo.nodos, state="readonly", width=20)
        self.cb_origen.pack(pady=5)
        
        ttk.Label(left_panel, text="Destino:", font=("Arial", 12, "bold")).pack(pady=5)
        self.destino_var = tk.StringVar(value="Quitumbe")
        self.cb_destino = ttk.Combobox(left_panel, textvariable=self.destino_var,
                                      values=self.grafo.nodos, state="readonly", width=20)
        self.cb_destino.pack(pady=5)

        ttk.Label(left_panel, text="Cliente:", font=("Arial", 12, "bold")).pack(pady=(20,5))
        self.cliente_entry = ttk.Entry(left_panel, width=25, font=("Arial", 12))
        self.cliente_entry.pack(pady=5)
        self.cliente_entry.insert(0, "Juan Pérez")

        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="➕ Agregar Cliente", 
                  command=self.agregar_cliente).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="Calcular Ruta (Dijkstra)", 
                  command=self.calcular_ruta).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="Cargar centros.txt", 
                  command=self.cargar_centros).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="Guardar rutas-cliente.txt", 
                  command=self.guardar_rutas).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="Procesar Todos", 
                  command=self.procesar_todos).pack(pady=5, fill="x")

        right_panel = ttk.LabelFrame(main_frame, text="Rutas Calculadas")
        main_frame.add(right_panel, weight=2)
        
        self.resultados_text = scrolledtext.ScrolledText(right_panel, height=30, font=("Consolas", 11))
        self.resultados_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_var = tk.StringVar(value="Listo - Agrega clientes y calcula rutas")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
        
    def agregar_cliente(self):
        cliente = self.cliente_entry.get().strip()
        origen = self.origen_var.get()
        destino = self.destino_var.get()
        
        if cliente and origen in self.grafo.nodos and destino in self.grafo.nodos:
            self.clientes_procesados.append((cliente, origen, destino))
            self.resultados_text.insert(tk.END, f"➕ {cliente}: {origen} → {destino}\n")
            self.cliente_entry.delete(0, tk.END)
            self.status_var.set(f"Cliente {cliente} agregado. Total: {len(self.clientes_procesados)}")
        else:
            messagebox.showwarning("Error", "Completa todos los campos correctamente")
    
    def calcular_ruta(self):
        cliente = self.cliente_entry.get().strip()
        if not cliente:
            messagebox.showwarning("Error", "Ingresa nombre del cliente")
            return
            
        try:
            orig_idx = self.grafo.nodos.index(self.origen_var.get())
            dest_idx = self.grafo.nodos.index(self.destino_var.get())
            ruta, km = self.grafo.dijkstra_entrega(orig_idx, dest_idx)
            costo = km * 0.50
            
            resultado = f"{cliente}\n"
            resultado += f"{self.origen_var.get()} → {self.destino_var.get()}\n"
            resultado += f"{' → '.join(ruta)}\n"
            resultado += f"{km:.1f} km → ${costo:.2f}\n\n"
            
            self.resultados_text.insert(tk.END, resultado)
            self.status_var.set(f"Ruta calculada: {km:.1f}km - ${costo:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No hay ruta: {str(e)}")
    
    def cargar_centros(self):
        """LEE centros.txt (misma funcionalidad original)"""
        filename = filedialog.askopenfilename(
            title="Seleccionar centros.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return
            
        try:
            self.clientes_procesados = []
            self.resultados_text.delete(1.0, tk.END)
            total_km = 0
            
            with open(filename, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        cliente, orig, dest = linea.strip().split(',')
                        if orig in self.grafo.nodos and dest in self.grafo.nodos:
                            self.clientes_procesados.append((cliente, orig, dest))
                            orig_idx, dest_idx = self.grafo.nodos.index(orig), self.grafo.nodos.index(dest)
                            ruta, km = self.grafo.dijkstra_entrega(orig_idx, dest_idx)
                            total_km += km
                            self.resultados_text.insert(tk.END, f"{cliente}: {' → '.join(ruta)} ({km:.1f}km)\n")
            
            self.status_var.set(f"Cargados {len(self.clientes_procesados)} clientes - {total_km:.1f}km total")
            messagebox.showinfo("Éxito", f"Cargados {len(self.clientes_procesados)} clientes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error leyendo archivo: {str(e)}")
    
    def guardar_rutas(self):
        """GUARDA rutas-cliente.txt (misma funcionalidad original)"""
        filename = filedialog.asksaveasfilename(
            title="Guardar rutas-cliente.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("FACTURAS DE ENTREGAS QUITO\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write("="*60 + "\n\n")
                f.write(self.resultados_text.get(1.0, tk.END))
            
            messagebox.showinfo("Guardado", f"Guardado en {filename}")
            self.status_var.set(f"Guardado: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando: {str(e)}")
    
    def procesar_todos(self):
        """Procesa todos los clientes agregados"""
        if not self.clientes_procesados:
            messagebox.showwarning("Advertencia", "No hay clientes para procesar")
            return
            
        self.resultados_text.delete(1.0, tk.END)
        total_km = 0
        total_costo = 0
        
        for cliente, orig, dest in self.clientes_procesados:
            try:
                i, f = self.grafo.nodos.index(orig), self.grafo.nodos.index(dest)
                ruta, km = self.grafo.dijkstra_entrega(i, f)
                costo = km * 0.50
                total_km += km
                total_costo += costo
                
                linea = f"{cliente}: {' → '.join(ruta)} ({km:.1f}km) → ${costo:.2f}\n"
                self.resultados_text.insert(tk.END, linea)
                
            except:
                self.resultados_text.insert(tk.END, f"{cliente}: Sin ruta\n")
        
        self.status_var.set(f"Procesados {len(self.clientes_procesados)} - Total: {total_km:.1f}km ${total_costo:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEntregasTkinter(root)
    root.mainloop()

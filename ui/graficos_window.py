"""
Ventana de Gráficos Estadísticos
Utiliza Matplotlib para renderizar gráficos dentro de Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from business.reportes_service import ReportesService

class GraficosWindow:
    """Ventana visual de gráficos estadísticos"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gráficos Estadísticos")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')
        
        # Variables de control
        self.anio_actual = date.today().year
        self.mes_actual = date.today().month
        
        self.crear_widgets()
        self.cargar_graficos_iniciales()
        
        # Traer al frente
        self.window.lift()
        self.window.focus_force()
        
        # Manejo de cierre correcto para liberar memoria de matplotlib
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cerrar_ventana(self):
        plt.close('all') # Cerrar todas las figuras para liberar memoria
        self.window.destroy()

    def crear_widgets(self):
        # --- HEADER ---
        frame_top = tk.Frame(self.window, bg='#f0f0f0', pady=10)
        frame_top.pack(fill=tk.X, padx=20)
        
        tk.Label(frame_top, text="📈 Dashboard Estadístico", font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(side=tk.LEFT)
        
        # Filtros Globales (Año/Mes)
        frame_filtros = tk.Frame(frame_top, bg='#f0f0f0')
        frame_filtros.pack(side=tk.RIGHT)
        
        tk.Label(frame_filtros, text="Año:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.spin_anio = tk.Spinbox(frame_filtros, from_=2020, to=2030, width=5)
        self.spin_anio.delete(0, tk.END)
        self.spin_anio.insert(0, self.anio_actual)
        self.spin_anio.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Mes:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.cmb_mes = ttk.Combobox(frame_filtros, values=list(range(1, 13)), width=3, state='readonly')
        self.cmb_mes.set(self.mes_actual)
        self.cmb_mes.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="🔄 Actualizar", command=self.actualizar_graficos, bg='#3498db', fg='white', relief=tk.FLAT).pack(side=tk.LEFT, padx=15)

        # --- AREA DE GRÁFICOS (Grid 2x2) ---
        self.frame_graficos = tk.Frame(self.window, bg='#f0f0f0')
        self.frame_graficos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configurar Grid 2x2
        self.frame_graficos.columnconfigure(0, weight=1)
        self.frame_graficos.columnconfigure(1, weight=1)
        self.frame_graficos.rowconfigure(0, weight=1)
        self.frame_graficos.rowconfigure(1, weight=1)
        
        # Contenedores para cada gráfico
        self.frame_g1 = tk.Frame(self.frame_graficos, bg='white', relief=tk.RAISED, bd=1)
        self.frame_g1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.frame_g2 = tk.Frame(self.frame_graficos, bg='white', relief=tk.RAISED, bd=1)
        self.frame_g2.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        self.frame_g3 = tk.Frame(self.frame_graficos, bg='white', relief=tk.RAISED, bd=1)
        self.frame_g3.grid(row=1, column=0, padx=5, pady=5, sticky='nsew') # Ocupa todo el ancho abajo
        
        self.frame_g4 = tk.Frame(self.frame_graficos, bg='white', relief=tk.RAISED, bd=1)
        self.frame_g4.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    def cargar_graficos_iniciales(self):
        self.actualizar_graficos()

    def actualizar_graficos(self):
        try:
            anio = int(self.spin_anio.get())
            mes = int(self.cmb_mes.get())
        except ValueError:
            anio = self.anio_actual
            mes = self.mes_actual

        # Limpiar gráficos anteriores
        for widget in self.frame_g1.winfo_children(): widget.destroy()
        for widget in self.frame_g2.winfo_children(): widget.destroy()
        for widget in self.frame_g3.winfo_children(): widget.destroy()
        for widget in self.frame_g4.winfo_children(): widget.destroy()

        # Generar nuevos
        self.grafico_estado_reservas(self.frame_g1)
        self.grafico_facturacion_anual(self.frame_g2, anio)
        self.grafico_utilizacion_mensual(self.frame_g3, anio, mes)
        self.grafico_top_canchas(self.frame_g4)

    # ----------------------------------------------------------------
    # 1. ESTADO DE RESERVAS (Pie Chart)
    # ----------------------------------------------------------------
    def grafico_estado_reservas(self, parent):
        tk.Label(parent, text="Estado de Reservas (Total)", font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        try:
            datos = ReportesService.reporte_estado_reservas() # Retorna dict {'pendiente': 5, ...}
            
            if not datos or sum(datos.values()) == 0:
                tk.Label(parent, text="Sin datos", bg='white').pack(expand=True)
                return

            labels = [k.capitalize() for k in datos.keys()]
            sizes = list(datos.values())
            colors = ['#f1c40f', '#2ecc71', '#e74c3c', '#3498db'] # Colores: Amarillo, Verde, Rojo, Azul
            
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal') # Para que sea un círculo
            
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Error: {e}", fg='red', bg='white').pack()

    # ----------------------------------------------------------------
    # 2. FACTURACIÓN ANUAL (Bar Chart)
    # ----------------------------------------------------------------
    def grafico_facturacion_anual(self, parent, anio):
        tk.Label(parent, text=f"Facturación Mensual {anio}", font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        try:
            # Nota: Solo suma reservas confirmadas/completadas (pagadas)
            datos = ReportesService.reporte_facturacion_mensual(anio) # {1: 1000, 2: 0...}
            
            meses = list(datos.keys())
            montos = list(datos.values())
            
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.bar(meses, montos, color='#27ae60')
            
            ax.set_xlabel('Mes')
            ax.set_ylabel('Monto ($)')
            ax.set_xticks(meses)
            
            # Formato simple si no hay datos
            if sum(montos) == 0:
                tk.Label(parent, text="Sin facturación confirmada este año", bg='white').pack(expand=True)
                plt.close(fig)
                return

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Error: {e}", fg='red', bg='white').pack()

    # ----------------------------------------------------------------
    # 3. UTILIZACIÓN MENSUAL (Line Chart)
    # ----------------------------------------------------------------
    def grafico_utilizacion_mensual(self, parent, anio, mes):
        meses_nom = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        nombre_mes = meses_nom[mes-1]
        tk.Label(parent, text=f"Reservas por Día - {nombre_mes} {anio}", font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        try:
            # Retorna dict {1: 2, 2: 0, 3: 5...} con todos los días del mes
            datos = ReportesService.reporte_utilizacion_mensual(anio, mes)
            
            dias = list(datos.keys())
            cantidades = list(datos.values())
            
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.plot(dias, cantidades, marker='o', linestyle='-', color='#e67e22')
            
            ax.set_xlabel('Día')
            ax.set_ylabel('Cant. Reservas')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Error: {e}", fg='red', bg='white').pack()

    # ----------------------------------------------------------------
    # 4. TOP CANCHAS (Horizontal Bar Chart)
    # ----------------------------------------------------------------
    def grafico_top_canchas(self, parent):
        tk.Label(parent, text="Top Canchas (Histórico)", font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        try:
            # Reutilizamos el reporte de ranking
            datos = ReportesService.reporte_canchas_mas_utilizadas()
            # Tomamos el top 5
            datos = datos[:5]
            
            if not datos:
                tk.Label(parent, text="Sin datos", bg='white').pack(expand=True)
                return

            nombres = [d['cancha'].nombre for d in datos]
            reservas = [d['total_reservas'] for d in datos]
            
            # Invertir para que el #1 quede arriba en gráfico horizontal
            nombres.reverse()
            reservas.reverse()
            
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.barh(nombres, reservas, color='#3498db')
            
            ax.set_xlabel('Total Reservas')
            
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Error: {e}", fg='red', bg='white').pack()
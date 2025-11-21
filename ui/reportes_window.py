"""
Ventana Unificada de Reportes y Gráficos
ACTUALIZADO: Gráfico de Ranking limpio (sin etiquetas de texto sobre las barras).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from business.reportes_service import ReportesService
from utils.helpers import formatear_monto

class ReportesWindow:
    """Ventana principal de reportes unificados"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Reportes del Sistema")
        
        try:
            self.window.state('zoomed')
        except:
            try:
                self.window.attributes('-zoomed', True)
            except:
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                self.window.geometry(f"{screen_width-50}x{screen_height-100}+0+0")
                
        self.window.configure(bg='#f0f0f0')
        
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", font=('Arial', 11, 'bold'), padding=[20, 10])
        
        self.anio_actual = date.today().year
        self.mes_actual = date.today().month
        
        self.crear_widgets()
        
        self.window.lift()
        self.window.focus_force()
        
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cerrar_ventana(self):
        plt.close('all')
        self.window.destroy()
    
    def crear_widgets(self):
        tk.Label(self.window, text="📊 Reportes y Estadísticas", font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(pady=15)
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.tab_estado = tk.Frame(self.notebook, bg='#f0f0f0')
        self.tab_ranking = tk.Frame(self.notebook, bg='#f0f0f0')
        self.tab_ingresos = tk.Frame(self.notebook, bg='#f0f0f0')
        
        self.notebook.add(self.tab_estado, text="Estado de Reservas")
        self.notebook.add(self.tab_ranking, text="Ranking de Canchas")
        self.notebook.add(self.tab_ingresos, text="Ingresos")
        
        self.crear_tab_estado()
        self.crear_tab_ranking()
        self.crear_tab_ingresos()

    # 1. ESTADO DE RESERVAS
    def crear_tab_estado(self):
        frame_filtros = tk.Frame(self.tab_estado, bg='#f0f0f0', pady=10)
        frame_filtros.pack(fill=tk.X)
        
        tk.Label(frame_filtros, text="Mes:", bg='#f0f0f0', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        self.cmb_mes_estado = ttk.Combobox(frame_filtros, values=list(range(1, 13)), width=3, state='readonly', font=('Arial', 11))
        self.cmb_mes_estado.set(self.mes_actual)
        self.cmb_mes_estado.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Año:", bg='#f0f0f0', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        self.spin_anio_estado = tk.Spinbox(frame_filtros, from_=2020, to=2030, width=5, font=('Arial', 11))
        self.spin_anio_estado.delete(0, tk.END)
        self.spin_anio_estado.insert(0, self.anio_actual)
        self.spin_anio_estado.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="Actualizar", command=self.cargar_grafico_estado, bg='#3498db', fg='white', relief=tk.FLAT, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=15)
        
        self.lbl_total_reservas = tk.Label(self.tab_estado, text="", font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#34495e')
        self.lbl_total_reservas.pack(pady=(0, 10))

        self.frame_graf_estado = tk.Frame(self.tab_estado, bg='white', relief=tk.RAISED, bd=1)
        self.frame_graf_estado.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.cargar_grafico_estado()

    def cargar_grafico_estado(self):
        for widget in self.frame_graf_estado.winfo_children(): widget.destroy()
        
        try:
            anio = int(self.spin_anio_estado.get())
            mes = int(self.cmb_mes_estado.get())
            datos = ReportesService.reporte_estado_reservas_mensual(anio, mes)
            
            val_confirmadas = datos.get('confirmada', 0) + datos.get('completada', 0)
            val_pendientes = datos.get('pendiente', 0)
            val_canceladas = datos.get('cancelada', 0)
            total_reservas = val_confirmadas + val_pendientes + val_canceladas
            
            self.lbl_total_reservas.config(text=f"Cantidad de Reservas: {total_reservas}")

            if total_reservas == 0:
                tk.Label(self.frame_graf_estado, text="Sin datos para este período", bg='white', font=('Arial', 12)).pack(expand=True)
                return

            sizes = []
            labels = []
            colors = []
            
            if val_confirmadas > 0:
                sizes.append(val_confirmadas)
                labels.append('Confirmadas')
                colors.append('#2ecc71')
            if val_pendientes > 0:
                sizes.append(val_pendientes)
                labels.append('Pendientes')
                colors.append('#f1c40f')
            if val_canceladas > 0:
                sizes.append(val_canceladas)
                labels.append('Canceladas')
                colors.append('#e74c3c')

            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
            ax.axis('equal')
            ax.set_title(f"Estado de Reservas - {mes}/{anio}", fontsize=14, fontweight='bold', pad=20)
            
            canvas = FigureCanvasTkAgg(fig, master=self.frame_graf_estado)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ValueError:
            messagebox.showerror("Error", "Año inválido")

    # 2. RANKING DE CANCHAS
    def crear_tab_ranking(self):
        frame_filtros = tk.Frame(self.tab_ranking, bg='#f0f0f0', pady=10)
        frame_filtros.pack(fill=tk.X)
        
        tk.Label(frame_filtros, text="Mes:", bg='#f0f0f0', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        self.cmb_mes_ranking = ttk.Combobox(frame_filtros, values=list(range(1, 13)), width=3, state='readonly', font=('Arial', 11))
        self.cmb_mes_ranking.set(self.mes_actual)
        self.cmb_mes_ranking.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Año:", bg='#f0f0f0', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        self.spin_anio_ranking = tk.Spinbox(frame_filtros, from_=2020, to=2030, width=5, font=('Arial', 11))
        self.spin_anio_ranking.delete(0, tk.END)
        self.spin_anio_ranking.insert(0, self.anio_actual)
        self.spin_anio_ranking.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="Actualizar", command=self.cargar_grafico_ranking, bg='#3498db', fg='white', relief=tk.FLAT, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=15)
        
        self.frame_graf_ranking = tk.Frame(self.tab_ranking, bg='white', relief=tk.RAISED, bd=1)
        self.frame_graf_ranking.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.cargar_grafico_ranking()

    def cargar_grafico_ranking(self):
        for widget in self.frame_graf_ranking.winfo_children(): widget.destroy()
        
        try:
            anio = int(self.spin_anio_ranking.get())
            mes = int(self.cmb_mes_ranking.get())
            
            datos = ReportesService.reporte_ranking_canchas_mensual(anio, mes)
            
            if not datos:
                tk.Label(self.frame_graf_ranking, text="Sin reservas para este período", bg='white', font=('Arial', 12)).pack(expand=True)
                return
                
            nombres = [d['nombre'] for d in datos]
            reservas = [d['reservas'] for d in datos]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Dibujar barras
            ax.bar(nombres, reservas, color='#9b59b6', width=0.6)
            
            ax.set_ylabel('Cantidad de Reservas', fontsize=11)
            ax.set_title(f"Top Canchas Más Utilizadas - {mes}/{anio}", fontsize=14, fontweight='bold', pad=20)
            
            # NOTA: Se eliminó el bucle que añadía etiquetas de texto (números) sobre las barras.
            
            canvas = FigureCanvasTkAgg(fig, master=self.frame_graf_ranking)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ValueError:
            messagebox.showerror("Error", "Año inválido")

    # 3. INGRESOS
    def crear_tab_ingresos(self):
        frame_filtros = tk.Frame(self.tab_ingresos, bg='#f0f0f0', pady=10)
        frame_filtros.pack(fill=tk.X)
        
        tk.Label(frame_filtros, text="Año:", bg='#f0f0f0', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        self.spin_anio_ingresos = tk.Spinbox(frame_filtros, from_=2020, to=2030, width=6, font=('Arial', 11))
        self.spin_anio_ingresos.delete(0, tk.END)
        self.spin_anio_ingresos.insert(0, self.anio_actual)
        self.spin_anio_ingresos.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="Calcular", command=self.cargar_ingresos, bg='#27ae60', fg='white', relief=tk.FLAT, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=15)
        
        self.paned = tk.PanedWindow(self.tab_ingresos, orient=tk.VERTICAL, bg='#f0f0f0')
        self.paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.frame_graf_ingresos = tk.Frame(self.paned, bg='white', relief=tk.RAISED, bd=1)
        self.paned.add(self.frame_graf_ingresos, height=450)
        
        self.frame_tabla_ingresos = tk.Frame(self.paned, bg='#f0f0f0')
        self.paned.add(self.frame_tabla_ingresos)
        
        scrollbar = ttk.Scrollbar(self.frame_tabla_ingresos)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_ingresos = ttk.Treeview(self.frame_tabla_ingresos, columns=('Mes', 'Ingreso'), show='headings', yscrollcommand=scrollbar.set)
        self.tree_ingresos.heading('Mes', text='Mes')
        self.tree_ingresos.heading('Ingreso', text='Total Ingresos')
        self.tree_ingresos.column('Mes', anchor='center', width=150)
        self.tree_ingresos.column('Ingreso', anchor='e', width=150)
        
        scrollbar.config(command=self.tree_ingresos.yview)
        self.tree_ingresos.pack(fill=tk.BOTH, expand=True)
        
        self.cargar_ingresos()

    def cargar_ingresos(self):
        for widget in self.frame_graf_ingresos.winfo_children(): widget.destroy()
        for item in self.tree_ingresos.get_children(): self.tree_ingresos.delete(item)
        
        try:
            anio = int(self.spin_anio_ingresos.get())
            datos = ReportesService.reporte_ingresos_anual(anio)
            
            meses_nom = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            montos = []
            total_anual = 0
            
            for mes_num in range(1, 13):
                ingreso = datos.get(mes_num, 0)
                montos.append(ingreso)
                total_anual += ingreso
                self.tree_ingresos.insert('', tk.END, values=(meses_nom[mes_num-1], formatear_monto(ingreso)))
            
            self.tree_ingresos.insert('', tk.END, values=("TOTAL ANUAL", formatear_monto(total_anual)), tags=('total',))
            self.tree_ingresos.tag_configure('total', font=('Arial', 10, 'bold'), background='#d4edda')
            
            if total_anual == 0:
                tk.Label(self.frame_graf_ingresos, text="Sin ingresos confirmados este año", bg='white', font=('Arial', 12)).pack(expand=True)
            else:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(meses_nom, montos, color='#27ae60')
                ax.set_ylabel('Ingresos ($)', fontsize=11)
                ax.set_title(f'Evolución de Ingresos - {anio}', fontsize=14, fontweight='bold', pad=15)
                canvas = FigureCanvasTkAgg(fig, master=self.frame_graf_ingresos)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
        except ValueError:
            messagebox.showerror("Error", "Año inválido")
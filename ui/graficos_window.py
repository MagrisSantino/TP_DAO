"""
Ventana de Gráficos Estadísticos
Visualización gráfica de estadísticas del sistema
VERSIÓN CORREGIDA - Manejo robusto de datos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, time
from tkcalendar import DateEntry
from business.reportes_service import ReportesService
from utils.graficos import Graficos
import matplotlib
matplotlib.use('TkAgg')


class GraficosWindow:
    """Ventana para visualización de gráficos estadísticos"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gráficos Estadísticos")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')
        
        self.crear_widgets()
        self.centrar_ventana()
        
        # Cargar gráfico inicial
        self.mostrar_utilizacion_mensual()
    
    def centrar_ventana(self):
        """Centra la ventana"""
        self.window.update_idletasks()
        ancho = self.window.winfo_width()
        alto = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.window.winfo_screenheight() // 2) - (alto // 2)
        self.window.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        """Crea todos los widgets"""
        # Frame superior con título
        frame_top = tk.Frame(self.window, bg='#2c3e50', height=80)
        frame_top.pack(fill=tk.X)
        frame_top.pack_propagate(False)
        
        tk.Label(
            frame_top,
            text="📊 Gráficos Estadísticos",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)
        
        # Frame de contenido
        content_frame = tk.Frame(self.window, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Opciones
        left_panel = tk.Frame(content_frame, bg='white', width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Título del panel
        tk.Label(
            left_panel,
            text="Seleccione Gráfico",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Botones de opciones
        btn_style = {
            'font': ('Arial', 10),
            'bg': '#3498db',
            'fg': 'white',
            'activebackground': '#2980b9',
            'activeforeground': 'white',
            'cursor': 'hand2',
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 10
        }
        
        tk.Button(
            left_panel,
            text="📈 Utilización Mensual",
            command=self.mostrar_utilizacion_mensual,
            **btn_style
        ).pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(
            left_panel,
            text="🏟️ Canchas Más Usadas",
            command=self.mostrar_canchas_mas_utilizadas,
            **btn_style
        ).pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(
            left_panel,
            text="💰 Facturación Anual",
            command=self.mostrar_facturacion_anual,
            **btn_style
        ).pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(
            left_panel,
            text="📊 Estado Reservas",
            command=self.mostrar_estado_reservas,
            **btn_style
        ).pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(
            left_panel,
            text="🕐 Distribución Horaria",
            command=self.mostrar_distribucion_horaria,
            **btn_style
        ).pack(fill=tk.X, padx=20, pady=5)
        
        # Separador
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)
        
        # Controles de fecha
        tk.Label(
            left_panel,
            text="Controles de Fecha",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=10)
        
        # Año
        frame_año = tk.Frame(left_panel, bg='white')
        frame_año.pack(padx=20, pady=5)
        
        tk.Label(frame_año, text="Año:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        self.spin_año = tk.Spinbox(
            frame_año,
            from_=2020,
            to=2030,
            width=10,
            font=('Arial', 10)
        )
        self.spin_año.pack(side=tk.LEFT, padx=5)
        self.spin_año.delete(0, tk.END)
        self.spin_año.insert(0, date.today().year)
        
        # Mes
        frame_mes = tk.Frame(left_panel, bg='white')
        frame_mes.pack(padx=20, pady=5)
        
        tk.Label(frame_mes, text="Mes:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        self.spin_mes = tk.Spinbox(
            frame_mes,
            from_=1,
            to=12,
            width=10,
            font=('Arial', 10)
        )
        self.spin_mes.pack(side=tk.LEFT, padx=5)
        self.spin_mes.delete(0, tk.END)
        self.spin_mes.insert(0, date.today().month)
        
        # Panel derecho - Área de gráficos
        self.graph_panel = tk.Frame(content_frame, bg='white')
        self.graph_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frame para botones de exportación
        export_frame = tk.Frame(self.window, bg='#f0f0f0')
        export_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(
            export_frame,
            text="💾 Guardar Gráfico",
            command=self.guardar_grafico,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
    
    def limpiar_panel(self):
        """Limpia el panel de gráficos"""
        for widget in self.graph_panel.winfo_children():
            widget.destroy()
    
    def convertir_fecha(self, fecha_obj):
        """Convierte diferentes formatos de fecha a objeto date"""
        if isinstance(fecha_obj, date):
            return fecha_obj
        elif isinstance(fecha_obj, str):
            try:
                return datetime.strptime(fecha_obj, '%Y-%m-%d').date()
            except:
                try:
                    return datetime.strptime(fecha_obj, '%d/%m/%Y').date()
                except:
                    return None
        return None
    
    def convertir_hora(self, hora_obj):
        """Convierte diferentes formatos de hora a objeto time"""
        if isinstance(hora_obj, time):
            return hora_obj
        elif isinstance(hora_obj, str):
            try:
                return datetime.strptime(hora_obj, '%H:%M:%S').time()
            except:
                try:
                    return datetime.strptime(hora_obj, '%H:%M').time()
                except:
                    return None
        return None
    
    def mostrar_utilizacion_mensual(self):
        """Muestra gráfico de utilización mensual de canchas"""
        try:
            self.limpiar_panel()
            
            año = int(self.spin_año.get())
            mes = int(self.spin_mes.get())
            
            # Obtener datos
            datos = ReportesService.reporte_utilizacion_mensual(año, mes)
            
            if not datos or datos.get('total_reservas', 0) == 0:
                tk.Label(
                    self.graph_panel,
                    text="No hay datos disponibles para el período seleccionado",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            # Crear gráfico
            self.current_fig = Graficos.crear_grafico_utilizacion_mensual(
                año, mes, datos, self.graph_panel
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_canchas_mas_utilizadas(self):
        """Muestra gráfico de canchas más utilizadas"""
        try:
            self.limpiar_panel()
            
            # Obtener datos
            datos_raw = ReportesService.reporte_canchas_mas_utilizadas()
            
            if not datos_raw:
                tk.Label(
                    self.graph_panel,
                    text="No hay datos disponibles",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            # Convertir datos al formato esperado
            datos = []
            for item in datos_raw:
                cancha = item.get('cancha')
                datos.append({
                    'nombre_cancha': cancha.nombre if cancha else 'Sin nombre',
                    'tipo_deporte': cancha.tipo_deporte if cancha else 'N/A',
                    'total_reservas': item.get('total_reservas', 0)
                })
            
            # Crear gráfico
            self.current_fig = Graficos.crear_grafico_canchas_mas_utilizadas(
                datos, self.graph_panel
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_facturacion_anual(self):
        """Muestra gráfico de facturación anual"""
        try:
            self.limpiar_panel()
            
            año = int(self.spin_año.get())
            
            # Obtener datos
            datos = ReportesService.reporte_facturacion_mensual(año)
            
            if not datos or datos.get('total_anual', 0) == 0:
                tk.Label(
                    self.graph_panel,
                    text=f"No hay datos de facturación para el año {año}",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            # Crear gráfico
            self.current_fig = Graficos.crear_grafico_facturacion_mensual(
                año, datos, self.graph_panel
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_estado_reservas(self):
        """Muestra gráfico de distribución de estados de reservas"""
        try:
            self.limpiar_panel()
            
            # Obtener datos
            datos_reporte = ReportesService.reporte_estado_reservas()
            
            if not datos_reporte or datos_reporte.get('total', 0) == 0:
                tk.Label(
                    self.graph_panel,
                    text="No hay reservas registradas",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            # Preparar datos para gráfico
            conteo = datos_reporte['conteo']
            datos = {
                'categorias': list(conteo.keys()),
                'valores': list(conteo.values())
            }
            
            # Crear gráfico
            self.current_fig = Graficos.crear_grafico_torta(
                datos,
                titulo='Distribución de Reservas por Estado',
                parent_frame=self.graph_panel,
                figsize=(8, 8)
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_distribucion_horaria(self):
        """Muestra distribución de reservas por horario"""
        try:
            self.limpiar_panel()
            
            from dao.reserva_dao import ReservaDAO
            
            # Obtener todas las reservas
            reservas = ReservaDAO.obtener_todas()
            
            if not reservas:
                tk.Label(
                    self.graph_panel,
                    text="No hay reservas registradas",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            # Contar por horario (día: antes de 18:00, noche: después)
            dia_count = 0
            noche_count = 0
            
            for r in reservas:
                if r.estado_reserva != 'cancelada':
                    # Convertir hora_inicio a time
                    hora = self.convertir_hora(r.hora_inicio)
                    
                    if hora:
                        if hora < time(18, 0):
                            dia_count += 1
                        else:
                            noche_count += 1
            
            if dia_count == 0 and noche_count == 0:
                tk.Label(
                    self.graph_panel,
                    text="No hay datos de horarios disponibles",
                    font=('Arial', 14),
                    bg='white',
                    fg='#7f8c8d'
                ).pack(expand=True)
                return
            
            datos = {
                'categorias': ['Día (08:00-18:00)', 'Noche (18:00-23:00)'],
                'valores': [dia_count, noche_count]
            }
            
            # Crear gráfico
            self.current_fig = Graficos.crear_grafico_distribucion_horaria(
                datos, self.graph_panel
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def guardar_grafico(self):
        """Guarda el gráfico actual como imagen"""
        try:
            if not hasattr(self, 'current_fig'):
                messagebox.showwarning("Advertencia", "No hay gráfico para guardar")
                return
            
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg"),
                    ("PDF", "*.pdf"),
                    ("Todos", "*.*")
                ]
            )
            
            if filename:
                Graficos.guardar_grafico(self.current_fig, filename)
                messagebox.showinfo("Éxito", f"Gráfico guardado en:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar gráfico: {e}")


if __name__ == "__main__":
    # Prueba standalone
    root = tk.Tk()
    root.withdraw()
    app = GraficosWindow(root)
    root.mainloop()
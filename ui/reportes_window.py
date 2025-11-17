"""
Ventana de Reportes y Estadísticas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from tkcalendar import DateEntry
from business.reportes_service import ReportesService
from utils.helpers import formatear_fecha, formatear_monto


class ReportesWindow:
    """Ventana de reportes y estadísticas"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Reportes y Estadísticas")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        self.crear_widgets()
        self.centrar_ventana()
        
        # Cargar reportes iniciales
        self.cargar_estado_reservas()
    
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
        # Frame superior
        frame_top = tk.Frame(self.window, bg='#f0f0f0')
        frame_top.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            frame_top,
            text="📊 Reportes y Estadísticas",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Pestaña 1: Estado de Reservas
        self.crear_tab_estado_reservas()
        
        # Pestaña 2: Canchas Más Utilizadas
        self.crear_tab_canchas_ranking()
        
        # Pestaña 3: Pagos Pendientes
        self.crear_tab_pagos_pendientes()
        
        # Pestaña 4: Reporte por Cliente
        self.crear_tab_reporte_cliente()
        
        # Pestaña 5: Ingresos por Período
        self.crear_tab_ingresos()
    
    def crear_tab_estado_reservas(self):
        """Pestaña de estado de reservas"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame, text='📈 Estado de Reservas')
        
        # Frame para gráfico
        info_frame = tk.LabelFrame(
            frame,
            text="Distribución de Reservas por Estado",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=20,
            pady=20
        )
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Text widget para mostrar resultados
        self.text_estado = tk.Text(
            info_frame,
            font=('Arial', 11),
            wrap=tk.WORD,
            height=15
        )
        self.text_estado.pack(fill=tk.BOTH, expand=True)
        
        # Botón actualizar
        tk.Button(
            frame,
            text="🔄 Actualizar",
            command=self.cargar_estado_reservas,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(pady=10)
    
    def crear_tab_canchas_ranking(self):
        """Pestaña de canchas más utilizadas"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame, text='🏆 Ranking de Canchas')
        
        # Tabla
        tabla_frame = tk.Frame(frame, bg='#f0f0f0')
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_ranking = ttk.Treeview(
            tabla_frame,
            columns=('Posición', 'Cancha', 'Deporte', 'Total Reservas', 'Total Horas', 'Ingresos'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree_ranking.yview)
        
        self.tree_ranking.heading('Posición', text='#')
        self.tree_ranking.heading('Cancha', text='Cancha')
        self.tree_ranking.heading('Deporte', text='Deporte')
        self.tree_ranking.heading('Total Reservas', text='Reservas')
        self.tree_ranking.heading('Total Horas', text='Horas')
        self.tree_ranking.heading('Ingresos', text='Ingresos')
        
        self.tree_ranking.column('Posición', width=50, anchor='center')
        self.tree_ranking.column('Cancha', width=200)
        self.tree_ranking.column('Deporte', width=120)
        self.tree_ranking.column('Total Reservas', width=100, anchor='center')
        self.tree_ranking.column('Total Horas', width=100, anchor='center')
        self.tree_ranking.column('Ingresos', width=120, anchor='e')
        
        self.tree_ranking.pack(fill=tk.BOTH, expand=True)
        
        # Botón actualizar
        tk.Button(
            frame,
            text="🔄 Actualizar Ranking",
            command=self.cargar_ranking_canchas,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Cargar datos iniciales
        self.cargar_ranking_canchas()
    
    def crear_tab_pagos_pendientes(self):
        """Pestaña de pagos pendientes"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame, text='💰 Pagos Pendientes')
        
        # Tabla
        tabla_frame = tk.Frame(frame, bg='#f0f0f0')
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_pagos = ttk.Treeview(
            tabla_frame,
            columns=('ID Reserva', 'Cliente', 'Fecha', 'Monto Total', 'Pagado', 'Pendiente'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree_pagos.yview)
        
        self.tree_pagos.heading('ID Reserva', text='ID')
        self.tree_pagos.heading('Cliente', text='Cliente')
        self.tree_pagos.heading('Fecha', text='Fecha Reserva')
        self.tree_pagos.heading('Monto Total', text='Total')
        self.tree_pagos.heading('Pagado', text='Pagado')
        self.tree_pagos.heading('Pendiente', text='Pendiente')
        
        self.tree_pagos.column('ID Reserva', width=50, anchor='center')
        self.tree_pagos.column('Cliente', width=200)
        self.tree_pagos.column('Fecha', width=120, anchor='center')
        self.tree_pagos.column('Monto Total', width=120, anchor='e')
        self.tree_pagos.column('Pagado', width=120, anchor='e')
        self.tree_pagos.column('Pendiente', width=120, anchor='e')
        
        self.tree_pagos.pack(fill=tk.BOTH, expand=True)
        
        # Tag para resaltar pendientes
        self.tree_pagos.tag_configure('pendiente', background='#fff3cd')
        
        # Botón actualizar
        tk.Button(
            frame,
            text="🔄 Actualizar Pagos Pendientes",
            command=self.cargar_pagos_pendientes,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Cargar datos iniciales
        self.cargar_pagos_pendientes()
    
    def crear_tab_reporte_cliente(self):
        """Pestaña de reporte por cliente"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame, text='👤 Por Cliente')
        
        # Frame superior para búsqueda
        search_frame = tk.Frame(frame, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            search_frame,
            text="Buscar Cliente:",
            font=('Arial', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_buscar_cliente = tk.Entry(search_frame, font=('Arial', 11), width=30)
        self.entry_buscar_cliente.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="🔍 Buscar",
            command=self.buscar_reporte_cliente,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.LEFT)
        
        # Text widget para resultados
        result_frame = tk.LabelFrame(
            frame,
            text="Resultados",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=20,
            pady=20
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.text_cliente = tk.Text(
            result_frame,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.text_cliente.pack(fill=tk.BOTH, expand=True)
    
    def crear_tab_ingresos(self):
        """Pestaña de ingresos por período"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame, text='💵 Ingresos')
        
        # Frame para selector de fechas
        fecha_frame = tk.Frame(frame, bg='#f0f0f0')
        fecha_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            fecha_frame,
            text="Desde:",
            font=('Arial', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.date_desde = DateEntry(
            fecha_frame,
            width=15,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            font=('Arial', 10),
            date_pattern='dd/mm/yyyy'
        )
        self.date_desde.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(
            fecha_frame,
            text="Hasta:",
            font=('Arial', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.date_hasta = DateEntry(
            fecha_frame,
            width=15,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            font=('Arial', 10),
            date_pattern='dd/mm/yyyy'
        )
        self.date_hasta.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Button(
            fecha_frame,
            text="📊 Generar Reporte",
            command=self.generar_reporte_ingresos,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.LEFT)
        
        # Text widget para resultados
        result_frame = tk.LabelFrame(
            frame,
            text="Reporte de Ingresos",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=20,
            pady=20
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.text_ingresos = tk.Text(
            result_frame,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.text_ingresos.pack(fill=tk.BOTH, expand=True)
    
    # ========== MÉTODOS PARA CARGAR DATOS ==========
    
    def cargar_estado_reservas(self):
        """Carga el reporte de estado de reservas"""
        self.text_estado.delete('1.0', tk.END)
        
        reporte = ReportesService.reporte_estado_reservas()
        
        if reporte:
            self.text_estado.insert(tk.END, "═" * 60 + "\n")
            self.text_estado.insert(tk.END, "  ESTADO DE RESERVAS\n")
            self.text_estado.insert(tk.END, "═" * 60 + "\n\n")
            
            total = sum(reporte['conteo'].values())
            
            for estado, cantidad in reporte['conteo'].items():
                porcentaje = (cantidad / total * 100) if total > 0 else 0
                
                self.text_estado.insert(tk.END, f"📍 {estado.upper()}\n")
                self.text_estado.insert(tk.END, f"   Cantidad: {cantidad}\n")
                self.text_estado.insert(tk.END, f"   Porcentaje: {porcentaje:.1f}%\n\n")
            
            self.text_estado.insert(tk.END, "─" * 60 + "\n")
            self.text_estado.insert(tk.END, f"TOTAL DE RESERVAS: {total}\n")
            self.text_estado.insert(tk.END, "─" * 60 + "\n")
    
    def cargar_ranking_canchas(self):
        """Carga el ranking de canchas más utilizadas"""
        # Limpiar tabla
        for item in self.tree_ranking.get_children():
            self.tree_ranking.delete(item)
        
        ranking = ReportesService.reporte_canchas_mas_utilizadas()
        
        for i, item in enumerate(ranking, 1):
            cancha = item['cancha']
            total_reservas = item.get('total_reservas', 0)
            total_horas = item.get('total_horas', 0)
            
            # Intentar obtener ingresos con múltiples nombres de clave
            ingresos = item.get('ingresos_generados', item.get('ingresos', 0))
            
            self.tree_ranking.insert('', tk.END, values=(
                f"#{i}",
                cancha.nombre,
                cancha.tipo_deporte,
                total_reservas,
                f"{total_horas:.1f}h",
                formatear_monto(ingresos)
            ))
    
    def cargar_pagos_pendientes(self):
        """Carga las reservas con pagos pendientes"""
        # Limpiar tabla
        for item in self.tree_pagos.get_children():
            self.tree_pagos.delete(item)
        
        pendientes = ReportesService.reporte_pagos_pendientes()
        
        for item in pendientes:
            reserva = item['reserva']
            
            # Obtener nombre del cliente
            from dao.cliente_dao import ClienteDAO
            cliente = ClienteDAO.obtener_por_id(reserva.id_cliente)
            nombre_cliente = cliente.get_nombre_completo() if cliente else "N/A"
            
            self.tree_pagos.insert('', tk.END, values=(
                reserva.id_reserva,
                nombre_cliente,
                formatear_fecha(reserva.fecha_reserva),
                formatear_monto(item['monto_total']),
                formatear_monto(item['total_pagado']),
                formatear_monto(item['saldo_pendiente'])
            ), tags=('pendiente',))

    def buscar_reporte_cliente(self):
        """Busca y genera reporte de un cliente"""
        self.text_cliente.delete('1.0', tk.END)
        
        termino = self.entry_buscar_cliente.get().strip()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        from business.cliente_service import ClienteService
        clientes = ClienteService.buscar_clientes(termino)
        
        if not clientes:
            self.text_cliente.insert(tk.END, "No se encontraron clientes.\n")
            return
        
        if len(clientes) > 1:
            self.text_cliente.insert(tk.END, f"Se encontraron {len(clientes)} clientes:\n\n")
            for cliente in clientes:
                self.text_cliente.insert(tk.END, f"• {cliente.get_nombre_completo()} (DNI: {cliente.dni})\n")
            self.text_cliente.insert(tk.END, "\nSeleccione un cliente más específico.\n")
            return
        
        # Generar reporte del cliente
        cliente = clientes[0]
        reporte = ReportesService.reporte_reservas_por_cliente(cliente.id_cliente)
        
        if reporte:
            stats = reporte['estadisticas']
            
            self.text_cliente.insert(tk.END, "═" * 60 + "\n")
            self.text_cliente.insert(tk.END, f"  REPORTE DE CLIENTE\n")
            self.text_cliente.insert(tk.END, "═" * 60 + "\n\n")
            
            self.text_cliente.insert(tk.END, f"👤 Cliente: {cliente.get_nombre_completo()}\n")
            self.text_cliente.insert(tk.END, f"📧 Email: {cliente.email}\n")
            self.text_cliente.insert(tk.END, f"📞 Teléfono: {cliente.telefono}\n\n")
            
            self.text_cliente.insert(tk.END, "─" * 60 + "\n")
            self.text_cliente.insert(tk.END, "ESTADÍSTICAS\n")
            self.text_cliente.insert(tk.END, "─" * 60 + "\n\n")
            
            self.text_cliente.insert(tk.END, f"Total de reservas: {stats['total_reservas']}\n")
            self.text_cliente.insert(tk.END, f"Confirmadas: {stats['confirmadas']}\n")
            self.text_cliente.insert(tk.END, f"Pendientes: {stats['pendientes']}\n")
            self.text_cliente.insert(tk.END, f"Canceladas: {stats['canceladas']}\n")
            self.text_cliente.insert(tk.END, f"Completadas: {stats['completadas']}\n\n")
            
            self.text_cliente.insert(tk.END, f"Monto total facturado: {formatear_monto(stats['monto_total'])}\n")
    
    def generar_reporte_ingresos(self):
        """Genera reporte de ingresos por período"""
        self.text_ingresos.delete('1.0', tk.END)
        
        fecha_desde = self.date_desde.get_date()
        fecha_hasta = self.date_hasta.get_date()
        
        if fecha_desde > fecha_hasta:
            messagebox.showerror("Error", "La fecha 'Desde' no puede ser posterior a 'Hasta'")
            return
        
        reporte = ReportesService.reporte_ingresos_periodo(fecha_desde, fecha_hasta)
        
        if reporte:
            self.text_ingresos.insert(tk.END, "═" * 60 + "\n")
            self.text_ingresos.insert(tk.END, "  REPORTE DE INGRESOS\n")
            self.text_ingresos.insert(tk.END, "═" * 60 + "\n\n")
            
            self.text_ingresos.insert(tk.END, f"📅 Período: {formatear_fecha(fecha_desde)} - {formatear_fecha(fecha_hasta)}\n\n")
            
            self.text_ingresos.insert(tk.END, "─" * 60 + "\n")
            self.text_ingresos.insert(tk.END, "RESUMEN\n")
            self.text_ingresos.insert(tk.END, "─" * 60 + "\n\n")
            
            self.text_ingresos.insert(tk.END, f"Total de reservas: {reporte['total_reservas']}\n")
            self.text_ingresos.insert(tk.END, f"Ingresos totales: {formatear_monto(reporte['ingresos_totales'])}\n")
            self.text_ingresos.insert(tk.END, f"Pagos recibidos: {formatear_monto(reporte['pagos_recibidos'])}\n")
            self.text_ingresos.insert(tk.END, f"Saldo pendiente: {formatear_monto(reporte['saldo_pendiente'])}\n\n")
            
            self.text_ingresos.insert(tk.END, f"Promedio por reserva: {formatear_monto(reporte['promedio_por_reserva'])}\n")
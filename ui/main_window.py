"""
Ventana Principal del Sistema
VERSIÓN OPTIMIZADA PARA NOTEBOOKS (COMPACTA)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO
from dao.reserva_dao import ReservaDAO


class MainWindow:
    """Ventana principal con dashboard y menú"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Reservas - Canchas Deportivas")
        
        # CONFIGURACIÓN PARA PANTALLA COMPLETA/MAXIMIZADA
        # Intentamos maximizar según el sistema operativo
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                # Si falla, usamos un tamaño seguro
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width-50}x{screen_height-100}+0+0")
        
        self.root.configure(bg='#f0f0f0')
        
        # Crear widgets
        self.crear_menu()
        self.crear_dashboard()

        # Comenzar actualización automática del dashboard
        self._actualizar_dashboard_periodicamente()
    
    def crear_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        
        # Menú Gestión
        menu_gestion = tk.Menu(menubar, tearoff=0)
        menu_gestion.add_command(label="👥 Clientes", command=self.abrir_clientes)
        menu_gestion.add_command(label="🏟️ Canchas", command=self.abrir_canchas)
        menu_gestion.add_command(label="📅 Reservas", command=self.abrir_reservas)
        menu_gestion.add_separator()
        menu_gestion.add_command(label="💰 Pagos", command=self.abrir_pagos)
        menubar.add_cascade(label="Gestión", menu=menu_gestion)
        
        # Menú Torneos
        menu_torneos = tk.Menu(menubar, tearoff=0)
        menu_torneos.add_command(label="🏆 Torneos", command=self.abrir_torneos)
        menu_torneos.add_command(label="⚽ Equipos", command=self.abrir_equipos)
        menubar.add_cascade(label="Torneos", menu=menu_torneos)
        
        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menu_reportes.add_command(label="📊 Reportes", command=self.abrir_reportes)
        menu_reportes.add_command(label="📈 Gráficos Estadísticos", command=self.abrir_graficos)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="ℹ️ Acerca de", command=self.mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        self.root.config(menu=menubar)
    
    def crear_dashboard(self):
        """Crea el dashboard con estadísticas (Versión Compacta)"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Título (Fuente reducida)
        titulo = tk.Label(
            main_frame,
            text="🏟️ Sistema de Reservas",
            font=('Arial', 18, 'bold'), # Reducido de 20
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 15)) # Padding reducido
        
        # Frame de estadísticas (expand=False para ahorrar espacio vertical)
        stats_frame = tk.Frame(main_frame, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, expand=False)
        
        # Obtener estadísticas
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        total_reservas = ReservaDAO.contar_total()
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))
        
        # Cards de estadísticas
        self.crear_stat_card(stats_frame, "👥 Clientes", total_clientes, "#3498db", 0, 0)
        self.crear_stat_card(stats_frame, "🏟️ Canchas", total_canchas, "#2ecc71", 0, 1)
        self.crear_stat_card(stats_frame, "📅 Reservas", total_reservas, "#e74c3c", 1, 0)
        self.crear_stat_card(stats_frame, "📆 Hoy", reservas_hoy, "#f39c12", 1, 1)
        
        # Frame de accesos rápidos
        accesos_frame = tk.LabelFrame(
            main_frame,
            text="Accesos Rápidos",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=10,
            pady=5
        )
        accesos_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Botones de acceso rápido - LISTA COMPLETA
        botones = [
            ("📅 Nueva Reserva", self.abrir_reservas, "#3498db"),
            ("👥 Nuevo Cliente", self.abrir_clientes, "#2ecc71"),
            ("🏟️ Gestionar Canchas", self.abrir_canchas, "#e74c3c"),
            ("💰 Gestionar Pagos", self.abrir_pagos, "#9b59b6"),
            ("🏆 Gestionar Torneos", self.abrir_torneos, "#e67e22"),
            ("📊 Ver Reportes", self.abrir_reportes, "#f39c12"),
            ("📈 Gráficos Estadísticos", self.abrir_graficos, "#1abc9c"),
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(
                accesos_frame,
                text=texto,
                command=comando,
                font=('Arial', 10, 'bold'), # Fuente reducida
                bg=color,
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                padx=10,
                pady=8, # Padding reducido drásticamente
                width=22
            )
            # Grid optimizado
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            # Efecto hover
            btn.bind('<Enter>', lambda e, b=btn: b.configure(relief=tk.RAISED))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(relief=tk.FLAT))
        
        # Configurar grid
        accesos_frame.grid_columnconfigure(0, weight=1)
        accesos_frame.grid_columnconfigure(1, weight=1)
    
    def crear_stat_card(self, parent, titulo, valor, color, row, col):
        """Crea una tarjeta de estadística (Versión Compacta)"""
        card = tk.Frame(
            parent,
            bg=color,
            relief=tk.RAISED,
            borderwidth=2
        )
        # Menos margen externo
        card.grid(row=row, column=col, padx=10, pady=5, sticky='nsew')
        
        # Configurar grid del parent
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Título (Fuente reducida)
        lbl_titulo = tk.Label(
            card,
            text=titulo,
            font=('Arial', 12, 'bold'), # Reducido de 14
            bg=color,
            fg='white'
        )
        lbl_titulo.pack(pady=(10, 2)) # Menos padding vertical
        
        # Valor (Fuente reducida)
        lbl_valor = tk.Label(
            card,
            text=str(valor),
            font=('Arial', 24, 'bold'), # Reducido de 32
            bg=color,
            fg='white'
        )
        lbl_valor.pack(pady=(2, 10)) # Menos padding vertical
        
        # Guardar referencia para actualizaciones
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[titulo] = lbl_valor

    def actualizar_dashboard(self):
        """Recalcula y actualiza los números de las tarjetas del dashboard."""
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        total_reservas = ReservaDAO.contar_total()
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))

        valores = {
            "👥 Clientes": total_clientes,
            "🏟️ Canchas": total_canchas,
            "📅 Reservas": total_reservas,
            "📆 Hoy": reservas_hoy,
        }

        if hasattr(self, "stat_labels"):
            for titulo, valor in valores.items():
                lbl = self.stat_labels.get(titulo)
                if lbl is not None:
                    lbl.config(text=str(valor))

    def _actualizar_dashboard_periodicamente(self):
        """Actualiza el dashboard cada 5 segundos."""
        self.actualizar_dashboard()
        self.root.after(5000, self._actualizar_dashboard_periodicamente)
    
    def abrir_clientes(self):
        """Abre la ventana de gestión de clientes"""
        from ui.cliente_window import ClienteWindow
        ClienteWindow(self.root)
    
    def abrir_canchas(self):
        """Abre la ventana de gestión de canchas"""
        from ui.cancha_window import CanchaWindow
        CanchaWindow(self.root)
    
    def abrir_reservas(self):
        """Abre la ventana de gestión de reservas"""
        from ui.reserva_window import ReservaWindow
        ReservaWindow(self.root)
    
    def abrir_pagos(self):
        """Abre la ventana de gestión de pagos"""
        from ui.pago_window import PagoWindow
        PagoWindow(self.root)
    
    def abrir_torneos(self):
        """Abre la ventana de gestión de torneos"""
        from ui.torneo_window import TorneoWindow
        TorneoWindow(self.root)
    
    def abrir_equipos(self):
        """Abre la ventana de gestión de equipos"""
        messagebox.showinfo("En desarrollo", "Módulo de equipos en desarrollo")
    
    def abrir_reportes(self):
        """Abre la ventana de reportes"""
        from ui.reportes_window import ReportesWindow
        ReportesWindow(self.root)
    
    def abrir_graficos(self):
        """Abre la ventana de gráficos estadísticos"""
        from ui.graficos_window import GraficosWindow
        GraficosWindow(self.root)
    
    def mostrar_acerca_de(self):
        """Muestra información sobre el sistema"""
        messagebox.showinfo(
            "Acerca de",
            "Sistema de Reservas de Canchas Deportivas\n\n"
            "Versión: 1.0\n"
            "Desarrollado para TP Laboratorio\n\n"
            "© 2024"
        )
    
    def run(self):
        """Inicia el loop principal"""
        self.root.mainloop()
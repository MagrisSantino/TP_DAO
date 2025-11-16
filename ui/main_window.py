"""
Ventana Principal del Sistema
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
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear widgets
        self.crear_menu()
        self.crear_dashboard()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
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
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="ℹ️ Acerca de", command=self.mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        self.root.config(menu=menubar)
    
    def crear_dashboard(self):
        """Crea el dashboard con estadísticas"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="🏟️ Sistema de Reservas de Canchas Deportivas",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 30))
        
        # Frame de estadísticas
        stats_frame = tk.Frame(main_frame, bg='#f0f0f0')
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
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
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=20,
            pady=20
        )
        accesos_frame.pack(fill=tk.BOTH, expand=True, pady=(30, 0))
        
        # Botones de acceso rápido
        botones = [
            ("📅 Nueva Reserva", self.abrir_reservas, "#3498db"),
            ("👥 Nuevo Cliente", self.abrir_clientes, "#2ecc71"),
            ("🏟️ Gestionar Canchas", self.abrir_canchas, "#e74c3c"),
            ("📊 Ver Reportes", self.abrir_reportes, "#f39c12")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(
                accesos_frame,
                text=texto,
                command=comando,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                padx=20,
                pady=15,
                width=20
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky='ew')
            
            # Efecto hover
            btn.bind('<Enter>', lambda e, b=btn: b.configure(relief=tk.RAISED))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(relief=tk.FLAT))
        
        # Configurar grid
        accesos_frame.grid_columnconfigure(0, weight=1)
        accesos_frame.grid_columnconfigure(1, weight=1)
    
    def crear_stat_card(self, parent, titulo, valor, color, row, col):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configurar grid
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Título
        lbl_titulo = tk.Label(
            card,
            text=titulo,
            font=('Arial', 14, 'bold'),
            bg=color,
            fg='white'
        )
        lbl_titulo.pack(pady=(20, 5))
        
        # Valor
        lbl_valor = tk.Label(
            card,
            text=str(valor),
            font=('Arial', 36, 'bold'),
            bg=color,
            fg='white'
        )
        lbl_valor.pack(pady=(5, 20))
    
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
"""
Ventana Principal del Sistema
VERSIÓN OPTIMIZADA: Tarjetas interactivas + Cierre Limpio (Fix Error Terminal)
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
        
        # Variable para controlar el loop de actualización
        self.after_id = None
        
        # CONFIGURACIÓN PARA PANTALLA COMPLETA/MAXIMIZADA
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width-50}x{screen_height-100}+0+0")
        
        self.root.configure(bg='#f0f0f0')
        
        # Configurar cierre limpio
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.crear_menu()
        self.crear_dashboard()
        self._actualizar_dashboard_periodicamente()
    
    def on_close(self):
        """Maneja el cierre de la aplicación cancelando procesos pendientes."""
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except:
                pass
        self.root.destroy()

    def crear_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        
        # Menú Gestión
        menu_gestion = tk.Menu(menubar, tearoff=0)
        menu_gestion.add_command(label="👥 Clientes", command=self.abrir_clientes)
        menu_gestion.add_command(label="⚽ Canchas", command=self.abrir_canchas)
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
        menu_reportes.add_command(label="📊 Ver Reportes", command=self.abrir_reportes)
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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="⚽ Sistema de Reservas",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 15))
        
        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, expand=False)
        
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        total_reservas = ReservaDAO.contar_total()
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))
        
        self.crear_stat_card(stats_frame, "👥 Clientes", total_clientes, "#3498db", 0, 0, command=self.abrir_clientes)
        self.crear_stat_card(stats_frame, "⚽ Canchas", total_canchas, "#2ecc71", 0, 1, command=self.abrir_canchas)
        self.crear_stat_card(stats_frame, "📅 Reservas", total_reservas, "#e74c3c", 1, 0, command=self.abrir_reservas)
        self.crear_stat_card(stats_frame, "📆 Reservas de hoy", reservas_hoy, "#f39c12", 1, 1, command=self.abrir_reservas_hoy)
        
        # Accesos Rápidos
        accesos_frame = tk.LabelFrame(main_frame, text="Accesos Rápidos", font=('Arial', 11, 'bold'), bg='#f0f0f0', fg='#2c3e50', padx=10, pady=5)
        accesos_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        botones = [
            ("📅 Reservas", self.abrir_reservas, "#3498db"),
            ("👥 Clientes", self.abrir_clientes, "#2ecc71"),
            ("⚽ Canchas", self.abrir_canchas, "#e74c3c"),
            ("💰 Pagos", self.abrir_pagos, "#9b59b6"),
            ("🏆 Torneos", self.abrir_torneos, "#e67e22"),
            ("📊 Reportes", self.abrir_reportes, "#f39c12"),
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(
                accesos_frame, text=texto, command=comando, font=('Arial', 10, 'bold'),
                bg=color, fg='white', relief=tk.FLAT, cursor='hand2', padx=10, pady=8, width=22
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            btn.bind('<Enter>', lambda e, b=btn: b.configure(relief=tk.RAISED))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(relief=tk.FLAT))
        
        accesos_frame.grid_columnconfigure(0, weight=1)
        accesos_frame.grid_columnconfigure(1, weight=1)
    
    def crear_stat_card(self, parent, titulo, valor, color, row, col, command=None):
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.grid(row=row, column=col, padx=10, pady=5, sticky='nsew')
        
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        lbl_titulo = tk.Label(card, text=titulo, font=('Arial', 12, 'bold'), bg=color, fg='white')
        lbl_titulo.pack(pady=(10, 2))
        
        lbl_valor = tk.Label(card, text=str(valor), font=('Arial', 24, 'bold'), bg=color, fg='white')
        lbl_valor.pack(pady=(2, 10))
        
        if command:
            card.config(cursor="hand2")
            lbl_titulo.config(cursor="hand2")
            lbl_valor.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: command())
            lbl_titulo.bind("<Button-1>", lambda e: command())
            lbl_valor.bind("<Button-1>", lambda e: command())
        
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[titulo] = lbl_valor

    def actualizar_dashboard(self):
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        total_reservas = ReservaDAO.contar_total()
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))

        valores = {
            "👥 Clientes": total_clientes,
            "⚽ Canchas": total_canchas,
            "📅 Reservas": total_reservas,
            "📆 Reservas de hoy": reservas_hoy,
        }

        if hasattr(self, "stat_labels"):
            for titulo, valor in valores.items():
                lbl = self.stat_labels.get(titulo)
                if lbl is not None:
                    lbl.config(text=str(valor))

    def _actualizar_dashboard_periodicamente(self):
        self.actualizar_dashboard()
        # Guardar el ID para poder cancelar
        self.after_id = self.root.after(5000, self._actualizar_dashboard_periodicamente)
    
    def abrir_clientes(self):
        from ui.cliente_window import ClienteWindow
        ClienteWindow(self.root)
    
    def abrir_canchas(self):
        from ui.cancha_window import CanchaWindow
        CanchaWindow(self.root)
    
    def abrir_reservas(self):
        from ui.reserva_window import ReservaWindow
        ReservaWindow(self.root)

    def abrir_reservas_hoy(self):
        from ui.reserva_window import ReservaWindow
        ventana = ReservaWindow(self.root)
        ventana.var_usar_fecha.set(True)
        ventana.date_desde.set_date(date.today())
        ventana.date_hasta.set_date(date.today())
        ventana.toggle_fechas()
        ventana.cargar_reservas()
    
    def abrir_pagos(self):
        from ui.pago_window import PagoWindow
        PagoWindow(self.root)
    
    def abrir_torneos(self):
        from ui.torneo_window import TorneoWindow
        TorneoWindow(self.root)
    
    def abrir_equipos(self):
        messagebox.showinfo("En desarrollo", "Módulo de equipos en desarrollo")
    
    def abrir_reportes(self):
        from ui.reportes_window import ReportesWindow
        ReportesWindow(self.root)
    
    def abrir_graficos(self):
        # Este método ya no se usa, se redirige o se borra
        self.abrir_reportes()
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Reservas\nVersión 2.0")
    
    def run(self):
        self.root.mainloop()
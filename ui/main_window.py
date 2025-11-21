"""
Ventana Principal del Sistema - Diseño Moderno
VERSIÓN OPTIMIZADA: Estilo Dark Theme con diseño moderno
ACTUALIZADO: Limpieza automática de reservas vencidas al inicio.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import date
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO
from dao.reserva_dao import ReservaDAO
from business.reserva_service import ReservaService  # Importar el servicio


class MainWindow:
    """Ventana principal con dashboard moderno"""
    
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    # Colores para las tarjetas de estadísticas
    CARD_COLORS = {
        'clientes': '#4a5f8f',
        'canchas': '#3d7068',
        'reservas': '#7a4d5a',
        'hoy': '#8f6b4a'
    }
    
    # Colores para los botones de acceso rápido
    BUTTON_COLORS = {
        'reservas': '#4a6fa5',
        'clientes': '#45796e',
        'canchas': '#5a6b7a',
        'pagos': '#7a5a7a',
        'torneos': '#8f6b4a',
        'reportes': '#8a5a4a'
    }
    
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
        
        self.root.configure(bg=self.BG_COLOR)
        
        # Configurar cierre limpio
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # --- EJECUTAR LIMPIEZA AUTOMÁTICA DE RESERVAS ---
        self.ejecutar_limpieza_reservas()
        
        self.crear_menu()
        self.crear_dashboard()
        self._actualizar_dashboard_periodicamente()
    
    def ejecutar_limpieza_reservas(self):
        """Cancela reservas pendientes que estén dentro de las 24hs"""
        try:
            canceladas = ReservaService.cancelar_pendientes_vencidas()
            if canceladas > 0:
                print(f"Sistema: Se han cancelado {canceladas} reservas pendientes por regla de 24hs.")
        except Exception as e:
            print(f"Error en limpieza automática: {e}")

    def on_close(self):
        """Maneja el cierre de la aplicación cancelando procesos pendientes."""
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except:
                pass
        self.root.destroy()

    def crear_menu(self):
        """Crea la barra de menú con estilo oscuro"""
        menubar = tk.Menu(self.root, bg=self.CARD_BG, fg=self.TEXT_COLOR, 
                         activebackground='#3a3a4e', activeforeground=self.TEXT_COLOR)
        
        # Menú Gestión
        menu_gestion = tk.Menu(menubar, tearoff=0, bg=self.CARD_BG, fg=self.TEXT_COLOR,
                               activebackground='#3a3a4e', activeforeground=self.TEXT_COLOR)
        menu_gestion.add_command(label="👥 Clientes", command=self.abrir_clientes)
        menu_gestion.add_command(label="⚽ Canchas", command=self.abrir_canchas)
        menu_gestion.add_command(label="📅 Reservas", command=self.abrir_reservas)
        menu_gestion.add_separator()
        menu_gestion.add_command(label="💰 Pagos", command=self.abrir_pagos)
        menubar.add_cascade(label="Gestión", menu=menu_gestion)
        
        # Menú Torneos
        menu_torneos = tk.Menu(menubar, tearoff=0, bg=self.CARD_BG, fg=self.TEXT_COLOR,
                               activebackground='#3a3a4e', activeforeground=self.TEXT_COLOR)
        menu_torneos.add_command(label="🏆 Torneos", command=self.abrir_torneos)
        menu_torneos.add_command(label="⚽ Equipos", command=self.abrir_equipos)
        menubar.add_cascade(label="Torneos", menu=menu_torneos)
        
        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0, bg=self.CARD_BG, fg=self.TEXT_COLOR,
                               activebackground='#3a3a4e', activeforeground=self.TEXT_COLOR)
        menu_reportes.add_command(label="📊 Ver Reportes", command=self.abrir_reportes)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0, bg=self.CARD_BG, fg=self.TEXT_COLOR,
                            activebackground='#3a3a4e', activeforeground=self.TEXT_COLOR)
        menu_ayuda.add_command(label="ℹ️ Acerca de", command=self.mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        self.root.config(menu=menubar)
    
    def crear_dashboard(self):
        """Crea el dashboard con diseño moderno"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Título
        titulo_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        titulo_frame.pack(pady=(0, 30))
        
        titulo = tk.Label(
            titulo_frame,
            text="📅 Sistema de Reservas",
            font=('Segoe UI', 24, 'bold'),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        )
        titulo.pack()
        
        # Frame para las tarjetas de estadísticas
        stats_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=(0, 40))
        
        # Configurar el grid para las 4 tarjetas
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Obtener datos
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        
        # CÁLCULO DE RESERVAS DEL MES ACTUAL
        hoy = date.today()
        ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
        fecha_inicio = date(hoy.year, hoy.month, 1)
        fecha_fin = date(hoy.year, hoy.month, ultimo_dia)
        reservas_mes = len(ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin))
        
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))
        
        # Crear tarjetas de estadísticas
        self.crear_stat_card_moderna(
            stats_frame, "👤", "Clientes", total_clientes, 
            self.CARD_COLORS['clientes'], 0, self.abrir_clientes
        )
        self.crear_stat_card_moderna(
            stats_frame, "⚽", "Canchas", total_canchas, 
            self.CARD_COLORS['canchas'], 1, self.abrir_canchas
        )
        self.crear_stat_card_moderna(
            stats_frame, "📅", "Reservas del Mes", reservas_mes, 
            self.CARD_COLORS['reservas'], 2, self.abrir_reservas_mes
        )
        self.crear_stat_card_moderna(
            stats_frame, "📆", "Reservas de hoy", reservas_hoy, 
            self.CARD_COLORS['hoy'], 3, self.abrir_reservas_hoy
        )
        
        # Accesos Rápidos
        accesos_titulo = tk.Label(
            main_frame,
            text="Accesos Rápidos",
            font=('Segoe UI', 18, 'bold'),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            anchor='w'
        )
        accesos_titulo.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para botones de acceso rápido
        accesos_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        accesos_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid 2x3
        for i in range(2):
            accesos_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            accesos_frame.grid_columnconfigure(i, weight=1)
        
        # Botones de acceso rápido
        botones = [
            ("📅", "Reservas", self.abrir_reservas, self.BUTTON_COLORS['reservas'], 0, 0),
            ("⚽", "Canchas", self.abrir_canchas, self.BUTTON_COLORS['canchas'], 0, 1),
            ("👥", "Clientes", self.abrir_clientes, self.BUTTON_COLORS['clientes'], 0, 2),
            ("💰", "Pagos", self.abrir_pagos, self.BUTTON_COLORS['pagos'], 1, 0),
            ("🏆", "Torneos", self.abrir_torneos, self.BUTTON_COLORS['torneos'], 1, 1),
            ("📊", "Reportes", self.abrir_reportes, self.BUTTON_COLORS['reportes'], 1, 2),
        ]
        
        for icono, texto, comando, color, row, col in botones:
            self.crear_boton_acceso_rapido(
                accesos_frame, icono, texto, comando, color, row, col
            )
    
    def crear_stat_card_moderna(self, parent, icono, titulo, valor, color, col, command=None):
        """Crea una tarjeta de estadística con diseño moderno"""
        card = tk.Frame(parent, bg=color, relief=tk.FLAT, borderwidth=0)
        card.grid(row=0, column=col, padx=12, pady=10, sticky='nsew')
        card.configure(height=210)
        card.grid_propagate(False)
        
        inner_frame = tk.Frame(card, bg=color)
        inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        lbl_icono = tk.Label(inner_frame, text=icono, font=('Segoe UI', 48), bg=color, fg=self.TEXT_COLOR)
        lbl_icono.pack(pady=(10, 5))
        
        lbl_titulo = tk.Label(inner_frame, text=titulo, font=('Segoe UI', 13), bg=color, fg=self.SUBTITLE_COLOR)
        lbl_titulo.pack(pady=(0, 5))
        
        lbl_valor = tk.Label(inner_frame, text=str(valor), font=('Segoe UI', 36, 'bold'), bg=color, fg=self.TEXT_COLOR)
        lbl_valor.pack(pady=(0, 10))
        
        if command:
            for widget in (card, inner_frame, lbl_icono, lbl_titulo, lbl_valor):
                widget.config(cursor="hand2")
                widget.bind("<Button-1>", lambda e: command())
                widget.bind("<Enter>", lambda e: self._on_enter_card(card, inner_frame, [lbl_icono, lbl_titulo, lbl_valor], color))
                widget.bind("<Leave>", lambda e: self._on_leave_card(card, inner_frame, [lbl_icono, lbl_titulo, lbl_valor], color))
        
        if not hasattr(self, 'stat_labels'): self.stat_labels = {}
        self.stat_labels[titulo] = lbl_valor
    
    def crear_boton_acceso_rapido(self, parent, icono, texto, comando, color, row, col):
        """Crea un botón de acceso rápido con diseño moderno tipo tarjeta"""
        card = tk.Frame(parent, bg=color, relief=tk.FLAT, borderwidth=0, cursor='hand2')
        card.grid(row=row, column=col, padx=12, pady=12, sticky='nsew')
        card.configure(height=70)
        card.grid_propagate(False)
        
        inner_frame = tk.Frame(card, bg=color, cursor='hand2')
        inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        lbl_icono = tk.Label(inner_frame, text=icono, font=('Segoe UI', 32), bg=color, fg=self.TEXT_COLOR, cursor='hand2')
        lbl_icono.pack(side=tk.LEFT, padx=(10, 15))
        
        lbl_texto = tk.Label(inner_frame, text=texto, font=('Segoe UI', 15, 'bold'), bg=color, fg=self.TEXT_COLOR, cursor='hand2')
        lbl_texto.pack(side=tk.LEFT, padx=(0, 10))
        
        for widget in (card, inner_frame, lbl_icono, lbl_texto):
            widget.bind("<Button-1>", lambda e: comando())
            widget.bind("<Enter>", lambda e: self._on_enter_card(card, inner_frame, [lbl_icono, lbl_texto], color))
            widget.bind("<Leave>", lambda e: self._on_leave_card(card, inner_frame, [lbl_icono, lbl_texto], color))
    
    def _on_enter_card(self, card, inner, labels, color):
        hover_color = self._lighten_color(color)
        card.configure(bg=hover_color)
        inner.configure(bg=hover_color)
        for lbl in labels: lbl.configure(bg=hover_color)

    def _on_leave_card(self, card, inner, labels, color):
        card.configure(bg=color)
        inner.configure(bg=color)
        for lbl in labels: lbl.configure(bg=color)

    def _lighten_color(self, color):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 20)
        g = min(255, g + 20)
        b = min(255, b + 20)
        return f'#{r:02x}{g:02x}{b:02x}'

    def actualizar_dashboard(self):
        """Actualiza los valores del dashboard"""
        total_clientes = ClienteDAO.contar_total()
        total_canchas = CanchaDAO.contar_total()
        
        hoy = date.today()
        ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
        fecha_inicio = date(hoy.year, hoy.month, 1)
        fecha_fin = date(hoy.year, hoy.month, ultimo_dia)
        reservas_mes = len(ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin))
        
        reservas_hoy = len(ReservaDAO.obtener_por_fecha(date.today()))

        valores = {
            "Clientes": total_clientes,
            "Canchas": total_canchas,
            "Reservas del Mes": reservas_mes,
            "Reservas de hoy": reservas_hoy,
        }

        if hasattr(self, "stat_labels"):
            for titulo, valor in valores.items():
                lbl = self.stat_labels.get(titulo)
                if lbl is not None:
                    lbl.config(text=str(valor))

    def _actualizar_dashboard_periodicamente(self):
        """Actualiza el dashboard cada 5 segundos"""
        self.actualizar_dashboard()
        self.after_id = self.root.after(5000, self._actualizar_dashboard_periodicamente)
    
    def abrir_reservas_mes(self):
        from ui.reserva_window import ReservaWindow
        ventana = ReservaWindow(self.root)
        ventana.cmb_estado.set("Todas")
        ventana.var_usar_fecha.set(True)
        ventana.toggle_fechas()
        
        hoy = date.today()
        ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
        fecha_inicio = date(hoy.year, hoy.month, 1)
        fecha_fin = date(hoy.year, hoy.month, ultimo_dia)
        
        ventana.date_desde.set_date(fecha_inicio)
        ventana.date_hasta.set_date(fecha_fin)
        ventana.cargar_reservas()

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
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Reservas\nVersión 2.0 - Diseño Moderno")
    
    def run(self):
        self.root.mainloop()
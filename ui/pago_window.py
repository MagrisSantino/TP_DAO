"""
Ventana de Gestión de Pagos - Estilo Moderno
CORREGIDO: Agregado método 'pago_online'.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from business.pago_service import PagoService
from business.reserva_service import ReservaService
from business.cliente_service import ClienteService
from dao.reserva_dao import ReservaDAO
from dao.torneo_dao import TorneoDAO 
from utils.helpers import formatear_monto, formatear_fecha


class PagoWindow:
    """Ventana de gestión de pagos (Historial)"""
    
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Pagos")
        self.window.geometry("1000x600")
        self.window.configure(bg=self.BG_COLOR)
        
        self.pago_seleccionado = None
        
        self.crear_widgets()
        
        # Inicializar filtros y cargar
        self.limpiar_filtros()
        
        self.centrar_ventana()
        
    def centrar_ventana(self):
        self.window.update_idletasks()
        ancho = self.window.winfo_width()
        alto = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.window.winfo_screenheight() // 2) - (alto // 2)
        self.window.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        # --- HEADER ---
        frame_top = tk.Frame(self.window, bg=self.BG_COLOR)
        frame_top.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(frame_top, text="💰 Historial de Pagos", font=('Segoe UI', 18, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side=tk.LEFT)
        
        # --- FILTROS ---
        frame_filtros = tk.LabelFrame(self.window, text="Filtros de Búsqueda", bg=self.BG_COLOR, fg=self.TEXT_COLOR, padx=10, pady=10, font=('Segoe UI', 10, 'bold'))
        frame_filtros.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.var_usar_fecha = tk.BooleanVar(value=False)
        chk_fecha = tk.Checkbutton(frame_filtros, text="Filtrar por fecha", variable=self.var_usar_fecha, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10), command=self.toggle_fechas)
        chk_fecha.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(frame_filtros, text="Desde:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.date_desde = DateEntry(frame_filtros, width=12, background='#4a6fa5', foreground='white', borderwidth=2, font=('Segoe UI', 9))
        self.date_desde.set_date(date.today())
        self.date_desde.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(frame_filtros, text="Hasta:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.date_hasta = DateEntry(frame_filtros, width=12, background='#4a6fa5', foreground='white', borderwidth=2, font=('Segoe UI', 9))
        self.date_hasta.set_date(date.today())
        self.date_hasta.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Button(frame_filtros, text="🔍 Aplicar Filtros", command=self.cargar_pagos, bg='#5a6b7a', fg='white', relief=tk.FLAT, padx=15, pady=5, font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)
        tk.Button(frame_filtros, text="🔄 Limpiar", command=self.limpiar_filtros, bg='#3a3a4e', relief=tk.FLAT, padx=15, pady=5, fg=self.TEXT_COLOR, font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)

        # --- TABLA ---
        frame_tabla = tk.Frame(self.window, bg=self.CARD_BG)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Estilo para Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                       background=self.CARD_BG,
                       foreground=self.TEXT_COLOR,
                       fieldbackground=self.CARD_BG,
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure("Treeview.Heading",
                       background='#3a3a4e',
                       foreground=self.TEXT_COLOR,
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        style.map('Treeview', background=[('selected', '#4a5f8f')])
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame_tabla, columns=('ID', 'Reserva', 'Cliente', 'Monto', 'Fecha', 'Método'), show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.heading('ID', text='ID Pago')
        self.tree.heading('Reserva', text='Ref. (R/T)')
        self.tree.heading('Cliente', text='Cliente / Org')
        self.tree.heading('Monto', text='Monto Pagado')
        self.tree.heading('Fecha', text='Fecha Pago')
        self.tree.heading('Método', text='Método')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Reserva', width=80, anchor='center')
        self.tree.column('Monto', width=100, anchor='e')
        self.tree.column('Fecha', width=100, anchor='center')
        
        self.toggle_fechas()

    def toggle_fechas(self):
        state = 'normal' if self.var_usar_fecha.get() else 'disabled'
        self.date_desde.configure(state=state)
        self.date_hasta.configure(state=state)

    def limpiar_filtros(self):
        self.var_usar_fecha.set(False)
        self.date_desde.set_date(date.today())
        self.date_hasta.set_date(date.today())
        self.toggle_fechas()
        self.cargar_pagos()

    def cargar_pagos(self):
        try:
            self.window.lift()
            self.window.focus_force()
        except:
            pass

        for item in self.tree.get_children():
            self.tree.delete(item)
            
        todos_pagos = PagoService.obtener_todos()
        
        usar_fechas = self.var_usar_fecha.get()
        try:
            f_desde = self.date_desde.get_date()
            f_hasta = self.date_hasta.get_date()
        except:
            f_desde = date.today()
            f_hasta = date.today()
            
        for p in todos_pagos:
            if usar_fechas:
                if not (f_desde <= p.fecha_pago <= f_hasta):
                    continue
            
            referencia = "N/A"
            cliente_nombre = "N/A"
            
            if p.id_reserva:
                referencia = f"Res #{p.id_reserva}"
                reserva = ReservaDAO.obtener_por_id(p.id_reserva)
                if reserva:
                    cliente = ClienteService.obtener_cliente(reserva.id_cliente)
                    if cliente: cliente_nombre = f"{cliente.nombre} {cliente.apellido}"
            elif p.id_torneo:
                referencia = f"Tor #{p.id_torneo}"
                torneo = TorneoDAO.obtener_por_id(p.id_torneo)
                if torneo and torneo.id_cliente:
                    cliente = ClienteService.obtener_cliente(torneo.id_cliente)
                    if cliente: cliente_nombre = f"{cliente.nombre} {cliente.apellido}"
            
            self.tree.insert('', tk.END, values=(
                p.id_pago, referencia, cliente_nombre, formatear_monto(p.monto), p.fecha_pago, p.metodo_pago
            ))


class NuevoPagoDialog:
    """
    Diálogo para registrar pago (Reserva o Torneo).
    """
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, id_reserva=None, callback=None, id_torneo=None):
        self.parent = parent
        self.id_reserva = id_reserva
        self.id_torneo = id_torneo
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        titulo = f"Pago Reserva #{id_reserva}" if id_reserva else f"Pago Torneo #{id_torneo}"
        self.dialog.title(titulo)
        self.dialog.geometry("500x500")
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.grab_set()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.reserva = ReservaDAO.obtener_por_id(self.id_reserva) if self.id_reserva else None
        self.torneo = TorneoDAO.obtener_por_id(self.id_torneo) if self.id_torneo else None
        
        self.crear_formulario()
        
        # Centrar
        self.dialog.update_idletasks()
        ancho = self.dialog.winfo_width()
        alto = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (alto // 2)
        self.dialog.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_formulario(self):
        main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="Confirmar y Pagar", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 20))
        
        # Información de la deuda
        info_frame = tk.LabelFrame(main, text="Detalle", bg=self.BG_COLOR, fg=self.TEXT_COLOR, padx=10, pady=10, font=('Segoe UI', 10, 'bold'))
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        pendiente = 0.0
        
        if self.reserva:
            cliente = ClienteService.obtener_cliente(self.reserva.id_cliente)
            nom = f"{cliente.nombre} {cliente.apellido}" if cliente else "-"
            tk.Label(info_frame, text=f"Cliente: {nom}", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            
            pagado = PagoService.obtener_monto_pagado(self.reserva.id_reserva)
            pendiente = self.reserva.monto_total - pagado
            tk.Label(info_frame, text=f"Total Reserva: {formatear_monto(self.reserva.monto_total)}", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            
        elif self.torneo:
            cliente = ClienteService.obtener_cliente(self.torneo.id_cliente)
            nom = f"{cliente.nombre} {cliente.apellido}" if cliente else "-"
            tk.Label(info_frame, text=f"Organizador: {nom}", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            tk.Label(info_frame, text=f"Torneo: {self.torneo.nombre}", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            
            pagado = PagoService.obtener_monto_pagado_torneo(self.torneo.id_torneo)
            pendiente = self.torneo.precio_total - pagado
            tk.Label(info_frame, text=f"Total Torneo: {formatear_monto(self.torneo.precio_total)}", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)

        tk.Label(info_frame, text=f"Pendiente: {formatear_monto(pendiente)}", bg=self.BG_COLOR, anchor='w', fg='#ff6b6b', font=('Segoe UI', 11, 'bold')).pack(fill=tk.X)
        self.monto_sugerido = pendiente

        # Campos
        tk.Label(main, text="Monto a Pagar:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.entry_monto = tk.Entry(main, font=('Segoe UI', 11), bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, relief=tk.FLAT, borderwidth=2)
        self.entry_monto.pack(fill=tk.X, pady=(0, 10), ipady=5)
        self.entry_monto.insert(0, str(self.monto_sugerido))
        
        tk.Label(main, text="Método de Pago:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_metodo = ttk.Combobox(main, values=['efectivo', 'tarjeta', 'transferencia', 'pago_online'], state='readonly', font=('Segoe UI', 10))
        self.cmb_metodo.pack(fill=tk.X, pady=(0, 10), ipady=3)
        self.cmb_metodo.set('efectivo')
        
        btn_frame = tk.Frame(main, bg=self.BG_COLOR, pady=20)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="✅ Pagar", command=self.registrar, bg='#45796e', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def registrar(self):
        try:
            monto = float(self.entry_monto.get())
            metodo = self.cmb_metodo.get()
            
            if monto <= 0:
                messagebox.showwarning("Advertencia", "El monto debe ser mayor a 0")
                return

            exito = False
            msg = ""
            
            if self.id_reserva:
                exito, msg, _ = PagoService.registrar_pago(self.id_reserva, monto, metodo)
            elif self.id_torneo:
                exito, msg, _ = PagoService.registrar_pago_torneo(self.id_torneo, monto, metodo)
                
            if exito:
                messagebox.showinfo("Éxito", msg)
                if self.callback: self.callback()
                self.cerrar_ventana()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
"""
Ventana de Gestión de Reservas - Estilo Moderno
Con Filtros Avanzados (Estado y Fechas)
ACTUALIZADO: Lógica de pago obligatorio para reservas dentro de las 24hs.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
from business.reserva_service import ReservaService
from business.cliente_service import ClienteService
from business.cancha_service import CanchaService
from dao.reserva_dao import ReservaDAO
from utils.helpers import formatear_fecha, formatear_hora, formatear_monto, parsear_hora

from ui.pago_window import NuevoPagoDialog

class ReservaWindow:
    """Ventana de gestión de reservas con filtros"""
    
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Reservas")
        self.window.geometry("1100x750") 
        self.window.configure(bg=self.BG_COLOR)
        
        # Variables
        self.reservas = []
        self.reserva_seleccionada = None
        
        # Crear interfaz
        self.crear_widgets()
        
        # Por defecto cargamos con los filtros iniciales (Pendiente)
        self.cargar_reservas()
        
        # Centrar ventana
        self.centrar_ventana()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.window.update_idletasks()
        ancho = self.window.winfo_width()
        alto = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.window.winfo_screenheight() // 2) - (alto // 2)
        self.window.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        """Crea todos los widgets de la ventana"""
        
        # --- HEADER Y BOTONES DE ACCIÓN ---
        frame_top = tk.Frame(self.window, bg=self.BG_COLOR)
        frame_top.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(
            frame_top,
            text="📅 Gestión de Reservas",
            font=('Segoe UI', 18, 'bold'),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(side=tk.LEFT)
        
        # Botones de acción (Derecha)
        btn_nueva = tk.Button(frame_top, text="➕ Nueva Reserva", command=self.nueva_reserva, bg='#4a6fa5', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
        btn_nueva.pack(side=tk.RIGHT, padx=5)
        
        btn_confirmar = tk.Button(frame_top, text="💲 Pagar y Confirmar", command=self.confirmar_reserva, bg='#45796e', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
        btn_confirmar.pack(side=tk.RIGHT, padx=5)
        
        btn_cancelar = tk.Button(frame_top, text="✗ Cancelar", command=self.cancelar_reserva, bg='#a04a4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
        btn_cancelar.pack(side=tk.RIGHT, padx=5)
        
        # --- PANEL DE FILTROS ---
        frame_filtros = tk.LabelFrame(self.window, text="Filtros de Búsqueda", bg=self.BG_COLOR, fg=self.TEXT_COLOR, padx=10, pady=10, font=('Segoe UI', 10, 'bold'))
        frame_filtros.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Filtro Estado
        tk.Label(frame_filtros, text="Estado:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.cmb_estado = ttk.Combobox(frame_filtros, values=["Todas", "Pendiente", "Confirmada", "Completada", "Cancelada"], state='readonly', width=15, font=('Segoe UI', 10))
        self.cmb_estado.set("Pendiente")
        self.cmb_estado.pack(side=tk.LEFT, padx=(0, 20))
        
        # Filtro Fechas
        self.var_usar_fecha = tk.BooleanVar(value=False)
        chk_fecha = tk.Checkbutton(frame_filtros, text="Filtrar por rango de fechas", variable=self.var_usar_fecha, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10), command=self.toggle_fechas)
        chk_fecha.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(frame_filtros, text="Desde:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.date_desde = DateEntry(frame_filtros, width=12, background='#4a6fa5', foreground='white', borderwidth=2, font=('Segoe UI', 9))
        self.date_desde.set_date(date.today())
        self.date_desde.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(frame_filtros, text="Hasta:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.date_hasta = DateEntry(frame_filtros, width=12, background='#4a6fa5', foreground='white', borderwidth=2, font=('Segoe UI', 9))
        self.date_hasta.set_date(date.today())
        self.date_hasta.pack(side=tk.LEFT, padx=(0, 20))
        
        self.toggle_fechas()

        # Botones de Filtro
        tk.Button(frame_filtros, text="🔍 Aplicar Filtros", command=self.cargar_reservas, bg='#5a6b7a', fg='white', relief=tk.FLAT, padx=15, pady=5, font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)
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
        
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=('ID', 'Cliente', 'Cancha', 'Fecha', 'Horario', 'Monto', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Cancha', text='Cancha')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Horario', text='Horario')
        self.tree.heading('Monto', text='Monto')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Cliente', width=200)
        self.tree.column('Cancha', width=150)
        self.tree.column('Fecha', width=100, anchor='center')
        self.tree.column('Horario', width=120, anchor='center')
        self.tree.column('Monto', width=100, anchor='e')
        self.tree.column('Estado', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Configurar colores de fila según estado
        self.tree.tag_configure('pendiente', background='#8f6b4a')
        self.tree.tag_configure('confirmada', background='#4a6fa5')
        self.tree.tag_configure('completada', background='#45796e')
        self.tree.tag_configure('cancelada', background='#a04a4a')
        
    def toggle_fechas(self):
        """Habilita o deshabilita los selectores de fecha"""
        state = 'normal' if self.var_usar_fecha.get() else 'disabled'
        self.date_desde.configure(state=state)
        self.date_hasta.configure(state=state)

    def limpiar_filtros(self):
        """Resetea los filtros a su estado original"""
        self.cmb_estado.set("Pendiente")
        self.var_usar_fecha.set(False)
        self.date_desde.set_date(date.today())
        self.date_hasta.set_date(date.today())
        self.toggle_fechas()
        self.cargar_reservas()
    
    def cargar_reservas(self):
        """Carga las reservas aplicando los filtros seleccionados"""
        try:
            self.window.lift()
            self.window.focus_force()
        except:
            pass

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener TODAS las reservas
        todas_reservas = ReservaDAO.obtener_todas()
        
        # Obtener valores de filtros
        filtro_estado = self.cmb_estado.get().lower()
        usar_fechas = self.var_usar_fecha.get()
        
        # Obtención segura de fechas
        try:
            fecha_desde = self.date_desde.get_date()
            fecha_hasta = self.date_hasta.get_date()
        except:
            fecha_desde = date.today()
            fecha_hasta = date.today()

        for reserva in todas_reservas:
            # 1. Filtro de Estado
            if filtro_estado != "todas" and reserva.estado_reserva != filtro_estado:
                continue
            
            # 2. Filtro de Fechas
            if usar_fechas:
                if not (fecha_desde <= reserva.fecha_reserva <= fecha_hasta):
                    continue
            
            # Si pasa los filtros, procesar datos para mostrar
            cliente = ClienteService.obtener_cliente(reserva.id_cliente)
            cancha = CanchaService.obtener_cancha(reserva.id_cancha)
            
            nombre_cliente = cliente.get_nombre_completo() if cliente else "N/A"
            nombre_cancha = cancha.nombre if cancha else "N/A"
            
            horario_str = f"{formatear_hora(reserva.hora_inicio)} - {formatear_hora(reserva.hora_fin)}"
            
            tag = reserva.estado_reserva
            self.tree.insert('', tk.END, values=(
                reserva.id_reserva,
                nombre_cliente,
                nombre_cancha,
                formatear_fecha(reserva.fecha_reserva),
                horario_str,
                formatear_monto(reserva.monto_total),
                reserva.estado_reserva.capitalize()
            ), tags=(tag,))
    
    def on_select(self, event):
        """Maneja la selección de una fila"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_reserva = item['values'][0]
            self.reserva_seleccionada = id_reserva
    
    def nueva_reserva(self):
        """Abre el diálogo para crear una nueva reserva"""
        NuevaReservaDialog(self.window, self.cargar_reservas)
    
    def confirmar_reserva(self):
        """Abre la ventana de pago para confirmar la reserva."""
        if not self.reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una reserva para confirmar")
            return
        
        reserva = ReservaDAO.obtener_por_id(self.reserva_seleccionada)
        if reserva.estado_reserva in ['confirmada', 'completada']:
             messagebox.showinfo("Info", "Esta reserva ya está confirmada.")
             return
        if reserva.estado_reserva == 'cancelada':
             messagebox.showerror("Error", "No se puede confirmar una reserva cancelada.")
             return

        # Abrir diálogo de pago
        NuevoPagoDialog(self.window, self.reserva_seleccionada, self.cargar_reservas)
    
    def cancelar_reserva(self):
        """Cancela la reserva seleccionada"""
        if not self.reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una reserva")
            return
        
        respuesta = messagebox.askyesno("Confirmar", "¿Desea cancelar esta reserva?")
        
        if respuesta:
            exito, mensaje = ReservaService.cancelar_reserva(self.reserva_seleccionada)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_reservas()
            else:
                messagebox.showerror("Error", mensaje)


class NuevaReservaDialog:
    """Diálogo para crear una nueva reserva"""
    
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Reserva")
        self.dialog.geometry("600x750")
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.grab_set()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_formulario()
        self.centrar_dialogo()
    
    def centrar_dialogo(self):
        """Centra el diálogo"""
        self.dialog.update_idletasks()
        ancho = self.dialog.winfo_width()
        alto = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (alto // 2)
        self.dialog.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_formulario(self):
        """Crea el formulario de nueva reserva"""
        main_frame = tk.Frame(self.dialog, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(main_frame, text="Nueva Reserva", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Cliente:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.cmb_cliente = ttk.Combobox(main_frame, state='readonly', font=('Segoe UI', 10))
        self.cmb_cliente.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        clientes = ClienteService.obtener_clientes_activos()
        self.cmb_cliente['values'] = [f"{c.id_cliente} - {c.get_nombre_completo()}" for c in clientes]
        
        tk.Label(main_frame, text="Cancha:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.cmb_cancha = ttk.Combobox(main_frame, state='readonly', font=('Segoe UI', 10))
        self.cmb_cancha.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        canchas = CanchaService.obtener_canchas_disponibles()
        self.cmb_cancha['values'] = [f"{c.id_cancha} - {c.nombre}" for c in canchas]
        
        tk.Label(main_frame, text="Fecha:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.date_entry = DateEntry(main_frame, width=20, background='#4a6fa5', foreground='white', borderwidth=2, mindate=date.today(), font=('Segoe UI', 10))
        self.date_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(main_frame, text="Hora Inicio (HH:MM):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.entry_hora_inicio = tk.Entry(main_frame, font=('Segoe UI', 10), bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, relief=tk.FLAT, borderwidth=2)
        self.entry_hora_inicio.insert(0, "10:00")
        self.entry_hora_inicio.pack(fill=tk.X, pady=(0, 15), ipady=5)
        
        tk.Label(main_frame, text="Hora Fin (HH:MM):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.entry_hora_fin = tk.Entry(main_frame, font=('Segoe UI', 10), bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, relief=tk.FLAT, borderwidth=2)
        self.entry_hora_fin.insert(0, "12:00")
        self.entry_hora_fin.pack(fill=tk.X, pady=(0, 15), ipady=5)
        
        self.var_iluminacion = tk.BooleanVar()
        chk_iluminacion = tk.Checkbutton(main_frame, text="Usar iluminación", variable=self.var_iluminacion, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10))
        chk_iluminacion.pack(anchor='w', pady=(0, 15))
        
        tk.Label(main_frame, text="Observaciones:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        self.text_obs = tk.Text(main_frame, height=4, font=('Segoe UI', 10), bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, relief=tk.FLAT, borderwidth=2)
        self.text_obs.pack(fill=tk.X, pady=(0, 20))
        
        frame_botones = tk.Frame(main_frame, bg=self.BG_COLOR)
        frame_botones.pack(fill=tk.X)
        
        tk.Button(frame_botones, text="Crear Reserva", command=self.crear_reserva, bg='#45796e', fg='white', font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2', padx=30, pady=10).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        tk.Button(frame_botones, text="Cerrar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2', padx=30, pady=10).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
    
    def limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.cmb_cliente.set('')
        self.cmb_cancha.set('')
        self.date_entry.set_date(date.today())
        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_inicio.insert(0, "10:00")
        self.entry_hora_fin.delete(0, tk.END)
        self.entry_hora_fin.insert(0, "12:00")
        self.var_iluminacion.set(False)
        self.text_obs.delete("1.0", tk.END)
        self.cmb_cliente.focus()

    def cerrar_ventana(self):
        """Cierra el diálogo y trae la ventana padre al frente"""
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def crear_reserva(self):
        """Crea la reserva con los datos ingresados, manejando pagos obligatorios si aplica."""
        try:
            cliente_sel = self.cmb_cliente.get()
            cancha_sel = self.cmb_cancha.get()
            
            if not cliente_sel or not cancha_sel:
                messagebox.showwarning("Advertencia", "Complete todos los campos")
                return
            
            id_cliente = int(cliente_sel.split(' - ')[0])
            id_cancha = int(cancha_sel.split(' - ')[0])
            fecha_reserva = self.date_entry.get_date()
            
            hora_inicio = parsear_hora(self.entry_hora_inicio.get())
            hora_fin = parsear_hora(self.entry_hora_fin.get())
            
            if not hora_inicio or not hora_fin:
                messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
                return
            
            usa_iluminacion = self.var_iluminacion.get()
            observaciones = self.text_obs.get("1.0", tk.END).strip()
            
            # 1. Verificar si es reserva urgente (< 24hs)
            es_urgente = ReservaService.es_reserva_urgente(fecha_reserva, hora_inicio)
            
            if es_urgente:
                respuesta = messagebox.askyesno(
                    "Reserva Inminente",
                    "Esta reserva comienza en menos de 24 horas.\n\n"
                    "⚠️ REGLA DEL SISTEMA: Debe ser pagada en el momento para confirmarse.\n"
                    "Si no se paga ahora, será cancelada.\n\n"
                    "¿Desea continuar al pago?"
                )
                if not respuesta:
                    return

            # 2. Crear reserva (Estado: Pendiente)
            exito, mensaje, reserva = ReservaService.crear_reserva(
                id_cliente=id_cliente, id_cancha=id_cancha, fecha_reserva=fecha_reserva,
                hora_inicio=hora_inicio, hora_fin=hora_fin, usa_iluminacion=usa_iluminacion,
                observaciones=observaciones
            )
            
            if exito:
                if es_urgente:
                    # 3. Flujo de pago obligatorio
                    # Abrir diálogo de pago y esperar
                    dialogo_pago = NuevoPagoDialog(
                        self.dialog, 
                        id_reserva=reserva.id_reserva,
                        callback=self.callback # Refrescar tabla si paga
                    )
                    self.dialog.wait_window(dialogo_pago.dialog)
                    
                    # 4. Verificar si se pagó (reserva confirmada)
                    # Consultar de nuevo la reserva para ver su estado o pagos
                    reserva_actualizada = ReservaDAO.obtener_por_id(reserva.id_reserva)
                    
                    if reserva_actualizada.estado_reserva != 'confirmada':
                        # ROLLBACK: Si cerró la ventana o no pagó todo, borramos la reserva
                        ReservaService.eliminar_fisicamente(reserva.id_reserva)
                        messagebox.showinfo("Cancelado", "La reserva se canceló por falta de pago inmediato.")
                        # No limpiamos formulario para que pueda intentar de nuevo
                    else:
                        # Éxito total
                        self.limpiar_formulario()
                        self.cerrar_ventana()
                else:
                    # Flujo normal (> 24hs)
                    messagebox.showinfo("Éxito", f"{mensaje}\n\nMonto total: {formatear_monto(reserva.monto_total)}\n\nPuede cargar otra reserva o cerrar la ventana.")
                    self.callback()
                    self.limpiar_formulario()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")
"""
Ventana de Gestión de Pagos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from business.pago_service import PagoService
from business.reserva_service import ReservaService
from dao.reserva_dao import ReservaDAO
from dao.cliente_dao import ClienteDAO
from utils.helpers import formatear_fecha, formatear_monto


class PagoWindow:
    """Ventana de gestión de pagos"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Pagos")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        self.pagos = []
        self.reserva_seleccionada = None
        
        self.crear_widgets()
        self.cargar_reservas_pendientes()
        self.centrar_ventana()
    
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
            text="💰 Gestión de Pagos",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            frame_top,
            text="💳 Registrar Pago",
            command=self.registrar_pago,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            frame_top,
            text="🔄 Actualizar",
            command=self.cargar_reservas_pendientes,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        # Tabla de reservas con saldo pendiente
        frame_tabla = tk.Frame(self.window, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            frame_tabla,
            text="Reservas con Saldo Pendiente",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=('ID', 'Cliente', 'Fecha', 'Cancha', 'Total', 'Pagado', 'Pendiente', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Cancha', text='Cancha')
        self.tree.heading('Total', text='Total')
        self.tree.heading('Pagado', text='Pagado')
        self.tree.heading('Pendiente', text='Pendiente')
        self.tree.heading('Estado', text='Estado Pago')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Cliente', width=150)
        self.tree.column('Fecha', width=100, anchor='center')
        self.tree.column('Cancha', width=150)
        self.tree.column('Total', width=100, anchor='e')
        self.tree.column('Pagado', width=100, anchor='e')
        self.tree.column('Pendiente', width=100, anchor='e')
        self.tree.column('Estado', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Tags
        self.tree.tag_configure('pendiente', background='#fff3cd')
        self.tree.tag_configure('pagado', background='#d4edda')
    
    def cargar_reservas_pendientes(self):
        """Carga reservas con saldo pendiente"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todas las reservas confirmadas o completadas
        from dao.reserva_dao import ReservaDAO
        reservas = ReservaDAO.obtener_por_estado('confirmada') + ReservaDAO.obtener_por_estado('completada')
        
        for reserva in reservas:
            # Verificar estado del pago
            esta_pagada, total, pagado = PagoService.verificar_pago_completo(reserva.id_reserva)
            pendiente = total - pagado
            
            # Obtener datos relacionados
            cliente = ClienteDAO.obtener_por_id(reserva.id_cliente)
            from dao.cancha_dao import CanchaDAO
            cancha = CanchaDAO.obtener_por_id(reserva.id_cancha)
            
            nombre_cliente = cliente.get_nombre_completo() if cliente else "N/A"
            nombre_cancha = cancha.nombre if cancha else "N/A"
            
            estado_pago = "Pagado" if esta_pagada else "Pendiente"
            tag = 'pagado' if esta_pagada else 'pendiente'
            
            self.tree.insert('', tk.END, values=(
                reserva.id_reserva,
                nombre_cliente,
                formatear_fecha(reserva.fecha_reserva),
                nombre_cancha,
                formatear_monto(total),
                formatear_monto(pagado),
                formatear_monto(pendiente),
                estado_pago
            ), tags=(tag,))
    
    def on_select(self, event):
        """Maneja la selección de una fila"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.reserva_seleccionada = item['values'][0]
    
    def registrar_pago(self):
        """Abre diálogo para registrar un pago"""
        if not self.reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una reserva")
            return
        
        RegistrarPagoDialog(self.window, self.reserva_seleccionada, self.cargar_reservas_pendientes)


class RegistrarPagoDialog:
    """Diálogo para registrar un pago"""
    
    def __init__(self, parent, id_reserva, callback):
        self.id_reserva = id_reserva
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Registrar Pago")
        self.dialog.geometry("450x400")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.grab_set()
        
        # Obtener info de la reserva
        self.reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not self.reserva:
            messagebox.showerror("Error", "Reserva no encontrada")
            self.dialog.destroy()
            return
        
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
        """Crea el formulario"""
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(
            main_frame,
            text="Registrar Pago",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # Info de la reserva
        info_frame = tk.LabelFrame(
            main_frame,
            text="Información de la Reserva",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            padx=15,
            pady=15
        )
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Calcular saldo
        esta_pagada, total, pagado = PagoService.verificar_pago_completo(self.id_reserva)
        pendiente = total - pagado
        
        tk.Label(
            info_frame,
            text=f"Reserva ID: {self.id_reserva}",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Monto Total: {formatear_monto(total)}",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Ya Pagado: {formatear_monto(pagado)}",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Saldo Pendiente: {formatear_monto(pendiente)}",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#e74c3c'
        ).pack(anchor='w')
        
        # Monto a pagar
        tk.Label(main_frame, text="Monto a Pagar: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_monto = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_monto.insert(0, str(pendiente))
        self.entry_monto.pack(fill=tk.X, pady=(0, 15))
        
        # Método de pago
        tk.Label(main_frame, text="Método de Pago: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.cmb_metodo = ttk.Combobox(main_frame, font=('Arial', 10), state='readonly')
        self.cmb_metodo['values'] = (
            'efectivo',
            'tarjeta_debito',
            'tarjeta_credito',
            'transferencia',
            'pago_online'
        )
        self.cmb_metodo.current(0)
        self.cmb_metodo.pack(fill=tk.X, pady=(0, 15))

        
        # Comprobante
        tk.Label(main_frame, text="N° Comprobante (opcional):", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_comprobante = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_comprobante.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        frame_botones = tk.Frame(main_frame, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X)
        
        tk.Button(
            frame_botones,
            text="💳 Registrar Pago",
            command=self.registrar,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=self.dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
    

    def registrar(self):
        """Registra el pago"""
        try:
            monto = float(self.entry_monto.get())
            metodo = self.cmb_metodo.get()
            comprobante = self.entry_comprobante.get().strip()

            # Si el método es pago online, aclaramos que se procesa en app externa
            if metodo == 'pago_online':
                messagebox.showinfo(
                    "Pago en línea",
                    "Este pago se registra como 'Pago Online' procesado desde una "
                    "aplicación o portal externo."
                )

            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return

            # Registrar pago
            exito, mensaje, pago = PagoService.registrar_pago(
                id_reserva=self.id_reserva,
                monto=monto,
                metodo_pago=metodo,
                comprobante=comprobante
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")

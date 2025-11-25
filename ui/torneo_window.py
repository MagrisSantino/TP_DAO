"""
Ventana de Gestión de Torneos - Estilo Moderno
CORREGIDO: Rollback automático si no se completa el pago al crear.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from business.torneo_service import TorneoService
from business.cliente_service import ClienteService
from business.pago_service import PagoService  # Necesario para verificar el pago
from dao.torneo_dao import TorneoDAO
from utils.helpers import formatear_monto, parsear_hora, formatear_hora
from ui.pago_window import NuevoPagoDialog

class TorneoWindow:
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Torneos")
        self.window.geometry("1100x600")
        self.window.configure(bg=self.BG_COLOR)
        self.torneo_seleccionado = None
        self.crear_widgets()
        self.cargar_torneos()
        self.window.lift()
        self.window.focus_force()
    
    def crear_widgets(self):
        frame_top = tk.Frame(self.window, bg=self.BG_COLOR)
        frame_top.pack(fill=tk.X, padx=20, pady=15)
        tk.Label(frame_top, text="🏆 Torneos (Reservas Masivas)", font=('Segoe UI', 18, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side=tk.LEFT)
        
        btn_nuevo = tk.Button(frame_top, text="➕ Nuevo Torneo", command=self.nuevo_torneo, bg='#4a6fa5', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        btn_nuevo.pack(side=tk.RIGHT, padx=5)
        btn_eliminar = tk.Button(frame_top, text="🗑 Cancelar Torneo", command=self.eliminar_torneo, bg='#a04a4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        btn_eliminar.pack(side=tk.RIGHT, padx=5)
        
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
        
        self.tree = ttk.Treeview(frame_tabla, columns=('ID', 'Nombre', 'Org', 'Deporte', 'Fecha', 'Horario', 'Canchas', 'Precio'), show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Org', text='Organizador')
        self.tree.heading('Deporte', text='Deporte')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Horario', text='Horario')
        self.tree.heading('Canchas', text='Canchas')
        self.tree.heading('Precio', text='Precio')
        self.tree.column('ID', width=40, anchor='center')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def cargar_torneos(self):
        try:
            self.window.lift()
            self.window.focus_force()
        except: pass
        
        for item in self.tree.get_children(): self.tree.delete(item)
        torneos = TorneoService.obtener_todos()
        for t in torneos:
            cliente = ClienteService.obtener_cliente(t.id_cliente) if t.id_cliente else None
            nombre_org = f"{cliente.nombre} {cliente.apellido}" if cliente else "Desconocido"
            horario = f"{formatear_hora(t.hora_inicio)} - {formatear_hora(t.hora_fin)}"
            self.tree.insert('', tk.END, values=(
                t.id_torneo, t.nombre, nombre_org, t.deporte, t.fecha, horario, 
                t.cantidad_canchas, formatear_monto(t.precio_total)
            ))

    def on_select(self, event):
        sel = self.tree.selection()
        if sel: self.torneo_seleccionado = self.tree.item(sel[0])['values'][0]

    def nuevo_torneo(self):
        NuevoTorneoDialog(self.window, self.cargar_torneos)

    def eliminar_torneo(self):
        if not self.torneo_seleccionado:
            messagebox.showwarning("Alerta", "Seleccione un torneo")
            self.window.lift()
            return
        if messagebox.askyesno("Confirmar", "¿Cancelar torneo y liberar canchas?"):
            exito, msg = TorneoService.eliminar_torneo(self.torneo_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_torneos()
            else:
                messagebox.showerror("Error", msg)
                self.window.lift()

class NuevoTorneoDialog:
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Torneo")
        self.dialog.geometry("500x650")
        self.dialog.configure(bg=self.BG_COLOR)
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_formulario()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')

    def crear_formulario(self):
        main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        tk.Label(main, text="Organizar Torneo", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 15))
        
        # 1. Fecha
        tk.Label(main, text="Fecha (Día único):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.date_fecha = DateEntry(main, width=20, background='#4a6fa5', foreground='white', borderwidth=2, font=('Segoe UI', 10))
        self.date_fecha.pack(fill=tk.X, pady=(0, 10))

        # 2. Organizador
        tk.Label(main, text="Organizador (Cliente):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_cliente = ttk.Combobox(main, state='readonly', font=('Segoe UI', 10))
        self.cmb_cliente.pack(fill=tk.X, pady=(0, 10), ipady=3)
        clientes = ClienteService.obtener_clientes_activos()
        self.cmb_cliente['values'] = [f"{c.id_cliente} - {c.nombre} {c.apellido}" for c in clientes]
        
        # 3. Nombre
        tk.Label(main, text="Nombre del Torneo:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.entry_nombre = tk.Entry(main, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.entry_nombre.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        # 4. Deporte
        tk.Label(main, text="Deporte:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_deporte = ttk.Combobox(main, values=['Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Tenis', 'Padel', 'Basket'], state='readonly', font=('Segoe UI', 10))
        self.cmb_deporte.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # 5. Horarios
        frame_hora = tk.Frame(main, bg=self.BG_COLOR)
        frame_hora.pack(fill=tk.X, pady=(0, 10))
        tk.Label(frame_hora, text="Hora Inicio:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.entry_h_ini = tk.Entry(frame_hora, width=8, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_h_ini.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_hora, text="Hora Fin:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.entry_h_fin = tk.Entry(frame_hora, width=8, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_h_fin.pack(side=tk.LEFT, padx=5)
        
        # 6. Cantidad
        tk.Label(main, text="Cantidad Canchas:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.spin_canchas = tk.Spinbox(main, from_=1, to=20, bg=self.CARD_BG, fg=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.spin_canchas.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # 7. Precio
        tk.Label(main, text="Precio Total:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.entry_precio = tk.Entry(main, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.entry_precio.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        btn_frame = tk.Frame(main, bg=self.BG_COLOR, pady=20)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Crear y Pagar", command=self.crear, bg='#45796e', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.cmb_deporte.set('')
        self.entry_h_ini.delete(0, tk.END)
        self.entry_h_fin.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_nombre.focus()

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except: pass

    def crear(self):
        try:
            cliente_sel = self.cmb_cliente.get()
            if not cliente_sel:
                messagebox.showwarning("Alerta", "Seleccione un organizador")
                self.dialog.lift()
                self.dialog.focus_force()
                return
            
            id_cliente = int(cliente_sel.split(' - ')[0])
            nombre = self.entry_nombre.get()
            deporte = self.cmb_deporte.get()
            fecha = self.date_fecha.get_date()
            h_ini = parsear_hora(self.entry_h_ini.get())
            h_fin = parsear_hora(self.entry_h_fin.get())
            cant = int(self.spin_canchas.get())
            precio = float(self.entry_precio.get())
            
            if not h_ini or not h_fin:
                messagebox.showerror("Error", "Horas inválidas")
                self.dialog.lift()
                self.dialog.focus_force()
                return
            
            # 1. Intentar crear el torneo
            exito, msg, torneo = TorneoService.crear_torneo(id_cliente, nombre, deporte, fecha, h_ini, h_fin, cant, precio)
            
            if exito:
                # 2. Cerrar ventana de creación y abrir pago
                self.dialog.destroy()
                
                # 3. Abrir diálogo de pago y ESPERAR (wait_window)
                # Usamos 'self.parent' como master porque 'self.dialog' ya se destruyó
                pago_dialog = NuevoPagoDialog(self.parent, id_reserva=None, callback=self.callback, id_torneo=torneo.id_torneo)
                self.parent.wait_window(pago_dialog.dialog)
                
                # 4. VERIFICAR PAGO OBLIGATORIO
                pagado = PagoService.obtener_monto_pagado_torneo(torneo.id_torneo)
                
                # Tolerancia pequeña por temas de float
                if pagado < (torneo.precio_total - 0.1):
                    # ROLLBACK: No pagó, se elimina el torneo
                    TorneoService.eliminar_torneo(torneo.id_torneo)
                    messagebox.showwarning("Operación Cancelada", "El torneo fue eliminado porque no se completó el pago.")
                    self.callback() # Actualizar lista (para asegurar que no aparezca)
                else:
                    # ÉXITO TOTAL
                    messagebox.showinfo("Éxito", f"{msg}\nPago registrado correctamente.")
                    self.callback()
            else:
                messagebox.showerror("Error", msg)
                self.dialog.lift()
                self.dialog.focus_force()
                
        except ValueError:
            messagebox.showerror("Error", "Datos numéricos inválidos")
            self.dialog.lift()
            self.dialog.focus_force()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.dialog.lift()
            self.dialog.focus_force()
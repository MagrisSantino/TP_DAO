"""
Ventana de Gestión de Torneos
CORREGIDO: Calendario arreglado removiendo modalidad.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from business.torneo_service import TorneoService
from business.cliente_service import ClienteService
from dao.torneo_dao import TorneoDAO
from utils.helpers import formatear_monto, parsear_hora, formatear_hora
from ui.pago_window import NuevoPagoDialog

class TorneoWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Torneos")
        self.window.geometry("1100x600")
        self.window.configure(bg='#f0f0f0')
        self.torneo_seleccionado = None
        self.crear_widgets()
        self.cargar_torneos()
        self.window.lift()
        self.window.focus_force()
    
    def crear_widgets(self):
        frame_top = tk.Frame(self.window, bg='#f0f0f0')
        frame_top.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(frame_top, text="🏆 Torneos (Reservas Masivas)", font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(side=tk.LEFT)
        
        btn_nuevo = tk.Button(frame_top, text="➕ Nuevo Torneo", command=self.nuevo_torneo, bg='#3498db', fg='white', font=('Arial', 10, 'bold'), relief=tk.FLAT, padx=15, pady=5)
        btn_nuevo.pack(side=tk.RIGHT, padx=5)
        btn_eliminar = tk.Button(frame_top, text="🗑 Cancelar Torneo", command=self.eliminar_torneo, bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), relief=tk.FLAT, padx=15, pady=5)
        btn_eliminar.pack(side=tk.RIGHT, padx=5)
        
        frame_tabla = tk.Frame(self.window, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
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
            return
        if messagebox.askyesno("Confirmar", "¿Cancelar torneo y liberar canchas?"):
            exito, msg = TorneoService.eliminar_torneo(self.torneo_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_torneos()
            else:
                messagebox.showerror("Error", msg)

class NuevoTorneoDialog:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Torneo")
        self.dialog.geometry("500x650")
        self.dialog.configure(bg='#f0f0f0')
        
        # Eliminada toda lógica de modalidad para arreglar calendario
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_formulario()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')

    def crear_formulario(self):
        main = tk.Frame(self.dialog, bg='#f0f0f0', padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        tk.Label(main, text="Organizar Torneo", font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=(0, 15))
        
        tk.Label(main, text="Organizador (Cliente):", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.cmb_cliente = ttk.Combobox(main, state='readonly')
        self.cmb_cliente.pack(fill=tk.X, pady=5)
        clientes = ClienteService.obtener_clientes_activos()
        self.cmb_cliente['values'] = [f"{c.id_cliente} - {c.nombre} {c.apellido}" for c in clientes]
        
        tk.Label(main, text="Nombre del Torneo:", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.entry_nombre = tk.Entry(main)
        self.entry_nombre.pack(fill=tk.X, pady=5)
        
        tk.Label(main, text="Deporte:", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.cmb_deporte = ttk.Combobox(main, values=['Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Tenis', 'Padel', 'Basket'], state='readonly')
        self.cmb_deporte.pack(fill=tk.X, pady=5)
        
        tk.Label(main, text="Fecha (Día único):", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.date_fecha = DateEntry(main, width=20, background='darkblue', foreground='white', borderwidth=2)
        self.date_fecha.pack(fill=tk.X, pady=5)
        
        frame_hora = tk.Frame(main, bg='#f0f0f0')
        frame_hora.pack(fill=tk.X, pady=5)
        tk.Label(frame_hora, text="Hora Inicio:", bg='#f0f0f0').pack(side=tk.LEFT)
        self.entry_h_ini = tk.Entry(frame_hora, width=8)
        self.entry_h_ini.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_hora, text="Hora Fin:", bg='#f0f0f0').pack(side=tk.LEFT)
        self.entry_h_fin = tk.Entry(frame_hora, width=8)
        self.entry_h_fin.pack(side=tk.LEFT, padx=5)
        
        tk.Label(main, text="Cantidad Canchas:", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.spin_canchas = tk.Spinbox(main, from_=1, to=20)
        self.spin_canchas.pack(fill=tk.X, pady=5)
        
        tk.Label(main, text="Precio Total:", bg='#f0f0f0', anchor='w').pack(fill=tk.X)
        self.entry_precio = tk.Entry(main)
        self.entry_precio.pack(fill=tk.X, pady=5)
        
        btn_frame = tk.Frame(main, bg='#f0f0f0', pady=20)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Crear y Pagar", command=self.crear, bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'), padx=20).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cerrar_ventana, bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'), padx=20).pack(side=tk.LEFT, expand=True, padx=5)

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
                return
            exito, msg, torneo = TorneoService.crear_torneo(id_cliente, nombre, deporte, fecha, h_ini, h_fin, cant, precio)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.callback() 
                self.dialog.destroy() 
                NuevoPagoDialog(self.parent, id_reserva=None, callback=self.callback, id_torneo=torneo.id_torneo)
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Datos numéricos inválidos")
        except Exception as e:
            messagebox.showerror("Error", str(e))
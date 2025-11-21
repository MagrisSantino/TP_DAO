"""
Ventana de Gestión de Canchas - Estilo Moderno
Actualizada: Mantiene el foco en la lista al realizar acciones.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from business.cancha_service import CanchaService
from dao.cancha_dao import CanchaDAO


class CanchaWindow:
    """Ventana de gestión de canchas"""
    
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Canchas")
        self.window.geometry("1100x650")
        self.window.configure(bg=self.BG_COLOR)
        
        self.cancha_seleccionada = None
        
        self.crear_widgets()
        self.cargar_canchas()
        self.centrar_ventana()
        
    def centrar_ventana(self):
        self.window.update_idletasks()
        ancho = self.window.winfo_width()
        alto = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.window.winfo_screenheight() // 2) - (alto // 2)
        self.window.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        # Top frame
        frame_top = tk.Frame(self.window, bg=self.BG_COLOR)
        frame_top.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(frame_top, text="🏟️ Gestión de Canchas", font=('Segoe UI', 18, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side=tk.LEFT)
        
        btn_nueva = tk.Button(frame_top, text="➕ Nueva Cancha", command=self.nueva_cancha, bg='#4a6fa5', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        btn_nueva.pack(side=tk.RIGHT, padx=5)
        
        btn_editar = tk.Button(frame_top, text="✏ Editar", command=self.editar_cancha, bg='#8f6b4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        btn_editar.pack(side=tk.RIGHT, padx=5)
        
        btn_eliminar = tk.Button(frame_top, text="🗑 Eliminar", command=self.eliminar_cancha, bg='#a04a4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        btn_eliminar.pack(side=tk.RIGHT, padx=5)
        
        # Tabla
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
            columns=('ID', 'Nombre', 'Deporte', 'Cap', 'Precio Día', 'Precio Noche', 'Detalles', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Deporte', text='Deporte')
        self.tree.heading('Cap', text='Cap.')
        self.tree.heading('Precio Día', text='$ Día')
        self.tree.heading('Precio Noche', text='$ Noche')
        self.tree.heading('Detalles', text='Detalles')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=40, anchor='center')
        self.tree.column('Nombre', width=180)
        self.tree.column('Deporte', width=100)
        self.tree.column('Cap', width=50, anchor='center')
        self.tree.column('Precio Día', width=80, anchor='e')
        self.tree.column('Precio Noche', width=80, anchor='e')
        self.tree.column('Detalles', width=150)
        self.tree.column('Estado', width=80, anchor='center')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def cargar_canchas(self):
        try:
            self.window.lift()
            self.window.focus_force()
        except:
            pass

        for item in self.tree.get_children():
            self.tree.delete(item)
        canchas = CanchaService.obtener_todas()
        for c in canchas:
            detalles = []
            if c.techada: detalles.append("Techada")
            if c.iluminacion: detalles.append("Luz")
            detalles_str = ", ".join(detalles) if detalles else "-"
            
            self.tree.insert('', tk.END, values=(
                c.id_cancha, 
                c.nombre, 
                c.tipo_deporte,
                c.capacidad_jugadores,
                f"${c.precio_hora_dia}",
                f"${c.precio_hora_noche}",
                detalles_str,
                c.estado
            ))

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.cancha_seleccionada = item['values'][0]

    def nueva_cancha(self):
        NuevaCanchaDialog(self.window, self.cargar_canchas)

    def editar_cancha(self):
        if not self.cancha_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una cancha")
            return
        cancha = CanchaDAO.obtener_por_id(self.cancha_seleccionada)
        if cancha:
            EditarCanchaDialog(self.window, cancha, self.cargar_canchas)

    def eliminar_cancha(self):
        if not self.cancha_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una cancha")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta cancha?"):
            exito, mensaje = CanchaService.eliminar_cancha(self.cancha_seleccionada)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_canchas()
            else:
                messagebox.showerror("Error", mensaje)


class NuevaCanchaDialog:
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Cancha")
        self.dialog.geometry("500x650")
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.grab_set()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_formulario()
        self.centrar_dialogo()

    def centrar_dialogo(self):
        self.dialog.update_idletasks()
        ancho = self.dialog.winfo_width()
        alto = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (alto // 2)
        self.dialog.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_formulario(self):
        main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="Nueva Cancha", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 20))
        
        tk.Label(main, text="Nombre:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.entry_nombre = tk.Entry(main, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.entry_nombre.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        tk.Label(main, text="Deporte:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_deporte = ttk.Combobox(main, values=['Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Tenis', 'Padel', 'Basket'], state='readonly', font=('Segoe UI', 10))
        self.cmb_deporte.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        tk.Label(main, text="Superficie:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_superficie = ttk.Combobox(main, values=['Césped Natural', 'Césped Sintético', 'Cemento', 'Polvo de Ladrillo', 'Parquet'], state='readonly', font=('Segoe UI', 10))
        self.cmb_superficie.pack(fill=tk.X, pady=(0, 10), ipady=3)
        self.cmb_superficie.set('Césped Sintético')

        tk.Label(main, text="Capacidad (jugadores):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.spin_capacidad = tk.Spinbox(main, from_=2, to=30, bg=self.CARD_BG, fg=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.spin_capacidad.pack(fill=tk.X, pady=(0, 10), ipady=3)
        self.spin_capacidad.delete(0, tk.END)
        self.spin_capacidad.insert(0, 10)
        
        frame_precios = tk.LabelFrame(main, text="Precios por Hora", bg=self.BG_COLOR, fg=self.TEXT_COLOR, padx=10, pady=10, font=('Segoe UI', 10, 'bold'))
        frame_precios.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_precios, text="Horario Día ($):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.entry_precio_dia = tk.Entry(frame_precios, width=10, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_precio_dia.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_precios, text="Horario Noche ($):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.entry_precio_noche = tk.Entry(frame_precios, width=10, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_precio_noche.pack(side=tk.LEFT, padx=5)
        
        self.var_techo = tk.BooleanVar()
        tk.Checkbutton(main, text="Es techada", variable=self.var_techo, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w', pady=5)
        
        self.var_luz = tk.BooleanVar()
        tk.Checkbutton(main, text="Tiene iluminación", variable=self.var_luz, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        
        btn_frame = tk.Frame(main, bg=self.BG_COLOR, pady=20)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Guardar", command=self.guardar, bg='#45796e', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.cmb_deporte.set('')
        self.entry_precio_dia.delete(0, tk.END)
        self.entry_precio_noche.delete(0, tk.END)
        self.var_techo.set(False)
        self.var_luz.set(False)
        self.entry_nombre.focus()

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def guardar(self):
        try:
            nombre = self.entry_nombre.get()
            deporte = self.cmb_deporte.get()
            superficie = self.cmb_superficie.get()
            capacidad = int(self.spin_capacidad.get())
            precio_dia = float(self.entry_precio_dia.get())
            precio_noche = float(self.entry_precio_noche.get())
            techada = self.var_techo.get()
            iluminacion = self.var_luz.get()
            
            exito, mensaje, _ = CanchaService.crear_cancha(
                nombre=nombre,
                tipo_deporte=deporte,
                tipo_superficie=superficie,
                techada=techada,
                iluminacion=iluminacion,
                capacidad_jugadores=capacidad,
                precio_hora_dia=precio_dia,
                precio_hora_noche=precio_noche
            )
            
            if exito:
                messagebox.showinfo("Éxito", f"{mensaje}\n\nPuede cargar otra cancha o cerrar.")
                self.callback()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", mensaje)
                
        except ValueError:
            messagebox.showerror("Error", "Verifique que los precios y capacidad sean números válidos")


class EditarCanchaDialog:
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, cancha, callback):
        self.parent = parent
        self.cancha = cancha
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Cancha")
        self.dialog.geometry("500x650")
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.grab_set()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_formulario()
        self.cargar_datos()
        self.centrar_dialogo()

    def centrar_dialogo(self):
        self.dialog.update_idletasks()
        ancho = self.dialog.winfo_width()
        alto = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (alto // 2)
        self.dialog.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_formulario(self):
        main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="Editar Cancha", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 15))
        
        tk.Label(main, text="Nombre:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.entry_nombre = tk.Entry(main, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.entry_nombre.pack(fill=tk.X, pady=(0, 8), ipady=5)
        
        tk.Label(main, text="Deporte:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_deporte = ttk.Combobox(main, values=['Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Tenis', 'Padel', 'Basket'], state='readonly', font=('Segoe UI', 10))
        self.cmb_deporte.pack(fill=tk.X, pady=(0, 8), ipady=3)
        
        tk.Label(main, text="Superficie:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_superficie = ttk.Combobox(main, values=['Césped Natural', 'Césped Sintético', 'Cemento', 'Polvo de Ladrillo', 'Parquet'], state='readonly', font=('Segoe UI', 10))
        self.cmb_superficie.pack(fill=tk.X, pady=(0, 8), ipady=3)

        tk.Label(main, text="Capacidad:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.spin_capacidad = tk.Spinbox(main, from_=2, to=30, bg=self.CARD_BG, fg=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.spin_capacidad.pack(fill=tk.X, pady=(0, 8), ipady=3)

        frame_precios = tk.LabelFrame(main, text="Precios", bg=self.BG_COLOR, fg=self.TEXT_COLOR, padx=5, pady=5, font=('Segoe UI', 10, 'bold'))
        frame_precios.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_precios, text="Día ($):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.entry_precio_dia = tk.Entry(frame_precios, width=10, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_precio_dia.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_precios, text="Noche ($):", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.entry_precio_noche = tk.Entry(frame_precios, width=10, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT)
        self.entry_precio_noche.pack(side=tk.LEFT, padx=5)
        
        self.var_techo = tk.BooleanVar()
        tk.Checkbutton(main, text="Es techada", variable=self.var_techo, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w', pady=3)
        
        self.var_luz = tk.BooleanVar()
        tk.Checkbutton(main, text="Tiene iluminación", variable=self.var_luz, bg=self.BG_COLOR, fg=self.TEXT_COLOR, selectcolor=self.CARD_BG, activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(anchor='w')
        
        tk.Label(main, text="Estado:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X, pady=(10,0))
        self.cmb_estado = ttk.Combobox(main, values=['disponible', 'mantenimiento', 'no_disponible'], state='readonly', font=('Segoe UI', 10))
        self.cmb_estado.pack(fill=tk.X, pady=(0, 8), ipady=3)

        btn_frame = tk.Frame(main, bg=self.BG_COLOR, pady=20)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Actualizar", command=self.guardar, bg='#8f6b4a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def cargar_datos(self):
        self.entry_nombre.insert(0, self.cancha.nombre)
        self.cmb_deporte.set(self.cancha.tipo_deporte)
        self.cmb_superficie.set(self.cancha.tipo_superficie)
        self.spin_capacidad.delete(0, tk.END)
        self.spin_capacidad.insert(0, self.cancha.capacidad_jugadores)
        self.entry_precio_dia.insert(0, self.cancha.precio_hora_dia)
        self.entry_precio_noche.insert(0, self.cancha.precio_hora_noche)
        self.var_techo.set(self.cancha.techada)
        self.var_luz.set(self.cancha.iluminacion)
        self.cmb_estado.set(self.cancha.estado)

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def guardar(self):
        try:
            nombre = self.entry_nombre.get()
            deporte = self.cmb_deporte.get()
            superficie = self.cmb_superficie.get()
            capacidad = int(self.spin_capacidad.get())
            precio_dia = float(self.entry_precio_dia.get())
            precio_noche = float(self.entry_precio_noche.get())
            techada = self.var_techo.get()
            iluminacion = self.var_luz.get()
            estado = self.cmb_estado.get()
            
            exito, mensaje = CanchaService.actualizar_cancha(
                self.cancha.id_cancha,
                nombre=nombre,
                tipo_deporte=deporte,
                tipo_superficie=superficie,
                techada=techada,
                iluminacion=iluminacion,
                capacidad_jugadores=capacidad,
                precio_hora_dia=precio_dia,
                precio_hora_noche=precio_noche,
                estado=estado
            )
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.callback()
                self.cerrar_ventana()
            else:
                messagebox.showerror("Error", mensaje)
                
        except ValueError:
            messagebox.showerror("Error", "Verifique que los números sean válidos")
"""
Ventana de Gestión de Canchas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from business.cancha_service import CanchaService


class CanchaWindow:
    """Ventana de gestión de canchas"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Canchas")
        self.window.geometry("900x600")
        self.window.configure(bg='#f0f0f0')
        
        self.canchas = []
        self.cancha_seleccionada = None
        
        self.crear_widgets()
        self.cargar_canchas()
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
            text="🏟️ Gestión de Canchas",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            frame_top,
            text="➕ Nueva Cancha",
            command=self.nueva_cancha,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            frame_top,
            text="✏️ Editar",
            command=self.editar_cancha,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        # Tabla
        frame_tabla = tk.Frame(self.window, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=('ID', 'Nombre', 'Deporte', 'Superficie', 'Techada', 'Iluminación', 'Precio Día', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Deporte', text='Deporte')
        self.tree.heading('Superficie', text='Superficie')
        self.tree.heading('Techada', text='Techada')
        self.tree.heading('Iluminación', text='Iluminación')
        self.tree.heading('Precio Día', text='Precio Día')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=150)
        self.tree.column('Deporte', width=100)
        self.tree.column('Superficie', width=120)
        self.tree.column('Techada', width=80, anchor='center')
        self.tree.column('Iluminación', width=100, anchor='center')
        self.tree.column('Precio Día', width=100, anchor='e')
        self.tree.column('Estado', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Tags
        self.tree.tag_configure('disponible', background='#d4edda')
        self.tree.tag_configure('mantenimiento', background='#fff3cd')
        self.tree.tag_configure('no_disponible', background='#f8d7da')
    
    def cargar_canchas(self):
        """Carga todas las canchas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.canchas = CanchaService.obtener_todas_canchas()
        
        for cancha in self.canchas:
            techada = "Sí" if cancha.techada else "No"
            iluminacion = "Sí" if cancha.iluminacion else "No"
            
            tag = cancha.estado
            self.tree.insert('', tk.END, values=(
                cancha.id_cancha,
                cancha.nombre,
                cancha.tipo_deporte,
                cancha.tipo_superficie,
                techada,
                iluminacion,
                f"${cancha.precio_hora_dia:,.2f}",
                cancha.estado.capitalize()
            ), tags=(tag,))
    
    def on_select(self, event):
        """Maneja la selección"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.cancha_seleccionada = item['values'][0]
    
    def nueva_cancha(self):
        """Abre diálogo para nueva cancha"""
        CanchaDialog(self.window, None, self.cargar_canchas)
    
    def editar_cancha(self):
        """Abre diálogo para editar cancha"""
        if not self.cancha_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una cancha")
            return
        
        cancha = CanchaService.obtener_cancha(self.cancha_seleccionada)
        if cancha:
            CanchaDialog(self.window, cancha, self.cargar_canchas)


class CanchaDialog:
    """Diálogo para crear/editar cancha"""
    
    def __init__(self, parent, cancha, callback):
        self.cancha = cancha
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Cancha" if cancha else "Nueva Cancha")
        self.dialog.geometry("450x650")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.grab_set()
        
        self.crear_formulario()
        self.centrar_dialogo()
        
        if cancha:
            self.cargar_datos()
    
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
        
        titulo = "Editar Cancha" if self.cancha else "Nueva Cancha"
        tk.Label(
            main_frame,
            text=titulo,
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # Nombre
        tk.Label(main_frame, text="Nombre: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_nombre = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_nombre.pack(fill=tk.X, pady=(0, 10))
        
        # Deporte
        tk.Label(main_frame, text="Deporte: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.cmb_deporte = ttk.Combobox(main_frame, font=('Arial', 10), state='readonly')
        self.cmb_deporte['values'] = ('Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Básquet', 'Tenis', 'Vóley', 'Pádel')
        self.cmb_deporte.pack(fill=tk.X, pady=(0, 10))
        
        # Superficie
        tk.Label(main_frame, text="Superficie: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.cmb_superficie = ttk.Combobox(main_frame, font=('Arial', 10), state='readonly')
        self.cmb_superficie['values'] = ('Césped sintético', 'Césped natural', 'Cemento', 'Parquet', 'Tierra batida')
        self.cmb_superficie.pack(fill=tk.X, pady=(0, 10))
        
        # Checkboxes
        self.var_techada = tk.BooleanVar()
        tk.Checkbutton(
            main_frame,
            text="Techada",
            variable=self.var_techada,
            bg='#f0f0f0',
            font=('Arial', 10)
        ).pack(anchor='w', pady=(5, 5))
        
        self.var_iluminacion = tk.BooleanVar()
        tk.Checkbutton(
            main_frame,
            text="Iluminación",
            variable=self.var_iluminacion,
            bg='#f0f0f0',
            font=('Arial', 10)
        ).pack(anchor='w', pady=(0, 10))
        
        # Capacidad
        tk.Label(main_frame, text="Capacidad de jugadores: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.spin_capacidad = tk.Spinbox(main_frame, from_=2, to=50, font=('Arial', 10))
        self.spin_capacidad.pack(fill=tk.X, pady=(0, 10))
        
        # Precios
        tk.Label(main_frame, text="Precio hora día: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_precio_dia = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_precio_dia.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(main_frame, text="Precio hora noche: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_precio_noche = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_precio_noche.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        frame_botones = tk.Frame(main_frame, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X)
        
        tk.Button(
            frame_botones,
            text="Guardar",
            command=self.guardar,
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
    
    def cargar_datos(self):
        """Carga los datos de la cancha"""
        self.entry_nombre.insert(0, self.cancha.nombre)
        self.cmb_deporte.set(self.cancha.tipo_deporte)
        self.cmb_superficie.set(self.cancha.tipo_superficie)
        self.var_techada.set(self.cancha.techada)
        self.var_iluminacion.set(self.cancha.iluminacion)
        self.spin_capacidad.delete(0, tk.END)
        self.spin_capacidad.insert(0, self.cancha.capacidad_jugadores)
        self.entry_precio_dia.insert(0, self.cancha.precio_hora_dia)
        self.entry_precio_noche.insert(0, self.cancha.precio_hora_noche)
    
    def guardar(self):
        """Guarda la cancha"""
        try:
            nombre = self.entry_nombre.get().strip()
            deporte = self.cmb_deporte.get()
            superficie = self.cmb_superficie.get()
            techada = self.var_techada.get()
            iluminacion = self.var_iluminacion.get()
            capacidad = int(self.spin_capacidad.get())
            precio_dia = float(self.entry_precio_dia.get())
            precio_noche = float(self.entry_precio_noche.get())
            
            if not all([nombre, deporte, superficie]):
                messagebox.showwarning("Advertencia", "Complete todos los campos obligatorios")
                return
            
            if self.cancha:
                # Editar
                exito, mensaje = CanchaService.modificar_cancha(
                    self.cancha.id_cancha,
                    nombre=nombre,
                    tipo_deporte=deporte,
                    tipo_superficie=superficie,
                    techada=techada,
                    iluminacion=iluminacion,
                    capacidad_jugadores=capacidad,
                    precio_hora_dia=precio_dia,
                    precio_hora_noche=precio_noche
                )
            else:
                # Crear
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
                messagebox.showinfo("Éxito", mensaje)
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)
                
        except ValueError:
            messagebox.showerror("Error", "Verifique que los números sean válidos")
"""
Ventana de Gestión de Clientes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from business.cliente_service import ClienteService
from utils.validaciones import validar_dni, validar_email, validar_telefono


class ClienteWindow:
    """Ventana de gestión de clientes"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Clientes")
        self.window.geometry("900x600")
        self.window.configure(bg='#f0f0f0')
        
        self.clientes = []
        self.cliente_seleccionado = None
        
        self.crear_widgets()
        self.cargar_clientes()
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
        """Crea todos los widgets"""
        # Frame superior
        frame_top = tk.Frame(self.window, bg='#f0f0f0')
        frame_top.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            frame_top,
            text="👥 Gestión de Clientes",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            frame_top,
            text="➕ Nuevo Cliente",
            command=self.nuevo_cliente,
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
            command=self.editar_cliente,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        # Búsqueda
        frame_buscar = tk.Frame(self.window, bg='#f0f0f0')
        frame_buscar.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(frame_buscar, text="🔍 Buscar:", bg='#f0f0f0', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.entry_buscar = tk.Entry(frame_buscar, font=('Arial', 10), width=30)
        self.entry_buscar.pack(side=tk.LEFT, padx=10)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.buscar_clientes())
        
        tk.Button(
            frame_buscar,
            text="Actualizar",
            command=self.cargar_clientes,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            pady=5
        ).pack(side=tk.LEFT)
        
        # Tabla
        frame_tabla = tk.Frame(self.window, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=('ID', 'DNI', 'Nombre', 'Email', 'Teléfono', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Nombre', text='Nombre Completo')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('DNI', width=100)
        self.tree.column('Nombre', width=200)
        self.tree.column('Email', width=200)
        self.tree.column('Teléfono', width=120)
        self.tree.column('Estado', width=100, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Tags
        self.tree.tag_configure('activo', background='#d4edda')
        self.tree.tag_configure('inactivo', background='#f8d7da')
    
    def cargar_clientes(self):
        """Carga todos los clientes"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.clientes = ClienteService.obtener_todos_clientes()
        
        for cliente in self.clientes:
            tag = cliente.estado
            self.tree.insert('', tk.END, values=(
                cliente.id_cliente,
                cliente.dni,
                cliente.get_nombre_completo(),
                cliente.email,
                cliente.telefono,
                cliente.estado.capitalize()
            ), tags=(tag,))
    
    def buscar_clientes(self):
        """Busca clientes por término"""
        termino = self.entry_buscar.get().strip()
        
        if not termino:
            self.cargar_clientes()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultados = ClienteService.buscar_clientes(termino)
        
        for cliente in resultados:
            tag = cliente.estado
            self.tree.insert('', tk.END, values=(
                cliente.id_cliente,
                cliente.dni,
                cliente.get_nombre_completo(),
                cliente.email,
                cliente.telefono,
                cliente.estado.capitalize()
            ), tags=(tag,))
    
    def on_select(self, event):
        """Maneja la selección"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.cliente_seleccionado = item['values'][0]
    
    def nuevo_cliente(self):
        """Abre diálogo para nuevo cliente"""
        ClienteDialog(self.window, None, self.cargar_clientes)
    
    def editar_cliente(self):
        """Abre diálogo para editar cliente"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return
        
        cliente = ClienteService.obtener_cliente(self.cliente_seleccionado)
        if cliente:
            ClienteDialog(self.window, cliente, self.cargar_clientes)


class ClienteDialog:
    """Diálogo para crear/editar cliente"""
    
    def __init__(self, parent, cliente, callback):
        self.cliente = cliente
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Cliente" if cliente else "Nuevo Cliente")
        self.dialog.geometry("450x500")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.grab_set()
        
        self.crear_formulario()
        self.centrar_dialogo()
        
        if cliente:
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
        
        titulo = "Editar Cliente" if self.cliente else "Nuevo Cliente"
        tk.Label(
            main_frame,
            text=titulo,
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # DNI
        tk.Label(main_frame, text="DNI: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_dni = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_dni.pack(fill=tk.X, pady=(0, 15))
        
        # Nombre
        tk.Label(main_frame, text="Nombre: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_nombre = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_nombre.pack(fill=tk.X, pady=(0, 15))
        
        # Apellido
        tk.Label(main_frame, text="Apellido: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_apellido = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_apellido.pack(fill=tk.X, pady=(0, 15))
        
        # Email
        tk.Label(main_frame, text="Email: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_email = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_email.pack(fill=tk.X, pady=(0, 15))
        
        # Teléfono
        tk.Label(main_frame, text="Teléfono: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.entry_telefono = tk.Entry(main_frame, font=('Arial', 10))
        self.entry_telefono.pack(fill=tk.X, pady=(0, 20))
        
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
        """Carga los datos del cliente"""
        self.entry_dni.insert(0, self.cliente.dni)
        self.entry_nombre.insert(0, self.cliente.nombre)
        self.entry_apellido.insert(0, self.cliente.apellido)
        self.entry_email.insert(0, self.cliente.email)
        self.entry_telefono.insert(0, self.cliente.telefono)
    
    def guardar(self):
        """Guarda el cliente"""
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        
        if not all([dni, nombre, apellido, email, telefono]):
            messagebox.showwarning("Advertencia", "Complete todos los campos obligatorios (*)")
            return
        
        if self.cliente:
            # Editar
            exito, mensaje = ClienteService.modificar_cliente(
                self.cliente.id_cliente,
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono
            )
        else:
            # Crear
            exito, mensaje, _ = ClienteService.crear_cliente(
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono
            )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", mensaje)
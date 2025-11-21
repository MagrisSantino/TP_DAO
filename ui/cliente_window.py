"""
Ventana de Gestión de Clientes - Estilo Moderno
Actualizada: Mantiene el foco en la lista al realizar acciones.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from business.cliente_service import ClienteService
from dao.cliente_dao import ClienteDAO


class ClienteWindow:
    """Ventana de gestión de clientes"""
    
    # Colores del tema oscuro
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    SUBTITLE_COLOR = '#a0a0b0'
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Clientes")
        self.window.geometry("1000x600")
        self.window.configure(bg=self.BG_COLOR)
        
        # Variables
        self.clientes = []
        self.cliente_seleccionado = None
        
        self.crear_widgets()
        self.cargar_clientes()
        self.centrar_ventana()
    
    def centrar_ventana(self):
        self.window.update_idletasks()
        ancho = self.window.winfo_width()
        alto = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.window.winfo_screenheight() // 2) - (alto // 2)
        self.window.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        # Frame superior
        frame_top = tk.Frame(self.window, bg=self.BG_COLOR)
        frame_top.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(frame_top, text="👥 Gestión de Clientes", font=('Segoe UI', 18, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side=tk.LEFT)
        
        # Búsqueda
        frame_busq = tk.Frame(frame_top, bg=self.BG_COLOR)
        frame_busq.pack(side=tk.LEFT, padx=40)
        
        tk.Label(frame_busq, text="Buscar:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.entry_buscar = tk.Entry(frame_busq, width=30, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
        self.entry_buscar.pack(side=tk.LEFT, padx=5, ipady=5)
        self.entry_buscar.bind('<Return>', lambda e: self.buscar_cliente())
        
        tk.Button(frame_busq, text="🔍", command=self.buscar_cliente, relief=tk.FLAT, bg='#3a3a4e', fg=self.TEXT_COLOR, font=('Segoe UI', 10), cursor='hand2', padx=8).pack(side=tk.LEFT)
        tk.Button(frame_busq, text="✖", command=self.cargar_clientes, relief=tk.FLAT, bg='#3a3a4e', fg=self.TEXT_COLOR, font=('Segoe UI', 10), cursor='hand2', padx=8).pack(side=tk.LEFT, padx=2)
        
        # Botones
        btn_nuevo = tk.Button(frame_top, text="➕ Nuevo Cliente", command=self.nuevo_cliente, bg='#4a6fa5', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
        btn_nuevo.pack(side=tk.RIGHT, padx=5)
        
        btn_editar = tk.Button(frame_top, text="✏ Editar", command=self.editar_cliente, bg='#8f6b4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
        btn_editar.pack(side=tk.RIGHT, padx=5)
        
        btn_eliminar = tk.Button(frame_top, text="🗑 Eliminar", command=self.eliminar_cliente, bg='#a04a4a', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2', padx=20, pady=8)
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
        
        self.tree = ttk.Treeview(frame_tabla, columns=('ID', 'Nombre', 'Apellido', 'DNI', 'Teléfono', 'Email', 'Estado'), show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=150)
        self.tree.column('Apellido', width=150)
        self.tree.column('DNI', width=100, anchor='center')
        self.tree.column('Teléfono', width=120)
        self.tree.column('Email', width=200)
        self.tree.column('Estado', width=80, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.tag_configure('activo', background=self.CARD_BG)
        self.tree.tag_configure('inactivo', background='#3a3a4e', foreground='#808080')

    def cargar_clientes(self):
        try:
            self.window.lift()
            self.window.focus_force()
        except:
            pass

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.clientes = ClienteService.obtener_todos()
        for c in self.clientes:
            self.tree.insert('', tk.END, values=(c.id_cliente, c.nombre, c.apellido, c.dni, c.telefono, c.email, c.estado), tags=(c.estado,))
        self.entry_buscar.delete(0, tk.END)

    def buscar_cliente(self):
        termino = self.entry_buscar.get().strip()
        if not termino:
            self.cargar_clientes()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultados = ClienteService.buscar_clientes(termino)
        for c in resultados:
            self.tree.insert('', tk.END, values=(c.id_cliente, c.nombre, c.apellido, c.dni, c.telefono, c.email, c.estado), tags=(c.estado,))

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.cliente_seleccionado = item['values'][0]

    def nuevo_cliente(self):
        NuevoClienteDialog(self.window, self.cargar_clientes)

    def editar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return
        cliente = ClienteDAO.obtener_por_id(self.cliente_seleccionado)
        if cliente:
            EditarClienteDialog(self.window, cliente, self.cargar_clientes)

    def eliminar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar/desactivar este cliente?"):
            exito, mensaje = ClienteService.eliminar_cliente(self.cliente_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", mensaje)


class NuevoClienteDialog:
    """Diálogo para crear nuevo cliente"""
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Cliente")
        # MODIFICADO: Aumentado el tamaño a 500x600
        self.dialog.geometry("500x600")
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
        main_frame = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Nuevo Cliente", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 20))
        
        self.entries = {}
        campos = [("Nombre", "nombre"), ("Apellido", "apellido"), ("DNI", "dni"), ("Teléfono", "telefono"), ("Email", "email")]
        
        for label_text, key in campos:
            tk.Label(main_frame, text=label_text + ":", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            entry = tk.Entry(main_frame, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
            entry.pack(fill=tk.X, pady=(0, 12), ipady=5)
            self.entries[key] = entry
            
        btn_frame = tk.Frame(main_frame, bg=self.BG_COLOR, pady=10)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Guardar", command=self.guardar_cliente, bg='#45796e', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def limpiar_formulario(self):
        """Limpia los campos para una nueva carga"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries['nombre'].focus()

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def guardar_cliente(self):
        datos = {k: v.get() for k, v in self.entries.items()}
        exito, mensaje, _ = ClienteService.crear_cliente(**datos)
        
        if exito:
            messagebox.showinfo("Éxito", f"{mensaje}\n\nPuede cargar otro cliente o cerrar la ventana.")
            self.callback()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)


class EditarClienteDialog:
    """Diálogo para editar cliente"""
    BG_COLOR = '#1e1e2e'
    CARD_BG = '#2a2a3e'
    TEXT_COLOR = '#ffffff'
    
    def __init__(self, parent, cliente, callback):
        self.parent = parent
        self.cliente = cliente
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Cliente")
        # MODIFICADO: Aumentado el tamaño a 500x600
        self.dialog.geometry("500x600")
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
        main_frame = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Editar Cliente", font=('Segoe UI', 16, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 20))
        
        self.entries = {}
        campos = [("Nombre", "nombre"), ("Apellido", "apellido"), ("DNI", "dni"), ("Teléfono", "telefono"), ("Email", "email")]
        
        for label_text, key in campos:
            tk.Label(main_frame, text=label_text + ":", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
            entry = tk.Entry(main_frame, bg=self.CARD_BG, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, font=('Segoe UI', 10), relief=tk.FLAT, borderwidth=2)
            entry.pack(fill=tk.X, pady=(0, 10), ipady=5)
            self.entries[key] = entry
        
        # Estado
        tk.Label(main_frame, text="Estado:", bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor='w', font=('Segoe UI', 10)).pack(fill=tk.X)
        self.cmb_estado = ttk.Combobox(main_frame, values=['activo', 'inactivo'], state='readonly', font=('Segoe UI', 10))
        self.cmb_estado.pack(fill=tk.X, pady=(0, 15), ipady=3)
            
        btn_frame = tk.Frame(main_frame, bg=self.BG_COLOR, pady=10)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_cliente, bg='#8f6b4a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cerrar_ventana, bg='#5a6b7a', fg='white', font=('Segoe UI', 11, 'bold'), padx=30, pady=10, relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, expand=True, padx=5)

    def cargar_datos(self):
        self.entries['nombre'].insert(0, self.cliente.nombre)
        self.entries['apellido'].insert(0, self.cliente.apellido)
        self.entries['dni'].insert(0, self.cliente.dni)
        self.entries['telefono'].insert(0, self.cliente.telefono)
        self.entries['email'].insert(0, self.cliente.email)
        self.cmb_estado.set(self.cliente.estado)

    def cerrar_ventana(self):
        self.dialog.destroy()
        try:
            self.parent.lift()
            self.parent.focus_force()
        except:
            pass

    def actualizar_cliente(self):
        exito, mensaje = ClienteService.actualizar_cliente(
            id_cliente=self.cliente.id_cliente,
            nombre=self.entries['nombre'].get(),
            apellido=self.entries['apellido'].get(),
            dni=self.entries['dni'].get(),
            telefono=self.entries['telefono'].get(),
            email=self.entries['email'].get(),
            estado=self.cmb_estado.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.callback()
            self.cerrar_ventana()
        else:
            messagebox.showerror("Error", mensaje)
"""
Ventana de Gestión de Torneos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from tkcalendar import DateEntry
from business.torneo_service import TorneoService
from utils.helpers import formatear_fecha


class TorneoWindow:
    """Ventana de gestión de torneos"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Torneos")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        self.torneos = []
        self.torneo_seleccionado = None
        
        self.crear_widgets()
        self.cargar_torneos()
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
            text="🏆 Gestión de Torneos",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            frame_top,
            text="➕ Nuevo Torneo",
            command=self.nuevo_torneo,
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
            text="⚽ Ver Equipos",
            command=self.ver_equipos,
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
            text="📋 Generar Fixture",
            command=self.generar_fixture,
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
            columns=('ID', 'Nombre', 'Deporte', 'Fecha Inicio', 'Fecha Fin', 'Equipos', 'Estado'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Deporte', text='Deporte')
        self.tree.heading('Fecha Inicio', text='Fecha Inicio')
        self.tree.heading('Fecha Fin', text='Fecha Fin')
        self.tree.heading('Equipos', text='Equipos')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=200)
        self.tree.column('Deporte', width=120)
        self.tree.column('Fecha Inicio', width=120, anchor='center')
        self.tree.column('Fecha Fin', width=120, anchor='center')
        self.tree.column('Equipos', width=100, anchor='center')
        self.tree.column('Estado', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Tags
        self.tree.tag_configure('planificado', background='#fff3cd')
        self.tree.tag_configure('en_curso', background='#d1ecf1')
        self.tree.tag_configure('finalizado', background='#d4edda')
    
    def cargar_torneos(self):
        """Carga todos los torneos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.torneos = TorneoService.obtener_todos_torneos()
        
        for torneo in self.torneos:
            tag = torneo.estado_torneo
            self.tree.insert('', tk.END, values=(
                torneo.id_torneo,
                torneo.nombre,
                torneo.deporte,
                formatear_fecha(torneo.fecha_inicio),
                formatear_fecha(torneo.fecha_fin),
                torneo.cantidad_equipos,
                torneo.estado_torneo.capitalize()
            ), tags=(tag,))
    
    def on_select(self, event):
        """Maneja la selección"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.torneo_seleccionado = item['values'][0]
    
    def nuevo_torneo(self):
        """Abre diálogo para nuevo torneo"""
        NuevoTorneoDialog(self.window, self.cargar_torneos)
    
    def ver_equipos(self):
        """Ver equipos del torneo seleccionado"""
        if not self.torneo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un torneo")
            return
        
        messagebox.showinfo("En desarrollo", "Funcionalidad de equipos en desarrollo")
    
    def generar_fixture(self):
        """Genera el fixture del torneo"""
        if not self.torneo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un torneo")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea generar el fixture para este torneo?"
        )
        
        if respuesta:
            exito, mensaje, cant = TorneoService.generar_fixture(self.torneo_seleccionado)
            
            if exito:
                messagebox.showinfo("Éxito", f"{mensaje}")
                self.cargar_torneos()
            else:
                messagebox.showerror("Error", mensaje)


class NuevoTorneoDialog:
    """Diálogo para crear un torneo"""
    
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Torneo")
        self.dialog.geometry("450x550")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.grab_set()
        
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
            text="Nuevo Torneo",
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
        self.cmb_deporte['values'] = ('Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Básquet', 'Vóley')
        self.cmb_deporte.pack(fill=tk.X, pady=(0, 10))
        
        # Fecha inicio
        tk.Label(main_frame, text="Fecha Inicio: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.date_inicio = DateEntry(
            main_frame,
            width=20,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            mindate=date.today(),
            font=('Arial', 10)
        )
        self.date_inicio.pack(fill=tk.X, pady=(0, 10))
        
        # Fecha fin
        tk.Label(main_frame, text="Fecha Fin: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.date_fin = DateEntry(
            main_frame,
            width=20,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            mindate=date.today() + timedelta(days=1),
            font=('Arial', 10)
        )
        self.date_fin.pack(fill=tk.X, pady=(0, 10))
        
        # Cantidad de equipos
        tk.Label(main_frame, text="Cantidad de Equipos: *", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.spin_equipos = tk.Spinbox(main_frame, from_=2, to=32, font=('Arial', 10))
        self.spin_equipos.pack(fill=tk.X, pady=(0, 10))
        
        # Descripción
        tk.Label(main_frame, text="Descripción:", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        self.text_descripcion = tk.Text(main_frame, height=4, font=('Arial', 10))
        self.text_descripcion.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        frame_botones = tk.Frame(main_frame, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X)
        
        tk.Button(
            frame_botones,
            text="Crear Torneo",
            command=self.crear,
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
    
    def crear(self):
        """Crea el torneo"""
        try:
            nombre = self.entry_nombre.get().strip()
            deporte = self.cmb_deporte.get()
            fecha_inicio = self.date_inicio.get_date()
            fecha_fin = self.date_fin.get_date()
            cantidad_equipos = int(self.spin_equipos.get())
            descripcion = self.text_descripcion.get("1.0", tk.END).strip()
            
            if not all([nombre, deporte]):
                messagebox.showwarning("Advertencia", "Complete los campos obligatorios")
                return
            
            if fecha_fin < fecha_inicio:
                messagebox.showerror("Error de Fechas", "La fecha de fin no puede ser anterior a la de inicio.")
                # Opcional: Resetear la fecha fin a la de inicio
                self.date_fin.set_date(fecha_inicio)
                return
            
            exito, mensaje, torneo = TorneoService.crear_torneo(
                nombre=nombre,
                deporte=deporte,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                cantidad_equipos=cantidad_equipos,
                descripcion=descripcion
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear torneo: {str(e)}")
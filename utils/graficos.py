"""
Utilidades para Generación de Gráficos Estadísticos
Utiliza Matplotlib para crear visualizaciones
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import date
from typing import List, Dict, Tuple
import tkinter as tk


class Graficos:
    """Clase para generar gráficos estadísticos"""
    
    @staticmethod
    def crear_grafico_barras(datos: Dict, titulo: str, xlabel: str, ylabel: str,
                            parent_frame: tk.Frame = None, figsize: Tuple = (10, 6)) -> Figure:
        """
        Crea un gráfico de barras.
        
        Args:
            datos: Dict con 'categorias' (list) y 'valores' (list)
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            parent_frame: Frame de Tkinter donde embeber el gráfico (opcional)
            figsize: Tamaño de la figura (ancho, alto)
        
        Returns:
            Figure de matplotlib
        """
        fig = Figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        
        categorias = datos.get('categorias', [])
        valores = datos.get('valores', [])
        
        # Crear barras con colores
        colores = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', 
                   '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400']
        
        barras = ax.bar(categorias, valores, color=colores[:len(categorias)], alpha=0.8)
        
        # Agregar valores en las barras
        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura,
                   f'{altura:.0f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotar etiquetas si son muchas
        if len(categorias) > 6:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Embeber en Tkinter si se proporciona frame
        if parent_frame:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return fig
    
    @staticmethod
    def crear_grafico_lineas(datos: Dict, titulo: str, xlabel: str, ylabel: str,
                            parent_frame: tk.Frame = None, figsize: Tuple = (12, 6)) -> Figure:
        """
        Crea un gráfico de líneas para mostrar tendencias.
        
        Args:
            datos: Dict con 'x' (list) y 'y' (list)
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            parent_frame: Frame de Tkinter donde embeber el gráfico (opcional)
            figsize: Tamaño de la figura
        
        Returns:
            Figure de matplotlib
        """
        fig = Figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        
        x_data = datos.get('x', [])
        y_data = datos.get('y', [])
        
        # Crear línea
        ax.plot(x_data, y_data, marker='o', linewidth=2, markersize=8,
               color='#3498db', markerfacecolor='#e74c3c', markeredgecolor='#c0392b')
        
        # Agregar valores en los puntos
        for i, (x, y) in enumerate(zip(x_data, y_data)):
            ax.text(x, y, f'{y:.0f}', ha='center', va='bottom', 
                   fontsize=9, fontweight='bold')
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        fig.tight_layout()
        
        # Embeber en Tkinter si se proporciona frame
        if parent_frame:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return fig
    
    @staticmethod
    def crear_grafico_torta(datos: Dict, titulo: str, parent_frame: tk.Frame = None,
                           figsize: Tuple = (8, 8)) -> Figure:
        """
        Crea un gráfico de torta para mostrar distribución porcentual.
        
        Args:
            datos: Dict con 'categorias' (list) y 'valores' (list)
            titulo: Título del gráfico
            parent_frame: Frame de Tkinter donde embeber el gráfico (opcional)
            figsize: Tamaño de la figura
        
        Returns:
            Figure de matplotlib
        """
        fig = Figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        
        categorias = datos.get('categorias', [])
        valores = datos.get('valores', [])
        
        # Colores
        colores = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
                   '#1abc9c', '#34495e', '#e67e22']
        
        # Crear gráfico de torta
        wedges, texts, autotexts = ax.pie(
            valores,
            labels=categorias,
            autopct='%1.1f%%',
            startangle=90,
            colors=colores[:len(categorias)],
            explode=[0.05] * len(categorias)  # Separar ligeramente las porciones
        )
        
        # Mejorar texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        fig.tight_layout()
        
        # Embeber en Tkinter si se proporciona frame
        if parent_frame:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return fig
    
    @staticmethod
    def crear_grafico_utilizacion_mensual(año: int, mes: int, datos: Dict,
                                         parent_frame: tk.Frame = None) -> Figure:
        """
        Crea gráfico específico de utilización mensual de canchas.
        
        Args:
            año: Año del reporte
            mes: Mes del reporte (1-12)
            datos: Dict con 'dias' y 'cantidad_reservas'
            parent_frame: Frame de Tkinter
        
        Returns:
            Figure de matplotlib
        """
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        titulo = f"Utilización de Canchas - {meses[mes-1]} {año}"
        
        datos_grafico = {
            'x': datos.get('dias', []),
            'y': datos.get('cantidad_reservas', [])
        }
        
        return Graficos.crear_grafico_lineas(
            datos_grafico,
            titulo=titulo,
            xlabel='Día del Mes',
            ylabel='Cantidad de Reservas',
            parent_frame=parent_frame,
            figsize=(14, 6)
        )
    
    @staticmethod
    def crear_grafico_canchas_mas_utilizadas(datos: List[Dict],
                                             parent_frame: tk.Frame = None) -> Figure:
        """
        Crea gráfico de barras de canchas más utilizadas.
        
        Args:
            datos: Lista de dict con info de canchas y cantidad de reservas
            parent_frame: Frame de Tkinter
        
        Returns:
            Figure de matplotlib
        """
        # Ordenar por cantidad de reservas (descendente)
        datos_ordenados = sorted(datos, key=lambda x: x['total_reservas'], reverse=True)
        
        # Tomar top 10
        top_canchas = datos_ordenados[:10]
        
        categorias = [f"{c['nombre_cancha']}\n({c['tipo_deporte']})" for c in top_canchas]
        valores = [c['total_reservas'] for c in top_canchas]
        
        datos_grafico = {
            'categorias': categorias,
            'valores': valores
        }
        
        return Graficos.crear_grafico_barras(
            datos_grafico,
            titulo='Top 10 Canchas Más Utilizadas',
            xlabel='Cancha',
            ylabel='Cantidad de Reservas',
            parent_frame=parent_frame,
            figsize=(12, 6)
        )
    
    @staticmethod
    def crear_grafico_facturacion_mensual(año: int, datos: Dict,
                                         parent_frame: tk.Frame = None) -> Figure:
        """
        Crea gráfico de barras de facturación mensual.
        
        Args:
            año: Año del reporte
            datos: Dict con 'meses' y 'facturacion'
            parent_frame: Frame de Tkinter
        
        Returns:
            Figure de matplotlib
        """
        datos_grafico = {
            'categorias': datos.get('meses', []),
            'valores': datos.get('facturacion', [])
        }
        
        return Graficos.crear_grafico_barras(
            datos_grafico,
            titulo=f'Facturación Mensual - Año {año}',
            xlabel='Mes',
            ylabel='Facturación ($)',
            parent_frame=parent_frame,
            figsize=(12, 6)
        )
    
    @staticmethod
    def crear_grafico_distribucion_horaria(datos: Dict,
                                          parent_frame: tk.Frame = None) -> Figure:
        """
        Crea gráfico de torta de distribución por horario (día/noche).
        
        Args:
            datos: Dict con 'categorias' y 'valores'
            parent_frame: Frame de Tkinter
        
        Returns:
            Figure de matplotlib
        """
        return Graficos.crear_grafico_torta(
            datos,
            titulo='Distribución de Reservas por Horario',
            parent_frame=parent_frame,
            figsize=(8, 8)
        )
    
    @staticmethod
    def guardar_grafico(fig: Figure, nombre_archivo: str):
        """
        Guarda un gráfico como imagen.
        
        Args:
            fig: Figure de matplotlib
            nombre_archivo: Ruta donde guardar el archivo
        """
        fig.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {nombre_archivo}")
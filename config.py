"""
Archivo de configuración global del sistema
"""

import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración de la base de datos
DB_PATH = os.path.join(BASE_DIR, 'database', 'reservas_canchas.db')

# Configuración de horarios del complejo
HORA_APERTURA = "08:00"
HORA_CIERRE = "23:00"

# Configuración de precios (ejemplo)
PRECIO_BASE_DIA = 5000.0  # Precio base por hora en horario diurno
PRECIO_BASE_NOCHE = 7000.0  # Precio base por hora en horario nocturno (después de las 18:00)
RECARGO_ILUMINACION = 1000.0  # Recargo por uso de iluminación

# Configuración de interfaz
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Sistema de Reservas de Canchas Deportivas"

# Colores del tema
COLOR_PRIMARY = "#2C3E50"
COLOR_SECONDARY = "#3498DB"
COLOR_SUCCESS = "#27AE60"
COLOR_DANGER = "#E74C3C"
COLOR_WARNING = "#F39C12"
COLOR_INFO = "#16A085"
COLOR_BACKGROUND = "#ECF0F1"
COLOR_TEXT = "#2C3E50"

# Estados de reserva
ESTADOS_RESERVA = ['pendiente', 'confirmada', 'cancelada', 'completada']
ESTADOS_CANCHA = ['disponible', 'mantenimiento', 'no_disponible']
ESTADOS_TORNEO = ['planificado', 'en_curso', 'finalizado']
ESTADOS_PARTIDO = ['programado', 'jugado', 'suspendido']
ESTADOS_PAGO = ['pendiente', 'pagado', 'reembolsado']

# Tipos de deporte
TIPOS_DEPORTE = ['Fútbol 5', 'Fútbol 7', 'Fútbol 11', 'Tenis', 'Paddle', 'Básquet', 'Vóley']

# Tipos de superficie
TIPOS_SUPERFICIE = ['Césped natural', 'Césped sintético', 'Cemento', 'Polvo de ladrillo', 'Parquet']

# Métodos de pago
METODOS_PAGO = ['efectivo', 'transferencia', 'tarjeta_debito', 'tarjeta_credito']
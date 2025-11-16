"""
Módulo de Helpers
Funciones auxiliares para formateo y utilidades generales
"""

from datetime import datetime, date, time
from typing import Optional


def formatear_fecha(fecha: date, formato: str = "%d/%m/%Y") -> str:
    """
    Formatea una fecha como string.
    
    Args:
        fecha (date): Fecha a formatear
        formato (str): Formato de salida (por defecto DD/MM/YYYY)
    
    Returns:
        str: Fecha formateada
    
    Examples:
        >>> from datetime import date
        >>> formatear_fecha(date(2024, 5, 15))
        '15/05/2024'
        >>> formatear_fecha(date(2024, 5, 15), "%Y-%m-%d")
        '2024-05-15'
    """
    if not isinstance(fecha, date):
        return ""
    
    return fecha.strftime(formato)


def formatear_hora(hora: time, formato: str = "%H:%M") -> str:
    """
    Formatea una hora como string.
    
    Args:
        hora (time): Hora a formatear
        formato (str): Formato de salida (por defecto HH:MM)
    
    Returns:
        str: Hora formateada
    
    Examples:
        >>> from datetime import time
        >>> formatear_hora(time(14, 30))
        '14:30'
        >>> formatear_hora(time(9, 5))
        '09:05'
    """
    if not isinstance(hora, time):
        return ""
    
    return hora.strftime(formato)


def formatear_monto(monto: float, simbolo: str = "$") -> str:
    """
    Formatea un monto con separadores de miles y decimales.
    
    Args:
        monto (float): Monto a formatear
        simbolo (str): Símbolo de moneda (por defecto $)
    
    Returns:
        str: Monto formateado
    
    Examples:
        >>> formatear_monto(1234.56)
        '$1,234.56'
        >>> formatear_monto(1000000)
        '$1,000,000.00'
        >>> formatear_monto(50.5, "USD")
        'USD50.50'
    """
    try:
        monto_float = float(monto)
        return f"{simbolo}{monto_float:,.2f}"
    except (ValueError, TypeError):
        return f"{simbolo}0.00"


def calcular_edad(fecha_nacimiento: date) -> int:
    """
    Calcula la edad a partir de una fecha de nacimiento.
    
    Args:
        fecha_nacimiento (date): Fecha de nacimiento
    
    Returns:
        int: Edad en años
    
    Examples:
        >>> from datetime import date
        >>> # Si hoy es 2024-05-15
        >>> calcular_edad(date(2000, 5, 15))
        24
        >>> calcular_edad(date(2000, 5, 16))
        23
    """
    if not isinstance(fecha_nacimiento, date):
        return 0
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si aún no cumplió años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def parsear_fecha(fecha_str: str, formato: str = "%d/%m/%Y") -> Optional[date]:
    """
    Convierte un string a fecha.
    
    Args:
        fecha_str (str): Fecha como string
        formato (str): Formato del string (por defecto DD/MM/YYYY)
    
    Returns:
        date: Objeto fecha o None si es inválido
    
    Examples:
        >>> parsear_fecha("15/05/2024")
        datetime.date(2024, 5, 15)
        >>> parsear_fecha("2024-05-15", "%Y-%m-%d")
        datetime.date(2024, 5, 15)
        >>> parsear_fecha("fecha_invalida")
        None
    """
    try:
        return datetime.strptime(fecha_str, formato).date()
    except (ValueError, TypeError):
        return None


def parsear_hora(hora_str: str, formato: str = "%H:%M") -> Optional[time]:
    """
    Convierte un string a hora.
    
    Args:
        hora_str (str): Hora como string
        formato (str): Formato del string (por defecto HH:MM)
    
    Returns:
        time: Objeto hora o None si es inválido
    
    Examples:
        >>> parsear_hora("14:30")
        datetime.time(14, 30)
        >>> parsear_hora("09:05")
        datetime.time(9, 5)
        >>> parsear_hora("hora_invalida")
        None
    """
    try:
        return datetime.strptime(hora_str, formato).time()
    except (ValueError, TypeError):
        return None


def normalizar_texto(texto: str) -> str:
    """
    Normaliza un texto (quita espacios extras, capitaliza).
    
    Args:
        texto (str): Texto a normalizar
    
    Returns:
        str: Texto normalizado
    
    Examples:
        >>> normalizar_texto("  juan  PEREZ  ")
        'Juan Perez'
        >>> normalizar_texto("MARIA")
        'Maria'
    """
    if not texto:
        return ""
    
    # Quitar espacios extras y capitalizar cada palabra
    return " ".join(texto.strip().split()).title()


def truncar_texto(texto: str, longitud_maxima: int = 50, sufijo: str = "...") -> str:
    """
    Trunca un texto si excede la longitud máxima.
    
    Args:
        texto (str): Texto a truncar
        longitud_maxima (int): Longitud máxima
        sufijo (str): Sufijo a agregar si se trunca
    
    Returns:
        str: Texto truncado
    
    Examples:
        >>> truncar_texto("Este es un texto muy largo", 15)
        'Este es un t...'
        >>> truncar_texto("Texto corto", 15)
        'Texto corto'
    """
    if not texto:
        return ""
    
    if len(texto) <= longitud_maxima:
        return texto
    
    return texto[:longitud_maxima - len(sufijo)] + sufijo


def obtener_nombre_dia_semana(fecha: date) -> str:
    """
    Obtiene el nombre del día de la semana en español.
    
    Args:
        fecha (date): Fecha
    
    Returns:
        str: Nombre del día
    
    Examples:
        >>> from datetime import date
        >>> # Si fecha es un lunes
        >>> obtener_nombre_dia_semana(date(2024, 5, 13))
        'Lunes'
    """
    dias = [
        'Lunes', 'Martes', 'Miércoles', 'Jueves', 
        'Viernes', 'Sábado', 'Domingo'
    ]
    
    if not isinstance(fecha, date):
        return ""
    
    return dias[fecha.weekday()]


def obtener_nombre_mes(mes: int) -> str:
    """
    Obtiene el nombre del mes en español.
    
    Args:
        mes (int): Número del mes (1-12)
    
    Returns:
        str: Nombre del mes
    
    Examples:
        >>> obtener_nombre_mes(5)
        'Mayo'
        >>> obtener_nombre_mes(12)
        'Diciembre'
    """
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    if 1 <= mes <= 12:
        return meses[mes - 1]
    
    return ""


def generar_codigo_reserva(id_reserva: int) -> str:
    """
    Genera un código de reserva formateado.
    
    Args:
        id_reserva (int): ID de la reserva
    
    Returns:
        str: Código formateado
    
    Examples:
        >>> generar_codigo_reserva(1)
        'RES-0001'
        >>> generar_codigo_reserva(123)
        'RES-0123'
    """
    return f"RES-{id_reserva:04d}"


def calcular_porcentaje(parte: float, total: float) -> float:
    """
    Calcula el porcentaje que representa una parte del total.
    
    Args:
        parte (float): Valor parcial
        total (float): Valor total
    
    Returns:
        float: Porcentaje (0-100)
    
    Examples:
        >>> calcular_porcentaje(25, 100)
        25.0
        >>> calcular_porcentaje(3, 4)
        75.0
        >>> calcular_porcentaje(10, 0)
        0.0
    """
    if total == 0:
        return 0.0
    
    try:
        return round((float(parte) / float(total)) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def es_fin_de_semana(fecha: date) -> bool:
    """
    Verifica si una fecha es fin de semana (sábado o domingo).
    
    Args:
        fecha (date): Fecha a verificar
    
    Returns:
        bool: True si es fin de semana
    
    Examples:
        >>> from datetime import date
        >>> # Si es sábado
        >>> es_fin_de_semana(date(2024, 5, 18))
        True
        >>> # Si es lunes
        >>> es_fin_de_semana(date(2024, 5, 13))
        False
    """
    if not isinstance(fecha, date):
        return False
    
    # weekday(): 0=Lunes, 5=Sábado, 6=Domingo
    return fecha.weekday() in [5, 6]


def limpiar_telefono(telefono: str) -> str:
    """
    Limpia un número de teléfono eliminando caracteres no numéricos.
    
    Args:
        telefono (str): Teléfono a limpiar
    
    Returns:
        str: Teléfono limpio (solo números)
    
    Examples:
        >>> limpiar_telefono("+54 351-1234567")
        '543511234567'
        >>> limpiar_telefono("(351) 123-4567")
        '3511234567'
    """
    if not telefono:
        return ""
    
    # Eliminar todo excepto dígitos
    return ''.join(c for c in telefono if c.isdigit())
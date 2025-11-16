"""
Módulo de Validaciones
Funciones para validar datos de entrada
"""

import re
from datetime import date


def validar_dni(dni: str) -> bool:
    """
    Valida formato de DNI argentino (7-8 dígitos).
    
    Args:
        dni (str): DNI a validar
    
    Returns:
        bool: True si es válido, False en caso contrario
    
    Examples:
        >>> validar_dni("12345678")
        True
        >>> validar_dni("1234567")
        True
        >>> validar_dni("123")
        False
        >>> validar_dni("abc12345")
        False
    """
    if not dni:
        return False
    
    # Eliminar espacios y guiones
    dni_limpio = dni.strip().replace(" ", "").replace("-", "")
    
    # Validar que tenga 7 u 8 dígitos numéricos
    patron = r'^\d{7,8}$'
    return bool(re.match(patron, dni_limpio))


def validar_email(email: str) -> bool:
    """
    Valida formato de email.
    
    Args:
        email (str): Email a validar
    
    Returns:
        bool: True si es válido, False en caso contrario
    
    Examples:
        >>> validar_email("usuario@example.com")
        True
        >>> validar_email("usuario.apellido@empresa.com.ar")
        True
        >>> validar_email("usuario@")
        False
        >>> validar_email("@example.com")
        False
    """
    if not email:
        return False
    
    # Patrón para email válido
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email.strip()))


def validar_telefono(telefono: str) -> bool:
    """
    Valida formato de teléfono argentino.
    Acepta formatos: 3511234567, 351-1234567, +54 351 1234567, etc.
    
    Args:
        telefono (str): Teléfono a validar
    
    Returns:
        bool: True si es válido, False en caso contrario
    
    Examples:
        >>> validar_telefono("3511234567")
        True
        >>> validar_telefono("351-1234567")
        True
        >>> validar_telefono("+54 351 1234567")
        True
        >>> validar_telefono("123")
        False
    """
    if not telefono:
        return False
    
    # Eliminar espacios, guiones y paréntesis
    tel_limpio = telefono.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Eliminar prefijo internacional si existe
    if tel_limpio.startswith("+54"):
        tel_limpio = tel_limpio[3:]
    elif tel_limpio.startswith("54"):
        tel_limpio = tel_limpio[2:]
    
    # Validar que tenga entre 8 y 10 dígitos
    patron = r'^\d{8,10}$'
    return bool(re.match(patron, tel_limpio))


def validar_fecha_no_pasada(fecha: date) -> bool:
    """
    Verifica que la fecha no sea pasada.
    
    Args:
        fecha (date): Fecha a validar
    
    Returns:
        bool: True si es hoy o futura, False si es pasada
    
    Examples:
        >>> from datetime import date, timedelta
        >>> validar_fecha_no_pasada(date.today())
        True
        >>> validar_fecha_no_pasada(date.today() + timedelta(days=1))
        True
        >>> validar_fecha_no_pasada(date.today() - timedelta(days=1))
        False
    """
    if not isinstance(fecha, date):
        return False
    
    return fecha >= date.today()


def es_fecha_valida(dia: int, mes: int, año: int) -> bool:
    """
    Verifica si una fecha es válida.
    
    Args:
        dia (int): Día
        mes (int): Mes
        año (int): Año
    
    Returns:
        bool: True si es válida, False en caso contrario
    
    Examples:
        >>> es_fecha_valida(15, 5, 2024)
        True
        >>> es_fecha_valida(31, 2, 2024)
        False
        >>> es_fecha_valida(29, 2, 2024)
        True
        >>> es_fecha_valida(29, 2, 2023)
        False
    """
    try:
        date(año, mes, dia)
        return True
    except ValueError:
        return False


def validar_rango_horario(hora_inicio: str, hora_fin: str) -> bool:
    """
    Valida que un rango horario sea correcto.
    
    Args:
        hora_inicio (str): Hora inicio en formato HH:MM
        hora_fin (str): Hora fin en formato HH:MM
    
    Returns:
        bool: True si el rango es válido
    
    Examples:
        >>> validar_rango_horario("10:00", "12:00")
        True
        >>> validar_rango_horario("12:00", "10:00")
        False
    """
    try:
        from datetime import datetime
        
        # Parsear horas
        inicio = datetime.strptime(hora_inicio, "%H:%M").time()
        fin = datetime.strptime(hora_fin, "%H:%M").time()
        
        # Validar que fin sea posterior a inicio
        return fin > inicio
    except ValueError:
        return False


def validar_monto_positivo(monto: float) -> bool:
    """
    Valida que un monto sea positivo.
    
    Args:
        monto (float): Monto a validar
    
    Returns:
        bool: True si es positivo, False en caso contrario
    """
    try:
        return float(monto) > 0
    except (ValueError, TypeError):
        return False


def validar_capacidad(capacidad: int) -> bool:
    """
    Valida que una capacidad sea válida (entre 2 y 50).
    
    Args:
        capacidad (int): Capacidad a validar
    
    Returns:
        bool: True si es válida, False en caso contrario
    """
    try:
        cap = int(capacidad)
        return 2 <= cap <= 50
    except (ValueError, TypeError):
        return False


def validar_texto_no_vacio(texto: str, longitud_minima: int = 1) -> bool:
    """
    Valida que un texto no esté vacío y tenga una longitud mínima.
    
    Args:
        texto (str): Texto a validar
        longitud_minima (int): Longitud mínima requerida
    
    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not texto:
        return False
    
    return len(texto.strip()) >= longitud_minima


def validar_numero_entero(valor: str) -> bool:
    """
    Valida que un valor sea un número entero.
    
    Args:
        valor (str): Valor a validar
    
    Returns:
        bool: True si es un entero válido, False en caso contrario
    """
    try:
        int(valor)
        return True
    except (ValueError, TypeError):
        return False


def validar_numero_decimal(valor: str) -> bool:
    """
    Valida que un valor sea un número decimal.
    
    Args:
        valor (str): Valor a validar
    
    Returns:
        bool: True si es un decimal válido, False en caso contrario
    """
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False
"""
Modelo Cancha - Representa una cancha deportiva
"""


class Cancha:
    """
    Clase que representa una cancha deportiva del complejo.
    Corresponde a la tabla 'cancha' en la base de datos.
    """
    
    def __init__(self, id_cancha=None, nombre='', tipo_deporte='', tipo_superficie='',
                 techada=False, iluminacion=False, capacidad_jugadores=0,
                 precio_hora_dia=0.0, precio_hora_noche=0.0, estado='disponible'):
        """
        Constructor de la clase Cancha.
        
        Args:
            id_cancha (int): ID único de la cancha
            nombre (str): Nombre identificatorio de la cancha
            tipo_deporte (str): Tipo de deporte (Fútbol 5, Tenis, etc.)
            tipo_superficie (str): Tipo de superficie (césped, sintético, etc.)
            techada (bool): Si la cancha está techada
            iluminacion (bool): Si la cancha tiene iluminación
            capacidad_jugadores (int): Capacidad máxima de jugadores
            precio_hora_dia (float): Precio por hora en horario diurno
            precio_hora_noche (float): Precio por hora en horario nocturno
            estado (str): Estado de la cancha
        """
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.tipo_deporte = tipo_deporte
        self.tipo_superficie = tipo_superficie
        self.techada = bool(techada)
        self.iluminacion = bool(iluminacion)
        self.capacidad_jugadores = capacidad_jugadores
        self.precio_hora_dia = float(precio_hora_dia)
        self.precio_hora_noche = float(precio_hora_noche)
        self.estado = estado
    
    def esta_disponible(self):
        """Verifica si la cancha está disponible para reservar"""
        return self.estado == 'disponible'
    
    def tiene_iluminacion(self):
        """Verifica si la cancha tiene iluminación"""
        return self.iluminacion
    
    def es_techada(self):
        """Verifica si la cancha está techada"""
        return self.techada
    
    def get_precio_por_hora(self, es_horario_nocturno=False):
        """
        Retorna el precio por hora según el horario.
        
        Args:
            es_horario_nocturno (bool): True si es después de las 18:00
        
        Returns:
            float: Precio por hora
        """
        return self.precio_hora_noche if es_horario_nocturno else self.precio_hora_dia
    
    def __str__(self):
        """Representación en string de la cancha"""
        return f"{self.nombre} - {self.tipo_deporte} ({self.estado})"
    
    def __repr__(self):
        """Representación para debugging"""
        return (f"Cancha(id={self.id_cancha}, nombre='{self.nombre}', "
                f"tipo_deporte='{self.tipo_deporte}', estado='{self.estado}')")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_cancha': self.id_cancha,
            'nombre': self.nombre,
            'tipo_deporte': self.tipo_deporte,
            'tipo_superficie': self.tipo_superficie,
            'techada': self.techada,
            'iluminacion': self.iluminacion,
            'capacidad_jugadores': self.capacidad_jugadores,
            'precio_hora_dia': self.precio_hora_dia,
            'precio_hora_noche': self.precio_hora_noche,
            'estado': self.estado
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea una instancia de Cancha desde un diccionario.
        
        Args:
            data (dict): Diccionario con los datos de la cancha
        
        Returns:
            Cancha: Instancia de Cancha
        """
        return Cancha(
            id_cancha=data.get('id_cancha'),
            nombre=data.get('nombre', ''),
            tipo_deporte=data.get('tipo_deporte', ''),
            tipo_superficie=data.get('tipo_superficie', ''),
            techada=bool(data.get('techada', False)),
            iluminacion=bool(data.get('iluminacion', False)),
            capacidad_jugadores=data.get('capacidad_jugadores', 0),
            precio_hora_dia=data.get('precio_hora_dia', 0.0),
            precio_hora_noche=data.get('precio_hora_noche', 0.0),
            estado=data.get('estado', 'disponible')
        )
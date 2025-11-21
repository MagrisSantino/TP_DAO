"""
Modelo Cancha
Actualizado con atributos extendidos.
"""

class Cancha:
    def __init__(self, id_cancha=None, nombre="", tipo_deporte="", 
                 tipo_superficie="Sintético", techada=False, iluminacion=False, 
                 capacidad_jugadores=5, precio_hora_dia=0.0, precio_hora_noche=0.0, 
                 estado="disponible"):
        
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.tipo_deporte = tipo_deporte
        self.tipo_superficie = tipo_superficie
        self.techada = techada
        self.iluminacion = iluminacion
        self.capacidad_jugadores = capacidad_jugadores
        self.precio_hora_dia = precio_hora_dia
        self.precio_hora_noche = precio_hora_noche
        self.estado = estado

    # Propiedad de compatibilidad para código viejo que busque .precio_hora
    @property
    def precio_hora(self):
        return self.precio_hora_dia

    def to_dict(self):
        return {
            "id_cancha": self.id_cancha,
            "nombre": self.nombre,
            "tipo_deporte": self.tipo_deporte,
            "tipo_superficie": self.tipo_superficie,
            "techada": self.techada,
            "iluminacion": self.iluminacion,
            "capacidad_jugadores": self.capacidad_jugadores,
            "precio_hora_dia": self.precio_hora_dia,
            "precio_hora_noche": self.precio_hora_noche,
            "estado": self.estado
        }
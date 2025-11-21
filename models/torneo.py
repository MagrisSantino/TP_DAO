"""
Modelo Torneo
Actualizado: Incluye id_cliente (Organizador) y estructura de reserva masiva.
"""

class Torneo:
    def __init__(self, id_torneo=None, nombre="", deporte="", fecha=None, 
                 hora_inicio=None, hora_fin=None, cantidad_canchas=0, 
                 precio_total=0.0, estado="confirmado", id_cliente=None):
        
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.deporte = deporte
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.cantidad_canchas = cantidad_canchas
        self.precio_total = precio_total
        self.estado = estado
        self.id_cliente = id_cliente # Nuevo campo

    def to_dict(self):
        return {
            "id_torneo": self.id_torneo,
            "nombre": self.nombre,
            "deporte": self.deporte,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "cantidad_canchas": self.cantidad_canchas,
            "precio_total": self.precio_total,
            "estado": self.estado,
            "id_cliente": self.id_cliente
        }
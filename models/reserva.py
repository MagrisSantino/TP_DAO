"""
Modelo Reserva
Actualizado: Incluye id_torneo para vincular reservas automáticas.
"""
from datetime import datetime

class Reserva:
    def __init__(self, id_reserva=None, id_cliente=0, id_cancha=0, fecha_reserva=None, 
                 hora_inicio=None, hora_fin=None, usa_iluminacion=False, 
                 estado_reserva="pendiente", monto_total=0.0, fecha_creacion=None, 
                 observaciones="", id_torneo=None):
        
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_cancha = id_cancha
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.usa_iluminacion = usa_iluminacion
        self.estado_reserva = estado_reserva
        self.monto_total = monto_total
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.observaciones = observaciones
        self.id_torneo = id_torneo # Nuevo campo

    def calcular_duracion_horas(self):
        if not self.hora_inicio or not self.hora_fin:
            return 0.0
        
        def to_minutes(t):
            if hasattr(t, 'hour'): return t.hour * 60 + t.minute
            try:
                h, m = map(int, str(t).split(':')[:2])
                return h * 60 + m
            except: return 0

        min_inicio = to_minutes(self.hora_inicio)
        min_fin = to_minutes(self.hora_fin)
        
        if min_fin < min_inicio:
            min_fin += 24 * 60
            
        return (min_fin - min_inicio) / 60.0

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "id_cliente": self.id_cliente,
            "id_cancha": self.id_cancha,
            "fecha_reserva": self.fecha_reserva,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "usa_iluminacion": self.usa_iluminacion,
            "estado_reserva": self.estado_reserva,
            "monto_total": self.monto_total,
            "fecha_creacion": self.fecha_creacion,
            "observaciones": self.observaciones,
            "id_torneo": self.id_torneo
        }
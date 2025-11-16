"""Modelo Partido"""
from datetime import date, time, datetime

class Partido:
    """Clase que representa un partido de torneo"""
    
    def __init__(self, id_partido=None, id_torneo=None, id_equipo_local=None,
                 id_equipo_visitante=None, id_reserva=None, fecha_partido=None,
                 hora_inicio=None, resultado_local=None, resultado_visitante=None,
                 estado_partido='programado'):
        self.id_partido = id_partido
        self.id_torneo = id_torneo
        self.id_equipo_local = id_equipo_local
        self.id_equipo_visitante = id_equipo_visitante
        self.id_reserva = id_reserva
        self.fecha_partido = fecha_partido
        self.hora_inicio = hora_inicio
        self.resultado_local = resultado_local
        self.resultado_visitante = resultado_visitante
        self.estado_partido = estado_partido
    
    def fue_jugado(self):
        return self.estado_partido == 'jugado'
    
    def get_resultado(self):
        if self.resultado_local is not None and self.resultado_visitante is not None:
            return f"{self.resultado_local} - {self.resultado_visitante}"
        return "Sin resultado"
    
    def __str__(self):
        return f"Partido #{self.id_partido} - {self.fecha_partido} ({self.estado_partido})"
    
    def to_dict(self):
        return {
            'id_partido': self.id_partido,
            'id_torneo': self.id_torneo,
            'id_equipo_local': self.id_equipo_local,
            'id_equipo_visitante': self.id_equipo_visitante,
            'id_reserva': self.id_reserva,
            'fecha_partido': str(self.fecha_partido) if self.fecha_partido else None,
            'hora_inicio': str(self.hora_inicio) if self.hora_inicio else None,
            'resultado_local': self.resultado_local,
            'resultado_visitante': self.resultado_visitante,
            'estado_partido': self.estado_partido
        }
    
    @staticmethod
    def from_dict(data):
        fecha_partido = data.get('fecha_partido')
        if isinstance(fecha_partido, str):
            fecha_partido = datetime.strptime(fecha_partido, '%Y-%m-%d').date()
        
        hora_inicio = data.get('hora_inicio')
        if isinstance(hora_inicio, str):
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
        
        return Partido(
            id_partido=data.get('id_partido'),
            id_torneo=data.get('id_torneo'),
            id_equipo_local=data.get('id_equipo_local'),
            id_equipo_visitante=data.get('id_equipo_visitante'),
            id_reserva=data.get('id_reserva'),
            fecha_partido=fecha_partido,
            hora_inicio=hora_inicio,
            resultado_local=data.get('resultado_local'),
            resultado_visitante=data.get('resultado_visitante'),
            estado_partido=data.get('estado_partido', 'programado')
        )
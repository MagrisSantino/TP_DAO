"""Modelo Torneo"""
from datetime import date, datetime

class Torneo:
    """Clase que representa un torneo deportivo"""
    
    def __init__(self, id_torneo=None, nombre='', deporte='', fecha_inicio=None,
                 fecha_fin=None, cantidad_equipos=0, estado_torneo='planificado',
                 descripcion=''):
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.deporte = deporte
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cantidad_equipos = cantidad_equipos
        self.estado_torneo = estado_torneo
        self.descripcion = descripcion
    
    def esta_activo(self):
        return self.estado_torneo == 'en_curso'
    
    def __str__(self):
        return f"Torneo: {self.nombre} ({self.deporte}) - {self.estado_torneo}"
    
    def to_dict(self):
        return {
            'id_torneo': self.id_torneo,
            'nombre': self.nombre,
            'deporte': self.deporte,
            'fecha_inicio': str(self.fecha_inicio) if self.fecha_inicio else None,
            'fecha_fin': str(self.fecha_fin) if self.fecha_fin else None,
            'cantidad_equipos': self.cantidad_equipos,
            'estado_torneo': self.estado_torneo,
            'descripcion': self.descripcion
        }
    
    @staticmethod
    def from_dict(data):
        fecha_inicio = data.get('fecha_inicio')
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        
        fecha_fin = data.get('fecha_fin')
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        return Torneo(
            id_torneo=data.get('id_torneo'),
            nombre=data.get('nombre', ''),
            deporte=data.get('deporte', ''),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cantidad_equipos=data.get('cantidad_equipos', 0),
            estado_torneo=data.get('estado_torneo', 'planificado'),
            descripcion=data.get('descripcion', '')
        )
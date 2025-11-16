"""Modelo Equipo"""
from datetime import date, datetime

class Equipo:
    """Clase que representa un equipo inscrito en un torneo"""
    
    def __init__(self, id_equipo=None, id_torneo=None, nombre_equipo='',
                 capitan='', telefono_contacto='', fecha_inscripcion=None):
        self.id_equipo = id_equipo
        self.id_torneo = id_torneo
        self.nombre_equipo = nombre_equipo
        self.capitan = capitan
        self.telefono_contacto = telefono_contacto
        self.fecha_inscripcion = fecha_inscripcion if fecha_inscripcion else date.today()
    
    def __str__(self):
        return f"Equipo: {self.nombre_equipo} (Capitán: {self.capitan})"
    
    def to_dict(self):
        return {
            'id_equipo': self.id_equipo,
            'id_torneo': self.id_torneo,
            'nombre_equipo': self.nombre_equipo,
            'capitan': self.capitan,
            'telefono_contacto': self.telefono_contacto,
            'fecha_inscripcion': str(self.fecha_inscripcion) if self.fecha_inscripcion else None
        }
    
    @staticmethod
    def from_dict(data):
        fecha_inscripcion = data.get('fecha_inscripcion')
        if isinstance(fecha_inscripcion, str):
            fecha_inscripcion = datetime.strptime(fecha_inscripcion, '%Y-%m-%d').date()
        
        return Equipo(
            id_equipo=data.get('id_equipo'),
            id_torneo=data.get('id_torneo'),
            nombre_equipo=data.get('nombre_equipo', ''),
            capitan=data.get('capitan', ''),
            telefono_contacto=data.get('telefono_contacto', ''),
            fecha_inscripcion=fecha_inscripcion
        )
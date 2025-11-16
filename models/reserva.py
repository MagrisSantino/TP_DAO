"""
Modelo Reserva - Representa una reserva de cancha
"""

from datetime import date, time, datetime


class Reserva:
    """
    Clase que representa una reserva de cancha.
    Corresponde a la tabla 'reserva' en la base de datos.
    """
    
    def __init__(self, id_reserva=None, id_cliente=None, id_cancha=None,
                 fecha_reserva=None, hora_inicio=None, hora_fin=None,
                 usa_iluminacion=False, estado_reserva='pendiente',
                 monto_total=0.0, fecha_creacion=None, observaciones=''):
        """
        Constructor de la clase Reserva.
        
        Args:
            id_reserva (int): ID único de la reserva
            id_cliente (int): ID del cliente que realiza la reserva
            id_cancha (int): ID de la cancha reservada
            fecha_reserva (date): Fecha de la reserva
            hora_inicio (time): Hora de inicio
            hora_fin (time): Hora de finalización
            usa_iluminacion (bool): Si se usa iluminación
            estado_reserva (str): Estado de la reserva
            monto_total (float): Monto total a pagar
            fecha_creacion (datetime): Fecha de creación del registro
            observaciones (str): Observaciones adicionales
        """
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_cancha = id_cancha
        self.fecha_reserva = fecha_reserva if fecha_reserva else date.today()
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.usa_iluminacion = bool(usa_iluminacion)
        self.estado_reserva = estado_reserva
        self.monto_total = float(monto_total)
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now()
        self.observaciones = observaciones
    
    def esta_confirmada(self):
        """Verifica si la reserva está confirmada"""
        return self.estado_reserva == 'confirmada'
    
    def esta_cancelada(self):
        """Verifica si la reserva está cancelada"""
        return self.estado_reserva == 'cancelada'
    
    def esta_completada(self):
        """Verifica si la reserva está completada"""
        return self.estado_reserva == 'completada'
    
    def calcular_duracion_horas(self):
        """
        Calcula la duración de la reserva en horas.
        
        Returns:
            float: Duración en horas
        """
        # Validar que existan las horas
        if not self.hora_inicio or not self.hora_fin:
            return 0.0
        
        # Convertir a time si viene como string desde la BD
        hora_inicio = self.hora_inicio
        hora_fin = self.hora_fin
        
        if isinstance(self.hora_inicio, str):
            from utils.helpers import parsear_hora
            hora_inicio = parsear_hora(self.hora_inicio)
            if not hora_inicio:  # Si falla el parseo
                return 0.0
        
        if isinstance(self.hora_fin, str):
            from utils.helpers import parsear_hora
            hora_fin = parsear_hora(self.hora_fin)
            if not hora_fin:  # Si falla el parseo
                return 0.0
        
        # Si después de todo aún son None, retornar 0
        if not hora_inicio or not hora_fin:
            return 0.0
        
        try:
            # Convertir time a datetime para poder restar
            inicio = datetime.combine(date.today(), hora_inicio)
            fin = datetime.combine(date.today(), hora_fin)
            
            duracion = fin - inicio
            return duracion.total_seconds() / 3600  # Convertir segundos a horas
        except (TypeError, ValueError):
            return 0.0
    
    def get_rango_horario(self):
        """Retorna el rango horario como string"""
        if self.hora_inicio and self.hora_fin:
            return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"
        return "Sin horario definido"
    
    def __str__(self):
        """Representación en string de la reserva"""
        return (f"Reserva #{self.id_reserva} - Cliente {self.id_cliente} - "
                f"Cancha {self.id_cancha} - {self.fecha_reserva} ({self.estado_reserva})")
    
    def __repr__(self):
        """Representación para debugging"""
        return (f"Reserva(id={self.id_reserva}, cliente={self.id_cliente}, "
                f"cancha={self.id_cancha}, fecha={self.fecha_reserva})")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_reserva': self.id_reserva,
            'id_cliente': self.id_cliente,
            'id_cancha': self.id_cancha,
            'fecha_reserva': str(self.fecha_reserva) if self.fecha_reserva else None,
            'hora_inicio': str(self.hora_inicio) if self.hora_inicio else None,
            'hora_fin': str(self.hora_fin) if self.hora_fin else None,
            'usa_iluminacion': self.usa_iluminacion,
            'estado_reserva': self.estado_reserva,
            'monto_total': self.monto_total,
            'fecha_creacion': str(self.fecha_creacion) if self.fecha_creacion else None,
            'observaciones': self.observaciones
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea una instancia de Reserva desde un diccionario.
        
        Args:
            data (dict): Diccionario con los datos de la reserva
        
        Returns:
            Reserva: Instancia de Reserva
        """
        # Convertir strings de fecha/hora a objetos date/time si es necesario
        fecha_reserva = data.get('fecha_reserva')
        if isinstance(fecha_reserva, str):
            fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
        
        hora_inicio = data.get('hora_inicio')
        if isinstance(hora_inicio, str):
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
        
        hora_fin = data.get('hora_fin')
        if isinstance(hora_fin, str):
            hora_fin = datetime.strptime(hora_fin, '%H:%M:%S').time()
        
        fecha_creacion = data.get('fecha_creacion')
        if isinstance(fecha_creacion, str):
            fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d %H:%M:%S')
        
        return Reserva(
            id_reserva=data.get('id_reserva'),
            id_cliente=data.get('id_cliente'),
            id_cancha=data.get('id_cancha'),
            fecha_reserva=fecha_reserva,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            usa_iluminacion=bool(data.get('usa_iluminacion', False)),
            estado_reserva=data.get('estado_reserva', 'pendiente'),
            monto_total=data.get('monto_total', 0.0),
            fecha_creacion=fecha_creacion,
            observaciones=data.get('observaciones', '')
        )
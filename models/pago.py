"""
Modelo Pago - Representa un pago asociado a una reserva
"""

from datetime import datetime


class Pago:
    """Clase que representa un pago de una reserva"""
    
    def __init__(self, id_pago=None, id_reserva=None, fecha_pago=None,
                 monto=0.0, metodo_pago='efectivo', estado_pago='pendiente',
                 comprobante=''):
        self.id_pago = id_pago
        self.id_reserva = id_reserva
        self.fecha_pago = fecha_pago if fecha_pago else datetime.now()
        self.monto = float(monto)
        self.metodo_pago = metodo_pago
        self.estado_pago = estado_pago
        self.comprobante = comprobante
    
    def esta_pagado(self):
        return self.estado_pago == 'pagado'
    
    def __str__(self):
        return f"Pago #{self.id_pago} - ${self.monto} ({self.metodo_pago})"
    
    def to_dict(self):
        return {
            'id_pago': self.id_pago,
            'id_reserva': self.id_reserva,
            'fecha_pago': str(self.fecha_pago) if self.fecha_pago else None,
            'monto': self.monto,
            'metodo_pago': self.metodo_pago,
            'estado_pago': self.estado_pago,
            'comprobante': self.comprobante
        }
    
    @staticmethod
    def from_dict(data):
        fecha_pago = data.get('fecha_pago')
        if isinstance(fecha_pago, str):
            fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d %H:%M:%S')
        
        return Pago(
            id_pago=data.get('id_pago'),
            id_reserva=data.get('id_reserva'),
            fecha_pago=fecha_pago,
            monto=data.get('monto', 0.0),
            metodo_pago=data.get('metodo_pago', 'efectivo'),
            estado_pago=data.get('estado_pago', 'pendiente'),
            comprobante=data.get('comprobante', '')
        )
"""
Modelo Pago
Actualizado: Soporta id_torneo y hace opcional id_reserva.
"""
from datetime import date

class Pago:
    def __init__(self, id_pago=None, id_reserva=None, id_torneo=None, 
                 monto=0.0, fecha_pago=None, metodo_pago="efectivo"):
        
        self.id_pago = id_pago
        self.id_reserva = id_reserva
        self.id_torneo = id_torneo # Nuevo campo para vincular torneos
        self.monto = monto
        self.fecha_pago = fecha_pago or date.today()
        self.metodo_pago = metodo_pago

    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "id_reserva": self.id_reserva,
            "id_torneo": self.id_torneo,
            "monto": self.monto,
            "fecha_pago": self.fecha_pago,
            "metodo_pago": self.metodo_pago
        }
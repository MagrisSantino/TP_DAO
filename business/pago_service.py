from typing import List, Tuple, Optional
from datetime import date
from models.pago import Pago
from dao.pago_dao import PagoDAO
from dao.reserva_dao import ReservaDAO
from dao.torneo_dao import TorneoDAO # Importar DAO Torneo

class PagoService:
    
    @staticmethod
    def registrar_pago(id_reserva: int, monto: float, metodo_pago: str) -> Tuple[bool, str, Optional[Pago]]:
        # (Lógica existente para reservas, sin cambios)
        try:
            reserva = ReservaDAO.obtener_por_id(id_reserva)
            if not reserva: return False, "Reserva inexistente", None
            
            pagado_actual = PagoService.obtener_monto_pagado(id_reserva)
            pendiente = reserva.monto_total - pagado_actual
            
            if monto > (pendiente + 0.1): return False, "Monto excede deuda", None
            
            nuevo_pago = Pago(id_reserva=id_reserva, monto=monto, metodo_pago=metodo_pago)
            id_pago = PagoDAO.insertar(nuevo_pago)
            
            if id_pago:
                if (pagado_actual + monto) >= (reserva.monto_total - 0.1):
                    ReservaDAO.cambiar_estado(id_reserva, 'confirmada')
                return True, "Pago registrado", nuevo_pago
            return False, "Error BD", None
        except Exception as e:
            return False, str(e), None

    @staticmethod
    def registrar_pago_torneo(id_torneo: int, monto: float, metodo_pago: str) -> Tuple[bool, str, Optional[Pago]]:
        """Registra el pago de un torneo completo."""
        try:
            torneo = TorneoDAO.obtener_por_id(id_torneo)
            if not torneo: return False, "Torneo inexistente", None
            
            # Validar montos (si quisieras pagos parciales de torneo, aquí va la lógica)
            # Asumimos pago total o parcial igual que reservas
            pagado_actual = PagoService.obtener_monto_pagado_torneo(id_torneo)
            pendiente = torneo.precio_total - pagado_actual
            
            if monto > (pendiente + 0.1): return False, f"Excede deuda. Restan: {pendiente}", None
            
            nuevo_pago = Pago(id_torneo=id_torneo, monto=monto, metodo_pago=metodo_pago)
            id_pago = PagoDAO.insertar(nuevo_pago) # Inserta con id_reserva NULL
            
            if id_pago:
                return True, "Pago de torneo registrado", nuevo_pago
            return False, "Error BD", None
            
        except Exception as e:
            return False, str(e), None

    @staticmethod
    def obtener_monto_pagado(id_reserva: int) -> float:
        pagos = PagoDAO.obtener_por_reserva(id_reserva)
        return sum(p.monto for p in pagos)

    @staticmethod
    def obtener_monto_pagado_torneo(id_torneo: int) -> float:
        pagos = PagoDAO.obtener_por_torneo(id_torneo)
        return sum(p.monto for p in pagos)

    @staticmethod
    def obtener_todos() -> List[Pago]:
        return PagoDAO.obtener_todos()
"""
Servicio de Pagos - Lógica de Negocio
"""

from typing import Tuple, Optional, List
from datetime import datetime
from models.pago import Pago
from models.reserva import Reserva
from dao.pago_dao import PagoDAO
from dao.reserva_dao import ReservaDAO


class PagoService:
    """Servicio para gestión de pagos con validaciones"""
    
    @staticmethod
    def registrar_pago(id_reserva: int, monto: float, metodo_pago: str,
                      comprobante: str = "") -> Tuple[bool, str, Optional[Pago]]:
        """
        Registra un nuevo pago para una reserva.
        
        Args:
            id_reserva: ID de la reserva
            monto: Monto del pago
            metodo_pago: Método de pago
            comprobante: Número de comprobante
        
        Returns:
            Tuple (éxito, mensaje, pago)
        """
        # Validar que la reserva existe
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada", None
        
        # Validar que la reserva no esté cancelada
        if reserva.estado_reserva == 'cancelada':
            return False, "No se puede pagar una reserva cancelada", None
        
        # Validar monto
        if monto <= 0:
            return False, "El monto debe ser mayor a 0", None
        
        # Validar que no se exceda el total de la reserva
        total_pagado = PagoDAO.calcular_total_pagado_reserva(id_reserva)
        if total_pagado + monto > reserva.monto_total:
            return False, f"El pago excede el total de la reserva. Restante: ${reserva.monto_total - total_pagado:.2f}", None
        
        # Validar método de pago
        metodos_validos = ['efectivo', 'transferencia', 'tarjeta_debito', 'tarjeta_credito']
        if metodo_pago not in metodos_validos:
            return False, "Método de pago inválido", None
        
        # Crear pago
        pago = Pago(
            id_reserva=id_reserva,
            fecha_pago=datetime.now(),
            monto=monto,
            metodo_pago=metodo_pago,
            estado_pago='pagado',
            comprobante=comprobante.strip()
        )
        
        # Guardar en BD
        id_pago = PagoDAO.insertar(pago)
        if id_pago:
            # Verificar si la reserva está completamente pagada
            nuevo_total = total_pagado + monto
            if nuevo_total >= reserva.monto_total:
                # Confirmar la reserva automáticamente si está pagada
                if reserva.estado_reserva == 'pendiente':
                    ReservaDAO.cambiar_estado(id_reserva, 'confirmada')
            
            return True, "Pago registrado exitosamente", pago
        else:
            return False, "Error al registrar el pago", None
    
    @staticmethod
    def verificar_pago_completo(id_reserva: int) -> Tuple[bool, float, float]:
        """
        Verifica si una reserva está completamente pagada.
        
        Args:
            id_reserva: ID de la reserva
        
        Returns:
            Tuple (está_pagada, total_reserva, total_pagado)
        """
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, 0.0, 0.0
        
        total_pagado = PagoDAO.calcular_total_pagado_reserva(id_reserva)
        esta_pagada = total_pagado >= reserva.monto_total
        
        return esta_pagada, reserva.monto_total, total_pagado
    
    @staticmethod
    def obtener_saldo_pendiente(id_reserva: int) -> float:
        """
        Obtiene el saldo pendiente de una reserva.
        
        Args:
            id_reserva: ID de la reserva
        
        Returns:
            float: Saldo pendiente
        """
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return 0.0
        
        total_pagado = PagoDAO.calcular_total_pagado_reserva(id_reserva)
        saldo = reserva.monto_total - total_pagado
        
        return max(0.0, saldo)  # No devolver valores negativos
    
    @staticmethod
    def obtener_pagos_reserva(id_reserva: int) -> List[Pago]:
        """Obtiene todos los pagos de una reserva."""
        return PagoDAO.obtener_por_reserva(id_reserva)
    
    @staticmethod
    def obtener_pago(id_pago: int) -> Optional[Pago]:
        """Obtiene un pago por ID."""
        return PagoDAO.obtener_por_id(id_pago)
    
    @staticmethod
    def obtener_todos_pagos() -> List[Pago]:
        """Obtiene todos los pagos."""
        return PagoDAO.obtener_todos()
    
    @staticmethod
    def anular_pago(id_pago: int) -> Tuple[bool, str]:
        """
        Anula un pago (cambia su estado a reembolsado).
        
        Args:
            id_pago: ID del pago
        
        Returns:
            Tuple (éxito, mensaje)
        """
        pago = PagoDAO.obtener_por_id(id_pago)
        if not pago:
            return False, "Pago no encontrado"
        
        if pago.estado_pago != 'pagado':
            return False, f"El pago ya está en estado: {pago.estado_pago}"
        
        pago.estado_pago = 'reembolsado'
        if PagoDAO.actualizar(pago):
            return True, "Pago anulado exitosamente"
        return False, "Error al anular el pago"
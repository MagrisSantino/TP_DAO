"""
Servicio de Reserva
Lógica de negocio para gestión de reservas.
ACTUALIZADO: Regla de 24hs (Pago inmediato para reservas próximas y cancelación automática).
"""
from datetime import datetime, timedelta, date, time
from typing import Tuple, Optional, List
from models.reserva import Reserva
from dao.reserva_dao import ReservaDAO
from dao.cancha_dao import CanchaDAO
from dao.cliente_dao import ClienteDAO
from config import RECARGO_ILUMINACION

class ReservaService:
    
    @staticmethod
    def crear_reserva(id_cliente, id_cancha, fecha_reserva, hora_inicio, hora_fin, usa_iluminacion, observaciones) -> Tuple[bool, str, Optional[Reserva]]:
        # 1. Validaciones básicas
        if not all([id_cliente, id_cancha, fecha_reserva, hora_inicio, hora_fin]):
            return False, "Faltan datos obligatorios", None
            
        if hora_inicio >= hora_fin:
            return False, "La hora de inicio debe ser anterior a la de fin", None
            
        if fecha_reserva < date.today():
            return False, "No se puede reservar en fechas pasadas", None

        # 2. Validar Cliente
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return False, "Cliente no encontrado", None

        # 3. Validar Cancha
        cancha = CanchaDAO.obtener_por_id(id_cancha)
        if not cancha:
            return False, "Cancha no encontrada", None
            
        if cancha.estado != 'disponible' and cancha.estado != 'activa':
            return False, f"La cancha no está disponible (Estado: {cancha.estado})", None

        # 4. Validar Disponibilidad (DAO)
        if not ReservaDAO.verificar_disponibilidad(id_cancha, fecha_reserva, hora_inicio, hora_fin):
            return False, "La cancha ya está reservada en ese horario", None

        # 5. Calcular Duración
        inicio_dt = datetime.combine(fecha_reserva, hora_inicio)
        fin_dt = datetime.combine(fecha_reserva, hora_fin)
        duracion_horas = (fin_dt - inicio_dt).total_seconds() / 3600

        # 6. Calcular Precio (Lógica Actualizada Día/Noche)
        hora_corte_noche = 19 
        
        if hora_inicio.hour >= hora_corte_noche:
            precio_base = cancha.precio_hora_noche
        else:
            precio_base = cancha.precio_hora_dia
            
        if precio_base == 0 and hasattr(cancha, 'precio_hora') and cancha.precio_hora > 0:
            precio_base = cancha.precio_hora

        monto_total = precio_base * duracion_horas

        if usa_iluminacion:
            recargo = 1000.0 * duracion_horas 
            monto_total += recargo

        # 7. Crear objeto
        nueva_reserva = Reserva(
            id_cliente=id_cliente,
            id_cancha=id_cancha,
            fecha_reserva=fecha_reserva,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            usa_iluminacion=usa_iluminacion,
            estado_reserva='pendiente',
            monto_total=monto_total,
            observaciones=observaciones
        )

        # 8. Guardar
        id_gen = ReservaDAO.insertar(nueva_reserva)
        if id_gen:
            nueva_reserva.id_reserva = id_gen
            return True, "Reserva creada exitosamente", nueva_reserva
        
        return False, "Error al guardar en base de datos", None

    @staticmethod
    def confirmar_reserva(id_reserva: int) -> Tuple[bool, str]:
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
            
        if reserva.estado_reserva == 'confirmada':
            return False, "La reserva ya está confirmada"
            
        if ReservaDAO.cambiar_estado(id_reserva, 'confirmada'):
            return True, "Reserva confirmada correctamente"
        return False, "Error al confirmar reserva"

    @staticmethod
    def cancelar_reserva(id_reserva: int) -> Tuple[bool, str]:
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
            
        if ReservaDAO.cambiar_estado(id_reserva, 'cancelada'):
            return True, "Reserva cancelada correctamente"
        return False, "Error al cancelar reserva"
        
    @staticmethod
    def eliminar_fisicamente(id_reserva: int) -> bool:
        """Elimina el registro de la BD (usado para rollbacks de reservas urgentes no pagadas)"""
        return ReservaDAO.eliminar(id_reserva)

    # --- NUEVA FUNCIONALIDAD: REGLA DE 24 HORAS ---

    @staticmethod
    def es_reserva_urgente(fecha_reserva: date, hora_inicio: time) -> bool:
        """
        Verifica si faltan menos de 24 horas para el inicio de la reserva.
        """
        ahora = datetime.now()
        inicio_reserva = datetime.combine(fecha_reserva, hora_inicio)
        diferencia = inicio_reserva - ahora
        
        # Si la diferencia es menor a 24 horas (o ya pasó), es urgente
        return diferencia < timedelta(hours=24)

    @staticmethod
    def cancelar_pendientes_vencidas() -> int:
        """
        Busca reservas 'pendientes' que inicien en menos de 24 horas
        y las cancela automáticamente.
        Retorna la cantidad de reservas canceladas.
        """
        reservas = ReservaDAO.obtener_por_estado('pendiente')
        canceladas = 0
        ahora = datetime.now()
        limite_urgencia = timedelta(hours=24)

        for r in reservas:
            # Construir fecha/hora inicio
            inicio_reserva = datetime.combine(r.fecha_reserva, r.hora_inicio)
            tiempo_restante = inicio_reserva - ahora
            
            # Si falta menos de 24hs (o ya pasó) y sigue pendiente, se cancela
            if tiempo_restante < limite_urgencia:
                r.estado_reserva = 'cancelada'
                r.observaciones = (r.observaciones or "") + " [Cancelada por sistema: Falta de pago 24hs antes]"
                ReservaDAO.actualizar(r)
                canceladas += 1
        
        return canceladas
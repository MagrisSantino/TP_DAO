"""
Servicio de Reserva
Lógica de negocio para gestión de reservas.
"""
from datetime import datetime, timedelta, date, time
from typing import Tuple, Optional
from models.reserva import Reserva
from dao.reserva_dao import ReservaDAO
from dao.cancha_dao import CanchaDAO
from dao.cliente_dao import ClienteDAO
from config import RECARGO_ILUMINACION # Asegúrate de que esto exista en config.py, si no, usa valor fijo

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
        # Asumimos horario noche a partir de las 19:00
        hora_corte_noche = 19 
        
        # Determinar precio base según horario de inicio
        if hora_inicio.hour >= hora_corte_noche:
            precio_base = cancha.precio_hora_noche
        else:
            precio_base = cancha.precio_hora_dia
            
        # Si por alguna razón los precios son 0 (datos viejos), intentar usar propiedad compatibilidad
        if precio_base == 0 and hasattr(cancha, 'precio_hora') and cancha.precio_hora > 0:
            precio_base = cancha.precio_hora

        monto_total = precio_base * duracion_horas

        # Recargo iluminación
        if usa_iluminacion:
            # Usar constante o valor fijo
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
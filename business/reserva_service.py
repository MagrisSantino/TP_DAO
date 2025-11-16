"""
Servicio de Reservas - Lógica de Negocio
Incluye validaciones y cálculo de costos
"""

from datetime import date, time, datetime, timedelta
from typing import Optional, List, Tuple
from models.reserva import Reserva
from models.cliente import Cliente
from models.cancha import Cancha
from dao.reserva_dao import ReservaDAO
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO
from config import HORA_APERTURA, HORA_CIERRE, RECARGO_ILUMINACION


class ReservaService:
    """Servicio para gestión de reservas con validaciones de negocio"""
    
    @staticmethod
    def crear_reserva(id_cliente: int, id_cancha: int, fecha_reserva: date,
                     hora_inicio: time, hora_fin: time, usa_iluminacion: bool = False,
                     observaciones: str = "") -> Tuple[bool, str, Optional[Reserva]]:
        """
        Crea una nueva reserva con todas las validaciones.
        
        Args:
            id_cliente: ID del cliente
            id_cancha: ID de la cancha
            fecha_reserva: Fecha de la reserva
            hora_inicio: Hora de inicio
            hora_fin: Hora de finalización
            usa_iluminacion: Si usa iluminación
            observaciones: Observaciones adicionales
        
        Returns:
            Tuple (éxito, mensaje, reserva)
        """
        # 1. Validar que el cliente existe y está activo
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return False, "Cliente no encontrado", None
        if not cliente.esta_activo():
            return False, "Cliente inactivo", None
        
        # 2. Validar que la cancha existe y está disponible
        cancha = CanchaDAO.obtener_por_id(id_cancha)
        if not cancha:
            return False, "Cancha no encontrada", None
        if not cancha.esta_disponible():
            return False, f"Cancha en estado: {cancha.estado}", None
        
        # 3. Validar fecha (no puede ser pasada)
        if fecha_reserva < date.today():
            return False, "No se pueden hacer reservas en fechas pasadas", None
        
        # 4. Validar horarios
        es_valido, msg_horario = ReservaService._validar_horarios(hora_inicio, hora_fin)
        if not es_valido:
            return False, msg_horario, None
        
        # 5. Validar iluminación
        if usa_iluminacion and not cancha.tiene_iluminacion():
            return False, "Esta cancha no tiene iluminación", None
        
        # 6. Verificar disponibilidad (no solapamiento)
        if not ReservaDAO.verificar_disponibilidad(id_cancha, fecha_reserva, 
                                                     hora_inicio, hora_fin):
            return False, "La cancha no está disponible en ese horario", None
        
        # 7. Calcular monto total
        monto_total = ReservaService.calcular_monto_reserva(
            cancha, hora_inicio, hora_fin, usa_iluminacion
        )
        
        # 8. Crear la reserva
        reserva = Reserva(
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
        
        # 9. Guardar en base de datos
        id_reserva = ReservaDAO.insertar(reserva)
        if id_reserva:
            return True, "Reserva creada exitosamente", reserva
        else:
            return False, "Error al guardar la reserva", None
    
    @staticmethod
    def calcular_monto_reserva(cancha: Cancha, hora_inicio: time, 
                               hora_fin: time, usa_iluminacion: bool) -> float:
        """
        Calcula el monto total de una reserva.
        
        Args:
            cancha: Objeto cancha
            hora_inicio: Hora de inicio
            hora_fin: Hora de finalización
            usa_iluminacion: Si usa iluminación
        
        Returns:
            float: Monto total a pagar
        """
        # Calcular duración en horas
        inicio_dt = datetime.combine(date.today(), hora_inicio)
        fin_dt = datetime.combine(date.today(), hora_fin)
        duracion_horas = (fin_dt - inicio_dt).total_seconds() / 3600
        
        # Determinar si es horario nocturno (después de las 18:00)
        es_nocturno = hora_inicio >= time(18, 0)
        
        # Calcular precio base
        precio_por_hora = cancha.get_precio_por_hora(es_nocturno)
        monto_base = precio_por_hora * duracion_horas
        
        # Agregar recargo por iluminación si aplica
        if usa_iluminacion:
            monto_base += (RECARGO_ILUMINACION * duracion_horas)
        
        return round(monto_base, 2)
    
    @staticmethod
    def modificar_reserva(id_reserva: int, id_cancha: int = None, 
                         fecha_reserva: date = None, hora_inicio: time = None,
                         hora_fin: time = None, usa_iluminacion: bool = None,
                         observaciones: str = None) -> Tuple[bool, str]:
        """
        Modifica una reserva existente.
        Solo permite modificar reservas en estado 'pendiente'.
        
        Returns:
            Tuple (éxito, mensaje)
        """
        # Obtener la reserva actual
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
        
        if reserva.estado_reserva not in ['pendiente', 'confirmada']:
            return False, f"No se puede modificar una reserva en estado: {reserva.estado_reserva}"
        
        # Actualizar solo los campos que se proporcionan
        if id_cancha is not None:
            cancha = CanchaDAO.obtener_por_id(id_cancha)
            if not cancha or not cancha.esta_disponible():
                return False, "Cancha no disponible"
            reserva.id_cancha = id_cancha
        
        if fecha_reserva is not None:
            if fecha_reserva < date.today():
                return False, "Fecha inválida"
            reserva.fecha_reserva = fecha_reserva
        
        if hora_inicio is not None:
            reserva.hora_inicio = hora_inicio
        
        if hora_fin is not None:
            reserva.hora_fin = hora_fin
        
        if usa_iluminacion is not None:
            reserva.usa_iluminacion = usa_iluminacion
        
        if observaciones is not None:
            reserva.observaciones = observaciones
        
        # Validar horarios
        es_valido, msg = ReservaService._validar_horarios(reserva.hora_inicio, reserva.hora_fin)
        if not es_valido:
            return False, msg
        
        # Verificar disponibilidad (excluyendo esta reserva)
        if not ReservaDAO.verificar_disponibilidad(
            reserva.id_cancha, reserva.fecha_reserva, 
            reserva.hora_inicio, reserva.hora_fin, id_reserva
        ):
            return False, "Conflicto de horario con otra reserva"
        
        # Recalcular monto
        cancha = CanchaDAO.obtener_por_id(reserva.id_cancha)
        reserva.monto_total = ReservaService.calcular_monto_reserva(
            cancha, reserva.hora_inicio, reserva.hora_fin, reserva.usa_iluminacion
        )
        
        # Actualizar en BD
        if ReservaDAO.actualizar(reserva):
            return True, "Reserva modificada exitosamente"
        return False, "Error al actualizar la reserva"
    
    @staticmethod
    def confirmar_reserva(id_reserva: int) -> Tuple[bool, str]:
        """Cambia el estado de una reserva a 'confirmada'."""
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
        
        if reserva.estado_reserva != 'pendiente':
            return False, f"La reserva ya está en estado: {reserva.estado_reserva}"
        
        if ReservaDAO.cambiar_estado(id_reserva, 'confirmada'):
            return True, "Reserva confirmada"
        return False, "Error al confirmar la reserva"
    
    @staticmethod
    def cancelar_reserva(id_reserva: int) -> Tuple[bool, str]:
        """Cancela una reserva."""
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
        
        if reserva.estado_reserva in ['cancelada', 'completada']:
            return False, f"No se puede cancelar una reserva en estado: {reserva.estado_reserva}"
        
        if ReservaDAO.cambiar_estado(id_reserva, 'cancelada'):
            return True, "Reserva cancelada"
        return False, "Error al cancelar la reserva"
    
    @staticmethod
    def completar_reserva(id_reserva: int) -> Tuple[bool, str]:
        """Marca una reserva como completada."""
        reserva = ReservaDAO.obtener_por_id(id_reserva)
        if not reserva:
            return False, "Reserva no encontrada"
        
        if reserva.estado_reserva != 'confirmada':
            return False, "Solo se pueden completar reservas confirmadas"
        
        if ReservaDAO.cambiar_estado(id_reserva, 'completada'):
            return True, "Reserva completada"
        return False, "Error al completar la reserva"
    
    @staticmethod
    def obtener_reservas_cliente(id_cliente: int) -> List[Reserva]:
        """Obtiene todas las reservas de un cliente."""
        return ReservaDAO.obtener_por_cliente(id_cliente)
    
    @staticmethod
    def obtener_reservas_cancha(id_cancha: int, fecha_desde: date = None, 
                                fecha_hasta: date = None) -> List[Reserva]:
        """Obtiene reservas de una cancha, opcionalmente filtradas por fecha."""
        if fecha_desde and fecha_hasta:
            reservas = ReservaDAO.obtener_por_rango_fechas(fecha_desde, fecha_hasta)
            return [r for r in reservas if r.id_cancha == id_cancha]
        return ReservaDAO.obtener_por_cancha(id_cancha)
    
    @staticmethod
    def obtener_horarios_disponibles(id_cancha: int, fecha: date) -> List[Tuple[time, time]]:
        """
        Obtiene los horarios disponibles de una cancha en una fecha.
        
        Returns:
            Lista de tuplas (hora_inicio, hora_fin) disponibles
        """
        # Obtener todas las reservas de la cancha en esa fecha
        reservas = ReservaDAO.obtener_por_fecha(fecha)
        reservas_cancha = [r for r in reservas if r.id_cancha == id_cancha 
                          and r.estado_reserva != 'cancelada']
        
        # Horarios ocupados
        horarios_ocupados = [(r.hora_inicio, r.hora_fin) for r in reservas_cancha]
        
        # Generar horarios disponibles (bloques de 1 hora)
        hora_apertura = datetime.strptime(HORA_APERTURA, "%H:%M").time()
        hora_cierre = datetime.strptime(HORA_CIERRE, "%H:%M").time()
        
        horarios_disponibles = []
        hora_actual = hora_apertura
        
        while hora_actual < hora_cierre:
            # Calcular hora fin (1 hora después)
            hora_fin_dt = datetime.combine(date.today(), hora_actual) + timedelta(hours=1)
            hora_fin = hora_fin_dt.time()
            
            if hora_fin <= hora_cierre:
                # Verificar si este horario está disponible
                disponible = True
                for inicio_ocupado, fin_ocupado in horarios_ocupados:
                    if not (hora_fin <= inicio_ocupado or hora_actual >= fin_ocupado):
                        disponible = False
                        break
                
                if disponible:
                    horarios_disponibles.append((hora_actual, hora_fin))
            
            # Avanzar 1 hora
            hora_actual = hora_fin
        
        return horarios_disponibles
    
    @staticmethod
    def _validar_horarios(hora_inicio: time, hora_fin: time) -> Tuple[bool, str]:
        """
        Valida que los horarios sean correctos.
        
        Returns:
            Tuple (es_valido, mensaje)
        """
        # Validar que hora_fin > hora_inicio
        if hora_inicio >= hora_fin:
            return False, "La hora de fin debe ser posterior a la hora de inicio"
        
        # Validar que estén dentro del horario de funcionamiento
        hora_apertura = datetime.strptime(HORA_APERTURA, "%H:%M").time()
        hora_cierre = datetime.strptime(HORA_CIERRE, "%H:%M").time()
        
        if hora_inicio < hora_apertura:
            return False, f"El horario de inicio debe ser después de las {HORA_APERTURA}"
        
        if hora_fin > hora_cierre:
            return False, f"El horario de fin debe ser antes de las {HORA_CIERRE}"
        
        # Validar duración mínima (30 minutos) y máxima (4 horas)
        duracion = (datetime.combine(date.today(), hora_fin) - 
                   datetime.combine(date.today(), hora_inicio)).total_seconds() / 3600
        
        if duracion < 0.5:
            return False, "La duración mínima es de 30 minutos"
        
        if duracion > 4:
            return False, "La duración máxima es de 4 horas"
        
        return True, "Horarios válidos"
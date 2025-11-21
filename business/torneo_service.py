from typing import List, Tuple, Optional
from datetime import date, time
from models.torneo import Torneo
from models.reserva import Reserva
from dao.torneo_dao import TorneoDAO
from dao.cancha_dao import CanchaDAO
from dao.reserva_dao import ReservaDAO

class TorneoService:
    
    @staticmethod
    def crear_torneo(id_cliente, nombre, deporte, fecha, hora_inicio, hora_fin, cantidad_canchas, precio_total) -> Tuple[bool, str, Optional[Torneo]]:
        # Validaciones
        if not nombre: return False, "Nombre obligatorio", None
        if cantidad_canchas < 1: return False, "Mínimo 1 cancha", None
        if fecha < date.today(): return False, "Fecha inválida", None
        if hora_inicio >= hora_fin: return False, "Horario inválido", None
        if not id_cliente: return False, "Debe seleccionar un organizador", None

        # 1. Buscar canchas del deporte solicitado
        todas_canchas = CanchaDAO.obtener_disponibles()
        canchas_deporte = [c for c in todas_canchas if c.tipo_deporte == deporte]
        
        if len(canchas_deporte) < cantidad_canchas:
            return False, f"Solo hay {len(canchas_deporte)} canchas de {deporte} disponibles.", None

        # 2. Verificar disponibilidad
        canchas_libres = []
        for c in canchas_deporte:
            if ReservaDAO.verificar_disponibilidad(c.id_cancha, fecha, hora_inicio, hora_fin):
                canchas_libres.append(c)
        
        if len(canchas_libres) < cantidad_canchas:
            return False, f"No hay suficientes canchas libres en ese horario. Disponibles: {len(canchas_libres)}", None

        # 3. Crear Torneo
        nuevo_torneo = Torneo(
            nombre=nombre,
            deporte=deporte,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            cantidad_canchas=cantidad_canchas,
            precio_total=precio_total,
            estado="confirmado",
            id_cliente=id_cliente
        )
        
        id_torneo = TorneoDAO.insertar(nuevo_torneo)
        if not id_torneo:
            return False, "Error al guardar torneo", None
            
        nuevo_torneo.id_torneo = id_torneo

        # 4. Generar Reservas Masivas (Confirmadas y Costo 0)
        canchas_a_reservar = canchas_libres[:cantidad_canchas]
        
        for c in canchas_a_reservar:
            reserva = Reserva(
                id_cliente=id_cliente,
                id_cancha=c.id_cancha,
                fecha_reserva=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                usa_iluminacion=False,
                estado_reserva="confirmada", # Se confirman al crear el torneo
                monto_total=0.0,             # Precio incluido en el torneo
                observaciones=f"Bloqueada por Torneo: {nombre}",
                id_torneo=id_torneo
            )
            ReservaDAO.insertar(reserva)

        return True, "Torneo creado exitosamente. Proceda al pago.", nuevo_torneo

    @staticmethod
    def obtener_todos() -> List[Torneo]:
        return TorneoDAO.obtener_todos()

    @staticmethod
    def eliminar_torneo(id_torneo: int) -> Tuple[bool, str]:
        if TorneoDAO.eliminar(id_torneo):
            reservas = ReservaDAO.obtener_todas()
            for r in reservas:
                if r.id_torneo == id_torneo:
                    ReservaDAO.cambiar_estado(r.id_reserva, 'cancelada')
            return True, "Torneo cancelado y canchas liberadas."
        return False, "Error al eliminar torneo"
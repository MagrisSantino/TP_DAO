"""
Servicio de Cancha
Actualizado para soportar CRUD con nuevos campos.
"""
from typing import List, Tuple, Optional
from models.cancha import Cancha
from dao.cancha_dao import CanchaDAO

class CanchaService:
    
    @staticmethod
    def crear_cancha(nombre, tipo_deporte, tipo_superficie, techada, iluminacion, 
                     capacidad_jugadores, precio_hora_dia, precio_hora_noche) -> Tuple[bool, str, Optional[Cancha]]:
        
        if not nombre:
            return False, "El nombre es obligatorio", None
        if precio_hora_dia < 0 or precio_hora_noche < 0:
            return False, "El precio no puede ser negativo", None
            
        nueva = Cancha(
            nombre=nombre, 
            tipo_deporte=tipo_deporte, 
            tipo_superficie=tipo_superficie,
            techada=techada, 
            iluminacion=iluminacion,
            capacidad_jugadores=capacidad_jugadores,
            precio_hora_dia=precio_hora_dia,
            precio_hora_noche=precio_hora_noche,
            estado='disponible'
        )
        
        id_gen = CanchaDAO.insertar(nueva)
        
        if id_gen:
            nueva.id_cancha = id_gen
            return True, "Cancha creada correctamente", nueva
        return False, "Error al guardar cancha en base de datos", None

    @staticmethod
    def obtener_todas() -> List[Cancha]:
        return CanchaDAO.obtener_todos()

    @staticmethod
    def obtener_canchas_disponibles() -> List[Cancha]:
        return CanchaDAO.obtener_disponibles()

    @staticmethod
    def obtener_cancha(id_cancha: int) -> Optional[Cancha]:
        return CanchaDAO.obtener_por_id(id_cancha)

    @staticmethod
    def actualizar_cancha(id_cancha, nombre, tipo_deporte, tipo_superficie, techada, 
                          iluminacion, capacidad_jugadores, precio_hora_dia, 
                          precio_hora_noche, estado) -> Tuple[bool, str]:
        
        cancha = Cancha(
            id_cancha=id_cancha, 
            nombre=nombre, 
            tipo_deporte=tipo_deporte, 
            tipo_superficie=tipo_superficie,
            techada=techada, 
            iluminacion=iluminacion,
            capacidad_jugadores=capacidad_jugadores,
            precio_hora_dia=precio_hora_dia,
            precio_hora_noche=precio_hora_noche,
            estado=estado
        )
        
        if CanchaDAO.actualizar(cancha):
            return True, "Cancha actualizada correctamente"
        return False, "Error al actualizar cancha"

    @staticmethod
    def eliminar_cancha(id_cancha: int) -> Tuple[bool, str]:
        if CanchaDAO.eliminar(id_cancha):
            return True, "Cancha eliminada (estado inactivo)."
        return False, "No se pudo eliminar la cancha."
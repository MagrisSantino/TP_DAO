"""
Servicio de Canchas - Lógica de Negocio
"""

from typing import Tuple, Optional, List
from models.cancha import Cancha
from dao.cancha_dao import CanchaDAO


class CanchaService:
    """Servicio para gestión de canchas con validaciones"""
    
    @staticmethod
    def crear_cancha(nombre: str, tipo_deporte: str, tipo_superficie: str,
                    techada: bool, iluminacion: bool, capacidad_jugadores: int,
                    precio_hora_dia: float, precio_hora_noche: float) -> Tuple[bool, str, Optional[Cancha]]:
        """
        Crea una nueva cancha con validaciones.
        
        Returns:
            Tuple (éxito, mensaje, cancha)
        """
        # Validar nombre
        if not nombre or len(nombre.strip()) < 3:
            return False, "El nombre debe tener al menos 3 caracteres", None
        
        # Validar tipo de deporte
        if not tipo_deporte or len(tipo_deporte.strip()) < 3:
            return False, "Tipo de deporte inválido", None
        
        # Validar capacidad
        if capacidad_jugadores < 2:
            return False, "La capacidad debe ser al menos 2 jugadores", None
        
        # Validar precios
        if precio_hora_dia <= 0:
            return False, "El precio hora día debe ser mayor a 0", None
        
        if precio_hora_noche <= 0:
            return False, "El precio hora noche debe ser mayor a 0", None
        
        # Crear cancha
        cancha = Cancha(
            nombre=nombre.strip().title(),
            tipo_deporte=tipo_deporte.strip(),
            tipo_superficie=tipo_superficie.strip(),
            techada=techada,
            iluminacion=iluminacion,
            capacidad_jugadores=capacidad_jugadores,
            precio_hora_dia=precio_hora_dia,
            precio_hora_noche=precio_hora_noche,
            estado='disponible'
        )
        
        # Guardar en BD
        id_cancha = CanchaDAO.insertar(cancha)
        if id_cancha:
            return True, "Cancha creada exitosamente", cancha
        else:
            return False, "Error al guardar la cancha", None
    
    @staticmethod
    def modificar_cancha(id_cancha: int, nombre: str = None, tipo_deporte: str = None,
                        tipo_superficie: str = None, techada: bool = None,
                        iluminacion: bool = None, capacidad_jugadores: int = None,
                        precio_hora_dia: float = None, precio_hora_noche: float = None,
                        estado: str = None) -> Tuple[bool, str]:
        """
        Modifica una cancha existente.
        
        Returns:
            Tuple (éxito, mensaje)
        """
        # Obtener cancha actual
        cancha = CanchaDAO.obtener_por_id(id_cancha)
        if not cancha:
            return False, "Cancha no encontrada"
        
        # Actualizar solo los campos proporcionados
        if nombre is not None:
            if len(nombre.strip()) < 3:
                return False, "El nombre debe tener al menos 3 caracteres"
            cancha.nombre = nombre.strip().title()
        
        if tipo_deporte is not None:
            cancha.tipo_deporte = tipo_deporte.strip()
        
        if tipo_superficie is not None:
            cancha.tipo_superficie = tipo_superficie.strip()
        
        if techada is not None:
            cancha.techada = techada
        
        if iluminacion is not None:
            cancha.iluminacion = iluminacion
        
        if capacidad_jugadores is not None:
            if capacidad_jugadores < 2:
                return False, "La capacidad debe ser al menos 2 jugadores"
            cancha.capacidad_jugadores = capacidad_jugadores
        
        if precio_hora_dia is not None:
            if precio_hora_dia <= 0:
                return False, "El precio hora día debe ser mayor a 0"
            cancha.precio_hora_dia = precio_hora_dia
        
        if precio_hora_noche is not None:
            if precio_hora_noche <= 0:
                return False, "El precio hora noche debe ser mayor a 0"
            cancha.precio_hora_noche = precio_hora_noche
        
        if estado is not None:
            if estado not in ['disponible', 'mantenimiento', 'no_disponible']:
                return False, "Estado inválido"
            cancha.estado = estado
        
        # Actualizar en BD
        if CanchaDAO.actualizar(cancha):
            return True, "Cancha modificada exitosamente"
        return False, "Error al modificar la cancha"
    
    @staticmethod
    def cambiar_estado_cancha(id_cancha: int, nuevo_estado: str) -> Tuple[bool, str]:
        """Cambia el estado de una cancha."""
        if nuevo_estado not in ['disponible', 'mantenimiento', 'no_disponible']:
            return False, "Estado inválido"
        
        cancha = CanchaDAO.obtener_por_id(id_cancha)
        if not cancha:
            return False, "Cancha no encontrada"
        
        if CanchaDAO.cambiar_estado(id_cancha, nuevo_estado):
            return True, f"Estado cambiado a: {nuevo_estado}"
        return False, "Error al cambiar el estado"
    
    @staticmethod
    def obtener_cancha(id_cancha: int) -> Optional[Cancha]:
        """Obtiene una cancha por ID."""
        return CanchaDAO.obtener_por_id(id_cancha)
    
    @staticmethod
    def obtener_todas_canchas() -> List[Cancha]:
        """Obtiene todas las canchas."""
        return CanchaDAO.obtener_todas()
    
    @staticmethod
    def obtener_canchas_disponibles() -> List[Cancha]:
        """Obtiene solo canchas disponibles."""
        return CanchaDAO.obtener_disponibles()
    
    @staticmethod
    def obtener_canchas_por_deporte(tipo_deporte: str) -> List[Cancha]:
        """Obtiene canchas de un deporte específico."""
        return CanchaDAO.obtener_por_deporte(tipo_deporte)
    
    @staticmethod
    def buscar_canchas(termino: str) -> List[Cancha]:
        """Busca canchas por nombre o tipo de deporte."""
        return CanchaDAO.buscar(termino)
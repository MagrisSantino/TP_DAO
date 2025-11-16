"""
Servicio de Torneos - Lógica de Negocio
"""

from typing import Tuple, Optional, List
from datetime import date
from models.torneo import Torneo
from models.equipo import Equipo
from models.partido import Partido
from dao.torneo_dao import TorneoDAO
from dao.equipo_dao import EquipoDAO
from dao.partido_dao import PartidoDAO


class TorneoService:
    """Servicio para gestión de torneos con validaciones"""
    
    @staticmethod
    def crear_torneo(nombre: str, deporte: str, fecha_inicio: date,
                    fecha_fin: date, cantidad_equipos: int,
                    descripcion: str = "") -> Tuple[bool, str, Optional[Torneo]]:
        """
        Crea un nuevo torneo con validaciones.
        
        Returns:
            Tuple (éxito, mensaje, torneo)
        """
        # Validar nombre
        if not nombre or len(nombre.strip()) < 3:
            return False, "El nombre debe tener al menos 3 caracteres", None
        
        # Validar deporte
        if not deporte or len(deporte.strip()) < 3:
            return False, "Deporte inválido", None
        
        # Validar fechas
        if fecha_inicio < date.today():
            return False, "La fecha de inicio no puede ser pasada", None
        
        if fecha_fin < fecha_inicio:
            return False, "La fecha de fin debe ser posterior a la fecha de inicio", None
        
        # Validar cantidad de equipos
        if cantidad_equipos < 2:
            return False, "El torneo debe tener al menos 2 equipos", None
        
        # Crear torneo
        torneo = Torneo(
            nombre=nombre.strip().title(),
            deporte=deporte.strip(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cantidad_equipos=cantidad_equipos,
            estado_torneo='planificado',
            descripcion=descripcion.strip()
        )
        
        # Guardar en BD
        id_torneo = TorneoDAO.insertar(torneo)
        if id_torneo:
            return True, "Torneo creado exitosamente", torneo
        else:
            return False, "Error al guardar el torneo", None
    
    @staticmethod
    def inscribir_equipo(id_torneo: int, nombre_equipo: str, capitan: str,
                        telefono_contacto: str) -> Tuple[bool, str, Optional[Equipo]]:
        """
        Inscribe un equipo en un torneo.
        
        Returns:
            Tuple (éxito, mensaje, equipo)
        """
        # Validar que el torneo existe
        torneo = TorneoDAO.obtener_por_id(id_torneo)
        if not torneo:
            return False, "Torneo no encontrado", None
        
        # Validar que el torneo está en estado planificado
        if torneo.estado_torneo != 'planificado':
            return False, f"No se pueden inscribir equipos. Torneo en estado: {torneo.estado_torneo}", None
        
        # Verificar capacidad del torneo
        equipos_inscritos = EquipoDAO.contar_por_torneo(id_torneo)
        if equipos_inscritos >= torneo.cantidad_equipos:
            return False, f"El torneo ya tiene {torneo.cantidad_equipos} equipos inscritos", None
        
        # Validar datos del equipo
        if not nombre_equipo or len(nombre_equipo.strip()) < 3:
            return False, "El nombre del equipo debe tener al menos 3 caracteres", None
        
        if not capitan or len(capitan.strip()) < 3:
            return False, "El nombre del capitán debe tener al menos 3 caracteres", None
        
        # Crear equipo
        equipo = Equipo(
            id_torneo=id_torneo,
            nombre_equipo=nombre_equipo.strip().title(),
            capitan=capitan.strip().title(),
            telefono_contacto=telefono_contacto.strip(),
            fecha_inscripcion=date.today()
        )
        
        # Guardar en BD
        id_equipo = EquipoDAO.insertar(equipo)
        if id_equipo:
            return True, "Equipo inscrito exitosamente", equipo
        else:
            return False, "Error al inscribir el equipo", None
    
    @staticmethod
    def generar_fixture(id_torneo: int) -> Tuple[bool, str, int]:
        """
        Genera el fixture de partidos para un torneo (todos contra todos).
        
        Returns:
            Tuple (éxito, mensaje, cantidad_partidos_creados)
        """
        from datetime import time  # ← AGREGAR ESTE IMPORT
        
        # Obtener torneo
        torneo = TorneoDAO.obtener_por_id(id_torneo)
        if not torneo:
            return False, "Torneo no encontrado", 0
        
        # Verificar que esté en estado planificado
        if torneo.estado_torneo != 'planificado':
            return False, "El fixture solo se puede generar en torneos planificados", 0
        
        # Obtener equipos inscritos
        equipos = EquipoDAO.obtener_por_torneo(id_torneo)
        if len(equipos) < 2:
            return False, "Se necesitan al menos 2 equipos para generar el fixture", 0
        
        # Verificar si ya hay partidos creados
        partidos_existentes = PartidoDAO.obtener_por_torneo(id_torneo)
        if len(partidos_existentes) > 0:
            return False, "Ya existe un fixture para este torneo", 0
        
        # Generar partidos (todos contra todos)
        partidos_creados = 0
        fecha_partido = torneo.fecha_inicio
        hora_default = time(10, 0)  # ← HORA POR DEFECTO: 10:00 AM
        
        for i in range(len(equipos)):
            for j in range(i + 1, len(equipos)):
                partido = Partido(
                    id_torneo=id_torneo,
                    id_equipo_local=equipos[i].id_equipo,
                    id_equipo_visitante=equipos[j].id_equipo,
                    id_reserva=None,  # Se asignará después
                    fecha_partido=fecha_partido,
                    hora_inicio=hora_default,  # ← CAMBIO AQUÍ: ahora tiene hora
                    resultado_local=None,
                    resultado_visitante=None,
                    estado_partido='programado'
                )
                
                if PartidoDAO.insertar(partido):
                    partidos_creados += 1
        
        if partidos_creados > 0:
            return True, f"Fixture generado: {partidos_creados} partidos creados", partidos_creados
        else:
            return False, "Error al generar el fixture", 0
    
    @staticmethod
    def iniciar_torneo(id_torneo: int) -> Tuple[bool, str]:
        """Cambia el estado de un torneo a 'en_curso'."""
        torneo = TorneoDAO.obtener_por_id(id_torneo)
        if not torneo:
            return False, "Torneo no encontrado"
        
        if torneo.estado_torneo != 'planificado':
            return False, f"No se puede iniciar un torneo en estado: {torneo.estado_torneo}"
        
        # Verificar que haya equipos
        equipos = EquipoDAO.obtener_por_torneo(id_torneo)
        if len(equipos) < 2:
            return False, "Se necesitan al menos 2 equipos para iniciar el torneo"
        
        # Verificar que haya fixture
        partidos = PartidoDAO.obtener_por_torneo(id_torneo)
        if len(partidos) == 0:
            return False, "Debe generar el fixture antes de iniciar el torneo"
        
        torneo.estado_torneo = 'en_curso'
        if TorneoDAO.actualizar(torneo):
            return True, "Torneo iniciado exitosamente"
        return False, "Error al iniciar el torneo"
    
    @staticmethod
    def finalizar_torneo(id_torneo: int) -> Tuple[bool, str]:
        """Cambia el estado de un torneo a 'finalizado'."""
        torneo = TorneoDAO.obtener_por_id(id_torneo)
        if not torneo:
            return False, "Torneo no encontrado"
        
        if torneo.estado_torneo != 'en_curso':
            return False, f"Solo se pueden finalizar torneos en curso"
        
        torneo.estado_torneo = 'finalizado'
        if TorneoDAO.actualizar(torneo):
            return True, "Torneo finalizado exitosamente"
        return False, "Error al finalizar el torneo"
    
    @staticmethod
    def registrar_resultado_partido(id_partido: int, resultado_local: int,
                                    resultado_visitante: int) -> Tuple[bool, str]:
        """
        Registra el resultado de un partido.
        
        Returns:
            Tuple (éxito, mensaje)
        """
        # Validar resultados
        if resultado_local < 0 or resultado_visitante < 0:
            return False, "Los resultados no pueden ser negativos"
        
        if PartidoDAO.registrar_resultado(id_partido, resultado_local, resultado_visitante):
            return True, "Resultado registrado exitosamente"
        return False, "Error al registrar el resultado"
    
    @staticmethod
    def obtener_torneo(id_torneo: int) -> Optional[Torneo]:
        """Obtiene un torneo por ID."""
        return TorneoDAO.obtener_por_id(id_torneo)
    
    @staticmethod
    def obtener_todos_torneos() -> List[Torneo]:
        """Obtiene todos los torneos."""
        return TorneoDAO.obtener_todos()
    
    @staticmethod
    def obtener_torneos_activos() -> List[Torneo]:
        """Obtiene torneos activos."""
        return TorneoDAO.obtener_activos()
    
    @staticmethod
    def obtener_equipos_torneo(id_torneo: int) -> List[Equipo]:
        """Obtiene todos los equipos de un torneo."""
        return EquipoDAO.obtener_por_torneo(id_torneo)
    
    @staticmethod
    def obtener_partidos_torneo(id_torneo: int) -> List[Partido]:
        """Obtiene todos los partidos de un torneo."""
        return PartidoDAO.obtener_por_torneo(id_torneo)
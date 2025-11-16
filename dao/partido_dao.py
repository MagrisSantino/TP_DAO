"""
DAO para la entidad Partido
"""
import sqlite3
from typing import List, Optional
from datetime import time
from models.partido import Partido
from database.db_connection import get_db_connection


class PartidoDAO:
    """Data Access Object para Partido"""
    
    @staticmethod
    def insertar(partido: Partido) -> Optional[int]:
        """Inserta un nuevo partido."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convertir time a string para SQLite
            hora_inicio_str = None
            if partido.hora_inicio:
                if isinstance(partido.hora_inicio, time):
                    hora_inicio_str = partido.hora_inicio.strftime('%H:%M:%S')
                else:
                    hora_inicio_str = partido.hora_inicio
            
            query = """
                INSERT INTO partido (id_torneo, id_equipo_local, id_equipo_visitante,
                                     id_reserva, fecha_partido, hora_inicio,
                                     resultado_local, resultado_visitante, estado_partido)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                partido.id_torneo, partido.id_equipo_local, partido.id_equipo_visitante,
                partido.id_reserva, partido.fecha_partido, hora_inicio_str,
                partido.resultado_local, partido.resultado_visitante, partido.estado_partido
            ))
            conn.commit()
            partido.id_partido = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar partido: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_partido: int) -> Optional[Partido]:
        """Obtiene un partido por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM partido WHERE id_partido = ?", (id_partido,))
            row = cursor.fetchone()
            return Partido.from_dict(dict(row)) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener partido: {e}")
            return None
    
    @staticmethod
    def obtener_por_torneo(id_torneo: int) -> List[Partido]:
        """Obtiene todos los partidos de un torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT * FROM partido 
                WHERE id_torneo = ? 
                ORDER BY fecha_partido, hora_inicio
            """
            cursor.execute(query, (id_torneo,))
            rows = cursor.fetchall()
            return [Partido.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener partidos del torneo: {e}")
            return []
    
    @staticmethod
    def obtener_por_equipo(id_equipo: int) -> List[Partido]:
        """Obtiene todos los partidos de un equipo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT * FROM partido 
                WHERE id_equipo_local = ? OR id_equipo_visitante = ?
                ORDER BY fecha_partido, hora_inicio
            """
            cursor.execute(query, (id_equipo, id_equipo))
            rows = cursor.fetchall()
            return [Partido.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener partidos del equipo: {e}")
            return []
    
    @staticmethod
    def obtener_todos() -> List[Partido]:
        """Obtiene todos los partidos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM partido ORDER BY fecha_partido DESC, hora_inicio")
            rows = cursor.fetchall()
            return [Partido.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener todos los partidos: {e}")
            return []
    
    @staticmethod
    def actualizar(partido: Partido) -> bool:
        """Actualiza un partido."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convertir time a string para SQLite
            hora_inicio_str = None
            if partido.hora_inicio:
                if isinstance(partido.hora_inicio, time):
                    hora_inicio_str = partido.hora_inicio.strftime('%H:%M:%S')
                else:
                    hora_inicio_str = partido.hora_inicio
            
            query = """
                UPDATE partido 
                SET id_torneo = ?, id_equipo_local = ?, id_equipo_visitante = ?,
                    id_reserva = ?, fecha_partido = ?, hora_inicio = ?,
                    resultado_local = ?, resultado_visitante = ?, estado_partido = ?
                WHERE id_partido = ?
            """
            cursor.execute(query, (
                partido.id_torneo, partido.id_equipo_local, partido.id_equipo_visitante,
                partido.id_reserva, partido.fecha_partido, hora_inicio_str,
                partido.resultado_local, partido.resultado_visitante, partido.estado_partido,
                partido.id_partido
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar partido: {e}")
            return False
    
    @staticmethod
    def registrar_resultado(id_partido: int, resultado_local: int, 
                           resultado_visitante: int) -> bool:
        """Registra el resultado de un partido."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE partido 
                SET resultado_local = ?, resultado_visitante = ?, estado_partido = 'jugado'
                WHERE id_partido = ?
            """
            cursor.execute(query, (resultado_local, resultado_visitante, id_partido))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al registrar resultado: {e}")
            return False
    
    @staticmethod
    def eliminar(id_partido: int) -> bool:
        """Elimina un partido."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM partido WHERE id_partido = ?", (id_partido,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar partido: {e}")
            return False
"""
DAO para la entidad Torneo
"""

import sqlite3
from typing import List, Optional
from models.torneo import Torneo
from database.db_connection import get_db_connection


class TorneoDAO:
    """Data Access Object para Torneo"""
    
    @staticmethod
    def insertar(torneo: Torneo) -> Optional[int]:
        """Inserta un nuevo torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO torneo (nombre, deporte, fecha_inicio, fecha_fin, 
                                    cantidad_equipos, estado_torneo, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                torneo.nombre, torneo.deporte, torneo.fecha_inicio,
                torneo.fecha_fin, torneo.cantidad_equipos,
                torneo.estado_torneo, torneo.descripcion
            ))
            conn.commit()
            torneo.id_torneo = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar torneo: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_torneo: int) -> Optional[Torneo]:
        """Obtiene un torneo por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM torneo WHERE id_torneo = ?", (id_torneo,))
            row = cursor.fetchone()
            return Torneo.from_dict(dict(row)) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener torneo: {e}")
            return None
    
    @staticmethod
    def obtener_todos() -> List[Torneo]:
        """Obtiene todos los torneos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM torneo ORDER BY fecha_inicio DESC")
            rows = cursor.fetchall()
            return [Torneo.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener torneos: {e}")
            return []
    
    @staticmethod
    def obtener_activos() -> List[Torneo]:
        """Obtiene torneos activos (planificados o en curso)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT * FROM torneo 
                WHERE estado_torneo IN ('planificado', 'en_curso')
                ORDER BY fecha_inicio
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Torneo.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener torneos activos: {e}")
            return []
    
    @staticmethod
    def actualizar(torneo: Torneo) -> bool:
        """Actualiza un torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE torneo 
                SET nombre = ?, deporte = ?, fecha_inicio = ?, fecha_fin = ?,
                    cantidad_equipos = ?, estado_torneo = ?, descripcion = ?
                WHERE id_torneo = ?
            """
            cursor.execute(query, (
                torneo.nombre, torneo.deporte, torneo.fecha_inicio,
                torneo.fecha_fin, torneo.cantidad_equipos,
                torneo.estado_torneo, torneo.descripcion, torneo.id_torneo
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar torneo: {e}")
            return False
    
    @staticmethod
    def eliminar(id_torneo: int) -> bool:
        """Elimina un torneo (elimina en cascada equipos y partidos)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM torneo WHERE id_torneo = ?", (id_torneo,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar torneo: {e}")
            return False
"""
DAO para la entidad Equipo
"""

import sqlite3
from typing import List, Optional
from models.equipo import Equipo
from database.db_connection import get_db_connection


class EquipoDAO:
    """Data Access Object para Equipo"""
    
    @staticmethod
    def insertar(equipo: Equipo) -> Optional[int]:
        """Inserta un nuevo equipo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO equipo (id_torneo, nombre_equipo, capitan, 
                                    telefono_contacto, fecha_inscripcion)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                equipo.id_torneo, equipo.nombre_equipo, equipo.capitan,
                equipo.telefono_contacto, equipo.fecha_inscripcion
            ))
            conn.commit()
            equipo.id_equipo = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar equipo: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_equipo: int) -> Optional[Equipo]:
        """Obtiene un equipo por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipo WHERE id_equipo = ?", (id_equipo,))
            row = cursor.fetchone()
            return Equipo.from_dict(dict(row)) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener equipo: {e}")
            return None
    
    @staticmethod
    def obtener_por_torneo(id_torneo: int) -> List[Equipo]:
        """Obtiene todos los equipos de un torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM equipo WHERE id_torneo = ? ORDER BY nombre_equipo"
            cursor.execute(query, (id_torneo,))
            rows = cursor.fetchall()
            return [Equipo.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener equipos del torneo: {e}")
            return []
    
    @staticmethod
    def obtener_todos() -> List[Equipo]:
        """Obtiene todos los equipos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipo ORDER BY id_torneo, nombre_equipo")
            rows = cursor.fetchall()
            return [Equipo.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener todos los equipos: {e}")
            return []
    
    @staticmethod
    def contar_por_torneo(id_torneo: int) -> int:
        """Cuenta los equipos inscritos en un torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) as total FROM equipo WHERE id_torneo = ?"
            cursor.execute(query, (id_torneo,))
            return cursor.fetchone()['total']
        except sqlite3.Error as e:
            print(f"Error al contar equipos: {e}")
            return 0
    
    @staticmethod
    def actualizar(equipo: Equipo) -> bool:
        """Actualiza un equipo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE equipo 
                SET id_torneo = ?, nombre_equipo = ?, capitan = ?,
                    telefono_contacto = ?, fecha_inscripcion = ?
                WHERE id_equipo = ?
            """
            cursor.execute(query, (
                equipo.id_torneo, equipo.nombre_equipo, equipo.capitan,
                equipo.telefono_contacto, equipo.fecha_inscripcion,
                equipo.id_equipo
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar equipo: {e}")
            return False
    
    @staticmethod
    def eliminar(id_equipo: int) -> bool:
        """Elimina un equipo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipo WHERE id_equipo = ?", (id_equipo,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print("No se puede eliminar el equipo. Tiene partidos asociados.")
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar equipo: {e}")
            return False
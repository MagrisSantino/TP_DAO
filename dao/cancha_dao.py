"""
DAO para la entidad Cancha
Versión FINAL: Sincronizada con Modelo actualizado y Base de Datos migrada.
"""
import sqlite3
from typing import List, Optional
from models.cancha import Cancha
from database.db_connection import get_db_connection

class CanchaDAO:
    
    @staticmethod
    def insertar(cancha: Cancha) -> Optional[int]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO cancha (nombre, tipo_deporte, tipo_superficie, techada, 
                                    iluminacion, capacidad_jugadores, 
                                    precio_hora_dia, precio_hora_noche, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                cancha.nombre, 
                cancha.tipo_deporte,
                cancha.tipo_superficie,
                int(cancha.techada),
                int(cancha.iluminacion),
                cancha.capacidad_jugadores,
                cancha.precio_hora_dia,
                cancha.precio_hora_noche,
                cancha.estado
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar cancha: {e}")
            return None

    @staticmethod
    def obtener_todos() -> List[Cancha]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cancha WHERE estado != 'no_disponible' AND estado != 'inactiva' ORDER BY nombre")
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener canchas: {e}")
            return []

    @staticmethod
    def obtener_disponibles() -> List[Cancha]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cancha WHERE estado = 'disponible' ORDER BY nombre")
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def obtener_por_id(id_cancha: int) -> Optional[Cancha]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cancha WHERE id_cancha = ?", (id_cancha,))
            row = cursor.fetchone()
            return CanchaDAO._row_to_cancha(row) if row else None
        except sqlite3.Error:
            return None

    @staticmethod
    def actualizar(cancha: Cancha) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE cancha 
                SET nombre=?, tipo_deporte=?, tipo_superficie=?, techada=?, 
                    iluminacion=?, capacidad_jugadores=?, precio_hora_dia=?, 
                    precio_hora_noche=?, estado=?
                WHERE id_cancha=?
            """
            cursor.execute(query, (
                cancha.nombre, cancha.tipo_deporte, cancha.tipo_superficie,
                int(cancha.techada), int(cancha.iluminacion),
                cancha.capacidad_jugadores,
                cancha.precio_hora_dia, cancha.precio_hora_noche,
                cancha.estado, cancha.id_cancha
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar: {e}")
            return False

    @staticmethod
    def eliminar(id_cancha: int) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "UPDATE cancha SET estado = 'no_disponible' WHERE id_cancha = ?"
            cursor.execute(query, (id_cancha,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar cancha: {e}")
            return False

    @staticmethod
    def contar_total() -> int:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cancha WHERE estado='disponible'")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    @staticmethod
    def _row_to_cancha(row) -> Cancha:
        """
        Mapea la fila de BD al objeto Cancha.
        Maneja la compatibilidad de nombres de columnas viejas y nuevas.
        """
        # Intentar leer precios nuevos, fallback a viejos
        p_dia = 0.0
        p_noche = 0.0
        
        try:
            p_dia = row['precio_hora_dia']
            p_noche = row['precio_hora_noche']
        except IndexError:
            # Si no existen las columnas nuevas, buscamos las viejas
            try:
                val = row['precio']
            except IndexError:
                try:
                    val = row['precio_hora']
                except IndexError:
                    val = 0.0
            p_dia = val
            p_noche = val

        # Datos opcionales con defaults
        superficie = 'Sintético'
        capacidad = 5
        try:
            superficie = row['tipo_superficie']
            capacidad = row['capacidad_jugadores']
        except IndexError:
            pass

        # Estado
        try:
            estado = row['estado']
            if not estado: estado = 'disponible'
        except IndexError:
            estado = 'disponible'

        return Cancha(
            id_cancha=row['id_cancha'],
            nombre=row['nombre'],
            tipo_deporte=row['tipo_deporte'],
            tipo_superficie=superficie,
            techada=bool(row['techada']),
            iluminacion=bool(row['iluminacion']),
            capacidad_jugadores=capacidad,
            precio_hora_dia=p_dia,
            precio_hora_noche=p_noche,
            estado=estado
        )
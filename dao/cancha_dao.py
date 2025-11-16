"""
DAO para la entidad Cancha
Operaciones CRUD sobre la tabla 'cancha'
"""

import sqlite3
from typing import List, Optional
from models.cancha import Cancha
from database.db_connection import get_db_connection


class CanchaDAO:
    """Data Access Object para Cancha"""
    
    @staticmethod
    def insertar(cancha: Cancha) -> Optional[int]:
        """
        Inserta una nueva cancha en la base de datos.
        
        Args:
            cancha (Cancha): Objeto cancha a insertar
        
        Returns:
            int: ID de la cancha insertada o None si falla
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO cancha (nombre, tipo_deporte, tipo_superficie, techada, 
                                    iluminacion, capacidad_jugadores, precio_hora_dia, 
                                    precio_hora_noche, estado)
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
            cancha.id_cancha = cursor.lastrowid
            return cursor.lastrowid
            
        except sqlite3.Error as e:
            print(f"Error al insertar cancha: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_cancha: int) -> Optional[Cancha]:
        """
        Obtiene una cancha por su ID.
        
        Args:
            id_cancha (int): ID de la cancha
        
        Returns:
            Cancha: Objeto cancha o None si no existe
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cancha WHERE id_cancha = ?"
            cursor.execute(query, (id_cancha,))
            
            row = cursor.fetchone()
            if row:
                return CanchaDAO._row_to_cancha(row)
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener cancha: {e}")
            return None
    
    @staticmethod
    def obtener_todas() -> List[Cancha]:
        """
        Obtiene todas las canchas.
        
        Returns:
            List[Cancha]: Lista de canchas
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cancha ORDER BY nombre"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener todas las canchas: {e}")
            return []
    
    @staticmethod
    def obtener_disponibles() -> List[Cancha]:
        """
        Obtiene solo las canchas disponibles.
        
        Returns:
            List[Cancha]: Lista de canchas disponibles
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cancha WHERE estado = 'disponible' ORDER BY nombre"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener canchas disponibles: {e}")
            return []
    
    @staticmethod
    def obtener_por_deporte(tipo_deporte: str) -> List[Cancha]:
        """
        Obtiene canchas filtradas por tipo de deporte.
        
        Args:
            tipo_deporte (str): Tipo de deporte
        
        Returns:
            List[Cancha]: Lista de canchas del deporte especificado
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cancha WHERE tipo_deporte = ? ORDER BY nombre"
            cursor.execute(query, (tipo_deporte,))
            
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener canchas por deporte: {e}")
            return []
    
    @staticmethod
    def obtener_con_iluminacion() -> List[Cancha]:
        """
        Obtiene canchas que tienen iluminación.
        
        Returns:
            List[Cancha]: Lista de canchas con iluminación
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cancha WHERE iluminacion = 1 ORDER BY nombre"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener canchas con iluminación: {e}")
            return []
    
    @staticmethod
    def actualizar(cancha: Cancha) -> bool:
        """
        Actualiza los datos de una cancha.
        
        Args:
            cancha (Cancha): Objeto cancha con datos actualizados
        
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE cancha 
                SET nombre = ?, tipo_deporte = ?, tipo_superficie = ?, techada = ?,
                    iluminacion = ?, capacidad_jugadores = ?, precio_hora_dia = ?,
                    precio_hora_noche = ?, estado = ?
                WHERE id_cancha = ?
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
                cancha.estado,
                cancha.id_cancha
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al actualizar cancha: {e}")
            return False
    
    @staticmethod
    def eliminar(id_cancha: int) -> bool:
        """
        Elimina una cancha de la base de datos.
        ADVERTENCIA: Solo usar si no tiene reservas asociadas.
        
        Args:
            id_cancha (int): ID de la cancha a eliminar
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM cancha WHERE id_cancha = ?"
            cursor.execute(query, (id_cancha,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"No se puede eliminar la cancha. Tiene reservas asociadas: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar cancha: {e}")
            return False
    
    @staticmethod
    def cambiar_estado(id_cancha: int, nuevo_estado: str) -> bool:
        """
        Cambia el estado de una cancha.
        
        Args:
            id_cancha (int): ID de la cancha
            nuevo_estado (str): 'disponible', 'mantenimiento' o 'no_disponible'
        
        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "UPDATE cancha SET estado = ? WHERE id_cancha = ?"
            cursor.execute(query, (nuevo_estado, id_cancha))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al cambiar estado de la cancha: {e}")
            return False
    
    @staticmethod
    def buscar(termino: str) -> List[Cancha]:
        """
        Busca canchas por nombre o tipo de deporte.
        
        Args:
            termino (str): Término de búsqueda
        
        Returns:
            List[Cancha]: Lista de canchas que coinciden con la búsqueda
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            termino_like = f"%{termino}%"
            query = """
                SELECT * FROM cancha 
                WHERE nombre LIKE ? OR tipo_deporte LIKE ?
                ORDER BY nombre
            """
            
            cursor.execute(query, (termino_like, termino_like))
            
            rows = cursor.fetchall()
            return [CanchaDAO._row_to_cancha(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al buscar canchas: {e}")
            return []
    
    @staticmethod
    def contar_total() -> int:
        """
        Cuenta el total de canchas.
        
        Returns:
            int: Número total de canchas
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM cancha"
            cursor.execute(query)
            
            return cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f"Error al contar canchas: {e}")
            return 0
    
    @staticmethod
    def contar_por_estado() -> dict:
        """
        Cuenta canchas agrupadas por estado.
        
        Returns:
            dict: Diccionario con el conteo por estado
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT estado, COUNT(*) as cantidad FROM cancha GROUP BY estado"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return {row['estado']: row['cantidad'] for row in rows}
            
        except sqlite3.Error as e:
            print(f"Error al contar canchas por estado: {e}")
            return {}
    
    @staticmethod
    def _row_to_cancha(row) -> Cancha:
        """
        Convierte una fila de la BD en un objeto Cancha.
        
        Args:
            row: Fila de la base de datos
        
        Returns:
            Cancha: Objeto cancha
        """
        return Cancha(
            id_cancha=row['id_cancha'],
            nombre=row['nombre'],
            tipo_deporte=row['tipo_deporte'],
            tipo_superficie=row['tipo_superficie'],
            techada=bool(row['techada']),
            iluminacion=bool(row['iluminacion']),
            capacidad_jugadores=row['capacidad_jugadores'],
            precio_hora_dia=row['precio_hora_dia'],
            precio_hora_noche=row['precio_hora_noche'],
            estado=row['estado']
        )
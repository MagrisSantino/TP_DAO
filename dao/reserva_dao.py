"""
DAO para la entidad Reserva
Operaciones CRUD sobre la tabla 'reserva'
Incluye validación de disponibilidad de canchas
"""
import sqlite3
from typing import List, Optional
from datetime import date, time, datetime
from models.reserva import Reserva
from database.db_connection import get_db_connection


class ReservaDAO:
    """Data Access Object para Reserva"""
    
    @staticmethod
    def insertar(reserva: Reserva) -> Optional[int]:
        """
        Inserta una nueva reserva en la base de datos.
        
        Args:
            reserva (Reserva): Objeto reserva a insertar
        
        Returns:
            int: ID de la reserva insertada o None si falla
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convertir time a string para SQLite
            hora_inicio_str = reserva.hora_inicio.strftime('%H:%M:%S') if isinstance(reserva.hora_inicio, time) else reserva.hora_inicio
            hora_fin_str = reserva.hora_fin.strftime('%H:%M:%S') if isinstance(reserva.hora_fin, time) else reserva.hora_fin
            
            query = """
                INSERT INTO reserva (id_cliente, id_cancha, fecha_reserva, hora_inicio, 
                                     hora_fin, usa_iluminacion, estado_reserva, monto_total, 
                                     fecha_creacion, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                reserva.id_cliente,
                reserva.id_cancha,
                reserva.fecha_reserva,
                hora_inicio_str,
                hora_fin_str,
                int(reserva.usa_iluminacion),
                reserva.estado_reserva,
                reserva.monto_total,
                reserva.fecha_creacion,
                reserva.observaciones
            ))
            
            conn.commit()
            reserva.id_reserva = cursor.lastrowid
            return cursor.lastrowid
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al insertar reserva (posible solapamiento): {e}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar reserva: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_reserva: int) -> Optional[Reserva]:
        """
        Obtiene una reserva por su ID.
        
        Args:
            id_reserva (int): ID de la reserva
        
        Returns:
            Reserva: Objeto reserva o None si no existe
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM reserva WHERE id_reserva = ?"
            cursor.execute(query, (id_reserva,))
            
            row = cursor.fetchone()
            if row:
                return ReservaDAO._row_to_reserva(row)
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener reserva: {e}")
            return None
    
    @staticmethod
    def obtener_todas() -> List[Reserva]:
        """
        Obtiene todas las reservas.
        
        Returns:
            List[Reserva]: Lista de reservas
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM reserva ORDER BY fecha_reserva DESC, hora_inicio DESC"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener todas las reservas: {e}")
            return []
    
    @staticmethod
    def obtener_por_cliente(id_cliente: int) -> List[Reserva]:
        """
        Obtiene todas las reservas de un cliente.
        
        Args:
            id_cliente (int): ID del cliente
        
        Returns:
            List[Reserva]: Lista de reservas del cliente
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM reserva 
                WHERE id_cliente = ? 
                ORDER BY fecha_reserva DESC, hora_inicio DESC
            """
            cursor.execute(query, (id_cliente,))
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener reservas del cliente: {e}")
            return []
    
    @staticmethod
    def obtener_por_cancha(id_cancha: int) -> List[Reserva]:
        """
        Obtiene todas las reservas de una cancha.
        
        Args:
            id_cancha (int): ID de la cancha
        
        Returns:
            List[Reserva]: Lista de reservas de la cancha
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM reserva 
                WHERE id_cancha = ? 
                ORDER BY fecha_reserva DESC, hora_inicio DESC
            """
            cursor.execute(query, (id_cancha,))
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener reservas de la cancha: {e}")
            return []
    
    @staticmethod
    def obtener_por_fecha(fecha: date) -> List[Reserva]:
        """
        Obtiene todas las reservas de una fecha específica.
        
        Args:
            fecha (date): Fecha de las reservas
        
        Returns:
            List[Reserva]: Lista de reservas de la fecha
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM reserva 
                WHERE fecha_reserva = ? 
                ORDER BY hora_inicio
            """
            cursor.execute(query, (fecha,))
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por fecha: {e}")
            return []
    
    @staticmethod
    def obtener_por_rango_fechas(fecha_inicio: date, fecha_fin: date) -> List[Reserva]:
        """
        Obtiene reservas en un rango de fechas.
        
        Args:
            fecha_inicio (date): Fecha inicial
            fecha_fin (date): Fecha final
        
        Returns:
            List[Reserva]: Lista de reservas en el rango
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM reserva 
                WHERE fecha_reserva BETWEEN ? AND ?
                ORDER BY fecha_reserva, hora_inicio
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por rango de fechas: {e}")
            return []
    
    @staticmethod
    def obtener_por_estado(estado: str) -> List[Reserva]:
        """
        Obtiene reservas filtradas por estado.
        
        Args:
            estado (str): Estado de la reserva
        
        Returns:
            List[Reserva]: Lista de reservas con el estado especificado
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM reserva 
                WHERE estado_reserva = ? 
                ORDER BY fecha_reserva DESC, hora_inicio DESC
            """
            cursor.execute(query, (estado,))
            
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por estado: {e}")
            return []
    
    @staticmethod
    def verificar_disponibilidad(id_cancha: int, fecha: date, hora_inicio: time, 
                                  hora_fin: time, id_reserva_excluir: int = None) -> bool:
        """
        Verifica si una cancha está disponible en el horario especificado.
        CRÍTICO: Evita solapamiento de reservas.
        
        Args:
            id_cancha (int): ID de la cancha
            fecha (date): Fecha de la reserva
            hora_inicio (time): Hora de inicio
            hora_fin (time): Hora de fin
            id_reserva_excluir (int): ID de reserva a excluir (para actualización)
        
        Returns:
            bool: True si está disponible, False si hay solapamiento
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convertir time a string para SQLite
            hora_inicio_str = hora_inicio.strftime('%H:%M:%S') if isinstance(hora_inicio, time) else hora_inicio
            hora_fin_str = hora_fin.strftime('%H:%M:%S') if isinstance(hora_fin, time) else hora_fin
            
            # Buscar reservas que se solapen en el mismo día y cancha
            # Excluimos reservas canceladas y opcionalmente una reserva específica
            if id_reserva_excluir:
                query = """
                    SELECT COUNT(*) as conflictos
                    FROM reserva
                    WHERE id_cancha = ? 
                    AND fecha_reserva = ?
                    AND estado_reserva != 'cancelada'
                    AND id_reserva != ?
                    AND (
                        (hora_inicio < ? AND hora_fin > ?)
                        OR (hora_inicio < ? AND hora_fin > ?)
                        OR (hora_inicio >= ? AND hora_inicio < ?)
                        OR (hora_fin > ? AND hora_fin <= ?)
                    )
                """
                params = (id_cancha, fecha, id_reserva_excluir,
                         hora_fin_str, hora_inicio_str,
                         hora_fin_str, hora_inicio_str,
                         hora_inicio_str, hora_fin_str,
                         hora_inicio_str, hora_fin_str)
            else:
                query = """
                    SELECT COUNT(*) as conflictos
                    FROM reserva
                    WHERE id_cancha = ? 
                    AND fecha_reserva = ?
                    AND estado_reserva != 'cancelada'
                    AND (
                        (hora_inicio < ? AND hora_fin > ?)
                        OR (hora_inicio < ? AND hora_fin > ?)
                        OR (hora_inicio >= ? AND hora_inicio < ?)
                        OR (hora_fin > ? AND hora_fin <= ?)
                    )
                """
                params = (id_cancha, fecha,
                         hora_fin_str, hora_inicio_str,
                         hora_fin_str, hora_inicio_str,
                         hora_inicio_str, hora_fin_str,
                         hora_inicio_str, hora_fin_str)
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            # Si no hay conflictos, está disponible
            return result['conflictos'] == 0
            
        except sqlite3.Error as e:
            print(f"Error al verificar disponibilidad: {e}")
            return False
    
    @staticmethod
    def actualizar(reserva: Reserva) -> bool:
        """
        Actualiza los datos de una reserva.
        
        Args:
            reserva (Reserva): Objeto reserva con datos actualizados
        
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convertir time a string para SQLite
            hora_inicio_str = reserva.hora_inicio.strftime('%H:%M:%S') if isinstance(reserva.hora_inicio, time) else reserva.hora_inicio
            hora_fin_str = reserva.hora_fin.strftime('%H:%M:%S') if isinstance(reserva.hora_fin, time) else reserva.hora_fin
            
            query = """
                UPDATE reserva 
                SET id_cliente = ?, id_cancha = ?, fecha_reserva = ?, 
                    hora_inicio = ?, hora_fin = ?, usa_iluminacion = ?,
                    estado_reserva = ?, monto_total = ?, observaciones = ?
                WHERE id_reserva = ?
            """
            
            cursor.execute(query, (
                reserva.id_cliente,
                reserva.id_cancha,
                reserva.fecha_reserva,
                hora_inicio_str,
                hora_fin_str,
                int(reserva.usa_iluminacion),
                reserva.estado_reserva,
                reserva.monto_total,
                reserva.observaciones,
                reserva.id_reserva
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al actualizar reserva: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar reserva: {e}")
            return False
    
    @staticmethod
    def cambiar_estado(id_reserva: int, nuevo_estado: str) -> bool:
        """
        Cambia el estado de una reserva.
        
        Args:
            id_reserva (int): ID de la reserva
            nuevo_estado (str): Nuevo estado de la reserva
        
        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "UPDATE reserva SET estado_reserva = ? WHERE id_reserva = ?"
            cursor.execute(query, (nuevo_estado, id_reserva))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al cambiar estado de la reserva: {e}")
            return False
    
    @staticmethod
    def eliminar(id_reserva: int) -> bool:
        """
        Elimina una reserva de la base de datos.
        
        Args:
            id_reserva (int): ID de la reserva a eliminar
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM reserva WHERE id_reserva = ?"
            cursor.execute(query, (id_reserva,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"No se puede eliminar la reserva. Tiene pagos asociados: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")
            return False
    
    @staticmethod
    def contar_total() -> int:
        """Cuenta el total de reservas."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reserva")
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar reservas: {e}")
            return 0
    
    @staticmethod
    def contar_por_estado() -> dict:
        """Cuenta reservas agrupadas por estado."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT estado_reserva, COUNT(*) as cantidad FROM reserva GROUP BY estado_reserva"
            cursor.execute(query)
            rows = cursor.fetchall()
            return {row['estado_reserva']: row['cantidad'] for row in rows}
        except sqlite3.Error as e:
            print(f"Error al contar reservas por estado: {e}")
            return {}
    
    @staticmethod
    def _row_to_reserva(row) -> Reserva:
        """Convierte una fila de la BD en un objeto Reserva."""
        return Reserva(
            id_reserva=row['id_reserva'],
            id_cliente=row['id_cliente'],
            id_cancha=row['id_cancha'],
            fecha_reserva=row['fecha_reserva'],
            hora_inicio=row['hora_inicio'],
            hora_fin=row['hora_fin'],
            usa_iluminacion=bool(row['usa_iluminacion']),
            estado_reserva=row['estado_reserva'],
            monto_total=row['monto_total'],
            fecha_creacion=row['fecha_creacion'],
            observaciones=row['observaciones']
        )
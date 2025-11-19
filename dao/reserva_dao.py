"""
DAO para la entidad Reserva
Operaciones CRUD sobre la tabla 'reserva'
CORREGIDO: Conversión correcta de tipos de datos (Fechas y Horas)
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
        """Inserta una nueva reserva."""
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
            print(f"Error de integridad al insertar reserva: {e}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar reserva: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_reserva: int) -> Optional[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE id_reserva = ?", (id_reserva,))
            row = cursor.fetchone()
            return ReservaDAO._row_to_reserva(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener reserva: {e}")
            return None
    
    @staticmethod
    def obtener_todas() -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva ORDER BY fecha_reserva DESC, hora_inicio DESC")
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener todas las reservas: {e}")
            return []
    
    @staticmethod
    def obtener_por_cliente(id_cliente: int) -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE id_cliente = ? ORDER BY fecha_reserva DESC", (id_cliente,))
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas del cliente: {e}")
            return []
    
    @staticmethod
    def obtener_por_cancha(id_cancha: int) -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE id_cancha = ? ORDER BY fecha_reserva DESC", (id_cancha,))
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas de la cancha: {e}")
            return []
    
    @staticmethod
    def obtener_por_fecha(fecha: date) -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE fecha_reserva = ? ORDER BY hora_inicio", (fecha,))
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por fecha: {e}")
            return []

    @staticmethod
    def obtener_por_rango_fechas(fecha_inicio: date, fecha_fin: date) -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE fecha_reserva BETWEEN ? AND ? ORDER BY fecha_reserva", (fecha_inicio, fecha_fin))
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por rango: {e}")
            return []

    @staticmethod
    def obtener_por_estado(estado: str) -> List[Reserva]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reserva WHERE estado_reserva = ? ORDER BY fecha_reserva DESC", (estado,))
            rows = cursor.fetchall()
            return [ReservaDAO._row_to_reserva(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por estado: {e}")
            return []

    @staticmethod
    def verificar_disponibilidad(id_cancha: int, fecha: date, hora_inicio: time, 
                                  hora_fin: time, id_reserva_excluir: int = None) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            hora_inicio_str = hora_inicio.strftime('%H:%M:%S') if isinstance(hora_inicio, time) else hora_inicio
            hora_fin_str = hora_fin.strftime('%H:%M:%S') if isinstance(hora_fin, time) else hora_fin
            
            if id_reserva_excluir:
                query = """
                    SELECT COUNT(*) as conflictos FROM reserva
                    WHERE id_cancha = ? AND fecha_reserva = ? AND estado_reserva != 'cancelada' AND id_reserva != ?
                    AND ((hora_inicio < ? AND hora_fin > ?) OR (hora_inicio < ? AND hora_fin > ?) OR (hora_inicio >= ? AND hora_inicio < ?) OR (hora_fin > ? AND hora_fin <= ?))
                """
                params = (id_cancha, fecha, id_reserva_excluir, hora_fin_str, hora_inicio_str, hora_fin_str, hora_inicio_str, hora_inicio_str, hora_fin_str, hora_inicio_str, hora_fin_str)
            else:
                query = """
                    SELECT COUNT(*) as conflictos FROM reserva
                    WHERE id_cancha = ? AND fecha_reserva = ? AND estado_reserva != 'cancelada'
                    AND ((hora_inicio < ? AND hora_fin > ?) OR (hora_inicio < ? AND hora_fin > ?) OR (hora_inicio >= ? AND hora_inicio < ?) OR (hora_fin > ? AND hora_fin <= ?))
                """
                params = (id_cancha, fecha, hora_fin_str, hora_inicio_str, hora_fin_str, hora_inicio_str, hora_inicio_str, hora_fin_str, hora_inicio_str, hora_fin_str)
            
            cursor.execute(query, params)
            return cursor.fetchone()['conflictos'] == 0
        except sqlite3.Error as e:
            print(f"Error al verificar disponibilidad: {e}")
            return False

    @staticmethod
    def actualizar(reserva: Reserva) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            hora_inicio_str = reserva.hora_inicio.strftime('%H:%M:%S') if isinstance(reserva.hora_inicio, time) else reserva.hora_inicio
            hora_fin_str = reserva.hora_fin.strftime('%H:%M:%S') if isinstance(reserva.hora_fin, time) else reserva.hora_fin
            
            query = """
                UPDATE reserva SET id_cliente = ?, id_cancha = ?, fecha_reserva = ?, 
                    hora_inicio = ?, hora_fin = ?, usa_iluminacion = ?,
                    estado_reserva = ?, monto_total = ?, observaciones = ?
                WHERE id_reserva = ?
            """
            cursor.execute(query, (reserva.id_cliente, reserva.id_cancha, reserva.fecha_reserva, hora_inicio_str, hora_fin_str, int(reserva.usa_iluminacion), reserva.estado_reserva, reserva.monto_total, reserva.observaciones, reserva.id_reserva))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar reserva: {e}")
            return False

    @staticmethod
    def cambiar_estado(id_reserva: int, nuevo_estado: str) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE reserva SET estado_reserva = ? WHERE id_reserva = ?", (nuevo_estado, id_reserva))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al cambiar estado: {e}")
            return False

    @staticmethod
    def eliminar(id_reserva: int) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reserva WHERE id_reserva = ?", (id_reserva,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")
            return False

    @staticmethod
    def contar_total() -> int:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reserva")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    @staticmethod
    def contar_por_estado() -> dict:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT estado_reserva, COUNT(*) as cantidad FROM reserva GROUP BY estado_reserva")
            rows = cursor.fetchall()
            return {row['estado_reserva']: row['cantidad'] for row in rows}
        except sqlite3.Error:
            return {}

    @staticmethod
    def _row_to_reserva(row) -> Reserva:
        """
        Convierte una fila de la BD en un objeto Reserva.
        Realiza la conversión crítica de strings a objetos date/time.
        """
        # 1. Parsear Fecha
        fecha_reserva = row['fecha_reserva']
        if isinstance(fecha_reserva, str):
            try:
                fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
            except ValueError:
                fecha_reserva = None

        # 2. Parsear Horas
        def parsear_hora_db(hora_str):
            if not isinstance(hora_str, str): return hora_str
            try:
                # Intenta formato largo (HH:MM:SS)
                return datetime.strptime(hora_str, '%H:%M:%S').time()
            except ValueError:
                try:
                    # Intenta formato corto (HH:MM)
                    return datetime.strptime(hora_str, '%H:%M').time()
                except ValueError:
                    return None

        hora_inicio = parsear_hora_db(row['hora_inicio'])
        hora_fin = parsear_hora_db(row['hora_fin'])

        # 3. Parsear Fecha Creación
        fecha_creacion = row['fecha_creacion']
        if isinstance(fecha_creacion, str):
            try:
                fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    fecha_creacion = datetime.now()

        return Reserva(
            id_reserva=row['id_reserva'],
            id_cliente=row['id_cliente'],
            id_cancha=row['id_cancha'],
            fecha_reserva=fecha_reserva,  # Ahora es un objeto date
            hora_inicio=hora_inicio,      # Ahora es un objeto time
            hora_fin=hora_fin,            # Ahora es un objeto time
            usa_iluminacion=bool(row['usa_iluminacion']),
            estado_reserva=row['estado_reserva'],
            monto_total=row['monto_total'],
            fecha_creacion=fecha_creacion,
            observaciones=row['observaciones']
        )
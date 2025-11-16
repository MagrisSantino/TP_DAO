"""
DAO para la entidad Pago
Operaciones CRUD sobre la tabla 'pago'
"""

import sqlite3
from typing import List, Optional
from models.pago import Pago
from database.db_connection import get_db_connection


class PagoDAO:
    """Data Access Object para Pago"""
    
    @staticmethod
    def insertar(pago: Pago) -> Optional[int]:
        """Inserta un nuevo pago."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO pago (id_reserva, fecha_pago, monto, metodo_pago, 
                                  estado_pago, comprobante)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                pago.id_reserva,
                pago.fecha_pago,
                pago.monto,
                pago.metodo_pago,
                pago.estado_pago,
                pago.comprobante
            ))
            
            conn.commit()
            pago.id_pago = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar pago: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_pago: int) -> Optional[Pago]:
        """Obtiene un pago por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago WHERE id_pago = ?", (id_pago,))
            row = cursor.fetchone()
            return PagoDAO._row_to_pago(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener pago: {e}")
            return None
    
    @staticmethod
    def obtener_por_reserva(id_reserva: int) -> List[Pago]:
        """Obtiene todos los pagos de una reserva."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM pago WHERE id_reserva = ? ORDER BY fecha_pago DESC"
            cursor.execute(query, (id_reserva,))
            rows = cursor.fetchall()
            return [PagoDAO._row_to_pago(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener pagos de la reserva: {e}")
            return []
    
    @staticmethod
    def obtener_todos() -> List[Pago]:
        """Obtiene todos los pagos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago ORDER BY fecha_pago DESC")
            rows = cursor.fetchall()
            return [PagoDAO._row_to_pago(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener todos los pagos: {e}")
            return []
    
    @staticmethod
    def calcular_total_pagado_reserva(id_reserva: int) -> float:
        """Calcula el total pagado de una reserva."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT SUM(monto) as total 
                FROM pago 
                WHERE id_reserva = ? AND estado_pago = 'pagado'
            """
            cursor.execute(query, (id_reserva,))
            result = cursor.fetchone()
            return result['total'] if result['total'] else 0.0
        except sqlite3.Error as e:
            print(f"Error al calcular total pagado: {e}")
            return 0.0
    
    @staticmethod
    def actualizar(pago: Pago) -> bool:
        """Actualiza los datos de un pago."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE pago 
                SET id_reserva = ?, fecha_pago = ?, monto = ?, 
                    metodo_pago = ?, estado_pago = ?, comprobante = ?
                WHERE id_pago = ?
            """
            cursor.execute(query, (
                pago.id_reserva, pago.fecha_pago, pago.monto,
                pago.metodo_pago, pago.estado_pago, pago.comprobante,
                pago.id_pago
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar pago: {e}")
            return False
    
    @staticmethod
    def eliminar(id_pago: int) -> bool:
        """Elimina un pago."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pago WHERE id_pago = ?", (id_pago,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar pago: {e}")
            return False
    
    @staticmethod
    def _row_to_pago(row) -> Pago:
        """Convierte una fila de la BD en un objeto Pago."""
        return Pago.from_dict(dict(row))
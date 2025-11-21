import sqlite3
from typing import List, Optional
from datetime import datetime, date
from models.pago import Pago
from database.db_connection import get_db_connection

class PagoDAO:
    
    @staticmethod
    def insertar(pago: Pago) -> Optional[int]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO pago (id_reserva, id_torneo, monto, fecha_pago, metodo_pago)
                VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                pago.id_reserva, # Puede ser None
                pago.id_torneo,  # Puede ser None
                pago.monto,
                pago.fecha_pago,
                pago.metodo_pago
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        except sqlite3.Error as e:
            print(f"Error al insertar pago: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_pago: int) -> Optional[Pago]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago WHERE id_pago = ?", (id_pago,))
            row = cursor.fetchone()
            return PagoDAO._row_to_pago(row) if row else None
        except sqlite3.Error:
            return None

    @staticmethod
    def obtener_todos() -> List[Pago]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago ORDER BY fecha_pago DESC")
            rows = cursor.fetchall()
            return [PagoDAO._row_to_pago(row) for row in rows]
        except sqlite3.Error:
            return []
    
    @staticmethod
    def obtener_por_reserva(id_reserva: int) -> List[Pago]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago WHERE id_reserva = ?", (id_reserva,))
            rows = cursor.fetchall()
            return [PagoDAO._row_to_pago(row) for row in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def obtener_por_torneo(id_torneo: int) -> List[Pago]:
        """Obtiene pagos asociados a un torneo."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pago WHERE id_torneo = ?", (id_torneo,))
            rows = cursor.fetchall()
            return [PagoDAO._row_to_pago(row) for row in rows]
        except sqlite3.Error:
            return []
    
    @staticmethod
    def _row_to_pago(row) -> Pago:
        fecha_pago = row['fecha_pago']
        if isinstance(fecha_pago, str):
            try:
                fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d').date()
            except ValueError:
                fecha_pago = date.today()
                
        # Manejo seguro de columnas nuevas/viejas
        id_torneo = None
        try: id_torneo = row['id_torneo']
        except: pass

        return Pago(
            id_pago=row['id_pago'],
            id_reserva=row['id_reserva'],
            id_torneo=id_torneo,
            monto=row['monto'],
            fecha_pago=fecha_pago,
            metodo_pago=row['metodo_pago']
        )
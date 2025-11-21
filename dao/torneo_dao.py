import sqlite3
from typing import List, Optional
from datetime import datetime, time
from models.torneo import Torneo
from database.db_connection import get_db_connection

class TorneoDAO:
    
    @staticmethod
    def insertar(torneo: Torneo) -> Optional[int]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            h_ini = torneo.hora_inicio.strftime('%H:%M:%S') if isinstance(torneo.hora_inicio, time) else torneo.hora_inicio
            h_fin = torneo.hora_fin.strftime('%H:%M:%S') if isinstance(torneo.hora_fin, time) else torneo.hora_fin
            
            query = """
                INSERT INTO torneo (nombre, deporte, fecha, hora_inicio, hora_fin, 
                                    cantidad_canchas, precio_total, estado, id_cliente)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                torneo.nombre, torneo.deporte, torneo.fecha,
                h_ini, h_fin, torneo.cantidad_canchas, 
                torneo.precio_total, torneo.estado, torneo.id_cliente
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar torneo: {e}")
            return None

    @staticmethod
    def obtener_todos() -> List[Torneo]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM torneo WHERE estado != 'cancelado' ORDER BY fecha DESC")
            rows = cursor.fetchall()
            return [TorneoDAO._row_to_torneo(row) for row in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def obtener_por_id(id_torneo: int) -> Optional[Torneo]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM torneo WHERE id_torneo = ?", (id_torneo,))
            row = cursor.fetchone()
            return TorneoDAO._row_to_torneo(row) if row else None
        except sqlite3.Error:
            return None

    @staticmethod
    def eliminar(id_torneo: int) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE torneo SET estado = 'cancelado' WHERE id_torneo = ?", (id_torneo,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def _row_to_torneo(row) -> Torneo:
        fecha = row['fecha']
        if isinstance(fecha, str):
            try: fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            except: pass
            
        def parse_h(h):
            if isinstance(h, str):
                try: return datetime.strptime(h, '%H:%M:%S').time()
                except:
                    try: return datetime.strptime(h, '%H:%M').time()
                    except: pass
            return h

        # Manejo seguro id_cliente (por si la migración falló o es viejo)
        id_cliente = None
        try: id_cliente = row['id_cliente']
        except: pass

        return Torneo(
            id_torneo=row['id_torneo'],
            nombre=row['nombre'],
            deporte=row['deporte'],
            fecha=fecha,
            hora_inicio=parse_h(row['hora_inicio']),
            hora_fin=parse_h(row['hora_fin']),
            cantidad_canchas=row['cantidad_canchas'],
            precio_total=row['precio_total'],
            estado=row['estado'],
            id_cliente=id_cliente
        )
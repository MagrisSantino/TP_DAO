"""
DAO para Cliente
"""
import sqlite3
from typing import List, Optional
from models.cliente import Cliente
from database.db_connection import get_db_connection

class ClienteDAO:
    
    @staticmethod
    def insertar(cliente: Cliente) -> Optional[int]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO cliente (nombre, apellido, dni, telefono, email, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.email, cliente.estado))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def obtener_todos() -> List[Cliente]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Solo mostramos activos por defecto o todos y filtramos en UI? 
            # Generalmente el DAO trae todo y el Service/UI filtra, o traemos ordenado.
            cursor.execute("SELECT * FROM cliente WHERE estado = 'activo' ORDER BY apellido, nombre")
            rows = cursor.fetchall()
            return [ClienteDAO._row_to_cliente(row) for row in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def obtener_por_id(id_cliente: int) -> Optional[Cliente]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cliente WHERE id_cliente = ?", (id_cliente,))
            row = cursor.fetchone()
            return ClienteDAO._row_to_cliente(row) if row else None
        except sqlite3.Error:
            return None

    @staticmethod
    def buscar(termino: str) -> List[Cliente]:
        """Busca por nombre, apellido, DNI o Email (incluyendo inactivos si es necesario buscar historial)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            termino_like = f"%{termino}%"
            query = """
                SELECT * FROM cliente 
                WHERE (nombre LIKE ? OR apellido LIKE ? OR dni LIKE ? OR email LIKE ?)
                AND estado = 'activo'
                ORDER BY apellido
            """
            cursor.execute(query, (termino_like, termino_like, termino_like, termino_like))
            rows = cursor.fetchall()
            return [ClienteDAO._row_to_cliente(row) for row in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def actualizar(cliente: Cliente) -> bool:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE cliente SET nombre=?, apellido=?, dni=?, telefono=?, email=?, estado=?
                WHERE id_cliente=?
            """
            cursor.execute(query, (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.email, cliente.estado, cliente.id_cliente))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def eliminar(id_cliente: int) -> bool:
        """
        Realiza un borrado lógico del cliente (estado = 'inactivo').
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "UPDATE cliente SET estado = 'inactivo' WHERE id_cliente = ?"
            cursor.execute(query, (id_cliente,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar cliente: {e}")
            return False

    @staticmethod
    def contar_total() -> int:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cliente WHERE estado='activo'")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    @staticmethod
    def _row_to_cliente(row) -> Cliente:
        return Cliente(
            id_cliente=row['id_cliente'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            dni=row['dni'],
            telefono=row['telefono'],
            email=row['email'],
            estado=row['estado']
        )
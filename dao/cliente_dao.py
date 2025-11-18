"""
DAO para la entidad Cliente
Operaciones CRUD sobre la tabla 'cliente'
"""

import sqlite3
from typing import List, Optional
from models.cliente import Cliente
from database.db_connection import get_db_connection


class ClienteDAO:
    """Data Access Object para Cliente"""
    
    @staticmethod
    def insertar(cliente: Cliente) -> Optional[int]:
        """
        Inserta un nuevo cliente en la base de datos.
        
        Args:
            cliente (Cliente): Objeto cliente a insertar
        
        Returns:
            int: ID del cliente insertado o None si falla
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO cliente (dni, nombre, apellido, email, telefono, fecha_registro, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                cliente.dni,
                cliente.nombre,
                cliente.apellido,
                cliente.email,
                cliente.telefono,
                cliente.fecha_registro,
                cliente.estado
            ))
            
            conn.commit()
            cliente.id_cliente = cursor.lastrowid
            return cursor.lastrowid
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al insertar cliente: {e}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar cliente: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_cliente: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID.
        
        Args:
            id_cliente (int): ID del cliente
        
        Returns:
            Cliente: Objeto cliente o None si no existe
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cliente WHERE id_cliente = ?"
            cursor.execute(query, (id_cliente,))
            
            row = cursor.fetchone()
            if row:
                return ClienteDAO._row_to_cliente(row)
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener cliente: {e}")
            return None
    
    @staticmethod
    def obtener_por_dni(dni: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su DNI.
        
        Args:
            dni (str): DNI del cliente
        
        Returns:
            Cliente: Objeto cliente o None si no existe
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cliente WHERE dni = ?"
            cursor.execute(query, (dni,))
            
            row = cursor.fetchone()
            if row:
                return ClienteDAO._row_to_cliente(row)
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener cliente por DNI: {e}")
            return None
    
    @staticmethod
    def obtener_por_email(email: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su email.
        
        Args:
            email (str): Email del cliente
        
        Returns:
            Cliente: Objeto cliente o None si no existe
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cliente WHERE email = ?"
            cursor.execute(query, (email,))
            
            row = cursor.fetchone()
            if row:
                return ClienteDAO._row_to_cliente(row)
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener cliente por email: {e}")
            return None
    
    @staticmethod
    def obtener_todos() -> List[Cliente]:
        """
        Obtiene todos los clientes.
        
        Returns:
            List[Cliente]: Lista de clientes
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cliente ORDER BY apellido, nombre"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [ClienteDAO._row_to_cliente(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener todos los clientes: {e}")
            return []
    
    @staticmethod
    def obtener_activos() -> List[Cliente]:
        """
        Obtiene solo los clientes activos.
        
        Returns:
            List[Cliente]: Lista de clientes activos
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM cliente WHERE estado = 'activo' ORDER BY apellido, nombre"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            return [ClienteDAO._row_to_cliente(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al obtener clientes activos: {e}")
            return []
    
    @staticmethod
    def actualizar(cliente: Cliente) -> bool:
        """
        Actualiza los datos de un cliente.
        
        Args:
            cliente (Cliente): Objeto cliente con datos actualizados
        
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE cliente 
                SET dni = ?, nombre = ?, apellido = ?, email = ?, 
                    telefono = ?, estado = ?
                WHERE id_cliente = ?
            """
            
            cursor.execute(query, (
                cliente.dni,
                cliente.nombre,
                cliente.apellido,
                cliente.email,
                cliente.telefono,
                cliente.estado,
                cliente.id_cliente
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al actualizar cliente: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar cliente: {e}")
            return False
    
    @staticmethod
    def eliminar(id_cliente: int) -> bool:
        """
        Elimina un cliente de la base de datos.
        ADVERTENCIA: Solo usar si no tiene reservas asociadas.
        
        Args:
            id_cliente (int): ID del cliente a eliminar
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM cliente WHERE id_cliente = ?"
            cursor.execute(query, (id_cliente,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"No se puede eliminar el cliente. Tiene reservas asociadas: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar cliente: {e}")
            return False
    
    @staticmethod
    def cambiar_estado(id_cliente: int, nuevo_estado: str) -> bool:
        """
        Cambia el estado de un cliente (activo/inactivo).
        Esta es la forma recomendada de "eliminar" un cliente.
        
        Args:
            id_cliente (int): ID del cliente
            nuevo_estado (str): 'activo' o 'inactivo'
        
        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "UPDATE cliente SET estado = ? WHERE id_cliente = ?"
            cursor.execute(query, (nuevo_estado, id_cliente))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al cambiar estado del cliente: {e}")
            return False
    
    @staticmethod
    def buscar(termino: str) -> List[Cliente]:
        """
        Busca clientes por nombre, apellido, nombre completo, DNI o email.
        
        Args:
            termino (str): Término de búsqueda
        
        Returns:
            List[Cliente]: Lista de clientes que coinciden con la búsqueda
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            termino_like = f"%{termino}%"
            
            # MODIFICACIÓN: Agregamos (nombre || ' ' || apellido) para buscar por nombre completo
            query = """
                SELECT * FROM cliente 
                WHERE nombre LIKE ? 
                   OR apellido LIKE ? 
                   OR (nombre || ' ' || apellido) LIKE ?
                   OR dni LIKE ? 
                   OR email LIKE ?
                ORDER BY apellido, nombre
            """
            
            # Debemos pasar el término 5 veces ahora (una por cada ?)
            cursor.execute(query, (
                termino_like, 
                termino_like, 
                termino_like, 
                termino_like, 
                termino_like
            ))
            
            rows = cursor.fetchall()
            return [ClienteDAO._row_to_cliente(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"Error al buscar clientes: {e}")
            return []
    
    @staticmethod
    def contar_total() -> int:
        """
        Cuenta el total de clientes en la base de datos.
        
        Returns:
            int: Número total de clientes
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM cliente"
            cursor.execute(query)
            
            return cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f"Error al contar clientes: {e}")
            return 0
    
    @staticmethod
    def contar_activos() -> int:
        """
        Cuenta el total de clientes activos.
        
        Returns:
            int: Número de clientes activos
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM cliente WHERE estado = 'activo'"
            cursor.execute(query)
            
            return cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f"Error al contar clientes activos: {e}")
            return 0
    
    @staticmethod
    def _row_to_cliente(row) -> Cliente:
        """
        Convierte una fila de la BD en un objeto Cliente.
        
        Args:
            row: Fila de la base de datos
        
        Returns:
            Cliente: Objeto cliente
        """
        return Cliente(
            id_cliente=row['id_cliente'],
            dni=row['dni'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            email=row['email'],
            telefono=row['telefono'],
            fecha_registro=row['fecha_registro'],
            estado=row['estado']
        )
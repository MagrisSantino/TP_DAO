"""
Módulo para gestionar la conexión a la base de datos SQLite
"""

import sqlite3
import os
from config import DB_PATH


class DatabaseConnection:
    """
    Clase singleton para gestionar la conexión a la base de datos.
    Garantiza que solo exista una instancia de conexión.
    """
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión si no existe"""
        self.db_path = DB_PATH
        if self._connection is None:
            self._connect()
    
    def _connect(self):
        """Establece la conexión con la base de datos"""
        try:
            # Crear el directorio database si no existe
            db_dir = os.path.dirname(DB_PATH)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # Conectar a la base de datos
            self._connection = sqlite3.connect(DB_PATH, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
            print(f"✓ Conexión establecida con la base de datos: {DB_PATH}")
            
            # Inicializar el schema si es necesario
            self._initialize_schema()
            
        except sqlite3.Error as e:
            print(f"✗ Error al conectar con la base de datos: {e}")
            raise
    
    def _initialize_schema(self):
        """Inicializa el schema de la base de datos si no existe"""
        try:
            schema_path = os.path.join(os.path.dirname(DB_PATH), 'schema.sql')
            
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                cursor = self._connection.cursor()
                cursor.executescript(schema_sql)
                self._connection.commit()
                print("✓ Schema de base de datos inicializado correctamente")
            else:
                print(f"⚠ Advertencia: No se encontró el archivo schema.sql en {schema_path}")
                
        except Exception as e:
            print(f"✗ Error al inicializar el schema: {e}")
            raise
    
    def get_connection(self):
        """Retorna la conexión activa"""
        if self._connection is None:
            self._connect()
        return self._connection
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("✓ Conexión cerrada")
    
    def commit(self):
        """Realiza commit de las transacciones pendientes"""
        if self._connection:
            self._connection.commit()
    
    def rollback(self):
        """Realiza rollback de las transacciones pendientes"""
        if self._connection:
            self._connection.rollback()


def get_db_connection():
    """
    Función auxiliar para obtener la conexión a la base de datos.
    Retorna la conexión singleton.
    """
    db = DatabaseConnection()
    return db.get_connection()


def close_db_connection():
    """
    Función auxiliar para cerrar la conexión a la base de datos.
    """
    db = DatabaseConnection()
    db.close()


# Función para ejecutar consultas SELECT
def execute_query(query, params=()):
    """
    Ejecuta una consulta SELECT y retorna los resultados.
    
    Args:
        query (str): Consulta SQL
        params (tuple): Parámetros de la consulta
    
    Returns:
        list: Lista de resultados
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error en execute_query: {e}")
        raise


# Función para ejecutar consultas INSERT, UPDATE, DELETE
def execute_update(query, params=()):
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE.
    
    Args:
        query (str): Consulta SQL
        params (tuple): Parámetros de la consulta
    
    Returns:
        int: ID del último registro insertado (para INSERT) o filas afectadas
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error en execute_update: {e}")
        raise


# Función para insertar datos de prueba
def insert_test_data():
    """Inserta datos de prueba en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM cliente")
        if cursor.fetchone()[0] > 0:
            print("⚠ Ya existen datos en la base de datos")
            return
        
        print("Insertando datos de prueba...")
        
        # Insertar clientes de prueba
        clientes = [
            ('12345678', 'Juan', 'Pérez', 'juan.perez@email.com', '351-1234567', 'activo'),
            ('87654321', 'María', 'González', 'maria.gonzalez@email.com', '351-7654321', 'activo'),
            ('11223344', 'Carlos', 'López', 'carlos.lopez@email.com', '351-1122334', 'activo'),
            ('44332211', 'Ana', 'Martínez', 'ana.martinez@email.com', '351-4433221', 'activo'),
            ('55667788', 'Luis', 'Rodríguez', 'luis.rodriguez@email.com', '351-5566778', 'activo'),
        ]
        
        cursor.executemany(
            """INSERT INTO cliente (dni, nombre, apellido, email, telefono, estado) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            clientes
        )
        
        # Insertar canchas de prueba
        canchas = [
            ('Cancha 1', 'Fútbol 5', 'Césped sintético', 0, 1, 10, 5000.0, 7000.0, 'disponible'),
            ('Cancha 2', 'Fútbol 5', 'Césped sintético', 1, 1, 10, 6000.0, 8000.0, 'disponible'),
            ('Cancha 3', 'Fútbol 7', 'Césped natural', 0, 1, 14, 7000.0, 9000.0, 'disponible'),
            ('Cancha 4', 'Paddle', 'Cemento', 0, 1, 4, 3000.0, 4000.0, 'disponible'),
            ('Cancha 5', 'Tenis', 'Polvo de ladrillo', 0, 1, 2, 3500.0, 4500.0, 'disponible'),
            ('Cancha 6', 'Básquet', 'Parquet', 1, 1, 10, 5500.0, 7500.0, 'mantenimiento'),
        ]
        
        cursor.executemany(
            """INSERT INTO cancha (nombre, tipo_deporte, tipo_superficie, techada, iluminacion, 
               capacidad_jugadores, precio_hora_dia, precio_hora_noche, estado) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            canchas
        )
        
        # Insertar algunas reservas de ejemplo
        reservas = [
            (1, 1, '2025-10-27', '10:00', '11:00', 0, 'confirmada', 5000.0, 'Reserva de prueba'),
            (2, 2, '2025-10-27', '15:00', '16:00', 0, 'confirmada', 6000.0, ''),
            (3, 1, '2025-10-28', '19:00', '20:00', 1, 'pendiente', 8000.0, 'Incluye iluminación'),
        ]
        
        cursor.executemany(
            """INSERT INTO reserva (id_cliente, id_cancha, fecha_reserva, hora_inicio, hora_fin, 
               usa_iluminacion, estado_reserva, monto_total, observaciones) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            reservas
        )
        
        conn.commit()
        print("✓ Datos de prueba insertados correctamente")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"✗ Error al insertar datos de prueba: {e}")
        raise


if __name__ == "__main__":
    # Test de conexión
    print("=== Probando conexión a la base de datos ===")
    try:
        db = DatabaseConnection()
        conn = db.get_connection()
        print("✓ Conexión exitosa")
        
        # Insertar datos de prueba
        insert_test_data()
        
        # Probar una consulta
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cliente")
        count = cursor.fetchone()[0]
        print(f"✓ Total de clientes en la base de datos: {count}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
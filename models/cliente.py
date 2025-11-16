"""
Modelo Cliente - Representa un cliente del sistema
"""

from datetime import date


class Cliente:
    """
    Clase que representa un cliente del complejo deportivo.
    Corresponde a la tabla 'cliente' en la base de datos.
    """
    
    def __init__(self, id_cliente=None, dni='', nombre='', apellido='', 
                 email='', telefono='', fecha_registro=None, estado='activo'):
        """
        Constructor de la clase Cliente.
        
        Args:
            id_cliente (int): ID único del cliente (generado por la BD)
            dni (str): Documento Nacional de Identidad
            nombre (str): Nombre del cliente
            apellido (str): Apellido del cliente
            email (str): Email del cliente
            telefono (str): Teléfono de contacto
            fecha_registro (date): Fecha de registro en el sistema
            estado (str): Estado del cliente ('activo' o 'inactivo')
        """
        self.id_cliente = id_cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro if fecha_registro else date.today()
        self.estado = estado
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        return f"{self.nombre} {self.apellido}"
    
    def esta_activo(self):
        """Verifica si el cliente está activo"""
        return self.estado == 'activo'
    
    def __str__(self):
        """Representación en string del cliente"""
        return f"Cliente: {self.get_nombre_completo()} (DNI: {self.dni})"
    
    def __repr__(self):
        """Representación para debugging"""
        return (f"Cliente(id={self.id_cliente}, dni='{self.dni}', "
                f"nombre='{self.nombre}', apellido='{self.apellido}')")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_cliente': self.id_cliente,
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': str(self.fecha_registro) if self.fecha_registro else None,
            'estado': self.estado
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea una instancia de Cliente desde un diccionario.
        Útil para convertir datos de la BD en objetos.
        
        Args:
            data (dict): Diccionario con los datos del cliente
        
        Returns:
            Cliente: Instancia de Cliente
        """
        return Cliente(
            id_cliente=data.get('id_cliente'),
            dni=data.get('dni', ''),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            email=data.get('email', ''),
            telefono=data.get('telefono', ''),
            fecha_registro=data.get('fecha_registro'),
            estado=data.get('estado', 'activo')
        )
"""
Servicio de Clientes - Lógica de Negocio
"""

from typing import Tuple, Optional, List
from datetime import date
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO
from utils.validaciones import validar_dni, validar_email, validar_telefono


class ClienteService:
    """Servicio para gestión de clientes con validaciones"""
    
    @staticmethod
    def crear_cliente(dni: str, nombre: str, apellido: str, 
                     email: str, telefono: str) -> Tuple[bool, str, Optional[Cliente]]:
        """
        Crea un nuevo cliente con validaciones.
        
        Returns:
            Tuple (éxito, mensaje, cliente)
        """
        # Validar DNI
        if not validar_dni(dni):
            return False, "DNI inválido. Debe tener 7-8 dígitos numéricos", None
        
        # Verificar DNI único
        if ClienteDAO.obtener_por_dni(dni):
            return False, "Ya existe un cliente con ese DNI", None
        
        # Validar email
        if not validar_email(email):
            return False, "Email inválido", None
        
        # Verificar email único
        if ClienteDAO.obtener_por_email(email):
            return False, "Ya existe un cliente con ese email", None
        
        # Validar teléfono
        if not validar_telefono(telefono):
            return False, "Teléfono inválido", None
        
        # Validar nombre y apellido
        if not nombre or len(nombre.strip()) < 2:
            return False, "El nombre debe tener al menos 2 caracteres", None
        
        if not apellido or len(apellido.strip()) < 2:
            return False, "El apellido debe tener al menos 2 caracteres", None
        
        # Crear cliente
        cliente = Cliente(
            dni=dni.strip(),
            nombre=nombre.strip().title(),
            apellido=apellido.strip().title(),
            email=email.strip().lower(),
            telefono=telefono.strip(),
            fecha_registro=date.today(),
            estado='activo'
        )
        
        # Guardar en BD
        id_cliente = ClienteDAO.insertar(cliente)
        if id_cliente:
            return True, "Cliente creado exitosamente", cliente
        else:
            return False, "Error al guardar el cliente", None
    
    @staticmethod
    def modificar_cliente(id_cliente: int, dni: str = None, nombre: str = None,
                         apellido: str = None, email: str = None, 
                         telefono: str = None) -> Tuple[bool, str]:
        """
        Modifica un cliente existente.
        
        Returns:
            Tuple (éxito, mensaje)
        """
        # Obtener cliente actual
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return False, "Cliente no encontrado"
        
        # Actualizar solo los campos proporcionados
        if dni is not None:
            if not validar_dni(dni):
                return False, "DNI inválido"
            # Verificar que no exista otro cliente con ese DNI
            cliente_existente = ClienteDAO.obtener_por_dni(dni)
            if cliente_existente and cliente_existente.id_cliente != id_cliente:
                return False, "Ya existe otro cliente con ese DNI"
            cliente.dni = dni.strip()
        
        if nombre is not None:
            if len(nombre.strip()) < 2:
                return False, "El nombre debe tener al menos 2 caracteres"
            cliente.nombre = nombre.strip().title()
        
        if apellido is not None:
            if len(apellido.strip()) < 2:
                return False, "El apellido debe tener al menos 2 caracteres"
            cliente.apellido = apellido.strip().title()
        
        if email is not None:
            if not validar_email(email):
                return False, "Email inválido"
            # Verificar que no exista otro cliente con ese email
            cliente_existente = ClienteDAO.obtener_por_email(email)
            if cliente_existente and cliente_existente.id_cliente != id_cliente:
                return False, "Ya existe otro cliente con ese email"
            cliente.email = email.strip().lower()
        
        if telefono is not None:
            if not validar_telefono(telefono):
                return False, "Teléfono inválido"
            cliente.telefono = telefono.strip()
        
        # Actualizar en BD
        if ClienteDAO.actualizar(cliente):
            return True, "Cliente modificado exitosamente"
        return False, "Error al modificar el cliente"
    
    @staticmethod
    def desactivar_cliente(id_cliente: int) -> Tuple[bool, str]:
        """Desactiva un cliente (baja lógica)."""
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return False, "Cliente no encontrado"
        
        if ClienteDAO.cambiar_estado(id_cliente, 'inactivo'):
            return True, "Cliente desactivado"
        return False, "Error al desactivar el cliente"
    
    @staticmethod
    def activar_cliente(id_cliente: int) -> Tuple[bool, str]:
        """Activa un cliente."""
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return False, "Cliente no encontrado"
        
        if ClienteDAO.cambiar_estado(id_cliente, 'activo'):
            return True, "Cliente activado"
        return False, "Error al activar el cliente"
    
    @staticmethod
    def obtener_cliente(id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por ID."""
        return ClienteDAO.obtener_por_id(id_cliente)
    
    @staticmethod
    def obtener_todos_clientes() -> List[Cliente]:
        """Obtiene todos los clientes."""
        return ClienteDAO.obtener_todos()
    
    @staticmethod
    def obtener_clientes_activos() -> List[Cliente]:
        """Obtiene solo clientes activos."""
        return ClienteDAO.obtener_activos()
    
    @staticmethod
    def buscar_clientes(termino: str) -> List[Cliente]:
        """Busca clientes por nombre, apellido, DNI o email."""
        return ClienteDAO.buscar(termino)
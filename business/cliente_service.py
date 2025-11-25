"""
Servicio de Cliente
"""
from typing import List, Tuple, Optional
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO
from utils.validaciones import validar_dni, validar_email, validar_telefono

class ClienteService:
    
    @staticmethod
    def crear_cliente(nombre, apellido, dni, telefono, email) -> Tuple[bool, str, Optional[Cliente]]:
        if not all([nombre, apellido, dni]):
            return False, "Complete los campos obligatorios", None
            
        if not validar_dni(dni):
            return False, "DNI inválido", None
            
        if email and not validar_email(email):
            return False, "Email inválido", None
        
        if telefono and not validar_telefono(telefono):
            return False, "Telefono invalido", None

        nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, dni=dni, telefono=telefono, email=email)
        id_gen = ClienteDAO.insertar(nuevo_cliente)
        
        if id_gen:
            nuevo_cliente.id_cliente = id_gen
            return True, "Cliente creado exitosamente", nuevo_cliente
        return False, "Error al crear cliente (Posible DNI duplicado)", None

    @staticmethod
    def obtener_todos() -> List[Cliente]:
        return ClienteDAO.obtener_todos()

    @staticmethod
    def buscar_clientes(termino: str) -> List[Cliente]:
        return ClienteDAO.buscar(termino)

    @staticmethod
    def obtener_cliente(id_cliente: int) -> Optional[Cliente]:
        return ClienteDAO.obtener_por_id(id_cliente)
    
    @staticmethod
    def obtener_clientes_activos() -> List[Cliente]:
        return ClienteDAO.obtener_todos()

    @staticmethod
    def actualizar_cliente(id_cliente, nombre, apellido, dni, telefono, email, estado) -> Tuple[bool, str]:
        if not all([nombre, apellido, dni]):
            return False, "Campos obligatorios vacíos"
            
        cliente = Cliente(id_cliente=id_cliente, nombre=nombre, apellido=apellido, dni=dni, telefono=telefono, email=email, estado=estado)
        
        if ClienteDAO.actualizar(cliente):
            return True, "Cliente actualizado correctamente"
        return False, "Error al actualizar cliente"

    @staticmethod
    def eliminar_cliente(id_cliente: int) -> Tuple[bool, str]:
        """
        Desactiva un cliente (Borrado lógico).
        """
        # Aquí se podría verificar si tiene deuda antes de borrar, pero asumimos que se puede desactivar.
        if ClienteDAO.eliminar(id_cliente):
            return True, "Cliente eliminado correctamente (Estado Inactivo)."
        return False, "No se pudo eliminar el cliente."
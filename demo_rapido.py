"""
Demo Rápido del Sistema
Muestra las funcionalidades principales de forma interactiva
"""

from datetime import date, time, timedelta
from database.db_connection import DatabaseConnection
from business.cliente_service import ClienteService
from business.cancha_service import CanchaService
from business.reserva_service import ReservaService
from business.pago_service import PagoService
from utils.helpers import formatear_fecha, formatear_hora, formatear_monto


def demo():
    """Ejecuta una demostración rápida del sistema"""
    
    print("\n" + "=" * 70)
    print("DEMO RÁPIDO - SISTEMA DE RESERVAS DE CANCHAS")
    print("=" * 70)
    
    # 1. Inicializar BD
    print("\n1. Inicializando base de datos...")
    db = DatabaseConnection()
    print(f"   ✓ Base de datos lista")
    
    # 2. Crear un cliente
    print("\n2. Creando un cliente de ejemplo...")
    exito, msg, cliente = ClienteService.crear_cliente(
        dni="40123456",
        nombre="María",
        apellido="González",
        email="maria.gonzalez@email.com",
        telefono="351-9876543"
    )
    
    if not exito:
        print(f"   ✗ Error: {msg}")
        # Intentar buscar cliente existente
        clientes = ClienteService.buscar_clientes("González")
        if clientes:
            cliente = clientes[0]
            print(f"   ℹ Usando cliente existente: {cliente.get_nombre_completo()}")
        else:
            print("   ✗ No se pudo crear o encontrar el cliente. Abortando demo.")
            return
    else:
        print(f"   ✓ Cliente creado: {cliente.get_nombre_completo()}")
        print(f"     ID: {cliente.id_cliente}")
        print(f"     Email: {cliente.email}")
    
    # 3. Crear una cancha
    print("\n3. Creando una cancha de ejemplo...")
    exito, msg, cancha = CanchaService.crear_cancha(
        nombre="Cancha Demo",
        tipo_deporte="Fútbol 5",
        tipo_superficie="Césped sintético",
        techada=False,
        iluminacion=True,
        capacidad_jugadores=10,
        precio_hora_dia=8000.0,
        precio_hora_noche=10000.0
    )
    
    if not exito:
        print(f"   ✗ Error: {msg}")
        # Intentar usar una cancha existente
        canchas = CanchaService.obtener_canchas_disponibles()
        if canchas:
            cancha = canchas[0]
            print(f"   ℹ Usando cancha existente: {cancha.nombre}")
        else:
            print("   ✗ No hay canchas disponibles. Abortando demo.")
            return
    else:
        print(f"   ✓ Cancha creada: {cancha.nombre}")
        print(f"     Precio día: {formatear_monto(cancha.precio_hora_dia)}")
        print(f"     Precio noche: {formatear_monto(cancha.precio_hora_noche)}")
    
    # 4. Crear una reserva
    print("\n4. Creando una reserva de ejemplo...")
    fecha_reserva = date.today() + timedelta(days=2)
    hora_inicio = time(15, 0)
    hora_fin = time(17, 0)
    
    exito, msg, reserva = ReservaService.crear_reserva(
        id_cliente=cliente.id_cliente,
        id_cancha=cancha.id_cancha,
        fecha_reserva=fecha_reserva,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        usa_iluminacion=False
    )
    
    if not exito:
        print(f"   ✗ Error: {msg}")
        return
    
    print(f"   ✓ Reserva creada (ID: {reserva.id_reserva})")
    print(f"     Fecha: {formatear_fecha(reserva.fecha_reserva)}")
    print(f"     Horario: {formatear_hora(reserva.hora_inicio)} - {formatear_hora(reserva.hora_fin)}")
    print(f"     Duración: {reserva.calcular_duracion_horas()} horas")
    print(f"     Monto: {formatear_monto(reserva.monto_total)}")
    print(f"     Estado: {reserva.estado_reserva}")
    
    # 5. Registrar un pago
    print("\n5. Registrando un pago...")
    exito, msg, pago = PagoService.registrar_pago(
        id_reserva=reserva.id_reserva,
        monto=reserva.monto_total,
        metodo_pago="transferencia"
    )
    
    if not exito:
        print(f"   ✗ Error: {msg}")
    else:
        print(f"   ✓ Pago registrado (ID: {pago.id_pago})")
        print(f"     Monto: {formatear_monto(pago.monto)}")
        print(f"     Método: {pago.metodo_pago}")
        
        # Verificar estado del pago
        esta_pagada, total, pagado = PagoService.verificar_pago_completo(reserva.id_reserva)
        if esta_pagada:
            print(f"   ✓ Reserva pagada completamente")
    
    # 6. Listar datos
    print("\n6. Resumen del sistema:")
    
    from dao.cliente_dao import ClienteDAO
    from dao.cancha_dao import CanchaDAO
    from dao.reserva_dao import ReservaDAO
    
    total_clientes = ClienteDAO.contar_total()
    total_canchas = CanchaDAO.contar_total()
    total_reservas = ReservaDAO.contar_total()
    
    print(f"   - Clientes en sistema: {total_clientes}")
    print(f"   - Canchas disponibles: {total_canchas}")
    print(f"   - Reservas totales: {total_reservas}")
    
    # 7. Mostrar horarios disponibles
    print(f"\n7. Horarios disponibles para {cancha.nombre} mañana:")
    horarios = ReservaService.obtener_horarios_disponibles(
        cancha.id_cancha, 
        date.today() + timedelta(days=1)
    )
    
    if horarios:
        print(f"   Hay {len(horarios)} bloques disponibles:")
        for inicio, fin in horarios[:5]:  # Mostrar solo los primeros 5
            print(f"     - {formatear_hora(inicio)} a {formatear_hora(fin)}")
    else:
        print("   No hay horarios disponibles")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\nPuedes ejecutar 'python main.py' para usar el sistema completo")
    print("O ejecutar 'python test_sistema.py' para ver todas las pruebas\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error durante la demo: {e}")
        import traceback
        traceback.print_exc()
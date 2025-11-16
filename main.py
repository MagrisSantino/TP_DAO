"""
Sistema de Reservas de Canchas Deportivas
Punto de entrada de la aplicación
"""

import sys
from database.db_connection import DatabaseConnection


def main():
    """Función principal"""
    print("=" * 60)
    print("SISTEMA DE RESERVAS DE CANCHAS DEPORTIVAS")
    print("=" * 60)
    print()
    
    # Inicializar base de datos
    print("Inicializando base de datos...")
    try:
        db = DatabaseConnection()
        print("✓ Base de datos inicializada correctamente")
        print(f"✓ Ubicación: {db.db_path}")
        print()
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        sys.exit(1)
    
    # Menú principal
    while True:
        print("\n" + "=" * 60)
        print("MENÚ PRINCIPAL")
        print("=" * 60)
        print("1. Gestión de Clientes")
        print("2. Gestión de Canchas")
        print("3. Gestión de Reservas")
        print("4. Gestión de Pagos")
        print("5. Gestión de Torneos")
        print("6. Reportes")
        print("7. Salir")
        print("=" * 60)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_canchas()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "4":
            menu_pagos()
        elif opcion == "5":
            menu_torneos()
        elif opcion == "6":
            menu_reportes()
        elif opcion == "7":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n✗ Opción inválida. Intente nuevamente.")


def menu_clientes():
    """Menú de gestión de clientes"""
    from business.cliente_service import ClienteService
    
    while True:
        print("\n" + "-" * 60)
        print("GESTIÓN DE CLIENTES")
        print("-" * 60)
        print("1. Listar clientes")
        print("2. Crear cliente")
        print("3. Buscar cliente")
        print("4. Volver")
        print("-" * 60)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            clientes = ClienteService.obtener_todos_clientes()
            print(f"\n{'ID':<5} {'DNI':<10} {'Nombre':<20} {'Email':<30} {'Estado':<10}")
            print("-" * 80)
            for c in clientes:
                print(f"{c.id_cliente:<5} {c.dni:<10} {c.get_nombre_completo():<20} {c.email:<30} {c.estado:<10}")
        
        elif opcion == "2":
            print("\n--- NUEVO CLIENTE ---")
            dni = input("DNI: ").strip()
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            
            exito, mensaje, cliente = ClienteService.crear_cliente(dni, nombre, apellido, email, telefono)
            if exito:
                print(f"\n✓ {mensaje}")
                print(f"  Cliente ID: {cliente.id_cliente}")
            else:
                print(f"\n✗ {mensaje}")
        
        elif opcion == "3":
            termino = input("\nIngrese término de búsqueda: ").strip()
            clientes = ClienteService.buscar_clientes(termino)
            
            if clientes:
                print(f"\n{'ID':<5} {'DNI':<10} {'Nombre':<20} {'Email':<30}")
                print("-" * 70)
                for c in clientes:
                    print(f"{c.id_cliente:<5} {c.dni:<10} {c.get_nombre_completo():<20} {c.email:<30}")
            else:
                print("\nNo se encontraron clientes.")
        
        elif opcion == "4":
            break
        else:
            print("\n✗ Opción inválida.")


def menu_canchas():
    """Menú de gestión de canchas"""
    from business.cancha_service import CanchaService
    
    while True:
        print("\n" + "-" * 60)
        print("GESTIÓN DE CANCHAS")
        print("-" * 60)
        print("1. Listar canchas")
        print("2. Crear cancha")
        print("3. Ver canchas disponibles")
        print("4. Volver")
        print("-" * 60)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            canchas = CanchaService.obtener_todas_canchas()
            print(f"\n{'ID':<5} {'Nombre':<20} {'Deporte':<15} {'Precio Día':<12} {'Estado':<15}")
            print("-" * 75)
            for c in canchas:
                print(f"{c.id_cancha:<5} {c.nombre:<20} {c.tipo_deporte:<15} ${c.precio_hora_dia:<11.2f} {c.estado:<15}")
        
        elif opcion == "2":
            print("\n--- NUEVA CANCHA ---")
            nombre = input("Nombre: ").strip()
            tipo_deporte = input("Deporte: ").strip()
            tipo_superficie = input("Superficie: ").strip()
            techada = input("¿Techada? (s/n): ").strip().lower() == 's'
            iluminacion = input("¿Tiene iluminación? (s/n): ").strip().lower() == 's'
            capacidad = int(input("Capacidad de jugadores: "))
            precio_dia = float(input("Precio hora día: "))
            precio_noche = float(input("Precio hora noche: "))
            
            exito, mensaje, cancha = CanchaService.crear_cancha(
                nombre, tipo_deporte, tipo_superficie, techada, 
                iluminacion, capacidad, precio_dia, precio_noche
            )
            
            if exito:
                print(f"\n✓ {mensaje}")
                print(f"  Cancha ID: {cancha.id_cancha}")
            else:
                print(f"\n✗ {mensaje}")
        
        elif opcion == "3":
            canchas = CanchaService.obtener_canchas_disponibles()
            print(f"\n{'ID':<5} {'Nombre':<20} {'Deporte':<15} {'Precio Día':<12}")
            print("-" * 55)
            for c in canchas:
                print(f"{c.id_cancha:<5} {c.nombre:<20} {c.tipo_deporte:<15} ${c.precio_hora_dia:<11.2f}")
        
        elif opcion == "4":
            break
        else:
            print("\n✗ Opción inválida.")


def menu_reservas():
    """Menú de gestión de reservas"""
    from business.reserva_service import ReservaService
    from dao.reserva_dao import ReservaDAO
    from datetime import date, time
    
    while True:
        print("\n" + "-" * 60)
        print("GESTIÓN DE RESERVAS")
        print("-" * 60)
        print("1. Listar todas las reservas")
        print("2. Crear reserva")
        print("3. Ver reservas de hoy")
        print("4. Confirmar reserva")
        print("5. Cancelar reserva")
        print("6. Volver")
        print("-" * 60)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            reservas = ReservaDAO.obtener_todas()
            print(f"\n{'ID':<5} {'Cliente ID':<12} {'Cancha ID':<11} {'Fecha':<12} {'Hora':<12} {'Estado':<15}")
            print("-" * 75)
            for r in reservas:
                hora = f"{r.hora_inicio}-{r.hora_fin}"
                print(f"{r.id_reserva:<5} {r.id_cliente:<12} {r.id_cancha:<11} {r.fecha_reserva} {hora:<12} {r.estado_reserva:<15}")
        
        elif opcion == "2":
            print("\n--- NUEVA RESERVA ---")
            id_cliente = int(input("ID Cliente: "))
            id_cancha = int(input("ID Cancha: "))
            fecha_str = input("Fecha (YYYY-MM-DD): ")
            hora_inicio_str = input("Hora inicio (HH:MM): ")
            hora_fin_str = input("Hora fin (HH:MM): ")
            usa_ilum = input("¿Usa iluminación? (s/n): ").strip().lower() == 's'
            obs = input("Observaciones: ").strip()
            
            from utils.helpers import parsear_fecha, parsear_hora
            fecha = parsear_fecha(fecha_str, "%Y-%m-%d")
            hora_inicio = parsear_hora(hora_inicio_str)
            hora_fin = parsear_hora(hora_fin_str)
            
            if fecha and hora_inicio and hora_fin:
                exito, mensaje, reserva = ReservaService.crear_reserva(
                    id_cliente, id_cancha, fecha, hora_inicio, hora_fin, usa_ilum, obs
                )
                
                if exito:
                    print(f"\n✓ {mensaje}")
                    print(f"  Reserva ID: {reserva.id_reserva}")
                    print(f"  Monto total: ${reserva.monto_total:.2f}")
                else:
                    print(f"\n✗ {mensaje}")
            else:
                print("\n✗ Fecha u hora inválida.")
        
        elif opcion == "3":
            reservas = ReservaDAO.obtener_por_fecha(date.today())
            print(f"\n{'ID':<5} {'Cliente ID':<12} {'Cancha ID':<11} {'Hora':<12} {'Estado':<15}")
            print("-" * 60)
            for r in reservas:
                hora = f"{r.hora_inicio}-{r.hora_fin}"
                print(f"{r.id_reserva:<5} {r.id_cliente:<12} {r.id_cancha:<11} {hora:<12} {r.estado_reserva:<15}")
        
        elif opcion == "4":
            id_reserva = int(input("\nID de la reserva: "))
            exito, mensaje = ReservaService.confirmar_reserva(id_reserva)
            print(f"\n{'✓' if exito else '✗'} {mensaje}")
        
        elif opcion == "5":
            id_reserva = int(input("\nID de la reserva: "))
            exito, mensaje = ReservaService.cancelar_reserva(id_reserva)
            print(f"\n{'✓' if exito else '✗'} {mensaje}")
        
        elif opcion == "6":
            break
        else:
            print("\n✗ Opción inválida.")


def menu_pagos():
    """Menú de gestión de pagos"""
    from business.pago_service import PagoService
    
    print("\n--- GESTIÓN DE PAGOS ---")
    print("(Funcionalidad básica - extender según necesidad)")
    input("\nPresione Enter para continuar...")


def menu_torneos():
    """Menú de gestión de torneos"""
    from business.torneo_service import TorneoService
    
    print("\n--- GESTIÓN DE TORNEOS ---")
    print("(Funcionalidad básica - extender según necesidad)")
    input("\nPresione Enter para continuar...")


def menu_reportes():
    """Menú de reportes"""
    from business.reportes_service import ReportesService
    
    print("\n--- REPORTES ---")
    print("(Funcionalidad básica - extender según necesidad)")
    input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
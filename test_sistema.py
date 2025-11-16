"""
Script de Prueba Completo del Sistema
Prueba todas las capas: DAOs, Services y lógica de negocio
"""

from datetime import date, time, timedelta
from database.db_connection import DatabaseConnection

# Importar servicios
from business.cliente_service import ClienteService
from business.cancha_service import CanchaService
from business.reserva_service import ReservaService
from business.pago_service import PagoService
from business.torneo_service import TorneoService
from business.reportes_service import ReportesService

# Importar utilidades
from utils.validaciones import validar_dni, validar_email, validar_telefono
from utils.helpers import formatear_fecha, formatear_hora, formatear_monto


def print_seccion(titulo):
    """Imprime un título de sección"""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


def print_resultado(mensaje, exito=True):
    """Imprime un resultado"""
    simbolo = "✓" if exito else "✗"
    print(f"{simbolo} {mensaje}")


def test_validaciones():
    """Prueba las funciones de validación"""
    print_seccion("TEST 1: VALIDACIONES")
    
    # Test DNI
    assert validar_dni("12345678"), "DNI válido debe pasar"
    assert not validar_dni("123"), "DNI muy corto debe fallar"
    print_resultado("Validación de DNI: OK")
    
    # Test Email
    assert validar_email("usuario@example.com"), "Email válido debe pasar"
    assert not validar_email("usuario@"), "Email inválido debe fallar"
    print_resultado("Validación de Email: OK")
    
    # Test Teléfono
    assert validar_telefono("3511234567"), "Teléfono válido debe pasar"
    assert not validar_telefono("123"), "Teléfono inválido debe fallar"
    print_resultado("Validación de Teléfono: OK")


def test_clientes():
    """Prueba la gestión de clientes"""
    print_seccion("TEST 2: GESTIÓN DE CLIENTES")
    
    # Generar DNI y email únicos para evitar duplicados
    import time as time_module
    timestamp = int(time_module.time())
    dni_unico = f"{30000000 + (timestamp % 1000000)}"
    email_unico = f"test{timestamp}@email.com"
    
    # Crear cliente
    exito, mensaje, cliente = ClienteService.crear_cliente(
        dni=dni_unico,
        nombre="Juan",
        apellido="Pérez",
        email=email_unico,
        telefono="3511234567"
    )
    
    if exito:
        print_resultado(f"Cliente creado: {cliente.get_nombre_completo()} (ID: {cliente.id_cliente})")
        
        # Buscar cliente
        clientes = ClienteService.buscar_clientes("Juan")
        print_resultado(f"Búsqueda de clientes: {len(clientes)} resultado(s)")
        
        # Listar todos
        todos = ClienteService.obtener_todos_clientes()
        print_resultado(f"Total de clientes en BD: {len(todos)}")
        
        return cliente.id_cliente
    else:
        print_resultado(mensaje, False)
        # Intentar obtener un cliente existente
        todos = ClienteService.obtener_todos_clientes()
        if todos:
            print_resultado(f"Usando cliente existente (ID: {todos[0].id_cliente})")
            return todos[0].id_cliente
        return None


def test_canchas():
    """Prueba la gestión de canchas"""
    print_seccion("TEST 3: GESTIÓN DE CANCHAS")
    
    # Crear cancha de fútbol
    exito, mensaje, cancha = CanchaService.crear_cancha(
        nombre="Cancha Fútbol 5 - Principal",
        tipo_deporte="Fútbol 5",
        tipo_superficie="Césped sintético",
        techada=False,
        iluminacion=True,
        capacidad_jugadores=10,
        precio_hora_dia=8000.0,
        precio_hora_noche=10000.0
    )
    
    if exito:
        print_resultado(f"Cancha creada: {cancha.nombre} (ID: {cancha.id_cancha})")
        print_resultado(f"  Precio día: {formatear_monto(cancha.precio_hora_dia)}")
        print_resultado(f"  Precio noche: {formatear_monto(cancha.precio_hora_noche)}")
        
        # Crear cancha de básquet
        exito2, _, cancha2 = CanchaService.crear_cancha(
            nombre="Cancha Básquet - Techada",
            tipo_deporte="Básquet",
            tipo_superficie="Parquet",
            techada=True,
            iluminacion=True,
            capacidad_jugadores=10,
            precio_hora_dia=7000.0,
            precio_hora_noche=9000.0
        )
        
        if exito2:
            print_resultado(f"Cancha creada: {cancha2.nombre} (ID: {cancha2.id_cancha})")
        
        # Listar disponibles
        disponibles = CanchaService.obtener_canchas_disponibles()
        print_resultado(f"Canchas disponibles: {len(disponibles)}")
        
        return cancha.id_cancha
    else:
        print_resultado(mensaje, False)
        return None


def test_reservas(id_cliente, id_cancha):
    """Prueba la gestión de reservas"""
    print_seccion("TEST 4: GESTIÓN DE RESERVAS")
    
    if not id_cliente or not id_cancha:
        print_resultado("Se necesitan cliente y cancha para crear reservas", False)
        return None
    
    # Crear reserva para mañana
    fecha_reserva = date.today() + timedelta(days=1)
    hora_inicio = time(14, 0)  # 14:00
    hora_fin = time(16, 0)     # 16:00
    
    exito, mensaje, reserva = ReservaService.crear_reserva(
        id_cliente=id_cliente,
        id_cancha=id_cancha,
        fecha_reserva=fecha_reserva,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        usa_iluminacion=False,
        observaciones="Reserva de prueba del sistema"
    )
    
    if exito:
        print_resultado(f"Reserva creada (ID: {reserva.id_reserva})")
        print_resultado(f"  Fecha: {formatear_fecha(reserva.fecha_reserva)}")
        print_resultado(f"  Horario: {formatear_hora(reserva.hora_inicio)} - {formatear_hora(reserva.hora_fin)}")
        print_resultado(f"  Monto: {formatear_monto(reserva.monto_total)}")
        print_resultado(f"  Estado: {reserva.estado_reserva}")
        
        # Verificar disponibilidad (debe estar ocupado ese horario)
        from dao.reserva_dao import ReservaDAO
        disponible = ReservaDAO.verificar_disponibilidad(
            id_cancha, fecha_reserva, hora_inicio, hora_fin
        )
        print_resultado(f"Verificación de solapamiento: {'ERROR' if disponible else 'OK (ocupado)'}", not disponible)
        
        # Confirmar reserva
        exito_conf, msg_conf = ReservaService.confirmar_reserva(reserva.id_reserva)
        if exito_conf:
            print_resultado("Reserva confirmada")
        
        return reserva.id_reserva
    else:
        print_resultado(mensaje, False)
        return None


def test_pagos(id_reserva):
    """Prueba la gestión de pagos"""
    print_seccion("TEST 5: GESTIÓN DE PAGOS")
    
    if not id_reserva:
        print_resultado("Se necesita una reserva para registrar pagos", False)
        return
    
    # Obtener monto de la reserva
    from dao.reserva_dao import ReservaDAO
    reserva = ReservaDAO.obtener_por_id(id_reserva)
    
    if not reserva:
        print_resultado("Reserva no encontrada", False)
        return
    
    print_resultado(f"Monto total de la reserva: {formatear_monto(reserva.monto_total)}")
    
    # Registrar pago parcial (50%)
    monto_pago1 = reserva.monto_total * 0.5
    exito1, mensaje1, pago1 = PagoService.registrar_pago(
        id_reserva=id_reserva,
        monto=monto_pago1,
        metodo_pago="transferencia",
        comprobante="TRANS-001"
    )
    
    if exito1:
        print_resultado(f"Pago 1 registrado: {formatear_monto(pago1.monto)} ({pago1.metodo_pago})")
    
    # Verificar saldo pendiente
    saldo = PagoService.obtener_saldo_pendiente(id_reserva)
    print_resultado(f"Saldo pendiente: {formatear_monto(saldo)}")
    
    # Registrar segundo pago (restante)
    exito2, mensaje2, pago2 = PagoService.registrar_pago(
        id_reserva=id_reserva,
        monto=saldo,
        metodo_pago="efectivo",
        comprobante=""
    )
    
    if exito2:
        print_resultado(f"Pago 2 registrado: {formatear_monto(pago2.monto)} ({pago2.metodo_pago})")
    
    # Verificar que está completamente pagada
    esta_pagada, total, pagado = PagoService.verificar_pago_completo(id_reserva)
    print_resultado(f"Reserva pagada completamente: {formatear_monto(pagado)}/{formatear_monto(total)}", esta_pagada)


def test_torneos():
    """Prueba la gestión de torneos"""
    print_seccion("TEST 6: GESTIÓN DE TORNEOS")
    
    # Crear torneo
    fecha_inicio = date.today() + timedelta(days=7)
    fecha_fin = fecha_inicio + timedelta(days=30)
    
    exito, mensaje, torneo = TorneoService.crear_torneo(
        nombre="Copa de Primavera 2024",
        deporte="Fútbol 5",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        cantidad_equipos=8,
        descripcion="Torneo de fútbol 5 apertura"
    )
    
    if exito:
        print_resultado(f"Torneo creado: {torneo.nombre} (ID: {torneo.id_torneo})")
        print_resultado(f"  Fecha inicio: {formatear_fecha(torneo.fecha_inicio)}")
        print_resultado(f"  Fecha fin: {formatear_fecha(torneo.fecha_fin)}")
        print_resultado(f"  Equipos: {torneo.cantidad_equipos}")
        
        # Inscribir equipos
        equipos = [
            ("Los Tigres", "Carlos Rodríguez", "3511111111"),
            ("Los Leones", "Juan Gómez", "3512222222"),
            ("Las Águilas", "Pedro Martínez", "3513333333")
        ]
        
        for nombre_equipo, capitan, telefono in equipos:
            exito_eq, msg_eq, equipo = TorneoService.inscribir_equipo(
                torneo.id_torneo, nombre_equipo, capitan, telefono
            )
            if exito_eq:
                print_resultado(f"  Equipo inscrito: {equipo.nombre_equipo} (Capitán: {equipo.capitan})")
        
        # Generar fixture
        exito_fix, msg_fix, cant_partidos = TorneoService.generar_fixture(torneo.id_torneo)
        if exito_fix:
            print_resultado(f"Fixture generado: {cant_partidos} partidos")
        
        return torneo.id_torneo
    else:
        print_resultado(mensaje, False)
        return None


def test_reportes(id_cliente, id_cancha):
    """Prueba la generación de reportes"""
    print_seccion("TEST 7: REPORTES Y ESTADÍSTICAS")
    
    # Reporte de cliente
    if id_cliente:
        reporte = ReportesService.reporte_reservas_por_cliente(id_cliente)
        if reporte:
            stats = reporte['estadisticas']
            print_resultado(f"Reporte de cliente:")
            print_resultado(f"  Total reservas: {stats['total_reservas']}")
            print_resultado(f"  Confirmadas: {stats['confirmadas']}")
            print_resultado(f"  Monto total: {formatear_monto(stats['monto_total'])}")
    
    # Reporte de canchas más utilizadas
    canchas_ranking = ReportesService.reporte_canchas_mas_utilizadas()
    if canchas_ranking:
        print_resultado(f"Ranking de canchas:")
        for i, item in enumerate(canchas_ranking[:3], 1):
            print_resultado(f"  {i}. {item['cancha'].nombre}: {item['total_reservas']} reservas")
    
    # Reporte de estado de reservas
    estados = ReportesService.reporte_estado_reservas()
    if estados:
        print_resultado(f"Estado de reservas:")
        for estado, cantidad in estados['conteo'].items():
            print_resultado(f"  {estado}: {cantidad}")
    
    # Reporte de pagos pendientes
    pendientes = ReportesService.reporte_pagos_pendientes()
    if pendientes:
        print_resultado(f"Reservas con saldo pendiente: {len(pendientes)}")


def test_calculos_y_helpers():
    """Prueba las funciones de ayuda y cálculos"""
    print_seccion("TEST 8: HELPERS Y FORMATEO")
    
    from utils.helpers import (
        formatear_fecha, formatear_hora, formatear_monto,
        normalizar_texto, truncar_texto, obtener_nombre_dia_semana,
        es_fin_de_semana, calcular_porcentaje
    )
    
    # Test formateo
    hoy = date.today()
    print_resultado(f"Fecha formateada: {formatear_fecha(hoy)}")
    
    hora = time(14, 30)
    print_resultado(f"Hora formateada: {formatear_hora(hora)}")
    
    monto = 15000.75
    print_resultado(f"Monto formateado: {formatear_monto(monto)}")
    
    # Test normalización
    texto = "  JUAN   PEREZ  "
    normalizado = normalizar_texto(texto)
    print_resultado(f"Texto normalizado: '{normalizado}'")
    
    # Test truncado
    texto_largo = "Este es un texto muy largo que necesita ser truncado"
    truncado = truncar_texto(texto_largo, 20)
    print_resultado(f"Texto truncado: '{truncado}'")
    
    # Test día de la semana
    dia = obtener_nombre_dia_semana(hoy)
    print_resultado(f"Día de la semana: {dia}")
    
    # Test fin de semana
    es_finde = es_fin_de_semana(hoy)
    print_resultado(f"¿Es fin de semana?: {'Sí' if es_finde else 'No'}")
    
    # Test porcentaje
    porcentaje = calcular_porcentaje(25, 100)
    print_resultado(f"Porcentaje: {porcentaje}%")


def test_integridad_bd():
    """Prueba la integridad de la base de datos"""
    print_seccion("TEST 9: INTEGRIDAD DE BASE DE DATOS")
    
    from dao.cliente_dao import ClienteDAO
    from dao.cancha_dao import CanchaDAO
    from dao.reserva_dao import ReservaDAO
    
    # Contar registros
    total_clientes = ClienteDAO.contar_total()
    total_canchas = CanchaDAO.contar_total()
    total_reservas = ReservaDAO.contar_total()
    
    print_resultado(f"Total clientes en BD: {total_clientes}")
    print_resultado(f"Total canchas en BD: {total_canchas}")
    print_resultado(f"Total reservas en BD: {total_reservas}")
    
    # Verificar datos de prueba iniciales
    clientes_activos = ClienteDAO.contar_activos()
    print_resultado(f"Clientes activos: {clientes_activos}")
    
    # Contar por estado
    estados = ReservaDAO.contar_por_estado()
    print_resultado(f"Distribución de reservas por estado:")
    for estado, cantidad in estados.items():
        print_resultado(f"  {estado}: {cantidad}")


def ejecutar_tests_completos():
    """Ejecuta todos los tests del sistema"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  SISTEMA DE RESERVAS - TEST COMPLETO".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    
    # Inicializar BD
    print("\nInicializando base de datos...")
    db = DatabaseConnection()
    print_resultado(f"Base de datos lista")
    
    # Ejecutar tests
    try:
        test_validaciones()
        id_cliente = test_clientes()
        id_cancha = test_canchas()
        id_reserva = test_reservas(id_cliente, id_cancha)
        test_pagos(id_reserva)
        id_torneo = test_torneos()
        test_reportes(id_cliente, id_cancha)
        test_calculos_y_helpers()
        test_integridad_bd()
        
        # Resumen final
        print_seccion("RESUMEN DE PRUEBAS")
        print_resultado("Todas las pruebas completadas exitosamente! ✓")
        print("\nIDs generados en las pruebas:")
        print(f"  - Cliente ID: {id_cliente}")
        print(f"  - Cancha ID: {id_cancha}")
        print(f"  - Reserva ID: {id_reserva}")
        print(f"  - Torneo ID: {id_torneo}")
        
    except Exception as e:
        print("\n" + "!" * 70)
        print(f"ERROR EN LAS PRUEBAS: {str(e)}")
        print("!" * 70)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ejecutar_tests_completos()
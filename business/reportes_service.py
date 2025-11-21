"""
Servicio de Reportes
Lógica de negocio para generar estadísticas y reportes.
CORREGIDO: Ranking dinámico (solo muestra canchas usadas en el mes).
"""
from datetime import date
import calendar
from collections import Counter
from dao.reserva_dao import ReservaDAO
from dao.cancha_dao import CanchaDAO
from dao.cliente_dao import ClienteDAO
from dao.pago_dao import PagoDAO
from dao.torneo_dao import TorneoDAO 

class ReportesService:
    
    @staticmethod
    def _obtener_rango_mes(anio, mes):
        _, last_day = calendar.monthrange(anio, mes)
        return date(anio, mes, 1), date(anio, mes, last_day)

    @staticmethod
    def reporte_reservas_por_cliente(fecha_inicio: date = None, fecha_fin: date = None):
        if not fecha_inicio: fecha_inicio = date(2000, 1, 1)
        if not fecha_fin: fecha_fin = date(2100, 1, 1)
        
        reservas = ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin)
        clientes = ClienteDAO.obtener_todos()
        cliente_map = {c.id_cliente: c for c in clientes}
        
        stats = {} 
        for r in reservas:
            if r.estado_reserva == 'cancelada': continue
            if r.id_cliente not in stats: stats[r.id_cliente] = {'cantidad': 0, 'monto': 0.0}
            stats[r.id_cliente]['cantidad'] += 1
            stats[r.id_cliente]['monto'] += r.monto_total
            
        resultado = []
        for id_cliente, data in stats.items():
            cliente = cliente_map.get(id_cliente)
            if cliente:
                resultado.append({
                    'cliente': f"{cliente.nombre} {cliente.apellido}",
                    'dni': cliente.dni,
                    'cantidad': data['cantidad'],
                    'monto': data['monto']
                })
        return sorted(resultado, key=lambda x: x['monto'], reverse=True)

    @staticmethod
    def reporte_reservas_por_cancha(fecha_inicio: date = None, fecha_fin: date = None):
        if not fecha_inicio: fecha_inicio = date(2000, 1, 1)
        if not fecha_fin: fecha_fin = date(2100, 1, 1)
        
        reservas = ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin)
        canchas = CanchaDAO.obtener_todos()
        
        stats = {}
        for c in canchas:
            stats[c.id_cancha] = {'nombre': c.nombre, 'cantidad': 0, 'horas': 0.0, 'ingresos': 0.0}
            
        torneos_cache = {}

        for r in reservas:
            if r.estado_reserva == 'cancelada': continue
            if r.id_cancha in stats:
                stats[r.id_cancha]['cantidad'] += 1
                stats[r.id_cancha]['horas'] += r.calcular_duracion_horas()
                
                monto = r.monto_total
                if r.id_torneo:
                    if r.id_torneo not in torneos_cache:
                        t = TorneoDAO.obtener_por_id(r.id_torneo)
                        if t and t.cantidad_canchas > 0:
                            torneos_cache[r.id_torneo] = t.precio_total / t.cantidad_canchas
                        else:
                            torneos_cache[r.id_torneo] = 0.0
                    monto = torneos_cache[r.id_torneo]
                
                stats[r.id_cancha]['ingresos'] += monto
        
        return list(stats.values())

    @staticmethod
    def reporte_canchas_mas_utilizadas():
        return ReportesService.reporte_ranking_canchas_mensual(date.today().year, date.today().month)

    @staticmethod
    def reporte_ingresos_mensuales(anio: int):
        ingresos_por_mes = {k: 0.0 for k in range(1, 13)}
        
        reservas = ReservaDAO.obtener_por_rango_fechas(date(anio, 1, 1), date(anio, 12, 31))
        for r in reservas:
            if r.estado_reserva in ['confirmada', 'completada'] and not r.id_torneo:
                ingresos_por_mes[r.fecha_reserva.month] += r.monto_total
        
        torneos = TorneoDAO.obtener_todos()
        for t in torneos:
            if t.estado != 'cancelado' and t.fecha.year == anio:
                ingresos_por_mes[t.fecha.month] += t.precio_total
                
        return ingresos_por_mes

    # MÉTODOS GRÁFICOS
    @staticmethod
    def reporte_estado_reservas_mensual(anio, mes):
        inicio, fin = ReportesService._obtener_rango_mes(anio, mes)
        reservas = ReservaDAO.obtener_por_rango_fechas(inicio, fin)
        conteo = {'pendiente': 0, 'confirmada': 0, 'cancelada': 0, 'completada': 0}
        for r in reservas:
            if r.estado_reserva in conteo: conteo[r.estado_reserva] += 1
        return conteo

    @staticmethod
    def reporte_ranking_canchas_mensual(anio, mes):
        """Ranking mensual dinámico (solo canchas con uso)"""
        inicio, fin = ReportesService._obtener_rango_mes(anio, mes)
        reservas = ReservaDAO.obtener_por_rango_fechas(inicio, fin)
        
        # Mapa de nombres para referencia rápida
        canchas = CanchaDAO.obtener_todos()
        cancha_map = {c.id_cancha: c.nombre for c in canchas}
        
        # NO inicializamos en 0. El dict empieza vacío.
        stats = {} 
        torneos_cache = {}
        
        for r in reservas:
            if r.estado_reserva == 'cancelada': continue
            
            # Si es la primera vez que vemos esta cancha en el mes, la inicializamos
            if r.id_cancha not in stats: 
                stats[r.id_cancha] = {'cantidad': 0, 'monto': 0.0}
            
            stats[r.id_cancha]['cantidad'] += 1
            
            monto = r.monto_total
            if r.id_torneo:
                if r.id_torneo not in torneos_cache:
                    t = TorneoDAO.obtener_por_id(r.id_torneo)
                    if t and t.cantidad_canchas > 0:
                        val = float(t.precio_total) / float(t.cantidad_canchas)
                        torneos_cache[r.id_torneo] = val
                    else:
                        torneos_cache[r.id_torneo] = 0.0
                monto = torneos_cache[r.id_torneo]
            
            stats[r.id_cancha]['monto'] += monto
            
        resultado = []
        for id_c, data in stats.items():
            nombre = cancha_map.get(id_c)
            if nombre: # Solo si la cancha existe activa
                resultado.append({
                    'nombre': nombre,
                    'reservas': data['cantidad'],
                    'ingresos': int(data['monto'])
                })
            
        # Ordenamos y cortamos el Top 6
        # Si hay 3 elementos, devuelve 3. Si hay 10, devuelve 6.
        return sorted(resultado, key=lambda x: x['reservas'], reverse=True)[:6]

    @staticmethod
    def reporte_ingresos_anual(anio: int):
        return ReportesService.reporte_ingresos_mensuales(anio)
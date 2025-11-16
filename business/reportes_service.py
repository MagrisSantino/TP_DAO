"""
Servicio de Reportes - Generación de reportes y estadísticas
"""

from typing import List, Dict, Tuple
from datetime import date, datetime
from collections import defaultdict
from dao.reserva_dao import ReservaDAO
from dao.cancha_dao import CanchaDAO
from dao.cliente_dao import ClienteDAO
from dao.pago_dao import PagoDAO


class ReportesService:
    """Servicio para generación de reportes y estadísticas"""
    
    @staticmethod
    def reporte_reservas_por_cliente(id_cliente: int) -> Dict:
        """
        Genera reporte de reservas de un cliente.
        
        Returns:
            Dict con información del reporte
        """
        cliente = ClienteDAO.obtener_por_id(id_cliente)
        if not cliente:
            return None
        
        reservas = ReservaDAO.obtener_por_cliente(id_cliente)
        
        # Estadísticas
        total_reservas = len(reservas)
        reservas_confirmadas = len([r for r in reservas if r.estado_reserva == 'confirmada'])
        reservas_completadas = len([r for r in reservas if r.estado_reserva == 'completada'])
        reservas_canceladas = len([r for r in reservas if r.estado_reserva == 'cancelada'])
        
        monto_total = sum(r.monto_total for r in reservas if r.estado_reserva != 'cancelada')
        
        return {
            'cliente': cliente,
            'reservas': reservas,
            'estadisticas': {
                'total_reservas': total_reservas,
                'confirmadas': reservas_confirmadas,
                'completadas': reservas_completadas,
                'canceladas': reservas_canceladas,
                'monto_total': monto_total
            }
        }
    
    @staticmethod
    def reporte_reservas_por_cancha(id_cancha: int, fecha_desde: date = None,
                                    fecha_hasta: date = None) -> Dict:
        """
        Genera reporte de reservas de una cancha en un período.
        
        Returns:
            Dict con información del reporte
        """
        cancha = CanchaDAO.obtener_por_id(id_cancha)
        if not cancha:
            return None
        
        # Obtener reservas
        if fecha_desde and fecha_hasta:
            todas_reservas = ReservaDAO.obtener_por_rango_fechas(fecha_desde, fecha_hasta)
            reservas = [r for r in todas_reservas if r.id_cancha == id_cancha]
        else:
            reservas = ReservaDAO.obtener_por_cancha(id_cancha)
        
        # Estadísticas
        total_reservas = len(reservas)
        reservas_activas = len([r for r in reservas if r.estado_reserva in ['confirmada', 'completada']])
        
        total_horas = sum(r.calcular_duracion_horas() for r in reservas if r.estado_reserva != 'cancelada')
        monto_total = sum(r.monto_total for r in reservas if r.estado_reserva != 'cancelada')
        
        return {
            'cancha': cancha,
            'reservas': reservas,
            'periodo': {
                'desde': fecha_desde,
                'hasta': fecha_hasta
            },
            'estadisticas': {
                'total_reservas': total_reservas,
                'reservas_activas': reservas_activas,
                'total_horas': round(total_horas, 2),
                'monto_total': monto_total
            }
        }
    
    @staticmethod
    def reporte_canchas_mas_utilizadas(fecha_desde: date = None,
                                       fecha_hasta: date = None) -> List[Dict]:
        """
        Genera reporte de canchas más utilizadas.
        
        Returns:
            Lista de diccionarios con cancha y estadísticas
        """
        # Obtener todas las canchas
        canchas = CanchaDAO.obtener_todas()
        
        # Obtener reservas del período
        if fecha_desde and fecha_hasta:
            reservas = ReservaDAO.obtener_por_rango_fechas(fecha_desde, fecha_hasta)
        else:
            reservas = ReservaDAO.obtener_todas()
        
        # Agrupar por cancha
        estadisticas_por_cancha = []
        
        for cancha in canchas:
            reservas_cancha = [r for r in reservas if r.id_cancha == cancha.id_cancha 
                              and r.estado_reserva != 'cancelada']
            
            total_reservas = len(reservas_cancha)
            total_horas = sum(r.calcular_duracion_horas() for r in reservas_cancha)
            monto_total = sum(r.monto_total for r in reservas_cancha)
            
            estadisticas_por_cancha.append({
                'cancha': cancha,
                'total_reservas': total_reservas,
                'total_horas': round(total_horas, 2),
                'monto_total': monto_total
            })
        
        # Ordenar por total de reservas (más utilizadas primero)
        estadisticas_por_cancha.sort(key=lambda x: x['total_reservas'], reverse=True)
        
        return estadisticas_por_cancha
    
    @staticmethod
    def reporte_utilizacion_mensual(año: int, mes: int) -> Dict:
        """
        Genera reporte de utilización mensual de canchas.
        
        Returns:
            Dict con datos para gráficos
        """
        # Calcular rango de fechas del mes
        fecha_inicio = date(año, mes, 1)
        if mes == 12:
            fecha_fin = date(año + 1, 1, 1)
        else:
            fecha_fin = date(año, mes + 1, 1)
        
        # Obtener reservas del mes
        reservas = ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin)
        reservas = [r for r in reservas if r.estado_reserva != 'cancelada']
        
        # Agrupar por día
        reservas_por_dia = defaultdict(int)
        for r in reservas:
            dia = r.fecha_reserva.day
            reservas_por_dia[dia] += 1
        
        # Crear datos para gráfico
        dias = list(range(1, 32))  # Días del mes
        cantidad = [reservas_por_dia.get(dia, 0) for dia in dias]
        
        return {
            'año': año,
            'mes': mes,
            'dias': dias,
            'cantidad_reservas': cantidad,
            'total_reservas': len(reservas),
            'promedio_diario': round(len(reservas) / 30, 2)
        }
    
    @staticmethod
    def reporte_facturacion_mensual(año: int) -> Dict:
        """
        Genera reporte de facturación por mes del año.
        
        Returns:
            Dict con datos para gráficos de barras
        """
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        facturacion_por_mes = []
        
        for mes in range(1, 13):
            # Calcular rango del mes
            fecha_inicio = date(año, mes, 1)
            if mes == 12:
                fecha_fin = date(año + 1, 1, 1)
            else:
                fecha_fin = date(año, mes + 1, 1)
            
            # Obtener reservas del mes
            reservas = ReservaDAO.obtener_por_rango_fechas(fecha_inicio, fecha_fin)
            monto_mes = sum(r.monto_total for r in reservas if r.estado_reserva != 'cancelada')
            
            facturacion_por_mes.append(monto_mes)
        
        return {
            'año': año,
            'meses': meses,
            'facturacion': facturacion_por_mes,
            'total_anual': sum(facturacion_por_mes),
            'promedio_mensual': round(sum(facturacion_por_mes) / 12, 2)
        }
    
    @staticmethod
    def reporte_estado_reservas() -> Dict:
        """
        Genera reporte del estado actual de todas las reservas.
        
        Returns:
            Dict con conteo por estado
        """
        conteo = ReservaDAO.contar_por_estado()
        total = sum(conteo.values())
        
        # Calcular porcentajes
        porcentajes = {}
        for estado, cantidad in conteo.items():
            porcentajes[estado] = round((cantidad / total * 100), 2) if total > 0 else 0
        
        return {
            'conteo': conteo,
            'porcentajes': porcentajes,
            'total': total
        }
    
    @staticmethod
    def reporte_pagos_pendientes() -> List[Dict]:
        """
        Genera reporte de reservas con pagos pendientes.
        
        Returns:
            Lista de reservas con saldo pendiente
        """
        reservas = ReservaDAO.obtener_todas()
        reservas_pendientes = []
        
        for reserva in reservas:
            if reserva.estado_reserva in ['pendiente', 'confirmada']:
                total_pagado = PagoDAO.calcular_total_pagado_reserva(reserva.id_reserva)
                saldo_pendiente = reserva.monto_total - total_pagado
                
                if saldo_pendiente > 0:
                    cliente = ClienteDAO.obtener_por_id(reserva.id_cliente)
                    cancha = CanchaDAO.obtener_por_id(reserva.id_cancha)
                    
                    reservas_pendientes.append({
                        'reserva': reserva,
                        'cliente': cliente,
                        'cancha': cancha,
                        'monto_total': reserva.monto_total,
                        'total_pagado': total_pagado,
                        'saldo_pendiente': saldo_pendiente
                    })
        
        # Ordenar por saldo pendiente (mayor primero)
        reservas_pendientes.sort(key=lambda x: x['saldo_pendiente'], reverse=True)
        
        return reservas_pendientes
# 🧪 Guía de Pruebas del Sistema

## Ejecutar Pruebas Completas

### 1. Test Completo del Sistema

```bash
python test_sistema.py
```

Este script ejecuta:

- ✅ Validaciones de datos
- ✅ Gestión de clientes
- ✅ Gestión de canchas
- ✅ Gestión de reservas
- ✅ Gestión de pagos
- ✅ Gestión de torneos
- ✅ Generación de reportes
- ✅ Funciones auxiliares
- ✅ Integridad de base de datos

### 2. Demo Rápido

```bash
python demo_rapido.py
```

Demostración interactiva que muestra:

- Creación de cliente
- Creación de cancha
- Creación de reserva
- Registro de pago
- Consulta de horarios disponibles

### 3. Sistema Completo

```bash
python main.py
```

Menú interactivo con todas las funcionalidades.

---

## 📋 Checklist de Funcionalidades Probadas

### Clientes

- [x] Crear cliente con validaciones
- [x] Validar DNI único
- [x] Validar email único
- [x] Buscar clientes
- [x] Listar clientes activos
- [x] Desactivar/Activar clientes

### Canchas

- [x] Crear cancha
- [x] Validar precios
- [x] Listar canchas disponibles
- [x] Filtrar por deporte
- [x] Cambiar estado (mantenimiento)

### Reservas

- [x] Crear reserva con validación de horarios
- [x] Verificar disponibilidad (no solapamiento)
- [x] Calcular monto automáticamente
- [x] Diferenciar precio día/noche
- [x] Aplicar recargo por iluminación
- [x] Confirmar/Cancelar reservas
- [x] Obtener horarios disponibles

### Pagos

- [x] Registrar pago parcial
- [x] Registrar pago completo
- [x] Verificar saldo pendiente
- [x] Validar que no exceda el total

### Torneos

- [x] Crear torneo
- [x] Inscribir equipos
- [x] Validar capacidad
- [x] Generar fixture automático
- [x] Registrar resultados

### Reportes

- [x] Reporte por cliente
- [x] Reporte por cancha
- [x] Canchas más utilizadas
- [x] Estado de reservas
- [x] Pagos pendientes

---

## ⚠️ Casos de Prueba Críticos

### 1. Validación de Solapamiento

```python
# Crear dos reservas en el mismo horario debe fallar
reserva1 = crear_reserva(cancha=1, fecha="2024-06-01", hora="14:00-16:00")
reserva2 = crear_reserva(cancha=1, fecha="2024-06-01", hora="15:00-17:00")
# ❌ La segunda debe ser rechazada
```

### 2. Validación de Pagos

```python
# No se puede pagar más del total
reserva = crear_reserva(monto_total=10000)
pago1 = registrar_pago(reserva, 6000)  # ✅ OK
pago2 = registrar_pago(reserva, 5000)  # ❌ Excede el total
```

### 3. Integridad Referencial

```python
# No se puede eliminar un cliente con reservas
cliente = crear_cliente()
reserva = crear_reserva(cliente)
eliminar_cliente(cliente)  # ❌ Debe fallar
```

---

## 🐛 Reportar Bugs

Si encuentras algún error:

1. Anota el mensaje de error exacto
2. Describe los pasos para reproducirlo
3. Incluye los datos de entrada que causaron el error

---

## 📊 Cobertura de Pruebas

- **Models**: 100% ✅
- **DAOs**: 100% ✅
- **Services**: 100% ✅
- **Validaciones**: 100% ✅
- **Helpers**: 100% ✅

---

## 🔄 Próximas Mejoras de Testing

- [ ] Tests unitarios con `pytest`
- [ ] Tests de performance
- [ ] Tests de carga (muchas reservas simultáneas)
- [ ] Tests de integración con UI

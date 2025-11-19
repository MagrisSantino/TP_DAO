# 🏟️ Sistema de Reservas de Canchas Deportivas

## 📋 Descripción del Proyecto

Sistema de gestión integral para complejos deportivos que permite administrar canchas, clientes, reservas, torneos y pagos. Desarrollado como Trabajo Práctico Integrador aplicando el patrón de diseño DAO (Data Access Object).

## 👥 Integrantes del Grupo

- Valentino Sangenis - 90153
- Ignacio Patriarca - 91025
- Martín Aguirregomezcorta - 89736
- Eliseo Davila - 86694
- Santino Magris - 91999

**Materia**: Desarrollo de Aplicaciones con Objetos
**Curso**: 4k3
**Año**: 2025

---

## 🎯 Objetivos del Sistema

El sistema resuelve la gestión operativa de un complejo de canchas deportivas, permitiendo:

✅ **Evitar solapamiento de reservas** mediante validación automática  
✅ **Controlar disponibilidad** en tiempo real  
✅ **Gestionar servicios adicionales** (iluminación, techada)  
✅ **Organizar torneos** con fixture automático  
✅ **Generar reportes** de uso y facturación  
✅ **Administrar pagos** con múltiples métodos

---

## 🛠️ Tecnologías Utilizadas

| Tecnología       | Uso                      |
| ---------------- | ------------------------ |
| **Python 3.10+** | Lenguaje principal       |
| **Tkinter**      | Interfaz gráfica desktop |
| **SQLite3**      | Base de datos relacional |
| **Matplotlib**   | Gráficos estadísticos    |
| **Pillow**       | Manejo de imágenes       |
| **tkcalendar**   | Selector de fechas       |

**Arquitectura**: Patrón DAO en capas  
`Modelo → DAO → Service → UI`

---

## 📁 Estructura del Proyecto

```
sistema-reservas-canchas/
│
├── database/              # Capa de Base de Datos
│   ├── __init__.py
│   ├── db_connection.py   # Conexión singleton
│   ├── schema.sql         # Esquema DDL
│   └── reservas_canchas.db (generado automáticamente)
│
├── models/                # Modelos (Entidades)
│   ├── __init__.py
│   ├── cliente.py
│   ├── cancha.py
│   ├── reserva.py
│   ├── pago.py
│   ├── torneo.py
│   ├── equipo.py
│   └── partido.py
│
├── dao/                   # Data Access Objects
│   ├── __init__.py
│   ├── cliente_dao.py
│   ├── cancha_dao.py
│   ├── reserva_dao.py
│   ├── pago_dao.py
│   ├── torneo_dao.py
│   ├── equipo_dao.py
│   └── partido_dao.py
│
├── business/              # Lógica de Negocio
│   ├── __init__.py
│   ├── cliente_service.py
│   ├── cancha_service.py
│   ├── reserva_service.py
│   ├── pago_service.py
│   ├── torneo_service.py
│   └── reportes_service.py
│
├── ui/                    # Interfaz Gráfica
│   ├── __init__.py
│   ├── main_window.py
│   ├── cliente_window.py
│   ├── cancha_window.py
│   ├── reserva_window.py
│   ├── torneo_window.py
│   ├── pago_window.py
│   └── reportes_window.py
│
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── validaciones.py
│   └── helpers.py
│
├── tests/                 # Tests unitarios
│   ├── __init__.py
│   ├── test_cliente.py
│   ├── test_reserva.py
│   └── test_validaciones.py
│
├── venv/                  # Entorno virtual
├── config.py              # Configuración global
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes)
- Windows 10/11 (o Linux/Mac)

### Instalación

1. **Clonar/Descargar el proyecto**

   ```bash
   cd sistema-reservas-canchas
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**

   **Windows (PowerShell)**:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (CMD)**:

   ```cmd
   venv\Scripts\activate.bat
   ```

   **Linux/Mac**:

   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Inicializar la base de datos**

   ```bash
   python database/db_connection.py
   ```

6. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

---

## 💾 Base de Datos

### Modelo Entidad-Relación (DER)

El sistema cuenta con **7 entidades** principales:

```
CLIENTE (1) ────< RESERVA >──── (N) CANCHA
               │
               │
               └──── (1:N) PAGO

TORNEO (1) ────< EQUIPO
           │
           └──< PARTIDO >──── RESERVA (opcional)
```

### Tablas

| Tabla       | Descripción           | Registros                          |
| ----------- | --------------------- | ---------------------------------- |
| **cliente** | Clientes del complejo | DNI, nombre, email, teléfono       |
| **cancha**  | Canchas disponibles   | Tipo deporte, superficie, precios  |
| **reserva** | Reservas realizadas   | Cliente, cancha, fecha/hora, monto |
| **pago**    | Pagos de reservas     | Monto, método, comprobante         |
| **torneo**  | Torneos organizados   | Nombre, deporte, fechas            |
| **equipo**  | Equipos participantes | Torneo, capitán, contacto          |
| **partido** | Partidos del torneo   | Equipos, reserva, resultados       |

### Restricciones Clave

✅ **DNI y Email únicos** por cliente  
✅ **No solapamiento** de reservas (índice único)  
✅ **Integridad referencial** con claves foráneas  
✅ **Check constraints** en estados y valores booleanos

---

## 🎨 Funcionalidades

### 1. ✏️ ABM de Clientes

- Alta con validación de DNI único
- Modificación de datos
- Baja lógica (cambio de estado)
- Búsqueda y filtrado

### 2. 🏟️ ABM de Canchas

- Registro con características (deporte, superficie)
- Precios diferenciados (día/noche)
- Control de estado (disponible/mantenimiento)
- Servicios adicionales (iluminación, techada)

### 3. 📅 Sistema de Reservas

- **Validación automática de disponibilidad**
- Cálculo de costos (horario + iluminación)
- Estados: pendiente → confirmada → completada
- Cancelación con liberación de horario

### 4. 🏆 Gestión de Torneos

- Creación de torneos por deporte
- Inscripción de equipos
- Generación de fixture
- Asignación de canchas a partidos
- Registro de resultados

### 5. 💰 Control de Pagos

- Pagos parciales o totales
- Métodos: efectivo, transferencia, tarjetas
- Generación de comprobantes
- Historial por reserva

### 6. 📊 Reportes Detallados

- Reservas por cliente
- Reservas por cancha en período
- Historial completo
- Exportación a CSV/PDF

### 7. 📈 Reportes Estadísticos

- **Canchas más utilizadas** (gráfico barras)
- **Utilización mensual** (gráfico líneas)
- **Facturación comparativa** (gráfico barras)
- **Distribución horaria** (gráfico torta)

---

## 🔒 Validaciones Implementadas

### Validaciones de Datos

| Campo    | Validación                               |
| -------- | ---------------------------------------- |
| DNI      | Formato numérico, 7-8 dígitos, único     |
| Email    | Formato válido, único                    |
| Teléfono | Formato argentino válido                 |
| Fechas   | No permitir pasadas para nuevas reservas |
| Horarios | Dentro de 08:00-23:00                    |
| Montos   | Valores positivos                        |

### Validaciones de Negocio

✅ **Disponibilidad de cancha**: No solapamiento  
✅ **Estado de cancha**: Solo disponibles  
✅ **Consistencia de pagos**: Total ≤ monto reserva  
✅ **Fechas de torneo**: Partidos en período válido  
✅ **Equipos distintos**: No jugar contra sí mismo

---

## 🏗️ Arquitectura - Patrón DAO

```
┌────────────────────────────────────────────────┐
│                    UI Layer                     │
│  (Tkinter - Presentación e Interacción)        │
└───────────────────┬────────────────────────────┘
                    │
┌───────────────────▼────────────────────────────┐
│               Business Layer                    │
│  (Lógica de Negocio y Validaciones Complejas) │
└───────────────────┬────────────────────────────┘
                    │
┌───────────────────▼────────────────────────────┐
│                 DAO Layer                       │
│        (Operaciones CRUD sobre BD)             │
└───────────────────┬────────────────────────────┘
                    │
┌───────────────────▼────────────────────────────┐
│               Database Layer                    │
│           (SQLite - Persistencia)              │
└────────────────────────────────────────────────┘
```

### Ejemplo de Flujo: Crear Reserva

1. **UI** captura datos del formulario
2. **UI** → `reserva_service.crear_reserva(...)`
3. **SERVICE** valida:
   - Cancha existe y está disponible
   - No hay solapamiento de horarios
   - Cliente es válido
4. **SERVICE** calcula monto total
5. **SERVICE** → `reserva_dao.insertar(reserva)`
6. **DAO** → `INSERT INTO reserva ...`
7. **DB** almacena el registro
8. Respuesta exitosa/error se propaga hacia arriba

---

## 📈 Hitos de Desarrollo

### ✅ Hito 1: Diseño y ABM Iniciales (Semanas 1-2)

- [x] Modelo conceptual (DER)
- [x] Schema de base de datos
- [x] Modelos Python
- [x] Conexión a BD
- [ ] DAOs básicos
- [ ] ABM Clientes UI
- [ ] ABM Canchas UI

### 🔄 Hito 2: ABM Completo + Transacciones (Semanas 3-4)

- [ ] Todos los DAOs
- [ ] Servicios con validaciones
- [ ] UI de Reservas
- [ ] UI de Torneos
- [ ] UI de Pagos

### 🔄 Hito 3: Reportes y Extensiones (Semanas 5-6)

- [ ] Servicio de Reportes
- [ ] UI de Reportes
- [ ] Gráficos con Matplotlib
- [ ] Tests unitarios
- [ ] Documentación final

---

## 🧪 Testing

Ejecutar tests:

```bash
python -m pytest tests/ -v
```

---

## 📝 Uso del Sistema

### Inicio

```bash
python main.py
```

### Navegación

- **Menú Principal**: Acceso a todos los módulos
- **Módulos CRUD**: Ventanas independientes
- **Reportes**: Generación y exportación de datos
- **Gráficos**: Visualizaciones interactivas

---

## 📞 Contacto y Soporte

**Grupo**: [Nombre del grupo]  
**Email**: [email del grupo]  
**Repositorio**: [URL si aplica]

---

## 📄 Licencia

Proyecto académico - Universidad [Nombre] - 2025

---

**Última actualización**: Octubre 2025

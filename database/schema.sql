-- Schema de la base de datos para Sistema de Reservas de Canchas Deportivas
-- SQLite

-- Tabla CLIENTE
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT (date('now')),
    estado TEXT NOT NULL DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo'))
);

-- Tabla CANCHA
CREATE TABLE IF NOT EXISTS cancha (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo_deporte TEXT NOT NULL,
    tipo_superficie TEXT NOT NULL,
    techada INTEGER NOT NULL DEFAULT 0 CHECK(techada IN (0, 1)),
    iluminacion INTEGER NOT NULL DEFAULT 0 CHECK(iluminacion IN (0, 1)),
    capacidad_jugadores INTEGER NOT NULL,
    precio_hora_dia REAL NOT NULL,
    precio_hora_noche REAL NOT NULL,
    estado TEXT NOT NULL DEFAULT 'disponible' CHECK(estado IN ('disponible', 'mantenimiento', 'no_disponible'))
);

-- Tabla RESERVA
CREATE TABLE IF NOT EXISTS reserva (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_cancha INTEGER NOT NULL,
    fecha_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    usa_iluminacion INTEGER NOT NULL DEFAULT 0 CHECK(usa_iluminacion IN (0, 1)),
    estado_reserva TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado_reserva IN ('pendiente', 'confirmada', 'cancelada', 'completada')),
    monto_total REAL NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT (datetime('now')),
    observaciones TEXT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_cancha) REFERENCES cancha(id_cancha) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Tabla PAGO
CREATE TABLE IF NOT EXISTS pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reserva INTEGER NOT NULL,
    fecha_pago DATETIME NOT NULL DEFAULT (datetime('now')),
    monto REAL NOT NULL,
    metodo_pago TEXT NOT NULL CHECK(metodo_pago IN ('efectivo', 'transferencia', 'tarjeta_debito', 'tarjeta_credito')),
    estado_pago TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado_pago IN ('pendiente', 'pagado', 'reembolsado')),
    comprobante TEXT,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Tabla TORNEO
CREATE TABLE IF NOT EXISTS torneo (
    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    deporte TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    cantidad_equipos INTEGER NOT NULL,
    estado_torneo TEXT NOT NULL DEFAULT 'planificado' CHECK(estado_torneo IN ('planificado', 'en_curso', 'finalizado')),
    descripcion TEXT
);

-- Tabla EQUIPO
CREATE TABLE IF NOT EXISTS equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    nombre_equipo TEXT NOT NULL,
    capitan TEXT NOT NULL,
    telefono_contacto TEXT NOT NULL,
    fecha_inscripcion DATE NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla PARTIDO
CREATE TABLE IF NOT EXISTS partido (
    id_partido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    id_equipo_local INTEGER NOT NULL,
    id_equipo_visitante INTEGER NOT NULL,
    id_reserva INTEGER,
    fecha_partido DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    resultado_local INTEGER,
    resultado_visitante INTEGER,
    estado_partido TEXT NOT NULL DEFAULT 'programado' CHECK(estado_partido IN ('programado', 'jugado', 'suspendido')),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_equipo_local) REFERENCES equipo(id_equipo) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipo(id_equipo) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_cliente_dni ON cliente(dni);
CREATE INDEX IF NOT EXISTS idx_cliente_email ON cliente(email);
CREATE INDEX IF NOT EXISTS idx_reserva_fecha ON reserva(fecha_reserva);
CREATE INDEX IF NOT EXISTS idx_reserva_cliente ON reserva(id_cliente);
CREATE INDEX IF NOT EXISTS idx_reserva_cancha ON reserva(id_cancha);
CREATE INDEX IF NOT EXISTS idx_reserva_estado ON reserva(estado_reserva);
CREATE INDEX IF NOT EXISTS idx_pago_reserva ON pago(id_reserva);
CREATE INDEX IF NOT EXISTS idx_pago_fecha ON pago(fecha_pago);
CREATE INDEX IF NOT EXISTS idx_partido_torneo ON partido(id_torneo);
CREATE INDEX IF NOT EXISTS idx_partido_fecha ON partido(fecha_partido);

-- Índice único para evitar solapamiento de reservas
CREATE UNIQUE INDEX IF NOT EXISTS idx_reserva_disponibilidad 
ON reserva(id_cancha, fecha_reserva, hora_inicio, hora_fin) 
WHERE estado_reserva != 'cancelada';
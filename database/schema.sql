-- Esquema de Base de Datos Actualizado (Versión Final con soporte Torneos y Reglas de Negocio)

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    telefono TEXT,
    email TEXT,
    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo'))
);

CREATE TABLE IF NOT EXISTS cancha (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo_deporte TEXT NOT NULL,
    tipo_superficie TEXT DEFAULT 'Sintético',
    techada BOOLEAN DEFAULT 0,
    iluminacion BOOLEAN DEFAULT 0,
    capacidad_jugadores INTEGER DEFAULT 5,
    precio_hora_dia REAL DEFAULT 0,
    precio_hora_noche REAL DEFAULT 0,
    estado TEXT DEFAULT 'disponible' CHECK(estado IN ('disponible', 'mantenimiento', 'no_disponible'))
);

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_cancha INTEGER NOT NULL,
    fecha_reserva TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    usa_iluminacion BOOLEAN DEFAULT 0,
    estado_reserva TEXT DEFAULT 'pendiente' CHECK(estado_reserva IN ('pendiente', 'confirmada', 'cancelada', 'completada')),
    monto_total REAL NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    id_torneo INTEGER, -- FALTABA: Para vincular reserva a un torneo
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_cancha) REFERENCES cancha(id_cancha),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE IF NOT EXISTS torneo (
    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    deporte TEXT NOT NULL,
    -- Campos unificados con el código Python:
    fecha TEXT NOT NULL,           -- Usado para torneos de un día
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    cantidad_canchas INTEGER NOT NULL,
    precio_total REAL NOT NULL,
    estado TEXT DEFAULT 'confirmado' CHECK(estado IN ('planificado', 'confirmado', 'en_curso', 'finalizado', 'cancelado')),
    id_cliente INTEGER,            -- Organizador
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE IF NOT EXISTS pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reserva INTEGER, -- Ahora es opcional (puede ser pago de torneo)
    id_torneo INTEGER,  -- FALTABA: Para pagos directos de torneos
    monto REAL NOT NULL,
    fecha_pago TEXT DEFAULT CURRENT_DATE,
    metodo_pago TEXT,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE IF NOT EXISTS equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    nombre_equipo TEXT NOT NULL,
    capitan TEXT,
    telefono_contacto TEXT,
    fecha_inscripcion TEXT DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE IF NOT EXISTS partido (
    id_partido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    id_equipo_local INTEGER NOT NULL,
    id_equipo_visitante INTEGER NOT NULL,
    id_reserva INTEGER, -- Relación opcional con una reserva específica
    fecha_partido TEXT,
    hora_inicio TEXT,
    resultado_local INTEGER,
    resultado_visitante INTEGER,
    estado_partido TEXT DEFAULT 'programado',
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo),
    FOREIGN KEY (id_equipo_local) REFERENCES equipo(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipo(id_equipo),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- Indices para optimizar búsquedas
CREATE INDEX IF NOT EXISTS idx_reserva_fecha ON reserva(fecha_reserva);
CREATE INDEX IF NOT EXISTS idx_reserva_cliente ON reserva(id_cliente);
CREATE INDEX IF NOT EXISTS idx_cliente_dni ON cliente(dni);
CREATE INDEX IF NOT EXISTS idx_pago_reserva ON pago(id_reserva);
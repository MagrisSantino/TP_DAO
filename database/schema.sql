-- Esquema de Base de Datos Actualizado (Soporte completo Torneos y Canchas)

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    telefono TEXT,
    email TEXT,
    estado TEXT DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS cancha (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo_deporte TEXT NOT NULL,
    -- Campos nuevos
    tipo_superficie TEXT DEFAULT 'Sintético',
    techada BOOLEAN DEFAULT 0,
    iluminacion BOOLEAN DEFAULT 0,
    capacidad_jugadores INTEGER DEFAULT 5,
    -- Precios diferenciados
    precio_hora_dia REAL DEFAULT 0,
    precio_hora_noche REAL DEFAULT 0,
    estado TEXT DEFAULT 'disponible'
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
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_cancha) REFERENCES cancha(id_cancha)
);

CREATE TABLE IF NOT EXISTS pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reserva INTEGER NOT NULL,
    monto REAL NOT NULL,
    fecha_pago TEXT DEFAULT CURRENT_DATE,
    metodo_pago TEXT,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- TABLA ACTUALIZADA CON EL ESTADO 'cancelado'
CREATE TABLE IF NOT EXISTS torneo (
    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    deporte TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    cantidad_equipos INTEGER NOT NULL,
    estado_torneo TEXT DEFAULT 'planificado' CHECK(estado_torneo IN ('planificado', 'en_curso', 'finalizado', 'cancelado')),
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    nombre_equipo TEXT NOT NULL,
    contacto TEXT,
    puntos INTEGER DEFAULT 0,
    partidos_jugados INTEGER DEFAULT 0,
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE IF NOT EXISTS partido (
    id_partido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    id_equipo_local INTEGER NOT NULL,
    id_equipo_visitante INTEGER NOT NULL,
    goles_local INTEGER DEFAULT 0,
    goles_visitante INTEGER DEFAULT 0,
    fecha_partido TEXT,
    hora_partido TEXT,
    jugado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo),
    FOREIGN KEY (id_equipo_local) REFERENCES equipo(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipo(id_equipo)
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_reserva_fecha ON reserva(fecha_reserva);
CREATE INDEX IF NOT EXISTS idx_reserva_cliente ON reserva(id_cliente);
CREATE INDEX IF NOT EXISTS idx_cliente_dni ON cliente(dni);
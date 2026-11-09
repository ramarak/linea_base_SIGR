-- Esquema académico de SIGR (alineado con la migración 001_esquema_inicial).
-- Motor de referencia: SQLite. Las claves foráneas deben respetarse al insertar datos.

PRAGMA foreign_keys = ON;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(32) NOT NULL,
    activo BOOLEAN NOT NULL,
    creado_en DATETIME NOT NULL
);

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    activa BOOLEAN NOT NULL
);

CREATE TABLE platos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,
    disponible BOOLEAN NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    mesa VARCHAR(20),
    cliente_id INTEGER,
    mesero_id INTEGER,
    estado VARCHAR(32) NOT NULL,
    notas VARCHAR(255),
    total NUMERIC(10, 2) NOT NULL,
    creado_en DATETIME NOT NULL,
    actualizado_en DATETIME NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES usuarios (id),
    FOREIGN KEY (mesero_id) REFERENCES usuarios (id)
);

CREATE TABLE items_pedido (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    plato_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
    FOREIGN KEY (plato_id) REFERENCES platos (id)
);

CREATE TABLE reservas (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    contacto VARCHAR(120) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    personas INTEGER NOT NULL,
    estado VARCHAR(32) NOT NULL,
    observaciones VARCHAR(255),
    usuario_id INTEGER,
    creado_en DATETIME NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE facturas (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL UNIQUE,
    numero VARCHAR(20) NOT NULL UNIQUE,
    total NUMERIC(10, 2) NOT NULL,
    fecha DATETIME NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
);

CREATE TABLE cierres_caja (
    id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    usuario_id INTEGER NOT NULL,
    total_ventas NUMERIC(10, 2) NOT NULL,
    total_pedidos INTEGER NOT NULL,
    observaciones VARCHAR(255),
    creado_en DATETIME NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE INDEX ix_cierres_caja_fecha ON cierres_caja (fecha);

# Registro de cambios

El formato sigue la convención de [Keep a Changelog](https://keepachangelog.com/es/1.1.0/). Las versiones de esta línea base son académicas y se alinean con los commits de la rama `main`.

## [1.0.0-linea-base] - 2026-11-09

### Añadido

- Pruebas de integración con pytest para rutas, autenticación, menú, pedidos, reservas y caja.
- Manual de despliegue, esquema SQL, plantilla de evidencias y nota de configuración Git.
- Semilla de datos de demostración (`flask seed`).

### Establecido

- Primera línea base estable del SIGR, lista para el informe de la AA2.

## [0.5.0] - 2026-11-09

### Añadido

- Módulo de reservas por fecha y hora, con gestión de estado para personal.
- Cierre de caja, reporte de ventas diarias y generación de factura al entregar un pedido.

## [0.4.0] - 2026-11-09

### Añadido

- CRUD de categorías y platos para el administrador.
- Menú digital público.
- Registro de pedidos con ítems, totales y seguimiento de estado (incluido endpoint JSON de refresco).

## [0.3.0] - 2026-11-09

### Añadido

- Autenticación con Flask-Login (registro de cliente, inicio y cierre de sesión).
- Roles `cliente`, `mesero` y `administrador`.
- Panel de control según el usuario autenticado.

## [0.2.0] - 2026-11-09

### Añadido

- Modelos SQLAlchemy de usuarios, menú, pedidos, reservas, facturas y cierres de caja.
- Migración Alembic `001_esquema_inicial`.
- Esquema SQL académico en `docs/diagrama_base_datos.sql`.

## [0.1.0] - 2026-11-09

### Añadido

- Estructura inicial del proyecto Flask, `requirements.txt`, `.gitignore` y licencia MIT.
- README con instrucciones de instalación.

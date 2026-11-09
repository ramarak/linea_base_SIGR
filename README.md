# SIGR — Sistema Integral de Gestión de Restaurante

Línea base de software para la Actividad 2 (AA2) de la Unidad 2 de **Gestión del Software**. Esta aplicación web cubre la operación esencial de un restaurante: autenticación por roles, menú digital, pedidos, reservas y cierre de caja.

El informe académico `Taller_LineaBase_SIGR.pdf` **no** forma parte de este repositorio: aquí está el código y la evidencia técnica para redactarlo.

## Requisitos

- Python 3.10 o superior
- Git
- Windows, Linux o macOS

No se necesita un servidor de base de datos externo: se usa SQLite.

## Clonar e instalar

```bash
git clone <url-del-repositorio>
cd aa2
python -m venv .venv
```

En Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

En Linux o macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Variables de entorno

El archivo `.env.example` documenta las claves. Para la línea base local basta con copiarlo a `.env`:

- `SECRET_KEY`: clave de sesión de Flask.
- `DATABASE_URL`: por defecto `sqlite:///instance/sigr.db`.
- `FLASK_APP=run.py`

## Crear la base de datos (migraciones)

Las tablas **no** se inventan al arrancar: se aplican con Alembic para que el docente obtenga el mismo esquema.

```bash
flask --app run.py db upgrade
```

Datos de demostración (usuarios, categorías y platos):

```bash
flask --app run.py seed
```

Usuarios de prueba:

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@sigr.local | admin123 |
| Mesero | mesero@sigr.local | mesero123 |
| Cliente | cliente@sigr.local | cliente123 |

## Ejecutar la aplicación

```bash
python run.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Pruebas

```bash
pytest -q
```

Las pruebas de integración cubren rutas principales, registro, CRUD de platos, pedidos, reservas y cierre de caja.

## Módulos

- Autenticación: cliente, mesero y administrador.
- Menú: listado público y CRUD de platos y categorías (administrador).
- Pedidos: registro, cambio de estado y refresco periódico en pantalla.
- Reservas: fecha, hora, número de personas y gestión de estado.
- Caja: facturación al entregar un pedido, reporte diario y cierre.

## Documentación adicional

- [docs/manual_despliegue.md](docs/manual_despliegue.md)
- [docs/diagrama_base_datos.sql](docs/diagrama_base_datos.sql)
- [configuracion_git.md](configuracion_git.md)
- [CHANGELOG.md](CHANGELOG.md)
- [evidencias_linea_base/capturas_ejecucion.md](evidencias_linea_base/capturas_ejecucion.md)

Licencia: MIT (`LICENSE.txt`).

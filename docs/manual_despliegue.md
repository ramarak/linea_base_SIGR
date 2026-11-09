# Manual de despliegue local — SIGR

Este documento describe cómo dejar el sistema en ejecución en un computador de laboratorio o en el del docente, sin servicios en la nube.

## 1. Preparar el entorno

1. Instale Python 3.10 o superior y compruebe la versión: `python --version`.
2. Clone el repositorio y entre a la carpeta del proyecto.
3. Cree y active un entorno virtual (`.venv`).
4. Instale dependencias: `pip install -r requirements.txt`.
5. Copie `.env.example` a `.env`. No es obligatorio cambiar valores para la demostración local.

## 2. Aplicar migraciones

Desde la raíz del proyecto:

```bash
flask --app run.py db upgrade
```

El comando crea `instance/sigr.db` con las tablas de usuarios, categorías, platos, pedidos, ítems, reservas, facturas y cierres de caja. El archivo de revisión es `migrations/versions/001_esquema_inicial.py`. Si el docente recibe el proyecto por ZIP, **debe** ejecutar este paso; no basta con copiar el código.

## 3. Cargar datos de demostración (opcional, recomendado)

```bash
flask --app run.py seed
```

El comando es idempotente: si el administrador de demo ya existe, no duplica registros.

## 4. Arrancar

```bash
python run.py
```

La aplicación queda en `http://127.0.0.1:5000`.

## 5. Recorrido mínimo de verificación

1. Ingrese como `admin@sigr.local` / `admin123`.
2. Revise el menú público y el panel de administración de platos.
3. Registre un pedido, cámbielo a **entregado** (se genera factura).
4. Cree una reserva.
5. Abra **Caja**, consulte el día y registre un cierre.
6. Cierre sesión e ingrese como cliente o mesero para contrastar permisos.

## 6. Pruebas automáticas

```bash
pytest -q
```

Las pruebas usan SQLite en memoria y no modifican `instance/sigr.db`.

## 7. Problemas frecuentes

- **No aparece el menú:** no se ejecutó `flask seed` o la migración no corrió.
- **Error de clave secreta o sesión:** verifique que existe `.env` o acepte el valor de desarrollo.
- **Puerto 5000 ocupado:** cierre la otra aplicación o arranque con `flask --app run.py run --port 5001`.
- **PowerShell bloquea el venv:** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

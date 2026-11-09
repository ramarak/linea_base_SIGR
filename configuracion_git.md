# Configuración de Git para la línea base SIGR

## Rama estable

La rama principal del proyecto es **`main`**. Toda la línea base académica vive en esa rama. No se exige un flujo Git Flow completo para esta entrega, pero sí un historial lineal con commits significativos.

## Flujo recomendado al docente y al equipo

1. Inicializar el repositorio en la raíz del proyecto (`git init`).
2. Nombrar la rama `main`.
3. Añadir el `.gitignore` antes del primer commit para no versionar `.venv`, `instance/` ni archivos `.db`.
4. Registrar commits por tema (estructura, modelo de datos, autenticación, menú y pedidos, reservas y caja, pruebas y documentación).
5. Tomar el hash del **último commit de la línea base** para el informe.

## Repositorio GitHub del equipo

El código se publica en [https://github.com/ramarak/linea_base_SIGR](https://github.com/ramarak/linea_base_SIGR.git).

En el enunciado de la actividad aparece el commit `a93b4f1` como ejemplo. Ese hash **no se puede reproducir**: Git lo calcula a partir del contenido, el mensaje, el autor y la fecha. En el informe `Taller_LineaBase_SIGR.pdf` hay que citar el hash real de `main`:

```bash
git log -1 --oneline
git log origin/main -1 --oneline
```

## Commits representativos de esta línea base

Historial temático de `main` (autor: Ramarak). Los hashes cortos corresponden al historial reescrito antes del commit que actualiza esta nota; el valor a citar en el informe es siempre `git rev-parse --short HEAD`.

1. `86cc6ff` — Commit inicial: estructura del proyecto, licencia MIT e instrucciones de instalacion.
2. `b8252bf` — Modelos de datos y migracion Alembic inicial del esquema SIGR.
3. `a8940d6` — Autenticacion por roles y panel de control.
4. `9022da6` — Menu digital con CRUD y seguimiento de pedidos.
5. `41d2eb7` — Reservas por fecha y hora, facturacion y cierre de caja.
6. `f31f0bc` — Pruebas de integracion, documentacion tecnica y criterio de linea base 1.0.0.
7. `02dfbea` — Documenta los hashes locales de la rama main para el informe.

**Hash de referencia previo a esta actualización de URLs:** `02dfbea`.

## Criterio de línea base

Se considera línea base el commit más reciente de `main` en el que:

- la aplicación arranca tras `flask db upgrade`;
- los cinco módulos obligatorios funcionan;
- `pytest` termina sin fallos;
- README, CHANGELOG, licencia y manual de despliegue están presentes.

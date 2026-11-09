# Configuración de Git para la línea base SIGR

## Rama estable

La rama principal del proyecto es **`main`**. Toda la línea base académica vive en esa rama. No se exige un flujo Git Flow completo para esta entrega, pero sí un historial lineal con commits significativos.

## Flujo recomendado al docente y al equipo

1. Inicializar el repositorio en la raíz del proyecto (`git init`).
2. Nombrar la rama `main`.
3. Añadir el `.gitignore` antes del primer commit para no versionar `.venv`, `instance/` ni archivos `.db`.
4. Registrar commits por tema (estructura, modelo de datos, autenticación, menú y pedidos, reservas y caja, pruebas y documentación).
5. Tomar el hash del **último commit de la línea base** para el informe.

## Hash de ejemplo del repositorio del equipo

En el enunciado de la actividad aparece el commit `a93b4f1` asociado al repositorio GitHub del equipo (`https://github.com/equipoX/sigr`).

Ese hash **no se puede reproducir** en este repositorio local: Git calcula el identificador a partir del contenido, el mensaje, el autor y la fecha. Al redactar `Taller_LineaBase_SIGR.pdf`, el estudiante debe sustituir `a93b4f1` por el hash real que obtenga con:

```bash
git log -1 --oneline
```

o, si el equipo ya publicó el código:

```bash
git log origin/main -1 --oneline
```

## Commits representativos de esta línea base local

Historial de `main` generado en el repositorio local (hashes cortos; use `git log --oneline` si el clon del equipo difiere):

1. `5cca813` — Commit inicial: estructura del proyecto, licencia MIT e instrucciones de instalacion.
2. `099d1b9` — Modelos de datos y migracion Alembic inicial del esquema SIGR.
3. `980dc41` — Autenticacion por roles y panel de control.
4. `5cc6b67` — Menu digital con CRUD y seguimiento de pedidos.
5. `35ac42a` — Reservas por fecha y hora, facturacion y cierre de caja.
6. `d2ac12b` — Pruebas de integracion, documentacion tecnica y criterio de linea base 1.0.0.

**Hash de línea base local de referencia:** `d2ac12b`. Si el equipo añade un commit posterior (por ejemplo, para anotar estos hashes), el valor a citar en el informe es el de `git rev-parse --short HEAD`.

## Criterio de línea base

Se considera línea base el commit más reciente de `main` en el que:

- la aplicación arranca tras `flask db upgrade`;
- los cinco módulos obligatorios funcionan;
- `pytest` termina sin fallos;
- README, CHANGELOG, licencia y manual de despliegue están presentes.

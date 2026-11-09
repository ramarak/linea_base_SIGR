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

El listado definitivo se completa después de inicializar Git. Consulte `git log --oneline` en `main`. Como guía:

1. Estructura inicial, licencia e instrucciones.
2. Modelos y migración de esquema.
3. Autenticación y panel.
4. Menú digital y pedidos.
5. Reservas y caja.
6. Pruebas, documentación y etiqueta de línea base 1.0.0.

## Criterio de línea base

Se considera línea base el commit más reciente de `main` en el que:

- la aplicación arranca tras `flask db upgrade`;
- los cinco módulos obligatorios funcionan;
- `pytest` termina sin fallos;
- README, CHANGELOG, licencia y manual de despliegue están presentes.

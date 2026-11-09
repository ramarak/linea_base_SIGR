# Plantilla de capturas para la línea base

Pegue aquí (o adjunte en el informe PDF) las capturas del sistema en ejecución. Conserve el orden para facilitar la rúbrica.

## 1. Control de versiones

- [ ] `git status` en rama `main`
- [ ] `git log --oneline` con al menos cinco commits hasta la línea base
- [ ] Hash del commit de línea base (reemplazar `a93b4f1` del ejemplo GitHub por el hash real)

## 2. Arranque

- [ ] Terminal con `flask db upgrade` exitoso
- [ ] Terminal con `python run.py` y la URL local
- [ ] Página de inicio SIGR en el navegador

## 3. Autenticación

- [ ] Formulario de inicio de sesión
- [ ] Panel de administrador
- [ ] Panel de mesero
- [ ] Panel de cliente

## 4. Menú

- [ ] Menú digital público
- [ ] Alta o edición de un plato (CRUD)

## 5. Pedidos

- [ ] Formulario de nuevo pedido
- [ ] Listado con cambio de estado

## 6. Reservas

- [ ] Formulario de reserva (fecha y hora)
- [ ] Listado de reservas

## 7. Caja

- [ ] Reporte de ventas del día
- [ ] Confirmación de cierre de caja

## 8. Pruebas

- [ ] Salida de `pytest -q` con todas las pruebas en verde

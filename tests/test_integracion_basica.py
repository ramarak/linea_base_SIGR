from app.extensions import db
from app.models import CierreCaja, Pedido, Plato, Reserva, Usuario
from tests.conftest import iniciar_sesion


def test_servidor_responde_rutas_principales(client):
    inicio = client.get("/")
    login = client.get("/login")
    menu = client.get("/menu/")
    assert inicio.status_code == 200
    assert login.status_code == 200
    assert menu.status_code == 200
    assert b"SIGR" in inicio.data


def test_crear_usuario_y_autenticarse(client, app):
    respuesta = client.post(
        "/registro",
        data={
            "nombre": "Cliente Nuevo",
                "email": "nuevo@example.com",
            "password": "clave123",
            "confirmar": "clave123",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert b"Panel de control" in respuesta.data
    with app.app_context():
        usuario = Usuario.query.filter_by(email="nuevo@example.com").first()
        assert usuario is not None
        assert usuario.rol == "cliente"


def test_crear_plato_crud(client, app, admin, categoria):
    iniciar_sesion(client, "admin@example.com", "clave123")
    respuesta = client.post(
        "/menu/platos/nuevo",
        data={
            "nombre": "Sopa de prueba",
            "descripcion": "Plato de integración",
            "precio": "12000",
            "categoria_id": str(categoria),
            "disponible": "y",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    with app.app_context():
        plato = Plato.query.filter_by(nombre="Sopa de prueba").first()
        assert plato is not None
        assert str(plato.precio) in ("12000", "12000.00")


def test_crear_pedido(client, app, admin, categoria):
    with app.app_context():
        plato = Plato(
            nombre="Jugo de prueba",
            descripcion="Bebida",
            precio=5000,
            disponible=True,
            categoria_id=categoria,
        )
        db.session.add(plato)
        db.session.commit()
        plato_id = plato.id

    iniciar_sesion(client, "admin@example.com", "clave123")
    respuesta = client.post(
        "/pedidos/nuevo",
        data={
            "mesa": "5",
            "notas": "Sin hielo",
            f"cantidad_{plato_id}": "2",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    with app.app_context():
        pedido = Pedido.query.first()
        assert pedido is not None
        assert pedido.estado == "recibido"
        assert len(pedido.items) == 1
        assert pedido.items[0].cantidad == 2


def test_crear_reserva(client, app, admin):
    iniciar_sesion(client, "admin@example.com", "clave123")
    respuesta = client.post(
        "/reservas/nueva",
        data={
            "nombre": "Mesa familiar",
            "contacto": "3001234567",
            "fecha": "2026-11-20",
            "hora": "19:30",
            "personas": "4",
            "observaciones": "Cumpleaños",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    with app.app_context():
        reserva = Reserva.query.first()
        assert reserva is not None
        assert reserva.personas == 4
        assert reserva.estado == "pendiente"


def test_cierre_caja_administrador(client, app, admin):
    iniciar_sesion(client, "admin@example.com", "clave123")
    consulta = client.get("/caja/")
    assert consulta.status_code == 200
    cierre = client.post(
        "/caja/cerrar",
        data={"observaciones": "Cierre de prueba"},
        follow_redirects=True,
    )
    assert cierre.status_code == 200
    with app.app_context():
        registro = CierreCaja.query.first()
        assert registro is not None
        assert registro.total_pedidos == 0

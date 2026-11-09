import pytest

from app import create_app
from app.extensions import db
from app.models import Categoria, Usuario


@pytest.fixture
def app():
    aplicacion = create_app("testing")
    with aplicacion.app_context():
        db.create_all()
        yield aplicacion
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin(app):
    with app.app_context():
        usuario = Usuario(nombre="Admin Prueba", email="admin@example.com", rol="administrador")
        usuario.set_password("clave123")
        db.session.add(usuario)
        db.session.commit()
        return usuario.id


@pytest.fixture
def categoria(app):
    with app.app_context():
        cat = Categoria(nombre="Pruebas", descripcion="Categoría de laboratorio", activa=True)
        db.session.add(cat)
        db.session.commit()
        return cat.id


def iniciar_sesion(client, email, password):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )

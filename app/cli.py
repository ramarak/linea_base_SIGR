from decimal import Decimal

import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Categoria, Plato, Usuario


@click.command("seed")
@with_appcontext
def seed_command():
    """Carga usuarios, categorías y platos de demostración."""
    if Usuario.query.filter_by(email="admin@sigr.local").first():
        click.echo("Los datos de demostración ya existen.")
        return

    admin = Usuario(nombre="Ana Admin", email="admin@sigr.local", rol="administrador")
    admin.set_password("admin123")
    mesero = Usuario(nombre="Mario Mesero", email="mesero@sigr.local", rol="mesero")
    mesero.set_password("mesero123")
    cliente = Usuario(nombre="Carla Cliente", email="cliente@sigr.local", rol="cliente")
    cliente.set_password("cliente123")
    db.session.add_all([admin, mesero, cliente])

    entradas = Categoria(nombre="Entradas", descripcion="Para abrir el apetito")
    fuertes = Categoria(nombre="Platos fuertes", descripcion="Especialidades de la casa")
    bebidas = Categoria(nombre="Bebidas", descripcion="Refrescos y jugos")
    postres = Categoria(nombre="Postres", descripcion="Dulces caseros")
    db.session.add_all([entradas, fuertes, bebidas, postres])
    db.session.flush()

    db.session.add_all(
        [
            Plato(
                nombre="Ajiaco santafereño",
                descripcion="Sopa tradicional con pollo, mazorca y guascas.",
                precio=Decimal("18000"),
                categoria_id=entradas.id,
            ),
            Plato(
                nombre="Empanadas de carne (3 und.)",
                descripcion="Fritas, con ají de la casa.",
                precio=Decimal("8000"),
                categoria_id=entradas.id,
            ),
            Plato(
                nombre="Bandeja paisa",
                descripcion="Frijoles, arroz, carne, chicharrón, huevo y aguacate.",
                precio=Decimal("32000"),
                categoria_id=fuertes.id,
            ),
            Plato(
                nombre="Trucha al ajillo",
                descripcion="Acompañada de papas criollas y ensalada.",
                precio=Decimal("28000"),
                categoria_id=fuertes.id,
            ),
            Plato(
                nombre="Limonada de coco",
                descripcion="Vaso 12 oz.",
                precio=Decimal("7000"),
                categoria_id=bebidas.id,
            ),
            Plato(
                nombre="Café de la casa",
                descripcion="Tinto o espresso.",
                precio=Decimal("3500"),
                categoria_id=bebidas.id,
            ),
            Plato(
                nombre="Tres leches",
                descripcion="Porción individual.",
                precio=Decimal("9000"),
                categoria_id=postres.id,
            ),
        ]
    )
    db.session.commit()
    click.echo("Datos de demostración creados.")
    click.echo("  admin@sigr.local / admin123")
    click.echo("  mesero@sigr.local / mesero123")
    click.echo("  cliente@sigr.local / cliente123")


def register_commands(app):
    app.cli.add_command(seed_command)

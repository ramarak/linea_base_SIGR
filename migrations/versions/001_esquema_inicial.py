"""Esquema inicial SIGR: usuarios, menú, pedidos, reservas, facturas y caja.

Revision ID: 001_esquema_inicial
Revises:
Create Date: 2026-11-09
"""

from alembic import op
import sqlalchemy as sa

revision = "001_esquema_inicial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("rol", sa.String(length=32), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)

    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255)),
        sa.Column("activa", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )

    op.create_table(
        "platos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("descripcion", sa.Text()),
        sa.Column("precio", sa.Numeric(10, 2), nullable=False),
        sa.Column("disponible", sa.Boolean(), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mesa", sa.String(length=20)),
        sa.Column("cliente_id", sa.Integer()),
        sa.Column("mesero_id", sa.Integer()),
        sa.Column("estado", sa.String(length=32), nullable=False),
        sa.Column("notas", sa.String(length=255)),
        sa.Column("total", sa.Numeric(10, 2), nullable=False),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["cliente_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["mesero_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "items_pedido",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("plato_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"]),
        sa.ForeignKeyConstraint(["plato_id"], ["platos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reservas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("contacto", sa.String(length=120), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("hora", sa.Time(), nullable=False),
        sa.Column("personas", sa.Integer(), nullable=False),
        sa.Column("estado", sa.String(length=32), nullable=False),
        sa.Column("observaciones", sa.String(length=255)),
        sa.Column("usuario_id", sa.Integer()),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "facturas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=False),
        sa.Column("total", sa.Numeric(10, 2), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pedido_id"),
        sa.UniqueConstraint("numero"),
    )

    op.create_table(
        "cierres_caja",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("total_ventas", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_pedidos", sa.Integer(), nullable=False),
        sa.Column("observaciones", sa.String(length=255)),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cierres_caja_fecha"), "cierres_caja", ["fecha"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_cierres_caja_fecha"), table_name="cierres_caja")
    op.drop_table("cierres_caja")
    op.drop_table("facturas")
    op.drop_table("reservas")
    op.drop_table("items_pedido")
    op.drop_table("pedidos")
    op.drop_table("platos")
    op.drop_table("categorias")
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")

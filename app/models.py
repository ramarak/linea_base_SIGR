from datetime import date, datetime, time

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager

ROLES = ("cliente", "mesero", "administrador")
ESTADOS_PEDIDO = (
    "recibido",
    "en_preparacion",
    "listo",
    "entregado",
    "cancelado",
)
ESTADOS_RESERVA = ("pendiente", "confirmada", "cancelada", "cumplida")


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(32), nullable=False, default="cliente")
    activo = db.Column(db.Boolean, nullable=False, default=True)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    pedidos_como_cliente = db.relationship(
        "Pedido", backref="cliente", foreign_keys="Pedido.cliente_id"
    )
    pedidos_como_mesero = db.relationship(
        "Pedido", backref="mesero", foreign_keys="Pedido.mesero_id"
    )
    cierres = db.relationship("CierreCaja", backref="usuario")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def es_admin(self):
        return self.rol == "administrador"

    def es_mesero(self):
        return self.rol == "mesero"

    def es_personal(self):
        return self.rol in ("mesero", "administrador")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    activa = db.Column(db.Boolean, nullable=False, default=True)

    platos = db.relationship("Plato", backref="categoria", lazy="dynamic")


class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.String(20))
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    mesero_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    estado = db.Column(db.String(32), nullable=False, default="recibido")
    notas = db.Column(db.String(255))
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items = db.relationship(
        "ItemPedido", backref="pedido", cascade="all, delete-orphan"
    )
    factura = db.relationship("Factura", backref="pedido", uselist=False)

    def recalcular_total(self):
        self.total = sum((item.subtotal for item in self.items), start=0)


class ItemPedido(db.Model):
    __tablename__ = "items_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    plato = db.relationship("Plato")

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    contacto = db.Column(db.String(120), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    hora = db.Column(db.Time, nullable=False, default=time(19, 0))
    personas = db.Column(db.Integer, nullable=False, default=2)
    estado = db.Column(db.String(32), nullable=False, default="pendiente")
    observaciones = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="reservas")


class Factura(db.Model):
    __tablename__ = "facturas"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), unique=True, nullable=False)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class CierreCaja(db.Model):
    __tablename__ = "cierres_caja"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    total_ventas = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_pedidos = db.Column(db.Integer, nullable=False, default=0)
    observaciones = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

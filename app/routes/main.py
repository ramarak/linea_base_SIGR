from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import CierreCaja, Pedido, Plato, Reserva

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dashboard.html")
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    resumen = {
        "platos": Plato.query.count(),
        "pedidos_abiertos": Pedido.query.filter(
            Pedido.estado.in_(["recibido", "en_preparacion", "listo"])
        ).count(),
        "reservas_hoy": Reserva.query.count(),
        "cierres": CierreCaja.query.count(),
    }
    return render_template("dashboard.html", resumen=resumen)

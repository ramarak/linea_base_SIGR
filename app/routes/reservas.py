from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import roles_required
from app.extensions import db
from app.forms import ReservaForm
from app.models import ESTADOS_RESERVA, Reserva

reservas_bp = Blueprint("reservas", __name__, url_prefix="/reservas")


@reservas_bp.route("/")
@login_required
def listar():
    if current_user.es_personal():
        reservas = Reserva.query.order_by(Reserva.fecha.desc(), Reserva.hora.desc()).all()
    else:
        reservas = (
            Reserva.query.filter_by(usuario_id=current_user.id)
            .order_by(Reserva.fecha.desc(), Reserva.hora.desc())
            .all()
        )
    return render_template("reservas/listar.html", reservas=reservas, estados=ESTADOS_RESERVA)


@reservas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    form = ReservaForm()
    if form.validate_on_submit():
        reserva = Reserva(
            nombre=form.nombre.data.strip(),
            contacto=form.contacto.data.strip(),
            fecha=form.fecha.data,
            hora=form.hora.data,
            personas=form.personas.data,
            observaciones=form.observaciones.data,
            usuario_id=current_user.id,
            estado="pendiente",
        )
        db.session.add(reserva)
        db.session.commit()
        flash("Reserva registrada.", "success")
        return redirect(url_for("reservas.listar"))
    if request.method == "GET" and current_user.is_authenticated:
        form.nombre.data = current_user.nombre
        form.contacto.data = current_user.email
    return render_template("reservas/form.html", form=form)


@reservas_bp.route("/<int:reserva_id>/estado", methods=["POST"])
@login_required
@roles_required("mesero", "administrador")
def cambiar_estado(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    nuevo = request.form.get("estado")
    if nuevo not in ESTADOS_RESERVA:
        flash("Estado no válido.", "danger")
        return redirect(url_for("reservas.listar"))
    reserva.estado = nuevo
    db.session.commit()
    flash("Reserva actualizada.", "success")
    return redirect(url_for("reservas.listar"))

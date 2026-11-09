from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import roles_required
from app.extensions import db
from app.forms import CierreCajaForm
from app.models import CierreCaja, Factura, Pedido

caja_bp = Blueprint("caja", __name__, url_prefix="/caja")


def _ventas_del_dia(dia):
    inicio = datetime.combine(dia, datetime.min.time())
    fin = datetime.combine(dia, datetime.max.time())
    facturas = Factura.query.filter(Factura.fecha >= inicio, Factura.fecha <= fin).all()
    pedidos_entregados = Pedido.query.filter(
        Pedido.estado == "entregado",
        Pedido.actualizado_en >= inicio,
        Pedido.actualizado_en <= fin,
    ).count()
    total = sum((f.total for f in facturas), start=0)
    return facturas, total, pedidos_entregados


@caja_bp.route("/")
@login_required
@roles_required("administrador")
def reporte():
    dia_txt = request.args.get("fecha")
    try:
        dia = date.fromisoformat(dia_txt) if dia_txt else date.today()
    except ValueError:
        dia = date.today()
    facturas, total, pedidos_entregados = _ventas_del_dia(dia)
    cierres = CierreCaja.query.filter_by(fecha=dia).order_by(CierreCaja.creado_en.desc()).all()
    form = CierreCajaForm()
    return render_template(
        "caja/reporte.html",
        dia=dia,
        facturas=facturas,
        total=total,
        pedidos_entregados=pedidos_entregados,
        cierres=cierres,
        form=form,
    )


@caja_bp.route("/cerrar", methods=["POST"])
@login_required
@roles_required("administrador")
def cerrar():
    form = CierreCajaForm()
    dia = date.today()
    if not form.validate_on_submit():
        flash("No se pudo registrar el cierre.", "danger")
        return redirect(url_for("caja.reporte"))
    _, total, pedidos_entregados = _ventas_del_dia(dia)
    cierre = CierreCaja(
        fecha=dia,
        usuario_id=current_user.id,
        total_ventas=total,
        total_pedidos=pedidos_entregados,
        observaciones=form.observaciones.data,
    )
    db.session.add(cierre)
    db.session.commit()
    flash("Cierre de caja registrado.", "success")
    return redirect(url_for("caja.reporte", fecha=dia.isoformat()))

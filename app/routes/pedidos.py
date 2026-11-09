from datetime import datetime
from decimal import Decimal

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import roles_required
from app.extensions import db
from app.forms import PedidoForm
from app.models import ESTADOS_PEDIDO, Factura, ItemPedido, Pedido, Plato

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")


def _siguiente_numero_factura():
    ultima = Factura.query.order_by(Factura.id.desc()).first()
    n = 1 if ultima is None else ultima.id + 1
    return f"FAC-{n:05d}"


def _facturar_si_entregado(pedido):
    if pedido.estado != "entregado" or pedido.factura:
        return
    factura = Factura(
        pedido_id=pedido.id,
        numero=_siguiente_numero_factura(),
        total=pedido.total,
        fecha=datetime.utcnow(),
    )
    db.session.add(factura)


@pedidos_bp.route("/")
@login_required
def listar():
    if current_user.es_personal():
        pedidos = Pedido.query.order_by(Pedido.creado_en.desc()).all()
    else:
        pedidos = (
            Pedido.query.filter_by(cliente_id=current_user.id)
            .order_by(Pedido.creado_en.desc())
            .all()
        )
    return render_template("pedidos/listar.html", pedidos=pedidos, estados=ESTADOS_PEDIDO)


@pedidos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    form = PedidoForm()
    platos = Plato.query.filter_by(disponible=True).order_by(Plato.nombre).all()
    if request.method == "POST":
        pedido = Pedido(
            mesa=form.mesa.data or None,
            notas=form.notas.data,
            estado="recibido",
            cliente_id=current_user.id if current_user.rol == "cliente" else None,
            mesero_id=current_user.id if current_user.es_personal() else None,
        )
        hay_items = False
        for plato in platos:
            raw = request.form.get(f"cantidad_{plato.id}", "0")
            try:
                cantidad = int(raw)
            except ValueError:
                cantidad = 0
            if cantidad > 0:
                hay_items = True
                pedido.items.append(
                    ItemPedido(
                        plato_id=plato.id,
                        cantidad=cantidad,
                        precio_unitario=Decimal(plato.precio),
                    )
                )
        if not hay_items:
            flash("Seleccione al menos un plato.", "warning")
            return render_template("pedidos/nuevo.html", form=form, platos=platos)
        pedido.recalcular_total()
        db.session.add(pedido)
        db.session.commit()
        flash(f"Pedido #{pedido.id} registrado.", "success")
        return redirect(url_for("pedidos.listar"))
    return render_template("pedidos/nuevo.html", form=form, platos=platos)


@pedidos_bp.route("/<int:pedido_id>/estado", methods=["POST"])
@login_required
@roles_required("mesero", "administrador")
def cambiar_estado(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    nuevo = request.form.get("estado")
    if nuevo not in ESTADOS_PEDIDO:
        flash("Estado no válido.", "danger")
        return redirect(url_for("pedidos.listar"))
    pedido.estado = nuevo
    pedido.actualizado_en = datetime.utcnow()
    if current_user.es_mesero() and not pedido.mesero_id:
        pedido.mesero_id = current_user.id
    _facturar_si_entregado(pedido)
    db.session.commit()
    flash(f"Pedido #{pedido.id} actualizado a {nuevo.replace('_', ' ')}.", "success")
    return redirect(url_for("pedidos.listar"))


@pedidos_bp.route("/api/estados")
@login_required
def api_estados():
    if current_user.es_personal():
        pedidos = Pedido.query.order_by(Pedido.creado_en.desc()).all()
    else:
        pedidos = Pedido.query.filter_by(cliente_id=current_user.id).all()
    return jsonify(
        [
            {
                "id": p.id,
                "estado": p.estado,
                "total": str(p.total),
                "mesa": p.mesa,
            }
            for p in pedidos
        ]
    )

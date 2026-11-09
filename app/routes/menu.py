from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.decorators import roles_required
from app.extensions import db
from app.forms import CategoriaForm, PlatoForm
from app.models import Categoria, Plato

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route("/")
def listar():
    categorias = Categoria.query.filter_by(activa=True).order_by(Categoria.nombre).all()
    return render_template("menu/listar.html", categorias=categorias)


@menu_bp.route("/admin")
@login_required
@roles_required("administrador")
def admin():
    platos = Plato.query.order_by(Plato.nombre).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("menu/admin.html", platos=platos, categorias=categorias)


@menu_bp.route("/categorias/nueva", methods=["GET", "POST"])
@login_required
@roles_required("administrador")
def categoria_nueva():
    form = CategoriaForm()
    if form.validate_on_submit():
        db.session.add(
            Categoria(
                nombre=form.nombre.data.strip(),
                descripcion=form.descripcion.data,
                activa=form.activa.data,
            )
        )
        db.session.commit()
        flash("Categoría creada.", "success")
        return redirect(url_for("menu.admin"))
    return render_template("menu/categoria_form.html", form=form, titulo="Nueva categoría")


@menu_bp.route("/categorias/<int:categoria_id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("administrador")
def categoria_editar(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data.strip()
        categoria.descripcion = form.descripcion.data
        categoria.activa = form.activa.data
        db.session.commit()
        flash("Categoría actualizada.", "success")
        return redirect(url_for("menu.admin"))
    return render_template("menu/categoria_form.html", form=form, titulo="Editar categoría")


@menu_bp.route("/categorias/<int:categoria_id>/eliminar", methods=["POST"])
@login_required
@roles_required("administrador")
def categoria_eliminar(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    if categoria.platos.count():
        flash("No se puede eliminar una categoría con platos. Desactívela.", "warning")
        return redirect(url_for("menu.admin"))
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría eliminada.", "success")
    return redirect(url_for("menu.admin"))


@menu_bp.route("/platos/nuevo", methods=["GET", "POST"])
@login_required
@roles_required("administrador")
def plato_nuevo():
    form = PlatoForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre)]
    if form.validate_on_submit():
        db.session.add(
            Plato(
                nombre=form.nombre.data.strip(),
                descripcion=form.descripcion.data,
                precio=form.precio.data,
                disponible=form.disponible.data,
                categoria_id=form.categoria_id.data,
            )
        )
        db.session.commit()
        flash("Plato creado.", "success")
        return redirect(url_for("menu.admin"))
    return render_template("menu/plato_form.html", form=form, titulo="Nuevo plato")


@menu_bp.route("/platos/<int:plato_id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("administrador")
def plato_editar(plato_id):
    plato = Plato.query.get_or_404(plato_id)
    form = PlatoForm(obj=plato)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre)]
    if request.method == "GET":
        form.categoria_id.data = plato.categoria_id
    if form.validate_on_submit():
        plato.nombre = form.nombre.data.strip()
        plato.descripcion = form.descripcion.data
        plato.precio = form.precio.data
        plato.disponible = form.disponible.data
        plato.categoria_id = form.categoria_id.data
        db.session.commit()
        flash("Plato actualizado.", "success")
        return redirect(url_for("menu.admin"))
    return render_template("menu/plato_form.html", form=form, titulo="Editar plato")


@menu_bp.route("/platos/<int:plato_id>/eliminar", methods=["POST"])
@login_required
@roles_required("administrador")
def plato_eliminar(plato_id):
    plato = Plato.query.get_or_404(plato_id)
    db.session.delete(plato)
    db.session.commit()
    flash("Plato eliminado.", "success")
    return redirect(url_for("menu.admin"))

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms import LoginForm, RegistroForm
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()
        if usuario and usuario.activo and usuario.check_password(form.password.data):
            login_user(usuario)
            flash(f"Bienvenido, {usuario.nombre}.", "success")
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("main.dashboard"))
        flash("Correo o contraseña incorrectos.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistroForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data.lower().strip()).first():
            flash("Ese correo ya está registrado.", "warning")
            return render_template("auth/registro.html", form=form)
        usuario = Usuario(
            nombre=form.nombre.data.strip(),
            email=form.email.data.lower().strip(),
            rol="cliente",
        )
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario)
        flash("Cuenta creada. Ya puede usar el sistema.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("auth/registro.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired()])


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired(), Length(max=120)])
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden.")],
    )


class CategoriaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    descripcion = StringField("Descripción", validators=[Length(max=255)])
    activa = BooleanField("Activa", default=True)


class PlatoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    descripcion = TextAreaField("Descripción")
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    disponible = BooleanField("Disponible", default=True)
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])


class PedidoForm(FlaskForm):
    mesa = StringField("Mesa", validators=[Length(max=20)])
    notas = StringField("Notas", validators=[Length(max=255)])


class ReservaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    contacto = StringField("Contacto", validators=[DataRequired(), Length(max=120)])
    fecha = DateField("Fecha", validators=[DataRequired()])
    hora = TimeField("Hora", validators=[DataRequired()])
    personas = IntegerField("Personas", validators=[DataRequired(), NumberRange(min=1, max=20)])
    observaciones = StringField("Observaciones", validators=[Length(max=255)])


class CierreCajaForm(FlaskForm):
    observaciones = TextAreaField("Observaciones", validators=[Length(max=255)])

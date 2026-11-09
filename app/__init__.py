import os

from flask import Flask, render_template

from app.config import DevelopmentConfig, TestingConfig
from app.extensions import csrf, db, login_manager, migrate


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    nombre = config_name or os.environ.get("FLASK_ENV", "development")
    if nombre == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(app.root_path), "instance"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Inicie sesión para continuar."
    login_manager.login_message_category = "warning"

    from app import models  # noqa: F401
    from app.cli import register_commands
    from app.routes.auth import auth_bp
    from app.routes.caja import caja_bp
    from app.routes.main import main_bp
    from app.routes.menu import menu_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.reservas import reservas_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(caja_bp)

    register_commands(app)

    @app.errorhandler(403)
    def prohibido(_error):
        return render_template("errors/403.html"), 403

    return app

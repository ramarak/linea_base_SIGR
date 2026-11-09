from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    def decorator(vista):
        @wraps(vista)
        def envuelta(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.rol not in roles:
                flash("No tiene permiso para acceder a esta sección.", "danger")
                abort(403)
            return vista(*args, **kwargs)

        return envuelta

    return decorator

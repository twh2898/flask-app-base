
def init_app(app):
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import debug
    app.register_blueprint(debug.bp)

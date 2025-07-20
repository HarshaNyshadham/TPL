from .main import main_bp
from .admin import admin_bp
from .auth import auth_bp

def init_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
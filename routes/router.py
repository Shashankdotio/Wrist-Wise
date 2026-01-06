from .health import health_bp
from .upload import upload_bp
from .count import count_bp
from .analytics import analytics_bp


def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(count_bp)
    app.register_blueprint(analytics_bp)

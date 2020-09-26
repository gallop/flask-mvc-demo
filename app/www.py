
from app.web.api import route_api


def register_blueprints(app):
    app.register_blueprint(route_api, url_prefix="/api")

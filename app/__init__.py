import datetime

from .application import Application
from . import www
from .models.Base import db


def create_app():
    app = Application(__name__)
    # session 过期设置，这里默认30分钟
    app.permanent_session_lifetime = datetime.timedelta(seconds=30 * 60)
    db.init_app(app)
    www.register_blueprints(app)

    return app
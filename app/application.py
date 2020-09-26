# -*- coding: utf-8 -*-
from datetime import datetime, date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
# from . import www
import os

from app.models.Base import db


# from app.web.api import route_api
class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return dict(obj)


class Flask(_Flask):
    json_encoder = JSONEncoder


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])


# db = SQLAlchemy()


# app.register_blueprint(route_api, url_prefix="/api")


json_result = {"status": 200, "msg": "操作成功~~", "data": {}}

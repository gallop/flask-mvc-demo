# -*- coding: utf-8 -*-
from flask import Blueprint

route_api = Blueprint('api_page', __name__)
from app.web.api.UserController import *

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.validators.Base import BaseForm


class ClientForm(BaseForm):
    username = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    password = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=6, max=32
    )])



from collections import namedtuple

from flask import current_app, request, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, \
    SignatureExpired

# scheme就是token前面的字符串，可以自定义，这里我使用JWT
from app.common.libs.error_code import AuthFailed
from app.common.libs.response_code import Const

auth = HTTPTokenAuth(scheme='JWT')
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_token
def verify_token(token):
    s = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY']
    )
    try:
        data = s.loads(token)
        print(data)
    except BadSignature:
        raise AuthFailed(msg='token不正确', status=Const.TOKEN_BAD_SIGNATURE)
    except SignatureExpired:
        raise AuthFailed(msg='token过期', status=Const.TOKEN_EXPIRED)

    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']

    g.current_user = User(uid, ac_type, scope)

    return True


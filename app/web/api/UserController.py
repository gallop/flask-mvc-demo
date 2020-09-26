from itsdangerous import BadSignature

from app.common.libs.ClientType import ClientTypeEnum
from app.common.libs.bms_auth import permission_required
from app.common.libs.jwt_auth import auth
from app.common.libs.response_code import Const
from app.service import UserService
from app.validators.Forms import ClientForm
from app.web.api import route_api
from flask import request, current_app, jsonify, g, session
from app.common.libs.JWTSerializer import JWTSericlizer as Serializer
from app.application import json_result


@route_api.route('/register', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if data and "username" in data:
        user_name = data["username"]
    else:
        user_name = None
    if data and "password" in data:
        password = str(data["password"])
    else:
        password = None

    print("username:%s, password:%s" % (user_name, password))

    UserService.register(user_name, password)

    return jsonify(json_result)


@route_api.route('/get_token', methods=['POST'])
def get_token():
    # get_json(self,force=False,silent=False,cache=True)：作为json解析并返回数据，
    # 如果MIME类型不是json，返回None（除非force设为True）；
    # 解析出错则抛出Werkzeug提供的BadRequest异常（如果未开启调试模式，则返回400错误响应），
    # 如果silent设为True则返回None；cache设置是否缓存解析后的json数据
    data = request.get_json(silent=True)
    if data and "username" in data:
        user_name = data["username"]
    else:
        user_name = None
    if data and "password" in data:
        password = data["password"]
    else:
        password = None

    identity = UserService.verify(user_name, password)
    # Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    print('wecharType:', ClientTypeEnum.WECHAR.value)
    token = generate_auth_token(identity['uid'],
                                ClientTypeEnum.WECHAR.value,
                                identity['scope'])
    print('original-token:', token)
    print('create-token:', token.decode('ascii'))
    json_result["data"]["token"] = token.decode('ascii')
    print('json_result:', json_result)
    return jsonify(json_result)


@route_api.route('/refresh_token', methods=['POST'])
def refresh_token():
    data = request.get_json(silent=True)
    new_token = ''
    if data and "token" in data:
        old_token = data["token"]
        try:
            s = Serializer(current_app.config['SECRET_KEY'])
            new_token = s.refresh_token(old_token)
            json_result['data']['token'] = new_token
        except BadSignature:
            json_result['status'] = Const.TOKEN_INVALID
            json_result['msg'] = "不可用的token～～"
    json_result['msg'] = "刷新token成功"
    return jsonify(json_result)


@route_api.route('/get_user_info', methods=['GET'])
@auth.login_required()
def get_user_info():
    current_user = g.current_user
    print('current_uid:', current_user.uid)
    user = UserService.get_user_info(g.current_user.uid)
    user = user.hide("login_pwd")
    json_result["data"] = user
    return jsonify(json_result)


def generate_auth_token(uid, ac_type, scope=None):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=current_app.config["TOKEN_EXPIRATION"])
    return s.dumps({
        'uid': uid,
        'type': ac_type,
        'scope': scope
    })


# -----------------以下是后台管理开发的权限验证例子-----------------------

@route_api.route('/login', methods=['POST'])
def login():
    session.permanent = True
    form = ClientForm().validate_for_api()
    UserService.verify_bms(form.username.data, form.password.data)
    json_result['msg'] = '登入成功！'
    return jsonify(json_result)


@route_api.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('current_user', None)
    session.pop('permissions', None)

    return jsonify(json_result)


@route_api.route('/user/<int:uid>', methods=['GET'])
@permission_required('admin:user:read')
def get_user(uid):
    user = UserService.get_user_info(uid)
    return jsonify(user)

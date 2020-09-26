from werkzeug.security import check_password_hash
from flask import session
from app.application import db
from app.common.libs.error_code import NotFoundError, AuthFailed
from app.models.Permission import Permission
from app.models.User import User


def check_password(hash_pwd, raw):
    return check_password_hash(hash_pwd, raw)


def verify(username, password):
    user = User.query.filter_by(login_name=username).first()
    if not user:
        raise NotFoundError()
    if not check_password(user.login_pwd, password):
        raise AuthFailed()
    return {'uid': user.uid, 'scope': "UserScope"}


# 用于做后台管理的账号登入验证，主要是加入对应用户的permission
# bms: backstage management system
def verify_bms(username, password):
    print('username: %s,password: %s' % (username, password))
    user = User.query.filter_by(login_name=username).first()
    if not user:
        raise NotFoundError("无此用户！")
    if not check_password(user.login_pwd, password):
        raise AuthFailed()

    user.roles = eval(user.role_ids)

    for role_id in user.roles:
        list_permis = get_permission_by_roleid(role_id)
        if list_permis:
            for permis in list_permis:
                user.permissions.append(permis.permission)
    session['current_user'] = user
    print('after-load-permissions:', user.permissions)
    session['permissions'] = user.permissions
    return user


def register(username, password):
    user = User()
    user.login_name = username
    user.password = password

    db.session.add(user)
    db.session.commit()


def get_user_info(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    if not user:
        raise NotFoundError("没有此用户")
    return user


def get_permission_by_roleid(role_id):
    print('role_id:', role_id)
    list_permission = Permission.query.filter_by(role_id=role_id).all()
    print('list_permission:', list_permission)

    return list_permission

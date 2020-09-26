from functools import wraps
from flask import session

from app.common.libs.error_code import Forbidden


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # if 'FREE_LOGIN_WHITELIST' in current_app.config and request.remote_addr in current_app.config[
            # 'FREE_LOGIN_WHITELIST']: return func(*args, **kwargs)
            user_info = session.get("current_user")
            # print('current_user:', user_info)
            # print('expect permis:',permission)
            # print('permission2:', session.get('permissions'))

            if user_info:
                if str(permission) in session.get('permissions'):
                    return func(*args, **kwargs)
                else:
                    raise Forbidden("没有相关权限！")
            else:
                raise Forbidden("未登陆，无权访问！")

        return decorated_function

    return decorator

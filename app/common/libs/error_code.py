from app.common.libs.error import APIException

class Success(APIException):
    code = 201
    msg = 'ok'
    status = 0


class DeleteSuccess(Success):
    code = 202
    status = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    status = 999


class ClientTypeError(APIException):
    # 400 401 403 404
    # 500
    # 200 201 204
    # 301 302
    code = 400
    msg = 'client is invalid'
    status = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    status = 1000


class NotFoundError(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    status = 1001


class AuthFailed(APIException):
    code = 401
    status = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    status = 1004
    msg = 'forbidden, not in scope'
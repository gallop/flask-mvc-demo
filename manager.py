from werkzeug.exceptions import HTTPException

from flask_script import Manager, Server
from app import create_app
from app.common.libs.error import APIException
from app.common.libs.error_code import ServerError
from app.common.libs.response_code import Const

app = create_app()

manager = Manager(app)

manager.add_command("runserver",
                    Server(host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=True, use_reloader=True))


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = Const.HTTP_ERROR
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


def main():
    manager.run( )


if __name__ == '__main__':
    # app.run(debug=True)
    try:
        import sys
        sys.exit(main() )
    except Exception as e:
        import traceback
        traceback.print_exc()

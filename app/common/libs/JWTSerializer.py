from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_, JSONWebSignatureSerializer, \
    BadSignature, BadHeader, SignatureExpired, Serializer


class JWTSericlizer(Serializer_):
    def __init__(self, secret_key, expires_in=None, **kwargs):
        self.expires_in = expires_in
        super(JWTSericlizer, self).__init__(secret_key, expires_in, **kwargs)

    def make_header(self, header_fields):
        header = JSONWebSignatureSerializer.make_header(self, header_fields)
        iat = self.now()
        exp = iat + self.expires_in
        refresh_exp = iat + current_app.config["TOKEN_REFRESH_TIME"]
        header["iat"] = iat
        header["exp"] = exp
        header["refresh_exp"] = refresh_exp
        return header

    def refresh_token(self, s, salt=None):
        payload, header = JSONWebSignatureSerializer.loads(
            self, s, salt, return_header=True
        )

        if "exp" not in header:
            raise BadSignature("Missing expiry date", payload=payload)

        int_date_error = BadHeader("Expiry date is not an IntDate", payload=payload)
        try:
            header["exp"] = int(header["exp"])
        except ValueError:
            raise int_date_error
        if header["exp"] < 0:
            raise int_date_error
        now = self.now()
        if header["exp"] < now:
            if header["refresh_exp"] < now:
                # 已经过了可刷新时间，直接抛出异常
                raise SignatureExpired(
                    "Signature expired",
                    payload=payload,
                    date_signed=self.get_issue_date(header),
                )
            else:
                # 生成新的token返回给前端
                serializer = Serializer(current_app.config["SECRET_KEY"], expires_in=self.expires_in)
                # 调用serializer的dumps方法将uid和type写入生成token
                token = serializer.dumps(payload)
                # res = make_response()
                # res.headers["Authorization"] = token
                # res.set_cookie("authorization", token.decode("ascii"))
                return token

        return ''

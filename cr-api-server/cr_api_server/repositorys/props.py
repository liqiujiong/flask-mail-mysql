# -*- coding:utf-8 -*-

from flask import request, g
from flask import jsonify
import functools
import traceback
import jwt
from webargs.flaskparser import FlaskParser
from ..config import Config
from cr_api_server.repositorys.token import IDToken

jwt_secret = Config.JWT_SECRET


def auth(f):
    """权限校验"""
    @functools.wraps(f)
    def warpper(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return error_with_noauth(reason='no token')
        try:
            payload = IDToken(jwt_secret).jwt_decode(token)
            print(payload)
        except jwt.ExpiredSignatureError:
            return error_with_noauth(reason='token expired')
        except jwt.InvalidSignatureError:
            return error_with_noauth(reason='invalid signature')
        except jwt.InvalidTokenError:
            return error_with_noauth(reason='invalid token')
        if not payload:
            return error(reason='no payload')

        g.user_id = payload['id']
        g.user_role = payload['role']
        g.user_province = payload['province']
        g.user_city = payload['city']
        return f(*args, **kwargs)

    return warpper


parser = FlaskParser()


class ValidateException(Exception):
    pass


class AuthException(Exception):
    pass


@parser.error_handler
def handle_error(error, req, schema):
    raise ValidateException(error.messages)


def panic(schema=None):
    """异常"""

    def outter(func):
        if schema:
            @parser.use_args(schema)
            def run_func(*args, **kwargs):
                return func(*args, **kwargs)
        else:
            run_func = func

        @functools.wraps(func)
        def warpper(*args, **kwargs):
            try:
                return run_func(*args, **kwargs)
            except ValidateException as e:
                return error(reason="{}".format(e))
            except AuthException as e:
                return error_with_noauth(reason="{}".format(e))
            except Exception as e:
                traceback.print_exc()
                return error(reason="{}".format(e))

        return warpper

    return outter


def success(data: dict = None):
    s = {
        "status": "ok"
    }
    if data:
        s.update(data)
    return jsonify(s)


def error(data: dict = None, reason: str = None):
    s = {
        "status": "error",
        "reason": reason
    }
    if data:
        s.update(data)
    return jsonify(s)


def error_with_noauth(data: dict = None, reason: str = None):
    s = {
        "status": "error",
        "reason": reason
    }

    if data:
        s.update(data)

    return jsonify(s), 403

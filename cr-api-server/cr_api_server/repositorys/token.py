import jwt
import time

"""
id_token: 实现JWT的encode同decode
"""


class IDToken(object):

    def __init__(self, secret):
        self._secret = secret

    def jwt_encode(self, payload: dict) -> str:
        base_payload = {
            # "iss": "",  # (issuer)：签发人
            "exp": int(time.time()) + 86400,  # (expiration time)：过期时间
            # "sub": "",  # (subject)：主题
            # "aud": "",  # (audience)：受众
            "nbf": int(time.time()),  # (Not Before)：生效时间
            "iat": int(time.time()),  # (Issued At)：签发时间
            # "jti": "",  # (JWT ID)：编号
        }
        payload.update(base_payload)
        return jwt.encode(payload, self._secret, algorithm='HS256')

    def jwt_decode(self, sign: str) -> dict:
        sign = sign.replace("Bearer ", "")
        return jwt.decode(sign, self._secret, algorithms='HS256')

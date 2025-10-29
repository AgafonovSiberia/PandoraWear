import datetime
from calendar import timegm
from uuid import UUID

import jwt
from app.config_reader import config
from app.utils.uuid import UUIDEncoder
from jwt import ExpiredSignatureError, InvalidSignatureError

TTL_AT = config.TTL_ACCESS_TOKEN
TTL_RT = config.TTL_REFRESH_TOKEN


def create_token(user_id: UUID, type_token: str, exp: int = None, secret_key: str = None):
    if exp is None:
        exp = timegm(
            (
                datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(minutes=TTL_AT if type_token == "access" else TTL_RT)
            ).utctimetuple()
        )

    if secret_key is None:
        secret_key = config.SECRET_KEY

    token = jwt.encode(
        payload={"user_id": user_id, "exp": exp},
        key=secret_key,
        headers={"type": "JWT", "type_token": type_token, "alg": "HS256"},
        algorithm="HS256",
        json_encoder=UUIDEncoder,
    )
    return token, exp


def check_token(token: str, leeway: int = 10):
    """Проверка валидности jwt-токена, созданного сервером"""
    try:
        if token is None:
            raise InvalidSignatureError
        payload = jwt.decode(
            jwt=token,
            key=config.SECRET_KEY,
            algorithms="HS256",
            verify_signature=True,
            leeway=leeway,
        )
    except InvalidSignatureError:
        return {"status": "error", "message": "invalid token"}
    except ExpiredSignatureError:
        return {"status": "error", "message": "token has expired"}
    else:
        return {"status": "ok", "message": "correct token", "payload": payload}
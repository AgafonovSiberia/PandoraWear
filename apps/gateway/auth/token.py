from datetime import UTC, datetime, timedelta
from typing import Any, Mapping, Optional

import jwt

ALGORITHM = "HS256"
TTL_TOKEN = 60 * 24


def generate_jwt(
    payload: Mapping[str, Any],
    secret: str,
    issuer: Optional[str] = "pandora-api",
    audience: Optional[str] = None,
    ttl: int = TTL_TOKEN,
) -> str:
    now = datetime.now(UTC)

    claims: dict[str, Any] = dict(payload)
    claims.setdefault("iat", now)
    claims.setdefault("nbf", now)
    claims.setdefault("exp", now + timedelta(seconds=TTL_TOKEN))
    if issuer is not None:
        claims.setdefault("iss", issuer)
    if audience is not None:
        claims.setdefault("aud", audience)

    token = jwt.encode(claims, secret, algorithm=ALGORITHM)
    return token


def decode_jwt(
    token: str,
    secret: str,
    issuer: str | None = "pandora-api",
    audience: str | None = None,
    leeway: int | float = 10,
) -> dict[str, Any]:
    options = {
        "require": ["exp", "iat", "nbf"],
    }

    decoded = jwt.decode(
        token,
        secret,
        algorithms=("HS256",),
        issuer=issuer,
        audience=audience,
        leeway=leeway,
        options=options,
    )
    return decoded

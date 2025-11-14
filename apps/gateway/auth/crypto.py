import bcrypt


def hash_value(value: str) -> bytes:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt())


def check_hashed_value(value: str, hashed_value: bytes) -> bool:
    try:
        return bcrypt.checkpw(value.encode(), hashed_value)
    except ValueError:
        return False

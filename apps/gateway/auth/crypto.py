import bcrypt


def hash_value(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_hashed_value(password: str, hash_password: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hash_password)
    except ValueError:
        return False

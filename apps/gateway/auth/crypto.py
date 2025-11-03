import bcrypt


def crypt_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hash_password: bytes) -> bool:
    try:
        bcrypt.checkpw(password.encode(), hash_password)
    except ValueError:
        return False
    else:
        return True
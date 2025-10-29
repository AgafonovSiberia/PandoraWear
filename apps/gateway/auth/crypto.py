import bcrypt


def crypt_password(password: str) -> str:
    return str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))


def check_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password.encode())

class APIError(Exception):
    pass


class LoginException(APIError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"[Authorization error] - {self.msg}"

class APIError(Exception):
    pass


class LoginException(APIError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"[Authorization error] - {self.msg}"


class NotDeviceId(APIError):
    def __init__(self, device_name: str):
        self.device_name = device_name

    def __str__(self):
        return f"[Device not found] - {self.device_name}"

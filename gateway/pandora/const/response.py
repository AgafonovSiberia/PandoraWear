from enum import StrEnum


class ResponseStatus(StrEnum):
    INVALID_SESSION = "Invalid session"
    EXPIRE_SESSION = "Session is expired"
    SID_EXPIRED = "sid-expired"

    @classmethod
    def session_expire_statuses(cls):
        return [
            cls.EXPIRE_SESSION,
            cls.INVALID_SESSION,
            cls.SID_EXPIRED
        ]

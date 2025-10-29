from enum import StrEnum


class AuthResponseField(StrEnum):
    STATUS = "status"
    SESSION_ID = "session_id"


class DeviceResponseField(StrEnum):
    ID = "id"
    NAME = "name"
    PHONE = "phone"

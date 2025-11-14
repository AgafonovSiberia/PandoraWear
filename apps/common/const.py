from enum import StrEnum


class ServiceName(StrEnum):
    PANDORA = "pandora_client"

class AlarmAction(StrEnum):
    START = "start"
    STOP = "stop"

    
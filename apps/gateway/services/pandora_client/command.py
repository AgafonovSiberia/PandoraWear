from enum import IntEnum


class PandoraEngineCommand(IntEnum):
    RUN_ENGINE = 4
    STOP_ENGINE = 8


class PandoraCommand(IntEnum):
    START = PandoraEngineCommand.RUN_ENGINE
    STOP = PandoraEngineCommand.STOP_ENGINE

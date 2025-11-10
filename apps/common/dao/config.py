from pydantic import BaseModel, ConfigDict

from apps.common.const import ServiceName


class _Config(BaseModel):
    id: int | None = None
    user_id: int
    service: str = ServiceName.PANDORA
    creds: dict = {}

    model_config = ConfigDict(from_attributes=True)


class ConfigIn(_Config): ...

class ConfigDomain(_Config): ...


class _PandoraCred(BaseModel):
    email: str = None
    password: str = None

    model_config = ConfigDict(from_attributes=True)

class PandoraCredIn(_PandoraCred): ...

class PandoraCredUpsert(_PandoraCred):
    user_id: int

class PandoraCredDomain(_PandoraCred): ...

class PandoraConfig(BaseModel):
    credentials: PandoraCredDomain
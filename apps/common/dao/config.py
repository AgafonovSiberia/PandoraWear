from pydantic import BaseModel, ConfigDict, Field

from apps.common.const import ServiceName


class _PandoraCred(BaseModel):
    id: int | None
    user_id: int
    service: str = ServiceName.PANDORA
    credentials: dict = {}

    model_config = ConfigDict(from_attributes=True)


class PandoraCredIn(_PandoraCred): ...


class PandoraCredDomain(_PandoraCred): ...

class PandoraEmptyCred(BaseModel):
    user_id: int
    service: ServiceName = ServiceName.PANDORA
    credentials: dict = Field(default_factory=dict)
    
    model_config = ConfigDict(from_attributes=True)

class PandoraConfig(BaseModel):
    credentials: PandoraCredDomain
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreatedCode(BaseModel):
    code: str
    expire_dt: datetime


class BindedDevice(BaseModel):
    device_id: UUID
    token: str
    user_id: int
    expire_dt: datetime

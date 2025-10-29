from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


@dataclass(frozen=True)
class DevicePrincipal:
    user_id: UUID
    device_id: UUID


@dataclass(frozen=True)
class AdminPrincipal:
    user_id: UUID
    email: str


class CreatedCode(BaseModel):
    code: str
    expire_dt: datetime


class BindedDevice(BaseModel):
    device_id: UUID
    token: str
    user_id: int
    expire_dt: datetime

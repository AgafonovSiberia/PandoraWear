import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceIn(BaseModel):
    id: uuid.UUID | None = None
    user_id: int
    name: str
    token_hash: bytes
    expires_at: datetime
    last_used_at: datetime = None
    last_rotated_at: datetime


class DeviceDomain(BaseModel):
    id: uuid.UUID
    user_id: int
    name: str
    token_hash: bytes
    expires_at: datetime = None
    last_used_at: datetime = None
    last_rotated_at: datetime = None

    model_config = ConfigDict(from_attributes=True)

class DeviceRegData(BaseModel):
    name: str
    
class DevicePairDataIn(BaseModel):
    code: str

class DevicePairDataOut(BaseModel):
    device_id: uuid.UUID
    token: str

class DeviceRevoke(BaseModel):
    device_id: str | uuid.UUID
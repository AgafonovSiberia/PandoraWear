from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, constr


# ----- Общие -----
class ApiMessage(BaseModel):
    message: str


# ----- Pairing -----
PairCode = constr(pattern=r"^[0-9]{6}$")


class PairCodeCreateOut(BaseModel):
    code: PairCode
    expires_at: datetime


class PairClaimIn(BaseModel):
    code: PairCode
    device_name: constr(min_length=1, max_length=64)


class PairClaimOut(BaseModel):
    token: str
    device_id: UUID
    user_id: UUID
    expires_at: datetime


class DeviceOut(BaseModel):
    id: UUID
    name: str
    status: Literal["linked", "revoked"]
    last_seen_at: Optional[datetime] = None
    created_at: datetime


class DeviceRenameIn(BaseModel):
    name: constr(min_length=1, max_length=64)


# ----- Telemetry -----
class TelemetryOut(BaseModel):
    temp: Optional[float] = None
    battery: Optional[float] = None
    status: Optional[str] = None
    ts: Optional[datetime] = None


# ----- Engine -----
class EngineCommandIn(BaseModel):
    action: Literal["start", "stop"]


class EngineAcceptedOut(BaseModel):
    status: Literal["accepted"] = "accepted"
    event_id: str

from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field

from apps.common.const import AlarmAction


class Features(BaseModel):
    active_security: int
    auto_check: int
    autostart: int
    beep: int
    bluetooth: int
    channel: int
    connection: int
    custom_phones: int
    events: int
    extend_props: int
    heater: int
    heater_from_40: int
    keep_alive: int
    light: int
    notification: int
    obd_codes: int
    schedule: int
    sensors: int
    tracking: int
    trunk: int
    value_100: int


class Permissions(BaseModel):
    alarms: int
    control: int
    detach: int
    events: int
    oauth: int
    rules: int
    settings: int
    settings_save: int
    status: int
    tanks: int
    tanks_save: int
    tracks: int


class PandoraDevice(BaseModel):
    active_sim: int
    auto_marka: str
    auto_model: str
    car_type: int
    color: str
    features: Features
    firmware: str
    fuel_tank: int
    id: int
    is_shared: bool
    model: str
    name: str
    owner_id: int
    permissions: Permissions
    phone: str
    phone1: str
    photo: str
    start_ownership: int
    tanks: List[Any] = Field(default_factory=list)
    type: str
    voice_version: str


class PandoraActionResponse(BaseModel):
    action_result: dict


class _AlarmAction(BaseModel):
    alarm_device_id: int
    action: AlarmAction

    model_config = ConfigDict(from_attributes=True)


class AlarmActionIn(_AlarmAction): ...

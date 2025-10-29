from pydantic import BaseModel, Field

from apps.gateway.services.pandora.const.field import DeviceResponseField


class Device(BaseModel):
    device_id: str | int = Field(alias=DeviceResponseField.ID, description="Device ID")
    name: str = Field(alias=DeviceResponseField.NAME, description="Device name")
    phone: str = Field(
        alias=DeviceResponseField.PHONE, description="Account phone number"
    )

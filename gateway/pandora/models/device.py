from pydantic import BaseModel, Field

from gateway.pandora.const.field import DeviceResponseField


class Device(BaseModel):
    device_id: str | int = Field(
        alias=DeviceResponseField.ID, description="Идентификатор устройства"
    )
    name: str = Field(alias=DeviceResponseField.NAME, description="Название устройства")
    phone: str = Field(
        alias=DeviceResponseField.PHONE, description="Телефон, привязанный к устройству"
    )

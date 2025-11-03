import uuid

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.core.protocols.repository import IDeviceRepo
from apps.common.dao.device import DeviceDomain, DeviceIn
from apps.common.infrastructure.database.models import Device


class DeviceRepo(IDeviceRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_devices(self, user_id: int) -> list[DeviceDomain]:
        stmt = select(Device).where(Device.user_id == user_id).order_by(Device.last_rotated_at.desc())
        rows = await self._session.scalars(stmt)
        return [DeviceDomain.model_validate(row) for row in rows.all()]

    async def get_by_name(self, device_name: str) -> DeviceDomain | None:
        res = await self._session.execute(select(Device).where(Device.name == device_name))
        device = res.scalar_one_or_none()
        return DeviceDomain.model_validate(device) if device else None

    async def upsert_device(self, device_in: DeviceIn) -> DeviceDomain:
        stmt = (
            insert(Device)
            .values(**device_in.model_dump(exclude={"id"}, exclude_none=True))
            .on_conflict_do_update(
                index_elements=[Device.id],
                set_=device_in.model_dump(exclude_unset=True),
            )
            .returning(Device)
        )
        result = await self._session.scalar(stmt)
        await self._session.flush()
        await self._session.refresh(result)
        await self._session.commit()

        return DeviceDomain.model_validate(result)


    async def delete_device(self, device_id: uuid.UUID):
        device = await self._session.execute(select(Device).where(Device.id == device_id))
        if not device:
            return
        await self._session.execute(delete(Device).where(Device.id == device_id))
        await self._session.commit()

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import UUID, DateTime, LargeBinary, String

from apps.common.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from apps.common.infrastructure.database.models.user import User


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    token_hash: Mapped[bytes] = mapped_column(LargeBinary(512), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, comment="Срок действия токена устройства"
    )

    last_used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Когда устройство последний раз использовало токен"
    )

    last_rotated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="Когда токен последний раз ротировался"
    )

    user: Mapped["User"] = relationship(back_populates="devices", lazy="joined")

    __table_args__ = (UniqueConstraint("name", name="uq_devices_name"),)

    def mark_used(self) -> None:
        """Обновить last_used_at."""
        self.last_used_at = datetime.now(UTC)

    def __repr__(self) -> str:
        return f"<Device id={self.id} name={self.name!r} user={self.user_id}>"

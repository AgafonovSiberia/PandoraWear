from typing import TYPE_CHECKING, Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, String

from apps.common.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from apps.common.infrastructure.database.models.user import User


class Credential(Base):
    __tablename__ = "credentials"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "service",
            name="uq_credentials_user_service",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service: Mapped[str] = mapped_column(String(64), nullable=False)
    creds: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    user: Mapped["User"] = relationship(back_populates="credentials")
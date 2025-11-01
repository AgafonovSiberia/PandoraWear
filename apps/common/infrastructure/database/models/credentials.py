from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String

from apps.common.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from apps.common.infrastructure.database.models.user import User


class Credential(Base):
    __tablename__ = "credentials"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    pandora_login: Mapped[str] = mapped_column(String(255), nullable=False)
    pandora_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Обратная связь
    user: Mapped["User"] = relationship(back_populates="credentials", lazy="joined")

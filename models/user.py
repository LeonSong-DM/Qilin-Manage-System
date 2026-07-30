# @Author: LeonSong
# @Date:   2026-07-29 21:13
# @Description: System user model.

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class User(TimeStampMixin, Base):
    """用户信息"""

    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(
        String(14), primary_key=True
    )  # 用户编号：QLUYYYYMMDDXXX

    name: Mapped[str] = mapped_column(String(16), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str]

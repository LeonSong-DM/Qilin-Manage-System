# @Author: LeonSong
# @Date:   2026-07-29 21:13
# @Description: System user model.

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.enum import UserRole, UserStatus
from db.base import Base, TimeStampMixin


class Users(TimeStampMixin, Base):
    """用户信息"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    user_number: Mapped[str] = mapped_column(String(14))  # 用户编号：QLUYYYYMMDDXXX
    name: Mapped[str] = mapped_column(String(16), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus), nullable=False, default=UserStatus.NORMAL
    )
    created_by: Mapped[int] = mapped_column(Integer(), nullable=False)

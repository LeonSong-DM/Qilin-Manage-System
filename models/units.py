# @Author: LeonSong
# @Date:   2026-07-30 17:45
# @Description: Model of units

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class Units(TimeStampMixin, Base):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(8), unique=True)
    created_by: Mapped[int] = mapped_column(Integer(), nullable=False)

# @Author: LeonSong
# @Date:   2026-07-30 17:45
# @Description: Model of units

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import AuditMixin, Base, TimeStampMixin


class Units(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(8), unique=True)

    orders: Mapped[list["Orders"]] = relationship(back_populates="goods_unit")

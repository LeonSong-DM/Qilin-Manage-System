# @Author: LeonSong
# @Date:   2026-07-30 17:50
# @Description: Model of goods specification

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import AuditMixin, Base, TimeStampMixin


class GoodsSpecifications(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "goods_specification"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))

    orders: Mapped[list["Orders"]] = relationship(back_populates="goods_specification")

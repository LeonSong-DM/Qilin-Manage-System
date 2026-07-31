# @Author: LeonSong
# @Date:   2026-07-30 17:50
# @Description: Model of goods specification

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class GoodsSpecifications(TimeStampMixin, Base):
    __tablename__ = "goods_specification"

    id: Mapped[str] = mapped_column(String(3), primary_key=True)  # XXX
    name: Mapped[str] = mapped_column(String(32))
    created_by: Mapped[str] = mapped_column(String(14))

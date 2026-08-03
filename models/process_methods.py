# @Author: LeonSong
# @Date:   2026-07-29 22:01
# @Description:

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import AuditMixin, Base, TimeStampMixin


class ProcessMethods(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "process_methods"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    method_name: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)

    orders: Mapped[list["Orders"]] = relationship(
        back_populates="goods_processing_method"
    )
    options: Mapped[list["ProcessOption"]] = relationship(
        back_populates="process_method"
    )

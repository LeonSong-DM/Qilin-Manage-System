# @Author: LeonSong
# @Date:   2026-07-29 22:04
# @Description: Model of process options

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import AuditMixin, Base, TimeStampMixin


class ProcessOption(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "process_options"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    option_name: Mapped[str] = mapped_column(String(16), unique=True)
    process_method_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("process_methods.id"), nullable=False
    )

    process_method: Mapped["ProcessMethods"] = relationship(back_populates="options")
    orders: Mapped[list["Orders"]] = relationship(
        back_populates="goods_processing_option"
    )

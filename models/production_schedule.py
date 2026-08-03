# @Author: LeonSong
# @Date:   2026-07-30 17:27
# @Description: Model of production schedule

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enum import SCHEDULE_STATUS
from db.base import AuditMixin, Base, TimeStampMixin


class ProductionSchedule(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "production_schedule"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    # 排产编号: QLPSYYYYMMDDXXX
    production_schedule_number: Mapped[str] = mapped_column(String(15), unique=True)
    order_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("orders.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    schedule_date: Mapped[date] = mapped_column(Date())  # 具体到日
    schedule_order: Mapped[int] = mapped_column(Integer())  # 用于实现排产拖拽
    schedule_status: Mapped[SCHEDULE_STATUS] = mapped_column(
        SQLEnum(SCHEDULE_STATUS), default=SCHEDULE_STATUS.IN_PRODUCTION
    )

    order: Mapped["Orders"] = relationship(back_populates="production_schedules")

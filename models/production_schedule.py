# @Author: LeonSong
# @Date:   2026-07-30 17:27
# @Description: Model of production schedule

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import AuditMixin, Base, TimeStampMixin


class ProductionSchedule(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "production_schedule"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    # 排产编号: QLPSYYYYMMDDXXX
    production_schedule_number: Mapped[str] = mapped_column(String(15), unique=True)
    order_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(DateTime())  # 具体到日
    schedule_order: Mapped[int] = mapped_column(Integer())  # 用于实现排产拖拽

# @Author: LeonSong
# @Date:   2026-07-30 17:27
# @Description: Model of production schedule

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class ProductionSchedule(TimeStampMixin, Base):
    __tablename__ = "production_schedule"

    # 排产编号: QLPSYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String(12), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(12), nullable=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(DateTime())  # 具体到日
    operate_user_id: Mapped[str] = mapped_column(String())

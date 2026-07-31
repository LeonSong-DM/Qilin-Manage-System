# @Author: LeonSong
# @Date:   2026-07-31 14:02
# @Description: For generate number

import datetime

from sqlalchemy import Date, Integer, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.enum import NumberType
from db.base import Base


class NumberSequence(Base):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date())
    type: Mapped[NumberType] = mapped_column(SQLEnum(NumberType))
    current_count: Mapped[int] = mapped_column(Integer())

    __table_args__ = UniqueConstraint(
        "date", "type", name="uq_number_sequence_date_type"
    )

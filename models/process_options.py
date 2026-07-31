# @Author: LeonSong
# @Date:   2026-07-29 22:04
# @Description: Model of process options

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class ProcessOption(TimeStampMixin, Base):
    __tablename__ = "process_options"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    option_name: Mapped[str] = mapped_column(String(16))
    process_method_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    created_by: Mapped[str] = mapped_column(String(14), nullable=False)

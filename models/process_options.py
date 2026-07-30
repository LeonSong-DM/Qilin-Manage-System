# @Author: LeonSong
# @Date:   2026-07-29 22:04
# @Description: Model of process options

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class ProcessOption(TimeStampMixin, Base):
    __tablename__ = "process_options"

    id: Mapped[str] = mapped_column(String(3), primary_key=True, autoincrement=True)
    process_option: Mapped[str] = mapped_column(String(16))
    process_method_id: Mapped[int] = mapped_column(Integer(), nullable=False)

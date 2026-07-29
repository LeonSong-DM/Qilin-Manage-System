# @Author: LeonSong
# @Date:   2026-07-29 22:01
# @Description:

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ProcessMethod(Base):
    __tablename__ = "process_method"

    process_method_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    process_method: Mapped[str] = mapped_column(String(16), nullable=False)

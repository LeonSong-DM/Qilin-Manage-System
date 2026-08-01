# @Author: LeonSong
# @Date:   2026-07-29 22:01
# @Description:

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class ProcessMethods(TimeStampMixin, Base):
    __tablename__ = "process_methods"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    method_name: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    created_by: Mapped[int] = mapped_column(Integer())

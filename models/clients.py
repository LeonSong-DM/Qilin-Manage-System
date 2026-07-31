# @Author: LeonSong
# @Date:   2026-07-30 20:34
# @Description: Model of client

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class Clinets(TimeStampMixin, Base):
    __tablename__ = "clients"

    # client id: QLCYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String(14), primary_key=True)
    client_name: Mapped[str] = mapped_column(String(64), nullable=False)
    contact_phone_number: Mapped[str] = mapped_column(String(11), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    created_by: Mapped[str] = mapped_column(String(14), nullable=False)

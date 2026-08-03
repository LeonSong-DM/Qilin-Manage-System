# @Author: LeonSong
# @Date:   2026-07-30 20:34
# @Description: Model of client

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import AuditMixin, Base, TimeStampMixin


class Clients(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    # client_number: QLCYYYYMMDDXXX
    client_number: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    client_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    contact_phone_number: Mapped[str] = mapped_column(
        String(11), nullable=True, unique=True
    )
    address: Mapped[str] = mapped_column(String(255), nullable=True)

    orders: Mapped[list["Orders"]] = relationship(back_populates="client")

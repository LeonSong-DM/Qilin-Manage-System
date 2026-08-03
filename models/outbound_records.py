# @Author: LeonSong
# @Date:   2026-07-29 21:14
# @Description: Outbound records model

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import AuditMixin, Base, TimeStampMixin


class OutBoundRecords(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "out_bound_orders"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    #  出库编号: QLOUTYYYYMMDDXXX
    outbound_number: Mapped[str] = mapped_column(String(12))
    order_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    outbound_quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    outbound_weight: Mapped[int] = mapped_column(Integer(), nullable=False)

# @Author: LeonSong
# @Date:   2026-07-29 21:14
# @Description: Outbound records model

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class OutBoundRecords(TimeStampMixin, Base):
    __tablename__ = "out_bound_orders"

    #  出库编号: QLOUTYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String(12), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(12), nullable=False)
    outbound_quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    outbound_unit_id: Mapped[str] = mapped_column(String(3), nullable=False)

    outbound_weight: Mapped[float] = mapped_column(Float(), nullable=False)
    created_by: Mapped[str] = mapped_column(String(14), nullable=False)

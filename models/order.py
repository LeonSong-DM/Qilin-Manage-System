# @Author: LeonSong
# @Date:   2026-07-29 21:16
# @Description: Order and inbound order yet.

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class Order(TimeStampMixin, Base):
    __tablename__ = "order"

    order_id: Mapped[str] = mapped_column(String(16), primary_key=True)

    goods_processing_method_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    goods_processing_option_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    is_closed: Mapped[bool] = mapped_column(Boolean(), default=False)

    goods_specification: Mapped[str] = mapped_column(String(255), nullable=False)
    goods_delivery_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    goods_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    goods_unit: Mapped[str] = mapped_column(String(8), nullable=False)
    goods_weight: Mapped[float] = mapped_column(Float(), nullable=False)

    goods_inbound_img1_path: Mapped[str] = mapped_column(String(255), nullable=False)
    goods_inbound_img2_path: Mapped[str] = mapped_column(String(255), nullable=True)
    goods_inbound_img3_path: Mapped[str] = mapped_column(String(255), nullable=True)

    order_priority: Mapped[str] = mapped_column(String(16), nullable=False)
    order_remarks: Mapped[str] = mapped_column(Text(), nullable=True)

    client_company: Mapped[str] = mapped_column(String(32), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(11), nullable=True)
    client_address: Mapped[str] = mapped_column(String(255), nullable=True)

    created_user_id: Mapped[int] = mapped_column(Integer(), nullable=False)

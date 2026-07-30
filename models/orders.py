# @Author: LeonSong
# @Date:   2026-07-29 21:16
# @Description: Model of orders

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.enum import OrderPriority, OrderStatus, OutboundStatus
from db.base import Base, TimeStampMixin


class Orders(TimeStampMixin, Base):
    __tablename__ = "orders"

    # 订单编号: QLORDYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String(16), primary_key=True)

    goods_processing_method_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    goods_processing_option_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    is_closed: Mapped[bool] = mapped_column(Boolean(), default=False)  # 仅针对镀锌

    goods_specification_id: Mapped[str] = mapped_column(String(3), nullable=False)
    goods_delivery_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    goods_quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    goods_unit_id: Mapped[str] = mapped_column(String(3), nullable=False)
    goods_weight: Mapped[int] = mapped_column(Integer(), nullable=False)

    order_priority: Mapped[OrderPriority] = mapped_column(
        SQLEnum(OrderPriority), nullable=False
    )
    order_status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus), nullable=False, default=OrderStatus.SCHEDULING
    )
    order_remarks: Mapped[str] = mapped_column(Text(), nullable=True)

    # 出库状态
    outbound_status: Mapped[OutboundStatus] = mapped_column(
        SQLEnum(OutboundStatus), nullable=False, default=OutboundStatus.NOT_OUTBOUND
    )

    # 剩余货物，用于部分出库计算剩余
    goods_remaining_quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    # 收获凭据
    confirm_harvest: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=False
    )
    client_id: Mapped[str] = mapped_column(String(14), nullable=False)
    created_user_id: Mapped[str] = mapped_column(String(14), nullable=False)

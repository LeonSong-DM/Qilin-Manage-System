# @Author: LeonSong
# @Date:   2026-07-31 20:24
# @Description: Schema of order

from datetime import datetime

from pydantic import BaseModel, Field

from core.enum import OrderPriority, OrderStatus, OutboundStatus


class OrderCreate(BaseModel):
    goods_processing_method_id: str = Field(...)
    goods_processing_option_id: str = Field(...)
    is_closed: bool
    goods_specification_id: str = Field(...)
    goods_delivery_time: datetime
    goods_quantity: int = Field(gt=0)
    goods_unit_id: str
    goods_weight: int = Field(gt=0)
    order_priority: OrderPriority
    order_status: OrderStatus
    order_remarks: str
    outbound_status: OutboundStatus
    goods_remaining_quantity: int = Field(ge=0)
    client_id: int = Field(min_length=14, max_length=14)

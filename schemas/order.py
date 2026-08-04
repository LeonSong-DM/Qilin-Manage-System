# @Author: LeonSong
# @Date:   2026-07-31 20:24
# @Description: Schema of order

from datetime import datetime

from pydantic import BaseModel, Field

from core.enum import OrderPriority, OrderStatus, OutboundStatus


class OrderCreate(BaseModel):
    goods_processing_method_id: int
    goods_processing_option_id: int | None = None
    is_closed: bool = False
    goods_specification_id: int
    goods_delivery_time: datetime | None = None
    goods_quantity: int = Field(gt=0)
    goods_unit_id: int
    goods_weight: int = Field(gt=0)
    order_priority: OrderPriority
    order_remarks: str | None = None
    client_id: int


class OrderUpdate(BaseModel):
    goods_processing_method_id: int | None = None
    goods_processing_option_id: int | None = None
    is_closed: bool | None = None
    goods_specification_id: int | None = None
    goods_delivery_time: datetime | None = None
    goods_quantity: int | None = Field(gt=0, default=None)
    goods_unit_id: int | None = None
    goods_weight: int | None = Field(gt=0, default=None)
    order_priority: OrderPriority | None = None
    order_status: OrderStatus | None = None
    order_remarks: str | None = None
    confirm_harvest: bool | None = None
    client_id: int | None = None


class OrderInfo(BaseModel):
    id: int
    order_number: str
    goods_processing_method_id: int
    goods_processing_option_id: int | None
    is_closed: bool
    goods_specification_id: int
    goods_delivery_time: datetime | None
    goods_quantity: int
    goods_unit_id: int
    goods_weight: int
    order_priority: OrderPriority
    order_status: OrderStatus
    order_remarks: str | None
    outbound_status: OutboundStatus
    goods_remaining_quantity: int
    confirm_harvest: bool
    client_id: int
    created_by: int
    updated_by: int | None
    create_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

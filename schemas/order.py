# @Author: LeonSong
# @Date:   2026-07-31 20:24
# @Description: Schema of order

from datetime import datetime

from pydantic import BaseModel, Field

from core.enum import OrderPriority


class OrderCreate(BaseModel):
    goods_processing_method_id: int
    goods_processing_option_id: int
    is_closed: bool
    goods_specification_id: int
    goods_delivery_time: datetime
    goods_quantity: int = Field(gt=0)
    goods_unit_id: int
    goods_weight: int = Field(gt=0)
    order_priority: OrderPriority
    order_remarks: str
    client_id: int

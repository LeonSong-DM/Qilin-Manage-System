# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.order import OrderCreate

from core.enum import NumberType
from models.orders import Orders
from service.number_generate import get_number_by_type


def create_order(session: Session, order_create: OrderCreate, current_user_id: int):
    """create new order"""
    order = Orders(
        order_number=get_number_by_type(NumberType.ORDER),
        goods_processing_method_id=order_create.goods_processing_method_id,
        goods_processing_option_id=order_create.goods_processing_option_id,
        is_closed=order_create.is_closed,
        goods_specification_id=order_create.goods_specification_id,
        goods_delivery_time=order_create.goods_delivery_time,
        goods_quantity=order_create.goods_quantity,
        goods_unit_id=order_create.goods_unit_id,
        goods_weight=order_create.goods_weight,
        order_prioriry=order_create.order_priority,
        order_status=order_create.order_status,
        order_remarks=order_create.order_remarks,
        outbound_status=order_create.outbound_status,
        goods_remaining_quantity=order_create.goods_remaining_quantity,
        confirm_harvest=False,
        client_id=order_create.client_id,
        created_by=current_user_id,
    )

    try:
        session.add(order)
        session.commit()
    except Exception as e:
        raise


# TODO create, modify ouboud record

#  TODO create, modify, delete unit

# TODO create, modify delete process method

# TODO create, modify delete process option

# TODO create, modify, delete order client


if __name__ == "__main__":
    pass

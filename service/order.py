# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.order import OrderCreate

from core.exception import OrderExistedException
from models.orders import Orders


def _is_order_exist(session: Session, order_number: str):
    stmt = select(Orders).where(Orders.order_number == order_number)
    result = session.execute(stmt).scalar_one_or_none()

    if result is not None:
        raise OrderExistedException(order_number)


def create_order(session: Session, order_create: OrderCreate):
    """create new order"""
    _is_order_exist(session, order_create.order_number)

    order = Orders(
        order_number=order_create.order_number,
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
        confirm_harvest=order_create.confirm_harvest,
        client_id=order_create.client_id,
        created_by=order_create.created_by,
    )
    session.add(order)


if __name__ == "__main__":
    from db.session import SessionLocal

    with SessionLocal() as session:
        _is_order_exist(session, order_number="sdkljfkls")

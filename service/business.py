# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.order import OrderCreate

from core.exception import (
    OrderExistedException,
    OutboundRecordExistedException,
    UnitExistedException,
    ProcessMethodExistedException,
    ProcessOptionExistedException,
    ClientExistedException,
)
from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.units import Units
from models.process_methods import ProcessMethods
from models.process_options import ProcessOption
from models.clients import Clients


def _is_order_exist(session: Session, order_number: str):
    stmt = select(Orders).where(Orders.order_number == order_number)
    result = session.execute(stmt).scalar_one_or_none()

    if result is not None:
        raise OrderExistedException(order_number)


def _is_outbound_record_exist(session: Session, outbound_number: str):
    stmt = select(OutBoundRecords).where(
        OutBoundRecords.outboud_number == outbound_number
    )

    res = session.execute(stmt).scalar_one_or_none()

    if res is not None:
        raise OutboundRecordExistedException(outbound_number)


def _is_unit_exist(session: Session, unit_name: str):
    stmt = select(Units).where(Units.name == unit_name)
    res = session.execute(stmt).scalar_one_or_none()

    if res is not None:
        raise UnitExistedException(unit_name)


def _is_process_method_exist(session: Session, method_name: str):
    stmt = select(ProcessMethods).where(ProcessMethods.method_name == method_name)
    res = session.execute(stmt).scalar_one_or_none()

    if res is not None:
        raise ProcessMethodExistedException(method_name)


def _is_process_option_exist(session: Session, option_name: str):
    stmt = select(ProcessOption).where(ProcessOption.option_name == option_name)
    res = session.execute(stmt).scalar_one_or_none()

    if res is not None:
        raise ProcessOptionExistedException(option_name)


def _is_client_exist(session: Session, client_number):
    stmt = select(Clients).where(Clients.client_number == client_number)
    res = session.execute(stmt).scalar_one_or_none()

    if res is not None:
        raise ClientExistedException(client_number=client_number)


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


# TODO create, modify ouboud record

#  TODO create, modify, delete unit

# TODO create, modify delete process method

# TODO create, modify delete process option

# TODO create, modify, delete order client


if __name__ == "__main__":
    from db.session import SessionLocal

    with SessionLocal() as session:
        _is_order_exist(session, order_number="sdkljfkls")

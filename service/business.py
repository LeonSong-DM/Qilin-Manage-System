# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from datetime import datetime

from sqlalchemy.orm import Session

from schemas.order import OrderCreate
from schemas.business import (
    OutboundRecordCreate,
    UnitCreate,
    ProcessMethodCreate,
    ProcessOptionCreate,
    ClientCreate,
)

from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.units import Units
from models.process_methods import ProcessMethods
from models.clients import Clients
from models.process_options import ProcessOption
from service.number_generate import get_number_by_type

from db.session import SessionLocal
from core.enum import OrderStatus, OutboundStatus, NumberType


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
        order_priority=order_create.order_priority,
        order_status=OrderStatus.SCHEDULING,
        order_remarks=order_create.order_remarks,
        outbound_status=OutboundStatus.NOT_OUTBOUND,
        goods_remaining_quantity=order_create.goods_quantity,
        confirm_harvest=False,
        client_id=order_create.client_id,
        created_by=current_user_id,
    )

    try:
        session.add(order)
        session.commit()
        return order
    except Exception:
        session.rollback()
        raise


# TODO create, modify ouboud record
def create_outbound_record(
    session: Session, outbound_record_create: OutboundRecordCreate, current_user_id: int
):
    outbound_record = OutBoundRecords(
        outbound_number=get_number_by_type(NumberType.OUTBOUND),
        order_id=outbound_record_create.order_id,
        outbound_quantity=outbound_record_create.outbound_quantity,
        outbound_weight=outbound_record_create.outboud_weight,
        created_by=current_user_id,
    )

    try:
        session.add(outbound_record)
        session.commit()
    except Exception:
        session.rollback()
        raise


#  TODO create, modify, delete unit
def create_unit(session: Session, unit_create: UnitCreate, current_user_id: int):
    unit = Units(name=unit_create.name, created_by=current_user_id)

    try:
        session.add(unit)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify delete process method
def create_process_method(
    session: Session, process_method_create: ProcessMethodCreate, current_user_id: int
):
    process_method = ProcessMethods(
        method_name=process_method_create.method_name, created_by=current_user_id
    )
    try:
        session.add(process_method)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify delete process option
def create_process_option(
    session: Session, process_option_created: ProcessOptionCreate, current_user_id: int
):
    process_option = ProcessOption(
        option_name=process_option_created.option_name,
        process_method_id=process_option_created.process_method_id,
        created_by=current_user_id,
    )

    try:
        session.add(process_option)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify, delete order client
def create_client(session: Session, client_create: ClientCreate, current_user_id: int):
    client = Clients(
        client_number=client_create.client_number,
        client_name=client_create.client_name,
        contact_phone_number=client_create.contact_phone_number,
        address=client_create.address,
        created_by=current_user_id,
    )
    try:
        session.add(client)
        session.commit()
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":

    process_method = ProcessMethodCreate(method_name="镀锌")
    process_option = ProcessOptionCreate(option_name="三价彩", process_method_id=1)
    client = ClientCreate(
        client_number=get_number_by_type(NumberType.CLIENT),
        client_name="Hello",
        contact_phone_number="17321100008",
        address="北京市中南海",
    )

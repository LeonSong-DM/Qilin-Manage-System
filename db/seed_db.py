# @Author: LeonSong
# @Date:   2026-08-03
# @Description: Seed development example data

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enum import OrderPriority, OrderStatus, OutboundStatus, UserRole, UserStatus
from core.security import hash_password
from db.db_init import init_db
from db.session import SessionLocal
from models.clients import Clients
from models.goods_specifications import GoodsSpecifications
from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.process_methods import ProcessMethods
from models.process_options import ProcessOption
from models.units import Units
from models.users import Users

SEED_USER_ID = 1
SEED_DATE = "20260803"


def seed_number(prefix: str, index: int) -> str:
    return f"{prefix}{SEED_DATE}{index:03d}"


def get_one_by_field(session: Session, model, field_name: str, value):
    stmt = select(model).where(getattr(model, field_name) == value)
    return session.execute(stmt).scalar_one_or_none()


def get_or_create_user(session: Session) -> Users:
    user = get_one_by_field(session, Users, "phone_number", "13800000001")
    if user is not None:
        return user

    user = Users(
        user_number=seed_number("QLU", 1),
        name="系统管理员",
        phone_number="13800000001",
        hashed_password=hash_password("admin123456"),
        role=UserRole.ADMIN,
        status=UserStatus.NORMAL,
        created_by=SEED_USER_ID,
        updated_by=SEED_USER_ID,
    )
    session.add(user)
    session.flush()
    return user


def get_or_create_unit(session: Session, name: str, current_user_id: int) -> Units:
    unit = get_one_by_field(session, Units, "name", name)
    if unit is not None:
        return unit

    unit = Units(name=name, created_by=current_user_id, updated_by=current_user_id)
    session.add(unit)
    session.flush()
    return unit


def get_or_create_process_method(
    session: Session, method_name: str, current_user_id: int
) -> ProcessMethods:
    method = get_one_by_field(session, ProcessMethods, "method_name", method_name)
    if method is not None:
        return method

    method = ProcessMethods(
        method_name=method_name,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(method)
    session.flush()
    return method


def get_or_create_process_option(
    session: Session,
    option_name: str,
    process_method_id: int,
    current_user_id: int,
) -> ProcessOption:
    option = get_one_by_field(session, ProcessOption, "option_name", option_name)
    if option is not None:
        return option

    option = ProcessOption(
        option_name=option_name,
        process_method_id=process_method_id,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(option)
    session.flush()
    return option


def get_or_create_client(
    session: Session,
    client_number: str,
    client_name: str,
    contact_phone_number: str,
    address: str,
    current_user_id: int,
) -> Clients:
    client = get_one_by_field(session, Clients, "client_name", client_name)
    if client is not None:
        return client

    client = Clients(
        client_number=client_number,
        client_name=client_name,
        contact_phone_number=contact_phone_number,
        address=address,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(client)
    session.flush()
    return client


def get_or_create_goods_specification(
    session: Session, name: str, current_user_id: int
) -> GoodsSpecifications:
    specification = get_one_by_field(session, GoodsSpecifications, "name", name)
    if specification is not None:
        return specification

    specification = GoodsSpecifications(
        name=name,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(specification)
    session.flush()
    return specification


def create_order_if_missing(
    session: Session,
    *,
    order_number: str,
    method_id: int,
    option_id: int | None,
    is_closed: bool,
    specification_id: int,
    delivery_days: int | None,
    quantity: int,
    unit_id: int,
    weight: int,
    priority: OrderPriority,
    outbound_status: OutboundStatus,
    remaining_quantity: int,
    remarks: str,
    client_id: int,
    current_user_id: int,
) -> Orders:
    order = get_one_by_field(session, Orders, "order_number", order_number)
    if order is not None:
        return order

    delivery_time = (
        datetime.now() + timedelta(days=delivery_days)
        if delivery_days is not None
        else None
    )
    order = Orders(
        order_number=order_number,
        goods_processing_method_id=method_id,
        goods_processing_option_id=option_id,
        is_closed=is_closed,
        goods_specification_id=specification_id,
        goods_delivery_time=delivery_time,
        goods_quantity=quantity,
        goods_unit_id=unit_id,
        goods_weight=weight,
        order_priority=priority,
        order_status=OrderStatus.SCHEDULING,
        order_remarks=remarks,
        outbound_status=outbound_status,
        goods_remaining_quantity=remaining_quantity,
        confirm_harvest=False,
        client_id=client_id,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(order)
    session.flush()
    return order


def create_outbound_record_if_missing(
    session: Session,
    *,
    outbound_number: str,
    order_id: int,
    quantity: int,
    weight: int,
    current_user_id: int,
) -> OutBoundRecords:
    outbound_record = get_one_by_field(
        session, OutBoundRecords, "outbound_number", outbound_number
    )
    if outbound_record is not None:
        return outbound_record

    outbound_record = OutBoundRecords(
        outbound_number=outbound_number,
        order_id=order_id,
        outbound_quantity=quantity,
        outbound_weight=weight,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    session.add(outbound_record)
    session.flush()
    return outbound_record


def seed_db() -> None:
    init_db()

    with SessionLocal() as session:
        try:
            admin = get_or_create_user(session)
            current_user_id = admin.id

            units = {
                name: get_or_create_unit(session, name, current_user_id)
                for name in ["个", "件", "框", "公斤"]
            }

            process_methods = {
                name: get_or_create_process_method(session, name, current_user_id)
                for name in ["镀锌", "镀镍", "镀铬"]
            }

            process_options = {
                name: get_or_create_process_option(
                    session,
                    name,
                    process_methods["镀锌"].id,
                    current_user_id,
                )
                for name in ["蓝白锌", "三价彩", "彩锌"]
            }

            specifications = [
                get_or_create_goods_specification(session, name, current_user_id)
                for name in [
                    "M8 螺栓",
                    "M10 螺母",
                    "连接片",
                    "冲压件",
                    "支架",
                    "法兰",
                    "垫片",
                    "轴套",
                    "挂件",
                    "异形件",
                ]
            ]

            clients = [
                get_or_create_client(
                    session,
                    seed_number("QLC", index),
                    name,
                    phone,
                    address,
                    current_user_id,
                )
                for index, (name, phone, address) in enumerate(
                    [
                        ("常州骐临样例客户一", "13800001001", "常州市新北区"),
                        ("常州骐临样例客户二", "13800001002", "常州市武进区"),
                        ("常州骐临样例客户三", "13800001003", "常州市天宁区"),
                    ],
                    start=1,
                )
            ]

            order_specs = [
                (OutboundStatus.FULLY_OUTBOUND, 0, 120, 120, 360, "整单出库样例 1"),
                (OutboundStatus.FULLY_OUTBOUND, 0, 80, 80, 240, "整单出库样例 2"),
                (OutboundStatus.FULLY_OUTBOUND, 0, 60, 60, 180, "整单出库样例 3"),
                (OutboundStatus.PARTIALLY_OUTBOUND, 70, 100, 30, 90, "部分出库样例 1"),
                (OutboundStatus.PARTIALLY_OUTBOUND, 45, 75, 30, 75, "部分出库样例 2"),
                (OutboundStatus.NOT_OUTBOUND, 50, 50, 0, 0, "未出库样例 1"),
                (OutboundStatus.NOT_OUTBOUND, 90, 90, 0, 0, "未出库样例 2"),
                (OutboundStatus.NOT_OUTBOUND, 30, 30, 0, 0, "未出库样例 3"),
                (OutboundStatus.NOT_OUTBOUND, 110, 110, 0, 0, "未出库样例 4"),
                (OutboundStatus.NOT_OUTBOUND, 40, 40, 0, 0, "未出库样例 5"),
            ]

            for index, (
                outbound_status,
                remaining_quantity,
                quantity,
                outbound_quantity,
                outbound_weight,
                remarks,
            ) in enumerate(order_specs, start=1):
                method = process_methods[["镀锌", "镀镍", "镀铬"][index % 3]]
                option = (
                    process_options["蓝白锌"]
                    if method.method_name == "镀锌"
                    else None
                )
                is_closed = method.method_name == "镀锌" and index % 2 == 0
                order = create_order_if_missing(
                    session,
                    order_number=seed_number("QLORD", index),
                    method_id=method.id,
                    option_id=option.id if option is not None else None,
                    is_closed=is_closed,
                    specification_id=specifications[index - 1].id,
                    delivery_days=index if index % 4 != 0 else None,
                    quantity=quantity,
                    unit_id=units[["个", "件", "框", "公斤"][index % 4]].id,
                    weight=quantity * 3,
                    priority=[
                        OrderPriority.P0,
                        OrderPriority.P1,
                        OrderPriority.P2,
                        OrderPriority.P3,
                    ][index % 4],
                    outbound_status=outbound_status,
                    remaining_quantity=remaining_quantity,
                    remarks=remarks,
                    client_id=clients[index % len(clients)].id,
                    current_user_id=current_user_id,
                )

                if outbound_status != OutboundStatus.NOT_OUTBOUND:
                    create_outbound_record_if_missing(
                        session,
                        outbound_number=seed_number("QLOUT", index),
                        order_id=order.id,
                        quantity=outbound_quantity,
                        weight=outbound_weight,
                        current_user_id=current_user_id,
                    )

            session.commit()
        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    seed_db()

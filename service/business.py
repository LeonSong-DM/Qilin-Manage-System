# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enum import NumberType, OutboundStatus
from core.exception import BusinessException
from models.clients import Clients
from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.process_methods import ProcessMethods
from models.process_options import ProcessOption
from models.units import Units
from schemas.business import (
    ClientCreate,
    ClientUpdate,
    OutboundRecordCreate,
    OutBoundRecordUpdate,
    ProcessMethodCreate,
    ProcessOptionCreate,
    UnitCreate,
    UnitUpdate,
)
from service.number_generate import get_number_by_type


def get_order_by_order_id(session: Session, order_id: int):
    order = session.get(Orders, order_id)
    if order is None:
        raise BusinessException("Order did not exists")

    return order


def create_outbound_record(
    session: Session,
    order_id: int,
    outbound_record_create: OutboundRecordCreate,
    current_user_id: int,
):
    """创建出库记录

    Args:
        session (Session): 数据库会话
        order_id (int): 对应的订单 ID
        outbound_record_create (OutboundRecordCreate): 创建订单范式
        current_user_id (int): 操作用户 ID

    Raises:
        BusinessException: 业务异常

    Returns:
        OutBoundRecord: 出库记录对象
    """
    order = get_order_by_order_id(session, order_id)

    if outbound_record_create.outbound_quantity > order.goods_remaining_quantity:
        raise BusinessException(
            "The quantity of goods to be shipped has exceeded the current inventory"
        )

    outbound_record = OutBoundRecords(
        outbound_number=get_number_by_type(NumberType.OUTBOUND),
        order_id=order_id,
        outbound_quantity=outbound_record_create.outbound_quantity,
        outbound_weight=outbound_record_create.outbound_weight,
        updated_by=current_user_id,
        created_by=current_user_id,
    )

    # update remaining quantity & OutBoundStatus & updated user
    order.goods_remaining_quantity -= outbound_record_create.outbound_quantity
    order.outbound_status = (
        OutboundStatus.FULLY_OUTBOUND
        if order.goods_remaining_quantity == 0
        else OutboundStatus.PARTIALLY_OUTBOUND
    )
    order.updated_by = current_user_id

    try:
        session.add(outbound_record)
        session.commit()
        session.refresh(outbound_record)
        return outbound_record
    except Exception:
        session.rollback()
        raise


def get_oubound_record_by_id(session: Session, outbound_record_id: int):
    """通过出库记录 ID 获取出库记录"""
    outbound_record = session.get(OutBoundRecords, outbound_record_id)

    if outbound_record is None:
        raise BusinessException("Outbound record did not exists")

    return outbound_record


def update_outbound_record(
    session: Session,
    order_id,
    outbound_record_id,
    outbound_record_update: OutBoundRecordUpdate,
    current_user_id: int,
):
    """更新出库记录"""
    outbound_record = get_oubound_record_by_id(session, outbound_record_id)
    if outbound_record.order_id != order_id:
        raise BusinessException(
            "The order ID provided dose not match the order ID in the outbound record"
        )
    order = get_order_by_order_id(session, order_id)

    if outbound_record_update.outbound_quantity is not None:
        new_goods_remaining_quantity = (
            order.goods_remaining_quantity
            + outbound_record.outbound_quantity
            - outbound_record_update.outbound_quantity
        )

        if new_goods_remaining_quantity < 0:
            raise BusinessException("Out of stock")

        # update outbound record
        outbound_record.outbound_quantity = outbound_record_update.outbound_quantity
        # update order
        order.goods_remaining_quantity = new_goods_remaining_quantity

    # update the weight value
    if outbound_record_update.outbound_weight is not None:
        outbound_record.outbound_weight = outbound_record_update.outbound_weight

    order.updated_by = current_user_id
    outbound_record.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(order)
        session.refresh(outbound_record)
    except Exception:
        session.rollback()
        raise


def create_unit(session: Session, unit_create: UnitCreate, current_user_id: int):
    """创建单位"""
    unit = Units(
        name=unit_create.name, updated_by=current_user_id, created_by=current_user_id
    )

    try:
        session.add(unit)
        session.commit()
    except Exception:
        session.rollback()
        raise


def modify_unit_name(
    session: Session, unit_id: int, unit_modify: UnitUpdate, current_user_id
):
    """modify the unit name"""
    unit = session.get(Units, unit_id)

    if unit is None:
        raise BusinessException(f"Unit {unit_id} did not exist")

    unit.name = unit_modify.name
    session.commit()
    session.refresh(unit)
    return unit


def delete_unit(session: Session, unit_id: int):
    """删除单位"""
    stmt = select(Units).where(Units.id == unit_id)
    unit = session.execute(stmt).scalar_one_or_none()

    if unit is None:
        raise BusinessException("The unit did not exists")

    try:
        session.delete(unit)
        session.commit()
    except Exception:
        session.rollback()
        raise


def create_process_method(
    session: Session, process_method_create: ProcessMethodCreate, current_user_id: int
):
    """创建处理方式"""
    process_method = ProcessMethods(
        method_name=process_method_create.method_name,
        updated_by=current_user_id,
        created_by=current_user_id,
    )
    try:
        session.add(process_method)
        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_process_method(session: Session, process_method_id: int):
    """ "删除处理方式"""
    stmt = select(ProcessMethods).where(ProcessMethods.id == process_method_id)
    process_method = session.execute(stmt).scalar_one_or_none()

    if process_method is None:
        raise BusinessException("The process method did not exists")

    try:
        session.delete(process_method)
        session.commit()
    except Exception:
        session.rollback()
        raise


def create_process_option(
    session: Session, process_option_created: ProcessOptionCreate, current_user_id: int
):
    """创建处理选项"""
    process_option = ProcessOption(
        option_name=process_option_created.option_name,
        process_method_id=process_option_created.process_method_id,
        updated_by=current_user_id,
        created_by=current_user_id,
    )

    try:
        session.add(process_option)
        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_process_option(session: Session, process_option_id: int):
    """删除处理选项"""
    stmt = select(ProcessOption).where(ProcessOption.id == process_option_id)
    process_option = session.execute(stmt).scalar_one_or_none()

    if process_option is None:
        raise BusinessException("The process option did not exists")

    try:
        session.delete(process_option)
        session.commit()
    except Exception:
        session.rollback()
        raise


def create_client(session: Session, client_create: ClientCreate, current_user_id: int):
    """创建客户"""
    client = Clients(
        client_number=client_create.client_number,
        client_name=client_create.client_name,
        contact_phone_number=client_create.contact_phone_number,
        address=client_create.address,
        updated_by=current_user_id,
        created_by=current_user_id,
    )
    try:
        session.add(client)
        session.commit()
    except Exception:
        session.rollback()
        raise


def update_client(
    session: Session, client_id: int, client_update: ClientUpdate, current_user_id
):
    """更新客户信息"""
    client = session.get(Clients, client_id)

    if client is None:
        raise BusinessException(f"Client {client_id} did not exists")

    client_update_data = client_update.model_dump(exclude_unset=True)

    changed = False

    for field, value in client_update_data.items():
        if getattr(client, field) != value:
            setattr(client, field, value)
            changed = True

    if not changed:
        return client

    client.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(client)
        return client
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":
    from db.session import SessionLocal

    process_method = ProcessMethodCreate(method_name="镀锌")
    process_option = ProcessOptionCreate(option_name="三价彩", process_method_id=1)
    client = ClientCreate(
        client_number=get_number_by_type(NumberType.CLIENT),
        client_name="Hello",
        contact_phone_number="17321100008",
        address="北京市中南海",
    )

    client_update = ClientUpdate(client_name="Nicee", address="上海市")

    with SessionLocal() as session:
        # delete_process_method(session, process_method_id=1)
        # delete_process_option(session, process_option_id=1)
        # create_unit(session, unit_create=UnitCreate(name="个"), current_user_id=1)
        # delete_unit(session, unit_id=2)
        # create_client(session, client_create=client, current_user_id=1)
        update_client(
            session, client_id=1, client_update=client_update, current_user_id=3
        )

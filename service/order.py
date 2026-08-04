# @Author: LeonSong
# @Date:   2026-08-02 22:33
# @Description: Service of order


from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.enum import NumberType, OrderPriority, OrderStatus, OutboundStatus
from core.exception import BusinessException
from models.clients import Clients
from models.goods_specifications import GoodsSpecifications
from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.process_methods import ProcessMethods
from models.process_options import ProcessOption
from models.production_schedule import ProductionSchedule
from models.units import Units
from schemas.order import OrderCreate, OrderUpdate
from service.number_generate import get_number_by_type


def get_order_by_id(session: Session, order_id: int) -> Orders:
    """通过订单 ID 获取订单"""
    order = session.get(Orders, order_id)

    if order is None:
        raise BusinessException(f"Order {order_id} did not exists")

    return order


def validate_order_references(
    session: Session,
    goods_processing_method_id: int,
    goods_processing_option_id: int | None,
    goods_specification_id: int,
    goods_unit_id: int,
    client_id: int,
) -> None:
    """校验订单关联数据存在且处理选项属于处理方式"""
    if session.get(ProcessMethods, goods_processing_method_id) is None:
        raise BusinessException("Process method did not exists")

    if goods_processing_option_id is not None:
        process_option = session.get(ProcessOption, goods_processing_option_id)
        if process_option is None:
            raise BusinessException("Process option did not exists")
        if process_option.process_method_id != goods_processing_method_id:
            raise BusinessException("Process option does not belong to process method")

    if session.get(GoodsSpecifications, goods_specification_id) is None:
        raise BusinessException("Goods specification did not exists")

    if session.get(Units, goods_unit_id) is None:
        raise BusinessException("Unit did not exists")

    if session.get(Clients, client_id) is None:
        raise BusinessException("Client did not exists")


def get_orders(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    client_id: int | None = None,
    order_priority: OrderPriority | None = None,
    order_status: OrderStatus | None = None,
    outbound_status: OutboundStatus | None = None,
    goods_processing_method_id: int | None = None,
    goods_specification_id: int | None = None,
    delivery_start: datetime | None = None,
    delivery_end: datetime | None = None,
):
    """查询订单列表"""
    if (
        delivery_start is not None
        and delivery_end is not None
        and delivery_start > delivery_end
    ):
        raise BusinessException("Delivery start can not be later than delivery end")

    stmt = select(Orders).order_by(Orders.id.desc())

    if client_id is not None:
        stmt = stmt.where(Orders.client_id == client_id)
    if order_priority is not None:
        stmt = stmt.where(Orders.order_priority == order_priority)
    if order_status is not None:
        stmt = stmt.where(Orders.order_status == order_status)
    if outbound_status is not None:
        stmt = stmt.where(Orders.outbound_status == outbound_status)
    if goods_processing_method_id is not None:
        stmt = stmt.where(
            Orders.goods_processing_method_id == goods_processing_method_id
        )
    if goods_specification_id is not None:
        stmt = stmt.where(Orders.goods_specification_id == goods_specification_id)
    if delivery_start is not None:
        stmt = stmt.where(Orders.goods_delivery_time >= delivery_start)
    if delivery_end is not None:
        stmt = stmt.where(Orders.goods_delivery_time <= delivery_end)

    return session.execute(stmt.offset(skip).limit(limit)).scalars().all()


def create_order(session: Session, order_create: OrderCreate, current_user_id: int):
    """create new order"""
    validate_order_references(
        session=session,
        goods_processing_method_id=order_create.goods_processing_method_id,
        goods_processing_option_id=order_create.goods_processing_option_id,
        goods_specification_id=order_create.goods_specification_id,
        goods_unit_id=order_create.goods_unit_id,
        client_id=order_create.client_id,
    )

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
        updated_by=current_user_id,
    )

    try:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    except Exception:
        session.rollback()
        raise


def update_order(
    session: Session,
    order_id: int,
    order_update: OrderUpdate,
    current_user_id: int,
) -> Orders:
    """更新订单信息"""
    order = get_order_by_id(session, order_id)
    order_update_data = order_update.model_dump(exclude_unset=True)

    goods_processing_method_id = order_update_data.get(
        "goods_processing_method_id", order.goods_processing_method_id
    )
    goods_processing_option_id = order_update_data.get(
        "goods_processing_option_id", order.goods_processing_option_id
    )
    goods_specification_id = order_update_data.get(
        "goods_specification_id", order.goods_specification_id
    )
    goods_unit_id = order_update_data.get("goods_unit_id", order.goods_unit_id)
    client_id = order_update_data.get("client_id", order.client_id)

    validate_order_references(
        session=session,
        goods_processing_method_id=goods_processing_method_id,
        goods_processing_option_id=goods_processing_option_id,
        goods_specification_id=goods_specification_id,
        goods_unit_id=goods_unit_id,
        client_id=client_id,
    )

    if order_update_data.get("confirm_harvest") is False and order.confirm_harvest:
        raise BusinessException("Confirm harvest can not be reverted")

    if order_update_data.get("confirm_harvest") is False:
        order_update_data.pop("confirm_harvest")

    if "goods_quantity" in order_update_data:
        outbound_quantity = order.goods_quantity - order.goods_remaining_quantity
        new_goods_quantity = order_update_data["goods_quantity"]
        if new_goods_quantity < outbound_quantity:
            raise BusinessException(
                "Goods quantity can not be less than outbound quantity"
            )

        order.goods_remaining_quantity = new_goods_quantity - outbound_quantity
        if order.goods_remaining_quantity == 0:
            order.outbound_status = OutboundStatus.FULLY_OUTBOUND
        elif order.goods_remaining_quantity == new_goods_quantity:
            order.outbound_status = OutboundStatus.NOT_OUTBOUND
        else:
            order.outbound_status = OutboundStatus.PARTIALLY_OUTBOUND

    changed = False
    for field, value in order_update_data.items():
        if getattr(order, field) != value:
            setattr(order, field, value)
            changed = True

    if not changed:
        return order

    order.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(order)
        return order
    except Exception:
        session.rollback()
        raise


def delete_order(session: Session, order_id: int) -> None:
    """删除未排产且未出库订单"""
    order = get_order_by_id(session, order_id)

    production_schedule_count_stmt = (
        select(func.count())
        .select_from(ProductionSchedule)
        .where(ProductionSchedule.order_id == order_id)
    )
    production_schedule_count = session.execute(
        production_schedule_count_stmt
    ).scalar_one()
    if production_schedule_count > 0:
        raise BusinessException("Order can not be deleted after scheduling")

    outbound_record_count_stmt = (
        select(func.count())
        .select_from(OutBoundRecords)
        .where(OutBoundRecords.order_id == order_id)
    )
    outbound_record_count = session.execute(outbound_record_count_stmt).scalar_one()
    if outbound_record_count > 0 or order.outbound_status != OutboundStatus.NOT_OUTBOUND:
        raise BusinessException("Order can not be deleted after outbound")

    try:
        session.delete(order)
        session.commit()
    except Exception:
        session.rollback()
        raise

# @Author: LeonSong
# @Date:   2026-08-03 16:14
# @Description: Router of orders

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from core.enum import OrderPriority, OrderStatus, OutboundStatus
from core.exception import BusinessException
from db.session import get_db
from models.users import Users
from schemas.order import OrderCreate, OrderInfo, OrderUpdate
from service.order import create_order, get_order_by_id, get_orders, update_order

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("/", response_model=list[OrderInfo])
async def list_orders(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    client_id: Annotated[int | None, Query()] = None,
    order_priority: Annotated[OrderPriority | None, Query()] = None,
    order_status: Annotated[OrderStatus | None, Query()] = None,
    outbound_status: Annotated[OutboundStatus | None, Query()] = None,
    goods_processing_method_id: Annotated[int | None, Query()] = None,
    goods_specification_id: Annotated[int | None, Query()] = None,
    delivery_start: Annotated[datetime | None, Query()] = None,
    delivery_end: Annotated[datetime | None, Query()] = None,
):
    """获取订单列表"""
    try:
        return get_orders(
            session=session,
            skip=skip,
            limit=limit,
            client_id=client_id,
            order_priority=order_priority,
            order_status=order_status,
            outbound_status=outbound_status,
            goods_processing_method_id=goods_processing_method_id,
            goods_specification_id=goods_specification_id,
            delivery_start=delivery_start,
            delivery_end=delivery_end,
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.post("/", response_model=OrderInfo, status_code=status.HTTP_201_CREATED)
async def create_order_info(
    session: Annotated[Session, Depends(get_db)],
    order_create: OrderCreate,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """创建订单"""
    try:
        return create_order(session, order_create, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("/{order_id}", response_model=OrderInfo)
async def get_order_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定订单信息"""
    try:
        return get_order_by_id(session, order_id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch("/{order_id}", response_model=OrderInfo)
async def update_order_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    order_update: OrderUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新订单信息"""
    try:
        return update_order(session, order_id, order_update, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

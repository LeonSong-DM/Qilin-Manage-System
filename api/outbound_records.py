# @Author: LeonSong
# @Date:   2026-08-03 16:14
# @Description: Router of outbound records

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from core.exception import BusinessException
from db.session import get_db
from models.users import Users
from schemas.business import (
    OutboundRecordCreate,
    OutboundRecordInfo,
    OutBoundRecordUpdate,
)
from service.business import (
    create_outbound_record,
    get_outbound_record_by_order_id,
    get_outbound_records_by_order_id,
    update_outbound_record,
)

router = APIRouter(
    prefix="/orders/{order_id}/outbound-records", tags=["Outbound Record"]
)


@router.get("/", response_model=list[OutboundRecordInfo])
async def list_outbound_records(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """获取订单下的出库记录列表"""
    try:
        return get_outbound_records_by_order_id(session, order_id, skip, limit)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.post(
    "/", response_model=OutboundRecordInfo, status_code=status.HTTP_201_CREATED
)
async def create_outbound_record_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    outbound_record_create: OutboundRecordCreate,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """创建出库记录"""
    try:
        return create_outbound_record(
            session, order_id, outbound_record_create, current_user.id
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("/{outbound_record_id}", response_model=OutboundRecordInfo)
async def get_outbound_record_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    outbound_record_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定出库记录"""
    try:
        return get_outbound_record_by_order_id(session, order_id, outbound_record_id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch("/{outbound_record_id}", response_model=OutboundRecordInfo)
async def update_outbound_record_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    outbound_record_id: int,
    outbound_record_update: OutBoundRecordUpdate,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """更新出库记录"""
    try:
        return update_outbound_record(
            session,
            order_id,
            outbound_record_id,
            outbound_record_update,
            current_user.id,
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

# @Author: LeonSong
# @Date:   2026-08-03 16:14
# @Description: Router of schedule

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from core.enum import SCHEDULE_STATUS
from core.exception import BusinessException
from db.session import get_db
from models.users import Users
from schemas.business import (
    ProductionScheduleCreate,
    ProductionScheduleInfo,
    ProductionScheduleReorder,
    ProductionScheduleStatusUpdate,
)
from service.business import (
    create_production_schedule,
    get_production_schedule_by_id,
    get_production_schedules,
    reorder_production_schedules,
    update_production_schedule_status,
)

router = APIRouter(prefix="/schedules", tags=["Schedule"])


@router.get("/", response_model=list[ProductionScheduleInfo])
async def list_production_schedules(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
    schedule_date: Annotated[date | None, Query()] = None,
    order_id: Annotated[int | None, Query()] = None,
    schedule_status: Annotated[SCHEDULE_STATUS | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """获取排产列表"""
    return get_production_schedules(
        session=session,
        schedule_date=schedule_date,
        order_id=order_id,
        schedule_status=schedule_status,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/", response_model=ProductionScheduleInfo, status_code=status.HTTP_201_CREATED
)
async def create_production_schedule_info(
    session: Annotated[Session, Depends(get_db)],
    production_schedule_create: ProductionScheduleCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """创建排产记录"""
    try:
        return create_production_schedule(
            session, production_schedule_create, current_user.id
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.patch(
    "/dates/{schedule_date}/reorder", response_model=list[ProductionScheduleInfo]
)
async def reorder_production_schedule_info(
    session: Annotated[Session, Depends(get_db)],
    schedule_date: date,
    production_schedule_reorder: ProductionScheduleReorder,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """重排指定日期的排产顺序"""
    try:
        return reorder_production_schedules(
            session, schedule_date, production_schedule_reorder, current_user.id
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("/{production_schedule_id}", response_model=ProductionScheduleInfo)
async def get_production_schedule_info(
    session: Annotated[Session, Depends(get_db)],
    production_schedule_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定排产记录"""
    try:
        return get_production_schedule_by_id(session, production_schedule_id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch("/{production_schedule_id}/status", response_model=ProductionScheduleInfo)
async def update_production_schedule_status_info(
    session: Annotated[Session, Depends(get_db)],
    production_schedule_id: int,
    production_schedule_status_update: ProductionScheduleStatusUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新排产状态"""
    try:
        return update_production_schedule_status(
            session,
            production_schedule_id,
            production_schedule_status_update,
            current_user.id,
        )
    except BusinessException as exc:
        if "did not exists" in exc.message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

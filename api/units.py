# @Author: LeonSong
# @Date:   2026-08-03 16:15
# @Description: Router of units

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from db.session import get_db
from models.users import Users
from schemas.business import UnitCreate, UnitInfo, UnitUpdate
from service.business import (
    create_unit,
    delete_unit,
    get_unit_by_id,
    get_units,
    modify_unit_name,
)

router = APIRouter(prefix="/units", tags=["Unit"])


@router.get("/", response_model=list[UnitInfo])
async def list_units(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """获取单位列表"""
    return get_units(session, skip, limit)


@router.post("/", response_model=UnitInfo, status_code=status.HTTP_201_CREATED)
async def create_unit_info(
    session: Annotated[Session, Depends(get_db)],
    unit_create: UnitCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """创建单位"""
    return create_unit(session, unit_create, current_user.id)


@router.get("/{unit_id}", response_model=UnitInfo)
async def get_unit_info(
    session: Annotated[Session, Depends(get_db)],
    unit_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定单位"""
    return get_unit_by_id(session, unit_id)


@router.patch("/{unit_id}", response_model=UnitInfo)
async def update_unit_info(
    session: Annotated[Session, Depends(get_db)],
    unit_id: int,
    unit_update: UnitUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新单位"""
    return modify_unit_name(session, unit_id, unit_update, current_user.id)


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit_info(
    session: Annotated[Session, Depends(get_db)],
    unit_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """删除单位"""
    delete_unit(session, unit_id)

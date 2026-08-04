# @Author: LeonSong
# @Date:   2026-08-04 10:28
# @Description: Router of statistics

from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.deps import require_admin
from db.session import get_db
from models.users import Users
from schemas.statistics import (
    StatisticsDistribution,
    StatisticsOverview,
    StatisticsTrend,
    TopClientsStatistics,
    TrendGranularity,
)
from service.statistics import (
    get_statistics_distribution,
    get_statistics_overview,
    get_statistics_trend,
    get_top_clients_statistics,
)

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/overview", response_model=StatisticsOverview)
async def get_statistics_overview_info(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)],
):
    """获取统计总览"""
    return get_statistics_overview(session)


@router.get("/trends", response_model=StatisticsTrend)
async def get_statistics_trend_info(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
    granularity: Annotated[TrendGranularity, Query()] = TrendGranularity.DAILY,
):
    """获取统计趋势"""
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=29)

    return get_statistics_trend(
        session=session,
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
    )


@router.get("/distributions", response_model=StatisticsDistribution)
async def get_statistics_distribution_info(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)],
):
    """获取状态分布统计"""
    return get_statistics_distribution(session)


@router.get("/top-clients", response_model=TopClientsStatistics)
async def get_top_clients_statistics_info(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """获取客户排行统计"""
    return get_top_clients_statistics(session, limit)

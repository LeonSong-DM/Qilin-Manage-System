# @Author: LeonSong
# @Date:   2026-08-04 10:28
# @Description: Service of statistics

from collections.abc import Sequence
from datetime import date, datetime, time

from sqlalchemy import Select, extract, func, select
from sqlalchemy.orm import Session

from core.enum import SCHEDULE_STATUS, OrderStatus, OutboundStatus
from core.exception import BusinessException
from models.clients import Clients
from models.orders import Orders
from models.outbound_records import OutBoundRecords
from models.production_schedule import ProductionSchedule
from schemas.statistics import (
    CountMetric,
    StatisticsDistribution,
    StatisticsOverview,
    StatisticsTrend,
    StatisticsTrendItem,
    TopClientMetric,
    TopClientsStatistics,
    TrendGranularity,
)


def count_rows(session: Session, stmt: Select) -> int:
    """执行 count 查询并返回 0 兜底"""
    return int(session.execute(stmt).scalar_one() or 0)


def sum_rows(session: Session, stmt: Select) -> int:
    """执行 sum 查询并返回 0 兜底"""
    return int(session.execute(stmt).scalar() or 0)


def get_statistics_overview(session: Session) -> StatisticsOverview:
    """获取统计总览"""
    total_orders = count_rows(session, select(func.count()).select_from(Orders))
    total_clients = count_rows(session, select(func.count()).select_from(Clients))
    total_production_schedules = count_rows(
        session, select(func.count()).select_from(ProductionSchedule)
    )
    total_outbound_records = count_rows(
        session, select(func.count()).select_from(OutBoundRecords)
    )

    scheduling_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.order_status == OrderStatus.SCHEDULING
        ),
    )
    finished_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.order_status == OrderStatus.FINISHED
        ),
    )
    not_outbound_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.outbound_status == OutboundStatus.NOT_OUTBOUND
        ),
    )
    partially_outbound_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.outbound_status == OutboundStatus.PARTIALLY_OUTBOUND
        ),
    )
    fully_outbound_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.outbound_status == OutboundStatus.FULLY_OUTBOUND
        ),
    )
    in_production_schedules = count_rows(
        session,
        select(func.count()).select_from(ProductionSchedule).where(
            ProductionSchedule.schedule_status == SCHEDULE_STATUS.IN_PRODUCTION
        ),
    )
    completed_schedules = count_rows(
        session,
        select(func.count()).select_from(ProductionSchedule).where(
            ProductionSchedule.schedule_status == SCHEDULE_STATUS.COMPLETED
        ),
    )
    pending_harvest_orders = count_rows(
        session,
        select(func.count()).select_from(Orders).where(
            Orders.order_status == OrderStatus.FINISHED,
            Orders.confirm_harvest.is_(False),
        ),
    )

    total_order_quantity = sum_rows(session, select(func.sum(Orders.goods_quantity)))
    total_remaining_quantity = sum_rows(
        session, select(func.sum(Orders.goods_remaining_quantity))
    )
    total_outbound_quantity = sum_rows(
        session, select(func.sum(OutBoundRecords.outbound_quantity))
    )
    total_outbound_weight = sum_rows(
        session, select(func.sum(OutBoundRecords.outbound_weight))
    )

    return StatisticsOverview(
        total_orders=total_orders,
        total_clients=total_clients,
        total_production_schedules=total_production_schedules,
        total_outbound_records=total_outbound_records,
        scheduling_orders=scheduling_orders,
        finished_orders=finished_orders,
        not_outbound_orders=not_outbound_orders,
        partially_outbound_orders=partially_outbound_orders,
        fully_outbound_orders=fully_outbound_orders,
        in_production_schedules=in_production_schedules,
        completed_schedules=completed_schedules,
        pending_harvest_orders=pending_harvest_orders,
        total_order_quantity=total_order_quantity,
        total_remaining_quantity=total_remaining_quantity,
        total_outbound_quantity=total_outbound_quantity,
        total_outbound_weight=total_outbound_weight,
    )


def validate_trend_date_range(start_date: date, end_date: date) -> None:
    """校验趋势日期范围"""
    if start_date > end_date:
        raise BusinessException("Start date can not be later than end date")


def get_month_index(value: date) -> int:
    return value.year * 12 + value.month


def build_periods(
    start_date: date, end_date: date, granularity: TrendGranularity
) -> list[str]:
    """生成趋势周期，确保没有数据的周期也返回 0"""
    if granularity == TrendGranularity.MONTHLY:
        periods: list[str] = []
        current_index = get_month_index(start_date)
        end_index = get_month_index(end_date)
        while current_index <= end_index:
            year = current_index // 12
            month = current_index % 12
            if month == 0:
                year -= 1
                month = 12
            periods.append(f"{year:04d}-{month:02d}")
            current_index += 1
        return periods

    days = (end_date - start_date).days
    return [
        date.fromordinal(start_date.toordinal() + offset).isoformat()
        for offset in range(days + 1)
    ]


def build_datetime_range(start_date: date, end_date: date) -> tuple[datetime, datetime]:
    return datetime.combine(start_date, time.min), datetime.combine(end_date, time.max)


def get_daily_counts(
    session: Session, model: type, column, start_date: date, end_date: date
) -> dict[str, int]:
    start_datetime, end_datetime = build_datetime_range(start_date, end_date)
    period = func.date(column)
    stmt = (
        select(period, func.count())
        .select_from(model)
        .where(column >= start_datetime, column <= end_datetime)
        .group_by(period)
    )
    return {str(row[0]): int(row[1]) for row in session.execute(stmt).all()}


def get_monthly_counts(
    session: Session, model: type, column, start_date: date, end_date: date
) -> dict[str, int]:
    start_datetime, end_datetime = build_datetime_range(start_date, end_date)
    year_expr = extract("year", column)
    month_expr = extract("month", column)
    stmt = (
        select(year_expr, month_expr, func.count())
        .select_from(model)
        .where(column >= start_datetime, column <= end_datetime)
        .group_by(year_expr, month_expr)
    )

    return {
        f"{int(row[0]):04d}-{int(row[1]):02d}": int(row[2])
        for row in session.execute(stmt).all()
    }


def get_schedule_daily_counts(
    session: Session, start_date: date, end_date: date
) -> dict[str, int]:
    stmt = (
        select(ProductionSchedule.schedule_date, func.count())
        .where(
            ProductionSchedule.schedule_date >= start_date,
            ProductionSchedule.schedule_date <= end_date,
        )
        .group_by(ProductionSchedule.schedule_date)
    )
    return {row[0].isoformat(): int(row[1]) for row in session.execute(stmt).all()}


def get_schedule_monthly_counts(
    session: Session, start_date: date, end_date: date
) -> dict[str, int]:
    year_expr = extract("year", ProductionSchedule.schedule_date)
    month_expr = extract("month", ProductionSchedule.schedule_date)
    stmt = (
        select(year_expr, month_expr, func.count())
        .where(
            ProductionSchedule.schedule_date >= start_date,
            ProductionSchedule.schedule_date <= end_date,
        )
        .group_by(year_expr, month_expr)
    )
    return {
        f"{int(row[0]):04d}-{int(row[1]):02d}": int(row[2])
        for row in session.execute(stmt).all()
    }


def get_statistics_trend(
    session: Session,
    start_date: date,
    end_date: date,
    granularity: TrendGranularity,
) -> StatisticsTrend:
    """获取订单、客户、排产、出库趋势"""
    validate_trend_date_range(start_date, end_date)

    if granularity == TrendGranularity.MONTHLY:
        order_counts = get_monthly_counts(
            session, Orders, Orders.create_at, start_date, end_date
        )
        client_counts = get_monthly_counts(
            session, Clients, Clients.create_at, start_date, end_date
        )
        outbound_counts = get_monthly_counts(
            session, OutBoundRecords, OutBoundRecords.create_at, start_date, end_date
        )
        schedule_counts = get_schedule_monthly_counts(session, start_date, end_date)
    else:
        order_counts = get_daily_counts(
            session, Orders, Orders.create_at, start_date, end_date
        )
        client_counts = get_daily_counts(
            session, Clients, Clients.create_at, start_date, end_date
        )
        outbound_counts = get_daily_counts(
            session, OutBoundRecords, OutBoundRecords.create_at, start_date, end_date
        )
        schedule_counts = get_schedule_daily_counts(session, start_date, end_date)

    items = [
        StatisticsTrendItem(
            period=period,
            order_count=order_counts.get(period, 0),
            client_count=client_counts.get(period, 0),
            production_schedule_count=schedule_counts.get(period, 0),
            outbound_record_count=outbound_counts.get(period, 0),
        )
        for period in build_periods(start_date, end_date, granularity)
    ]

    return StatisticsTrend(
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
        items=items,
    )


def build_count_metrics(rows: Sequence[tuple[object, int]]) -> list[CountMetric]:
    return [
        CountMetric(
            name=row[0].value if hasattr(row[0], "value") else str(row[0]),
            count=int(row[1]),
        )
        for row in rows
    ]


def get_enum_distribution(session: Session, model: type, column) -> list[CountMetric]:
    stmt = select(column, func.count()).select_from(model).group_by(column)
    return build_count_metrics(session.execute(stmt).all())


def get_statistics_distribution(session: Session) -> StatisticsDistribution:
    """获取状态类统计分布"""
    return StatisticsDistribution(
        order_status=get_enum_distribution(session, Orders, Orders.order_status),
        outbound_status=get_enum_distribution(session, Orders, Orders.outbound_status),
        order_priority=get_enum_distribution(session, Orders, Orders.order_priority),
        schedule_status=get_enum_distribution(
            session, ProductionSchedule, ProductionSchedule.schedule_status
        ),
    )


def get_top_clients_statistics(
    session: Session, limit: int = 10
) -> TopClientsStatistics:
    """按订单数量获取客户排行"""
    stmt = (
        select(
            Clients.id,
            Clients.client_number,
            Clients.client_name,
            func.count(Orders.id).label("order_count"),
            func.coalesce(func.sum(Orders.goods_quantity), 0).label("goods_quantity"),
            func.coalesce(func.sum(Orders.goods_weight), 0).label("goods_weight"),
        )
        .join(Orders, Orders.client_id == Clients.id)
        .group_by(Clients.id, Clients.client_number, Clients.client_name)
        .order_by(func.count(Orders.id).desc(), Clients.id)
        .limit(limit)
    )

    return TopClientsStatistics(
        items=[
            TopClientMetric(
                client_id=row.id,
                client_number=row.client_number,
                client_name=row.client_name,
                order_count=int(row.order_count),
                goods_quantity=int(row.goods_quantity),
                goods_weight=int(row.goods_weight),
            )
            for row in session.execute(stmt).all()
        ]
    )

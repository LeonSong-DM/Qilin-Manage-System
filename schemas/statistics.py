# @Author: LeonSong
# @Date:   2026-08-04 10:28
# @Description: Schemas of statistics

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class TrendGranularity(str, Enum):
    DAILY = "daily"
    MONTHLY = "monthly"


class CountMetric(BaseModel):
    name: str
    count: int


class StatisticsOverview(BaseModel):
    total_orders: int
    total_clients: int
    total_production_schedules: int
    total_outbound_records: int
    scheduling_orders: int
    finished_orders: int
    not_outbound_orders: int
    partially_outbound_orders: int
    fully_outbound_orders: int
    in_production_schedules: int
    completed_schedules: int
    pending_harvest_orders: int
    total_order_quantity: int
    total_remaining_quantity: int
    total_outbound_quantity: int
    total_outbound_weight: int


class StatisticsTrendQuery(BaseModel):
    start_date: date
    end_date: date
    granularity: TrendGranularity = TrendGranularity.DAILY


class StatisticsTrendItem(BaseModel):
    period: str
    order_count: int
    client_count: int
    production_schedule_count: int
    outbound_record_count: int


class StatisticsTrend(BaseModel):
    start_date: date
    end_date: date
    granularity: TrendGranularity
    items: list[StatisticsTrendItem]


class StatisticsDistribution(BaseModel):
    order_status: list[CountMetric]
    outbound_status: list[CountMetric]
    order_priority: list[CountMetric]
    schedule_status: list[CountMetric]


class TopClientMetric(BaseModel):
    client_id: int
    client_number: str
    client_name: str
    order_count: int
    goods_quantity: int
    goods_weight: int


class TopClientsStatistics(BaseModel):
    items: list[TopClientMetric] = Field(default_factory=list)

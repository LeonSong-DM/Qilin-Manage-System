# @Author: LeonSong
# @Date:   2026-08-01 11:44
# @Description:  Schemas of business

from datetime import date, datetime

from pydantic import BaseModel, Field

from core.enum import SCHEDULE_STATUS


class UnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=8)


class UnitUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=8)


class UnitInfo(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int | None

    model_config = {"from_attributes": True}


class OutboundRecordCreate(BaseModel):
    outbound_quantity: int = Field(gt=0)
    outbound_weight: int = Field(gt=0)


class OutBoundRecordUpdate(BaseModel):
    outbound_quantity: int | None = Field(gt=0, default=None)
    outbound_weight: int | None = Field(gt=0, default=None)


class OutboundRecordInfo(BaseModel):
    id: int
    outbound_number: str
    order_id: int
    outbound_quantity: int
    outbound_weight: int
    created_by: int
    updated_by: int | None
    create_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProcessMethodCreate(BaseModel):
    method_name: str = Field(min_length=1, max_length=16)


class ProcessMethodUpdate(BaseModel):
    method_name: str = Field(min_length=1, max_length=16)


class ProcessMethodInfo(BaseModel):
    id: int
    method_name: str
    created_by: int
    updated_by: int | None

    model_config = {"from_attributes": True}


class ProcessOptionCreate(BaseModel):
    option_name: str = Field(min_length=1, max_length=16)


class ProcessOptionUpdate(BaseModel):
    option_name: str = Field(min_length=1, max_length=16)


class ProcessOptionInfo(BaseModel):
    id: int
    option_name: str
    process_method_id: int
    created_by: int
    updated_by: int | None

    model_config = {"from_attributes": True}


class ClientCreate(BaseModel):
    client_number: str = Field(min_length=14, max_length=14)
    client_name: str = Field(min_length=1, max_length=64)
    contact_phone_number: str = Field(
        min_length=11, max_length=11, pattern=r"^1[3-9]\d{9}$"
    )
    address: str = Field(max_length=255)


class ClientUpdate(BaseModel):
    client_name: str | None = Field(min_length=1, max_length=64, default=None)
    contact_phone_number: str | None = Field(min_length=11, max_length=11, default=None)
    address: str | None = Field(max_length=255, default=None)


class ProductionScheduleCreate(BaseModel):
    order_id: int
    quantity: int = Field(gt=0)
    schedule_date: date


class ProductionScheduleReorder(BaseModel):
    schedule_ids: list[int] = Field(min_length=1)


class ProductionScheduleStatusUpdate(BaseModel):
    schedule_status: SCHEDULE_STATUS


class ProductionScheduleInfo(BaseModel):
    id: int
    production_schedule_number: str
    order_id: int
    quantity: int
    schedule_date: date
    schedule_order: int
    schedule_status: SCHEDULE_STATUS
    created_by: int
    updated_by: int | None

    model_config = {"from_attributes": True}

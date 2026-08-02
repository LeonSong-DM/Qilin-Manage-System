# @Author: LeonSong
# @Date:   2026-08-01 11:44
# @Description:  Schemas of business

from pydantic import BaseModel, Field


class UnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=8)


class OutboundRecordCreate(BaseModel):
    order_id: int
    outbound_quantity: int = Field(gt=0)
    outboud_weight: int = Field(gt=0)


class ProcessMethodCreate(BaseModel):
    method_name: str = Field(min_length=1, max_length=16)


class ProcessOptionCreate(BaseModel):
    option_name: str = Field(min_length=1, max_length=16)
    process_method_id: int = Field()


class ClientCreate(BaseModel):
    client_number: str = Field(min_length=14, max_length=14)
    client_name: str = Field(min_length=1, max_length=64)
    contact_phone_number: str = Field(
        min_length=11, max_length=11, pattern=r"^1[3-9]\d{9}$"
    )
    address: str = Field(max_length=255)

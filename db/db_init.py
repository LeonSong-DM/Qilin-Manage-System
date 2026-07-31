# @Author: LeonSong
# @Date:   2026-07-30 22:22
# @Description: Init database

from sqlalchemy import create_engine

from core.settings import Settings
from db.base import Base
from models import (  # noqa: F401
    clients,
    goods_specifications,
    order_attachments,
    orders,
    outbound_records,
    process_methods,
    process_options,
    production_schedule,
    units,
    users,
)

engine = create_engine(url=Settings.DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)

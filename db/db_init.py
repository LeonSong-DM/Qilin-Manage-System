# @Author: LeonSong
# @Date:   2026-07-30 22:22
# @Description: Init database


from db.base import Base
from db.session import engine
from models import (  # noqa: F401
    clients,
    goods_specifications,
    order_attachments,
    orders,
    outbound_records,
    process_methods,
    process_options,
    production_schedule,
    number_sequence,
    units,
    users,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

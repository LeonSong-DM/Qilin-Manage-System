# @Author: LeonSong
# @Date:   2026-07-31 20:41
# @Description: Operations of order

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from core.enum import NumberType
from core.exception import BusinessException
from models.clients import Clients
from models.outbound_records import OutBoundRecords
from models.process_methods import ProcessMethods
from models.process_options import ProcessOption
from models.units import Units
from schemas.business import (
    ClientCreate,
    OutboundRecordCreate,
    ProcessMethodCreate,
    ProcessOptionCreate,
    UnitCreate,
)
from service.number_generate import get_number_by_type


# TODO create, modify ouboud record
def create_outbound_record(
    session: Session, outbound_record_create: OutboundRecordCreate, current_user_id: int
):
    outbound_record = OutBoundRecords(
        outbound_number=get_number_by_type(NumberType.OUTBOUND),
        order_id=outbound_record_create.order_id,
        outbound_quantity=outbound_record_create.outbound_quantity,
        outbound_weight=outbound_record_create.outbound_weight,
        created_by=current_user_id,
    )

    try:
        session.add(outbound_record)
        session.commit()
    except Exception:
        session.rollback()
        raise


#  TODO create, modify, delete unit
def create_unit(session: Session, unit_create: UnitCreate, current_user_id: int):
    unit = Units(name=unit_create.name, created_by=current_user_id)

    try:
        session.add(unit)
        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_unit(session: Session, unit_id: int):

    stmt = select(Units).where(Units.id == unit_id)
    res = session.execute(stmt).scalar_one_or_none()

    if res is None:
        raise BusinessException("The unit did not exists")

    stmt = delete(Units).where(Units.id == unit_id)
    try:
        session.execute(stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify delete process method
def create_process_method(
    session: Session, process_method_create: ProcessMethodCreate, current_user_id: int
):
    process_method = ProcessMethods(
        method_name=process_method_create.method_name, created_by=current_user_id
    )
    try:
        session.add(process_method)
        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_process_method(session: Session, process_method_id: int):
    stmt = select(ProcessMethods).where(ProcessMethods.id == process_method_id)
    res = session.execute(stmt).scalar_one_or_none()

    if res is None:
        raise BusinessException("The process method did not exists")

    stmt = delete(ProcessMethods).where(ProcessMethods.id == process_method_id)
    try:
        session.execute(stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify delete process option
def create_process_option(
    session: Session, process_option_created: ProcessOptionCreate, current_user_id: int
):
    process_option = ProcessOption(
        option_name=process_option_created.option_name,
        process_method_id=process_option_created.process_method_id,
        created_by=current_user_id,
    )

    try:
        session.add(process_option)
        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_process_option(session: Session, process_option_id: int):
    stmt = select(ProcessOption).where(ProcessOption.id == process_option_id)
    res = session.execute(stmt).scalar_one_or_none()

    if res is None:
        raise BusinessException("The process option did not exists")

    stmt = delete(ProcessOption).where(ProcessOption.id == process_option_id)
    try:
        session.execute(stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise


# TODO create, modify, delete order client
def create_client(session: Session, client_create: ClientCreate, current_user_id: int):
    client = Clients(
        client_number=client_create.client_number,
        client_name=client_create.client_name,
        contact_phone_number=client_create.contact_phone_number,
        address=client_create.address,
        created_by=current_user_id,
    )
    try:
        session.add(client)
        session.commit()
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":
    from db.session import SessionLocal

    process_method = ProcessMethodCreate(method_name="镀锌")
    process_option = ProcessOptionCreate(option_name="三价彩", process_method_id=1)
    client = ClientCreate(
        client_number=get_number_by_type(NumberType.CLIENT),
        client_name="Hello",
        contact_phone_number="17321100008",
        address="北京市中南海",
    )

    with SessionLocal() as session:
        # delete_process_method(session, process_method_id=1)
        delete_process_option(session, process_option_id=1)

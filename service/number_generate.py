# @Author: LeonSong
# @Date:   2026-07-31 14:23
# @Description: Automate number generation

from datetime import date

from sqlalchemy import select, update

from core.enum import NumberType
from db.session import SessionLocal
from models.number_sequence import NumberSequence


def fromat_number(number_type: NumberType, today: date, current_count: int) -> str:
    """concatenate the traversal number string"""
    return f"{number_type.value}{today.strftime("%Y%m%d")}{current_count+1:03d}"


def get_number_by_type(number_type: NumberType) -> str:
    """get number string by type

    Args:
        number_type (NumberType): ...

    Returns:
        str: traversal number string
    """
    today = date.today()

    stmt = select(NumberSequence.current_count).where(
        NumberSequence.type == number_type and NumberSequence.date == today
    )

    with SessionLocal() as session:
        current_count = session.execute(stmt).scalar()

    if current_count == None:
        ns = NumberSequence(date=today, type=number_type, current_count=0)

        with SessionLocal() as session:
            session.add(ns)
            session.commit()

    with SessionLocal() as session:
        current_count = session.execute(stmt).scalar()
    assert current_count != None

    # update current count
    with SessionLocal() as session:
        stmt = (
            update(NumberSequence)
            .where(
                NumberSequence.date == today,
                NumberSequence.type == number_type,
            )
            .values(current_count=NumberSequence.current_count + 1)
        )
        session.execute(stmt)
        session.commit()

    number = fromat_number(number_type, today, current_count)

    return number


if __name__ == "__main__":

    number = get_number_by_type(NumberType.ATTACHMENT)
    print(number)

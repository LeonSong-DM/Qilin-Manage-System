# @Author: LeonSong
# @Date:   2026-07-31 14:23
# @Description: Automate number generation

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enum import NumberType
from models.number_sequence import NumberSequence


def format_number(number_type: NumberType, today: date, current_count: int) -> str:
    """concatenate the traversal number string"""
    return f"{number_type.value}{today.strftime("%Y%m%d")}{current_count+1:03d}"


def get_number_by_type(session: Session, number_type: NumberType) -> str:
    """get number string by type

    Args:
        session (Session): current transaction session
        number_type (NumberType): ...

    Returns:
        str: traversal number string
    """
    today = date.today()

    stmt = (
        select(NumberSequence)
        .where(NumberSequence.type == number_type, NumberSequence.date == today)
        .with_for_update()
    )
    number_sequence = session.execute(stmt).scalar_one_or_none()

    if number_sequence is None:
        number_sequence = NumberSequence(
            date=today,
            type=number_type,
            current_count=0,
        )
        session.add(number_sequence)
        session.flush()

    number = format_number(number_type, today, number_sequence.current_count)
    number_sequence.current_count += 1

    return number


if __name__ == "__main__":
    from db.session import SessionLocal

    with SessionLocal() as session:
        number = get_number_by_type(session, NumberType.ATTACHMENT)
        session.commit()
        print(number)

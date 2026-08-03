# @Author: LeonSong
# @Date:   2026-07-31 14:21
# @Description: Operations of user

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enum import NumberType
from core.exception import UserExistedException
from core.security import hash_password
from models.users import Users
from schemas.user import UserCreate
from service.number_generate import get_number_by_type


def is_user_existed(session: Session, phone_number: str):
    stmt = select(Users).where(Users.phone_number == phone_number)
    return session.execute(stmt).scalar_one_or_none()


def create_user(session: Session, user_create: UserCreate, current_user_id: int):
    # check user is existed
    if is_user_existed(session, user_create.phone_number):
        raise UserExistedException(user_create)

    # generate number
    user_number = get_number_by_type(NumberType.USER)
    user = Users(
        user_number=user_number,
        name=user_create.name,
        phone_number=user_create.phone_number,
        hashed_password=hash_password(user_create.hashed_password._secret_value),
        role=user_create.role,
        status=user_create.status,
        created_by=current_user_id,
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":
    from pydantic import SecretStr

    from core.enum import UserRole, UserStatus
    from db.session import SessionLocal

    user_create = UserCreate(
        name="宋宇阳",
        phone_number="17321100008",
        hashed_password=SecretStr("1213123131"),
        role=UserRole.ADMIN,
        status=UserStatus.NORMAL,
    )
    with SessionLocal() as session:
        create_user(session, user_create, current_user_id=1)

# @Author: LeonSong
# @Date:   2026-07-31 14:21
# @Description: Operations of user

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.users import Users
from schemas.user import UserCreate


def is_user_existed(session: Session, phone_number: str):
    stmt = select(Users).where(Users.phone_number == phone_number)
    res = session.execute(stmt).scalar_one_or_none()

    return res is not None


def create_user(session: Session, user_create: UserCreate):
    # check user is existed

    # generate number
    pass


if __name__ == "__main__":
    from db.session import SessionLocal

    with SessionLocal() as session:
        res = is_user_existed(session, "122342")
        print(res)

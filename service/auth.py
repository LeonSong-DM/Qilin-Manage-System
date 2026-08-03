# @Author: LeonSong
# @Date:   2026-08-03 16:43
# @Description: Authentication service

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.exception import AccountException
from core.security import get_access_token, verify_password
from models.users import Users
from schemas.user import UserLogin


def user_authentication(session: Session, user_login: UserLogin):
    stmt = select(Users).where(Users.phone_number == user_login.phone_number)
    user = session.execute(stmt).scalar_one_or_none()

    if user is None:
        raise AccountException("User did not exists")

    passwd_verify_res = verify_password(
        user_login.password.get_secret_value(), user.hashed_password
    )

    if not passwd_verify_res:
        raise AccountException("Incorrect phone number or passowrd")

    return get_access_token(str(user.id))

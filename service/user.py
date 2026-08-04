# @Author: LeonSong
# @Date:   2026-07-31 14:21
# @Description: Operations of user

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enum import NumberType, UserRole, UserStatus
from core.exception import BusinessException, UserExistedException
from core.security import hash_password, verify_password
from models.users import Users
from schemas.user import (
    UserCreate,
    UserPasswordUpdate,
    UserSelfPasswordUpdate,
    UserUpdate,
)
from service.number_generate import get_number_by_type


def is_user_existed(
    session: Session, phone_number: str, exclude_user_id: int | None = None
):
    stmt = select(Users).where(Users.phone_number == phone_number)
    if exclude_user_id is not None:
        stmt = stmt.where(Users.id != exclude_user_id)

    return session.execute(stmt).scalar_one_or_none()


def get_users(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    phone_number: str | None = None,
    role: UserRole | None = None,
    status: UserStatus | None = None,
):
    """查询用户列表"""
    stmt = select(Users).order_by(Users.id)

    if name is not None:
        stmt = stmt.where(Users.name.like(f"%{name}%"))
    if phone_number is not None:
        stmt = stmt.where(Users.phone_number.like(f"%{phone_number}%"))
    if role is not None:
        stmt = stmt.where(Users.role == role)
    if status is not None:
        stmt = stmt.where(Users.status == status)

    return session.execute(stmt.offset(skip).limit(limit)).scalars().all()


def get_user_by_id(session: Session, user_id: int) -> Users:
    """通过用户 ID 获取用户"""
    user = session.get(Users, user_id)

    if user is None:
        raise BusinessException(f"User {user_id} did not exists")

    return user


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
        hashed_password=hash_password(user_create.password.get_secret_value()),
        role=user_create.role,
        status=user_create.status,
        created_by=current_user_id,
        updated_by=current_user_id,
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def update_user(
    session: Session,
    user_id: int,
    user_update: UserUpdate,
    current_user_id: int,
) -> Users:
    """更新用户信息"""
    user = get_user_by_id(session, user_id)
    user_update_data = user_update.model_dump(exclude_unset=True)

    if "phone_number" in user_update_data and is_user_existed(
        session,
        user_update_data["phone_number"],
        exclude_user_id=user_id,
    ):
        raise BusinessException("Phone number already exists")

    changed = False
    for field, value in user_update_data.items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            changed = True

    if not changed:
        return user

    user.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def update_user_password(
    session: Session,
    user_id: int,
    user_password_update: UserPasswordUpdate,
    current_user_id: int,
) -> Users:
    """管理员重置用户密码"""
    user = get_user_by_id(session, user_id)
    user.hashed_password = hash_password(
        user_password_update.password.get_secret_value()
    )
    user.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def update_current_user_password(
    session: Session,
    current_user: Users,
    user_self_password_update: UserSelfPasswordUpdate,
) -> Users:
    """用户修改自己的密码"""
    old_password_verified = verify_password(
        user_self_password_update.old_password.get_secret_value(),
        current_user.hashed_password,
    )
    if not old_password_verified:
        raise BusinessException("Incorrect old password")

    current_user.hashed_password = hash_password(
        user_self_password_update.new_password.get_secret_value()
    )
    current_user.updated_by = current_user.id

    try:
        session.commit()
        session.refresh(current_user)
        return current_user
    except Exception:
        session.rollback()
        raise


def delete_user(session: Session, user_id: int, current_user_id: int) -> Users:
    """禁用用户，保留历史审计关联"""
    if user_id == current_user_id:
        raise BusinessException("Can not delete current user")

    user = get_user_by_id(session, user_id)
    user.status = UserStatus.FORBIDDEN
    user.updated_by = current_user_id

    try:
        session.commit()
        session.refresh(user)
        return user
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
        password=SecretStr("1213123131"),
        role=UserRole.ADMIN,
        status=UserStatus.NORMAL,
    )
    with SessionLocal() as session:
        create_user(session, user_create, current_user_id=1)

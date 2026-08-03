# @Author: LeonSong
# @Date:   2026-08-03 17:13
# @Description:

from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from core.security import parse_jwt_token
from models.users import Users


def get_current_user(session: Session, token: str) -> Users:
    """获取当前用户"""
    try:
        payload = parse_jwt_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = session.get(Users, int(payload["sub"]))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

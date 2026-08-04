# @Author: LeonSong
# @Date:   2026-08-03 17:13
# @Description:

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from core.security import parse_jwt_token
from db.session import get_db
from models.users import Users

bearer_scheme = HTTPBearer()


def get_token_from_credentials(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> str:
    """从 Authorization 请求头中获取 token"""
    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    return credentials.credentials


def get_current_user(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(get_token_from_credentials)],
) -> Users:
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

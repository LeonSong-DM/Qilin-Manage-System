# @Author: LeonSong
# @Date:   2026-08-04
# @Description: Exception handlers

from fastapi import Request
from fastapi.responses import JSONResponse

from core.exception import AuthenticationException, BusinessException


async def business_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """处理业务异常"""
    assert isinstance(exc, BusinessException)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


async def authentication_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """处理认证异常"""
    assert isinstance(exc, AuthenticationException)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )

# @Author: LeonSong
# @Date:   2026-08-04
# @Description: Exception handlers

from fastapi import Request
from fastapi.responses import JSONResponse

from core.exception import AuthenticationException, BusinessException


async def business_exception_handler(
    request: Request, exc: BusinessException
) -> JSONResponse:
    """处理业务异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


async def authentication_exception_handler(
    request: Request, exc: AuthenticationException
) -> JSONResponse:
    """处理认证异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )

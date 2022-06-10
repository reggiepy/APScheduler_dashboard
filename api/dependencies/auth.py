# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 6:00 
from typing import Optional, Union, Any

import jwt
from fastapi import Header, HTTPException, Depends, Request
from starlette import status

from api.exception_handlers.error_code import StatusCode
from core import security
from core.security import OAuth2Scheme
from api.exception_handlers import exceptions


def check_jwt_token(
        request: Request,
        token: str = Depends(OAuth2Scheme)
) -> Union[str, Any]:
    """
    解析验证token  默认验证headers里面为token字段的数据
    可以给 headers 里面token替换别名, 以下示例为 X-Token
    token: Optional[str] = Header(None, alias="X-Token")
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="UNAUTHORIZED",
        headers={"token": token},
    )
    payload = security.decode_access_token(token)
    if not payload:
        raise credentials_exception
    request.state.payload = payload
    request.state.token = token
    return payload


async def get_current_user(payload: str = Depends(check_jwt_token)):
    user = payload
    return user

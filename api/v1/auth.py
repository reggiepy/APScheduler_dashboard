# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 4:19 
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import settings
from core import security
from models.auth import AccessToken

api = APIRouter()


@api.post(
    path="/auth/access_token",
    response_model=AccessToken,
    name="登录系统",
    summary="登录系统 - OAuth2登录方式",
    operation_id="auth::access_token")
async def auth_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_name = form_data.username
    user_password = form_data.password
    scopes = form_data.scopes
    access_token = security.create_access_token(
        subject={"username": user_name, "scopes": scopes},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return AccessToken(access_token=access_token, token_type="bearer")

# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 4:24

from pydantic import BaseModel
from pydantic import Field


class AccessToken(BaseModel):
    access_token: str = Field(None, title="X-Access-Token")
    token_type: str = Field(None, title="Token类型")


class LoginInRequest(BaseModel):
    username: str = Field(..., title="用户名")
    password: str = Field(..., title="密码")

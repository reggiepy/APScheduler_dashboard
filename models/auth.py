# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 4:24 
from typing import Optional, List

from pydantic import BaseModel
from pydantic import Field


class AccessToken(BaseModel):
    access_token: str = Field(None, title="X-Access-Token")
    token_type: str = Field(None, title="Token类型")

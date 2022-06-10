# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 6:53

from fastapi import APIRouter

from api.v1 import test

api_router = APIRouter()
api_router.include_router(test.api, tags=["环境测试"])

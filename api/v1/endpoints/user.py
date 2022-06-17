# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/15 下午 4:33 
from datetime import timedelta, datetime
from typing import Any, Union, List
import time

from apscheduler.util import get_callable_name, convert_to_datetime
from fastapi import APIRouter, Depends, Path, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.types import UUID

from api.dependencies.auth import get_current_user
from core import security
from core.sys_schedule import schedule
from models.auth import AccessToken
from models.schedule_jobs import Job
from models.user import UserIn, UserOut

api = APIRouter()


@api.get(
    path="/user",
    response_model=List[UserOut],
    name="获取所有用户",
    summary="user - 获取所有用户",
    operation_id="user::get_users")
async def get_users(
        # user: Any = Depends(get_current_user),
):
    pass


@api.get(
    path="/user/{user_id}",
    response_model=UserOut,
    name="获取用户",
    summary="user - 获取用户",
    operation_id="user::get_user")
async def get_user(
        # user: Any = Depends(get_current_user),
        user_id: int = Path(..., description="用户id"),
):
    pass


@api.post(
    path="/user",
    response_model=UserOut,
    name="添加用户",
    summary="user - 添加用户",
    operation_id="user::user")
async def add_user(
        # user: Any = Depends(get_current_user),
        user: UserIn = Body(..., description="用户信息")
):
    pass

@api.put(
    path="/user/{user_id}",
    response_model=UserOut,
    name="更新用户",
    summary="user - 更新用户",
    operation_id="user::update_user")
async def update_user(
        # user: Any = Depends(get_current_user),
        user_id: int = Path(..., description="用户id"),
):
    pass


@api.delete(
    path="/user/{user_id}",
    response_model=Any,
    name="删除用户",
    summary="user - 删除用户",
    operation_id="user::delete_user")
async def delete_user(
        # user: Any = Depends(get_current_user),
        user_id: int = Path(..., description="用户id"),
):
    pass

# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 6:02 
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import settings
from api import get_current_user
from core import security
from models.auth import AccessToken

api = APIRouter()


@api.post(
    path="/add_job",
    response_model=Any,
    name="添加job",
    summary="APSchedule - 添加job",
    operation_id="schedule::add_job")
async def add_job(
        user: Any = Depends(get_current_user)
):
    pass


@api.delete(
    path="/delete_job",
    response_model=Any,
    name="删除job",
    summary="APSchedule - 删除job",
    operation_id="schedule::delete_job")
async def delete_job(
):
    pass


@api.get(
    path="/get_job",
    response_model=Any,
    name="获取job",
    summary="APSchedule - 获取job",
    operation_id="schedule::delete_job")
async def get_job(
):
    pass


@api.get(
    path="/get_jobs",
    response_model=Any,
    name="获取job列表",
    summary="APSchedule - 获取job列表",
    operation_id="schedule::delete_job")
async def get_jobs(
):
    pass


@api.get(
    path="/schedule_info",
    response_model=Any,
    name="获取job列表",
    summary="APSchedule - 获取job列表",
    operation_id="schedule::delete_job")
async def delete_job(
):
    pass


@api.post(
    path="/pause_job",
    response_model=Any,
    name="暂停job",
    summary="APSchedule - 暂停job",
    operation_id="schedule::pause_job")
async def pause_job(
):
    pass


@api.post(
    path="/resume_job",
    response_model=Any,
    name="恢复job",
    summary="APSchedule - 恢复job",
    operation_id="schedule::resume_job")
async def resume_job(
):
    pass


@api.post(
    path="/run_job",
    response_model=Any,
    name="启动job",
    summary="APSchedule - 启动job",
    operation_id="schedule::run_job")
async def run_job(
):
    pass


@api.put(
    path="/update_job",
    response_model=Any,
    name="更新job",
    summary="APSchedule - 更新job",
    operation_id="schedule::update_job")
async def update_job(
):
    pass

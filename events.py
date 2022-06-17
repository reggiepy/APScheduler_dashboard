# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 6:05 
from typing import Callable

from fastapi import FastAPI

from core.db.database import database
from core.sys_schedule import schedule


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        schedule.init_scheduler()
        await database.connect()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        schedule.shutdown()
        await database.disconnect()

    return stop_app

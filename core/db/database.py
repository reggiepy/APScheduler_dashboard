# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/14 下午 2:00 
from typing import Union

import databases
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from settings import DATABASE_URL

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

# 只允许导出 database 实例化对象
__all__ = ["database", "metadata", "engine"]

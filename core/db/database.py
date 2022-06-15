# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/14 下午 2:00 
from typing import List, Union

import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
import databases

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"


metadata = sqlalchemy.MetaData()


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._database = None

    def init_database(self, database_url) -> None:
        self._database = databases.Database(database_url)

    # 使实例化后的对象 赋予 databases.Database 对象的方法和属性
    def __getattr__(self, item):
        return getattr(self._database, item)


# 创建 database 对象
database: Union[databases.Database, Database] = Database()

# 只允许导出 database 实例化对象
__all__ = ["database"]

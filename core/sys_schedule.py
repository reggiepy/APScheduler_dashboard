# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 6:51
from typing import Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging

logger = logging.getLogger("apscheduler.scheduler")


# SQLAlchemyJobStore 显示执行的 sql
def _show_sql(func):
    def inner(*args, **kwargs):
        sql = str(args[0]).replace('\n', '')
        logger.info(f"SQLAlchemyJobStore SQL: {sql}")
        out = func(*args, **kwargs)
        return out

    return inner


class ScheduleCli(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        # 对象 在 @app.on_event("startup") 中初始化
        self._schedule = None

    def init_scheduler(self, show_sql=True) -> None:
        """
        初始化 apscheduler
        :return:
        """
        job_stores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        self._schedule = AsyncIOScheduler(jobstores=job_stores, timezone="Asia/Shanghai")

        # SQLAlchemyJobStore 支持显示执行的 sql
        if show_sql:
            for alia, job_store in self._schedule._jobstores.items():
                if isinstance(job_store, SQLAlchemyJobStore):
                    job_store.engine.execute = _show_sql(job_store.engine.execute)
        self._schedule.start()

    # 使实例化后的对象 赋予apscheduler对象的方法和属性
    def __getattr__(self, name):
        return getattr(self._schedule, name)

    def __getitem__(self, name):
        return self._schedule[name]

    def __setitem__(self, name, value):
        self._schedule[name] = value

    def __delitem__(self, name):
        del self._schedule[name]


# 创建schedule对象
schedule: Union[AsyncIOScheduler, ScheduleCli] = ScheduleCli()

# 只允许导出 redis_client 实例化对象
__all__ = ["schedule"]

# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 4:24
from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class JobBase(BaseModel):
    trigger: str = Field("", title="控制此作业计划的触发器对象")
    executor: str = Field("", title="将运行此作业的执行者的名称")
    func: str = Field("", title="可调用的执行")
    args: list = Field(None, title="可调用的位置参数")
    kwargs: dict = Field(None, title="可调用的位置参数")
    id: str = Field(None, title="此作业的唯一标识符")
    name: str = Field(None, title="这份工作的描述")
    misfire_grace_time: int = Field(0, title="允许该作业执行延迟的时间（以秒为单位）（``None`` 表示“无论多晚都允许作业运行”）")
    coalesce: bool = Field(False, title="是否在多个运行时间到期时只运行一次作业")
    max_instances: int = Field(0, title="允许的最大并发执行实例数")
    next_run_time: datetime = Field(None, title="此作业的下一个计划运行时间")
    pending: bool = Field(False, title="待办的")


class Job(JobBase):
    pass


class LoginInRequest(BaseModel):
    username: str = Field(..., title="用户名")
    password: str = Field(..., title="密码")

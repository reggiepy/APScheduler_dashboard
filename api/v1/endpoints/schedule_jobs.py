# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 6:02 
from datetime import timedelta, datetime
from typing import Any, Union
import time

from apscheduler.util import get_callable_name, convert_to_datetime
from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm

import settings
from api.dependencies.auth import get_current_user
from core import security
from core.sys_schedule import schedule
from models.auth import AccessToken
from models.schedule_jobs import Job

api = APIRouter()


class Helper:
    @classmethod
    def parse_job(cls, job):
        return Job.parse_obj({
            'trigger': str(job.trigger),
            'executor': job.executor,
            'func': get_callable_name(job.func),
            'args': job.args,
            'kwargs': job.kwargs,
            'id': job.id,
            'name': job.name,
            'misfire_grace_time': job.misfire_grace_time if hasattr(job, "coalesce") else 0,
            'coalesce': job.coalesce if hasattr(job, "coalesce") else False,
            'max_instances': job.max_instances if hasattr(job, "max_instances") else 0,
            'next_run_time': job.next_run_time if hasattr(job, "next_run_time") else None,
            'pending': job.pending if hasattr(job, "pending") else False
        })

    @classmethod
    def parse_schedule(cls, schedule):
        return {
            'jobstore_retry_interval': schedule.jobstore_retry_interval,
            'running': schedule.running,
            'state': schedule.state,
            'timezone': str(schedule.timezone),
        }


@api.get(
    path="/schedule_info",
    response_model=Any,
    name="获取调度器详细信息",
    summary="APSchedule - 获取调度器详细信息",
    operation_id="schedule::schedule_info")
async def delete_job(
        # user: Any = Depends(get_current_user),
):
    return Helper.parse_schedule(schedule._schedule)


@api.get(
    path="/get_jobs",
    response_model=Any,
    name="获取job列表",
    summary="APSchedule - 获取job列表",
    operation_id="schedule::get_jobs")
async def get_jobs(
        # # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
):
    results = []
    jobs = schedule.get_jobs()
    for job in jobs:
        results.append(
            Helper.parse_job(job)
        )
    return results


@api.get(
    path="/get_job",
    response_model=Any,
    name="获取job",
    summary="APSchedule - 获取job",
    operation_id="schedule::get_job")
async def get_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    job = schedule.get_job(job_id=job_id, jobstore=jobstore)
    return Helper.parse_job(job)

def func():
    time.sleep(1)
    print(datetime.now().strftime("%Y.%m.%d %H:%M:%S' '%m/%d/%Y"))
@api.post(
    path="/add_job",
    response_model=Any,
    name="添加job",
    summary="APSchedule - 添加job",
    operation_id="schedule::add_job")
async def add_job(
        # user: Any = Depends(get_current_user),
):

    print(id(schedule._schedule))
    print(schedule.state)
    job = schedule.add_job(func=func, trigger="cron", second=3)
    return Helper.parse_job(job)


@api.post(
    path="/pause_job/{job_id}",
    response_model=Any,
    name="暂停job",
    summary="APSchedule - 暂停job",
    operation_id="schedule::pause_job")
async def pause_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    schedule.pause_job(job_id=job_id, jobstore=jobstore)
    return True


@api.post(
    path="/resume_job/{job_id}",
    response_model=Any,
    name="恢复job",
    summary="APSchedule - 恢复job",
    operation_id="schedule::resume_job")
async def resume_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    schedule.resume_job(job_id=job_id, jobstore=jobstore)
    return True


@api.post(
    path="/run_job/{job_id}",
    response_model=Any,
    name="启动job",
    summary="APSchedule - 启动job",
    operation_id="schedule::run_job")
async def run_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    job = schedule.get_job(job_id=job_id, jobstore=jobstore)
    job.next_run_time = convert_to_datetime(datetime.now(), schedule.timezone, 'next_run_time')
    return True


@api.put(
    path="/update_job/{job_id}",
    response_model=Any,
    name="更新job",
    summary="APSchedule - 更新job",
    operation_id="schedule::update_job")
async def update_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    pass


@api.delete(
    path="/delete_job/{job_id}",
    response_model=Any,
    name="删除job",
    summary="APSchedule - 删除job",
    operation_id="schedule::delete_job")
async def delete_job(
        # user: Any = Depends(get_current_user),
        jobstore: Union[None, str] = Query(None, description="任务存储"),
        job_id: str = Path(..., description="任务id"),
):
    try:
        schedule.remove_job(job_id=job_id, jobstore=jobstore)
    except Exception as e:
        return False
    return True

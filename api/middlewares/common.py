# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 6:55
import time

from starlette.requests import Request


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
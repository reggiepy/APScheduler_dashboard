# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 下午 1:56 
import json
import time
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from log import request_log


class LogRoute(APIRoute):
    @staticmethod
    async def request_params(request: Request) -> dict:
        def check_form(k, v):
            if type(v).__name__ == 'UploadFile':
                k = "UploadFile"
                v = v.filename
            if type(v) == bytes:
                v = "*"
            if k == "password":
                v = "*"
            return k, v

        try:
            json_data = await request.json()
        except:  # noqa
            json_data = {}
        log_info = {
            "url": request.url.path,
            "path_params": request.path_params,
            "query_params": dict((k, v) for k, v in request.query_params.multi_items()),
            "form": dict(check_form(k, v) for k, v in (await request.form()).multi_items()),
            "json": json_data
        }
        return log_info

    @staticmethod
    def save_request_log(request_id: str, log_ip: str, log_info: dict, method: str):
        """
        记录HTTP请求日志
        :param request_id: 请求
        :param log_ip: 客户端IP
        :param log_info: 日志内容
        :return:
        """
        request_log.info(json.dumps({
            "time": f"{datetime.now():%Y-%m-%d %H:%M:%S}",
            "request_id": request_id,
            "ip": log_ip,
            "request": log_info,
            "method": method
        }))

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_id = request.state.request_id
            before = time.time()
            response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            self.save_request_log(
                request_id=request_id,
                log_ip=request.headers.get("x-real-ip", request.client.host),
                log_info=await self.request_params(request),
                method=request.method,
            )
            return response

        return custom_route_handler

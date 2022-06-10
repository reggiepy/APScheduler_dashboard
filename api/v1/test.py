import asyncio
import logging
import time

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi.responses import JSONResponse

from api.custon_route import LogRoute

api = APIRouter(route_class=LogRoute)

logger = logging.getLogger()


@api.post(
    "/test",
    response_model=str,
    name="API接口测试",
    summary="API接口测试",
    description="测试API接口是否正常响应")
async def test():
    return JSONResponse(
        {"message": "it works!"}
    )


@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        await websocket.send_text("Time: {}".format(time.asctime()))

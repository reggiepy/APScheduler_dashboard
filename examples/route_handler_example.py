# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/10 上午 10:57 
import time
from typing import Callable

import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router_1 = APIRouter(route_class=TimedRoute)


@router_1.get("/")
async def not_timed():
    return {"message": "Not timed"}


@router_1.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}


# The route is no longer timed
router = APIRouter()
router.include_router(router_1)

# This also doesnt work
# router = APIRouter()
# router.include_router(router_1)
# router.route_class = TimedRoute

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    from pathlib import Path
    uvicorn.run(
        app=f"{Path(__file__).stem}:app",
        host="127.0.0.1",
        port=2323,
    )

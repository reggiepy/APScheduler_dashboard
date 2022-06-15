# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/13 上午 10:39 
from fastapi import APIRouter

from api.v1.endpoints import test, auth, schedule_jobs

api_router = APIRouter()
# api_router.include_router(test.api, tags=["环境测试"], dependencies=[Depends(OAuth2Scheme)])
# check_authority 权限验证内部包含了 token 验证 如果不校验权限可直接 dependencies=[Depends(check_jwt_token)]
# api_router.include_router(test.api, tags=["环境测试"], dependencies=[Depends(OAuth2Scheme)])
api_router.include_router(test.api, tags=["环境测试"])
api_router.include_router(auth.api, tags=["系统认证"])
api_router.include_router(schedule_jobs.api, prefix="/scheduler", tags=["调度器任务"])

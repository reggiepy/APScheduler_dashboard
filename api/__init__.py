# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 6:53

from fastapi import APIRouter, Depends

from api.dependencies.auth import check_jwt_token, get_current_user
from api.v1 import test, auth, jobs

api_router = APIRouter()
# api_router.include_router(test.api, tags=["环境测试"], dependencies=[Depends(OAuth2Scheme)])
# check_authority 权限验证内部包含了 token 验证 如果不校验权限可直接 dependencies=[Depends(check_jwt_token)]
# api_router.include_router(test.api, tags=["环境测试"], dependencies=[Depends(OAuth2Scheme)])
api_router.include_router(test.api, tags=["环境测试"])
api_router.include_router(auth.api, tags=["系统认证"])
api_router.include_router(jobs.api, prefix="/scheduler", tags=["定时任务"])

# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 5:13 
import time
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html, get_redoc_html
from pip._vendor.requests import RequestException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

import events
import settings
from api import api_router
from api.exception_handlers.http_error import http_error_handler, http_400_error_handler
from api.exception_handlers.validation_error import http_422_error_handler
from api.middlewares.audit import AuditMiddleware
from api.middlewares.common import add_process_time_header
from log import log_init


def get_application() -> FastAPI:
    application = FastAPI(
        debug=settings.PROJECT_DEBUG,
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESC,
        version=settings.PROJECT_VERSION,
        docs_url=None,
        redoc_url=None,
    )

    @application.get(settings.PROJECT_DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="swagger/swagger-ui-bundle.js",
            swagger_css_url="swagger/swagger-ui.css",
            swagger_favicon_url="swagger/favicon.png",
        )

    @application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @application.get(settings.PROJECT_REDOC_URL, include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="swagger/redoc.standalone.js",
            redoc_favicon_url="swagger/favicon.png",
            with_google_fonts=False
        )
    application.include_router(api_router, prefix=settings.PROJECT_URL_PREFIX)
    application.add_event_handler("startup", events.create_start_app_handler(application))
    application.add_event_handler("shutdown", events.create_stop_app_handler(application))
    application.add_exception_handler(RequestValidationError, http_422_error_handler)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestException, http_400_error_handler)
    application.add_middleware(HTTPSRedirectMiddleware)
    application.add_middleware(AuditMiddleware)
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS if settings.ALLOWED_HOSTS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.mount("/static", StaticFiles(directory=settings.STATIC_RESOURCE_PATH, html=True), name="static")
    application.mount("/swagger", StaticFiles(directory=settings.SWAGGER_RESOURCE_PATH, html=True), name="swagger")
    # for route in application.routes:
    #     print(route.path)
    return application


app = get_application()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = uuid4().hex
    request.state.request_id = request_id
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Middleware"] = str(process_time)
    # if response.status_code == 404:
    #     response = FileResponse(f"{settings.STATIC_RESOURCE_PATH}/index.html", status_code=200, method="GET")
    response.headers["Request-ID"] = request_id
    return response


if __name__ == '__main__':
    # Load the configuration
    log_init(log_to_stderr="1")
    uvicorn.run(
        app="dash:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        ssl_keyfile=settings.SSL_KEYFILE,
        ssl_certfile=settings.SSL_CERTFILE,
        workers=settings.SERVER_WORKERS,
        # log_config=LOGGING_CONFIG,
    )

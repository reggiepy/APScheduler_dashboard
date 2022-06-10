from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status

from api.exception_handlers.exceptions import RequestException


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def http_400_error_handler(_: Request, exc: RequestException) -> JSONResponse:
    return JSONResponse(exc.error, status_code=status.HTTP_400_BAD_REQUEST)

from pydantic import BaseModel
from pydantic import Field

from api.exception_handlers.error_code import error_code_to_message


class ErrorInResponse(BaseModel):
    request_id: str = Field(None, title="请求ID")
    error_class: str = Field(None, title="错误类型")
    error_code: str = Field(None, title="错误代码")
    message: str = Field(None, title="错误消息")
    description: str = Field(None, title="错误的详细描述")
    host_id: str = Field(None, title="主机ID")


class RequestException(Exception):
    def __init__(
            self,
            request_id,
            error_class,
            error_code,
            message: str = None,
            description: str = None,
            host_id: str = None
    ):
        error = ErrorInResponse(
            request_id=request_id,
            error_class=error_class,
            error_code=error_code,
            message=message if message else error_code_to_message(error_code),
            description=description,
            host_id=host_id
        )
        self.error = error.dict()

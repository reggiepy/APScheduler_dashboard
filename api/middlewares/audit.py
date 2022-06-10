from starlette.types import ASGIApp
from starlette.types import Receive, Scope, Send


class AuditMiddleware:

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)

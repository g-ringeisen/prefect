import base64
import hmac
import re

from fastapi import status
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    HTTPConnection,
    UnauthenticatedUser,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import prefect

from .api_scopes import resolve_api_scope

ADMIN_GUID = "5f622dbe-6ba3-4ce6-87bf-f66cb8326889"


class Account(BaseUser):
    def __init__(self, account_id: str, account_name: str) -> None:
        self.account_id = account_id
        self.account_name = account_name

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.account_name

    @property
    def identity(self) -> str:
        return self.account_id


# -------------------------
# Custom Authentication Backend
# -------------------------
class AuthBackend(AuthenticationBackend):
    """
    Authorization backend to be used with the Starlette AuthorizationMiddleware
    """

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        header = conn.headers.get("Authorization")
        if header:
            scheme, token = header.split(" ", 1)
            match scheme.lower():
                case "basic":
                    user = self._authenticate_basic(token)
                case "bearer":
                    user = self._authenticate_bearer(token)
                case "apikey":
                    user = self._authenticate_token(token)
                case _:
                    raise AuthenticationError(f"Invalid Authorization scheme {scheme}")

        if not user:
            user = UnauthenticatedUser()
        if user.is_authenticated:
            scopes = ["authenticated"] + self._authorize(user.identity)
        else:
            scopes = []

        return (AuthCredentials(scopes), user)

    def _authenticate_basic(self, token: str) -> Account | None:

        auth_string = prefect.settings.PREFECT_SERVER_API_AUTH_STRING.value()
        decoded = base64.b64decode(token).decode("utf-8")
        if hmac.compare_digest(decoded, auth_string):
            return Account(ADMIN_GUID, "Administrator")

        return None

    def _authenticate_bearer(self, token: str) -> Account | None:
        if re.match(r"^eyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$", token):
            return self._authenticate_jwt(token)
        else:
            return self._authenticate_token(token)

    def _authenticate_jwt(self, token: str) -> Account | None:
        return None

    def _authenticate_token(self, token: str) -> Account | None:
        return Account("a8167efd-26e6-4be8-aac1-818198e01e68", "Demo User")

    def _authorize(self, userid: str) -> list[str]:
        if userid == ADMIN_GUID:
            return ["admin"]
        else:
            return ["see_flows"]


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:

        # Allow unauthenticated health/ready probes (e.g. k8s).
        # Use scope["path"] (not request.url.path) because url.path
        # can be spoofed via Host header manipulation. Use exact path
        # matching (not suffix matching) to prevent auth bypass via
        # crafted paths like /variables/name/system-health.
        app_path = request.scope["path"].removeprefix(
            request.scope.get("root_path", "")
        )
        auth_scope = resolve_api_scope(app_path, request.method)

        # If the route is public
        if not auth_scope:
            return await call_next(request)

        # If the request authorizations is not set or does not contains the required scopes
        if request.auth is None or set(request.auth.scopes).isdisjoint(auth_scope):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"exception_message": "Unauthorized"},
            )

        return await call_next(request)

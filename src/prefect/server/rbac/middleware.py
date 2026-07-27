import base64
import hmac
import re
from uuid import UUID

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
from prefect.server.rbac.api_scopes import resolve_api_scope
from prefect.server.rbac.models import get_scopes_for_account
from prefect.server.rbac.schemas import Account


class AuthUser(BaseUser):
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


ADMIN_GUID = UUID("5f622dbe-6ba3-4ce6-87bf-f66cb8326889")
ADMIN_USER = AuthUser(ADMIN_GUID, "Administrator")
ADMIN_SCOPES = ["admin", "authenticated"]


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
        account: Account = None
        header = conn.headers.get("Authorization")
        if header:
            scheme, token = header.split(" ", 1)
            match scheme.lower():
                case "basic":
                    auth_string = (
                        prefect.settings.PREFECT_SERVER_API_AUTH_STRING.value()
                    )
                    decoded = base64.b64decode(token).decode("utf-8")
                    if hmac.compare_digest(decoded, auth_string):
                        return (AuthCredentials(ADMIN_SCOPES), ADMIN_USER)
                    account = await self._authenticate_basic(token)
                case "bearer":
                    account = await self._authenticate_bearer(token)
                case "apikey":
                    account = await self._authenticate_token(token)
                case _:
                    raise AuthenticationError(f"Invalid Authorization scheme {scheme}")

        if not account:
            user = UnauthenticatedUser()
            scopes = []
        else:
            user = AuthUser(account.id, account.name)
            scopes = ["authenticated"]
            scopes += await self._authorize(account.id)
        return (AuthCredentials(scopes), user)

    async def _authenticate_basic(self, token: str) -> Account | None:
        return None

    async def _authenticate_bearer(self, token: str) -> Account | None:
        if re.match(r"^eyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$", token):
            return self._authenticate_jwt(token)
        else:
            return self._authenticate_token(token)

    async def _authenticate_jwt(self, token: str) -> Account | None:
        return None

    async def _authenticate_token(self, token: str) -> Account | None:
        return None

    async def _authorize(self, account_id: UUID) -> list[str]:
        if account_id == ADMIN_GUID:
            return ["admin"]
        else:
            return get_scopes_for_account(UUID(account_id))


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
        route_scopes = resolve_api_scope(app_path, request.method)
        user_scopes = set(request.auth.scopes) if request.auth is not None else []

        # If the route is public or the user is super admin
        if not route_scopes or "admin" in user_scopes:
            return await call_next(request)

        # If the request authorizations is not set or does not contains the required scopes
        if request.auth is None or user_scopes.issubset(route_scopes):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"exception_message": "Unauthorized"},
            )

        return await call_next(request)

# src/prefect/server/rbac/schemas.py

"""
Pydantic schemas for RBAC — accounts, roles, and scope management.

Convention: follows the same split used in the rest of Prefect schemas:
  - *Base      : shared fields (PrefectBaseModel)
  - *Create    : payload for POST (ActionBaseModel — extra fields forbidden)
  - *Update    : payload for PATCH (ActionBaseModel — all fields Optional)
  - *Response  : what the API returns (ORMBaseModel — includes id/created/updated
                 and from_attributes=True for ORM serialization)
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from prefect.server.rbac.scopes import Scope
from prefect.server.utilities.schemas.bases import (
    ActionBaseModel,
    ORMBaseModel,
)

# --------------------------------------------------------------------------- #
# Account type
# --------------------------------------------------------------------------- #


class AccountType(str, Enum):
    """Discriminates between human users, service accounts, and API keys."""

    USER = "user"
    SERVICE = "service"
    API_KEY = "api_key"


# --------------------------------------------------------------------------- #
# Role schemas
# --------------------------------------------------------------------------- #


class Role(ORMBaseModel):
    """
    Returned by all role endpoints.

    Inherits id, created, updated from ORMBaseModel.
    """

    name: str
    scopes: List[Scope] = []


class RoleCreate(ActionBaseModel):
    """Payload for POST /api/roles."""

    name: str
    scopes: List[Scope] = []


class RoleUpdate(ActionBaseModel):
    """Payload for PATCH /api/roles/{role_id} — all fields are optional."""

    name: Optional[str] = None
    scopes: Optional[List[Scope]] = None


class RoleScopesUpdate(ActionBaseModel):
    """
    Payload for POST /api/roles/{role_id}/scopes.

    The provided list is treated as the new authoritative set —
    any scope not included is revoked.
    """

    scopes: List[Scope]


# --------------------------------------------------------------------------- #
# Api Key schemas
# --------------------------------------------------------------------------- #
class ApiKey(ORMBaseModel):
    key: str


# --------------------------------------------------------------------------- #
# Account schemas
# --------------------------------------------------------------------------- #


class Account(ORMBaseModel):
    """
    Returned by account read endpoints.

    Roles are not embedded — use GET /api/accounts/{id}/roles.
    Inherits id, created, updated from ORMBaseModel.
    """

    name: str
    username: str
    email: str


class AccountCreate(ActionBaseModel):
    """Payload for POST /api/accounts."""

    name: str
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class AccountUpdate(ActionBaseModel):
    """Payload for PATCH /api/accounts/{account_id} — all fields are optional."""

    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class AccountWithRoles(Account):
    """Extended account response that includes the assigned roles."""

    roles: List[Role] = []

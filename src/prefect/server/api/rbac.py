# src/prefect/server/api/rbac.py

"""
RBAC routers — accounts and roles.

Two routers are defined here and must be registered in API_ROUTERS
inside src/prefect/server/api/server.py:

    import prefect.server.api as api
    ...
    API_ROUTERS = (
        ...
        api.rbac.accounts_router,
        api.rbac.roles_router,
        api.root.router,   # must remain last
    )

And declared in src/prefect/server/api/__init__.py:

    if TYPE_CHECKING:
        from prefect.server.api import (
            ...
            rbac,
        )

    __all__ = [
        ...
        "rbac",
    ]

Each router delegates persistence to a (yet-to-be-implemented) backend
module via the `provide_rbac_store` dependency.
"""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import HTTPException, Path, status

import prefect.server.rbac.models as models
import prefect.server.rbac.schemas as schema
from prefect.server.utilities.server import PrefectRouter

# --------------------------------------------------------------------------- #
# Accounts router  —  /api/accounts
# --------------------------------------------------------------------------- #

accounts_router = PrefectRouter(prefix="/accounts", tags=["Accounts"])


@accounts_router.get("/")
async def list_accounts() -> List[schema.Account]:
    """List all accounts."""
    return await models.list_accounts()


@accounts_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    payload: schema.AccountCreate,
) -> schema.Account:
    """Create a new account."""
    return await models.create_account(payload)


@accounts_router.get("/{account_id}")
async def get_account(
    account_id: UUID = Path(..., description="The account ID."),
) -> schema.Account:
    """Get a single account by ID."""
    account = await models.get_account(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )
    return account


@accounts_router.patch("/{account_id}")
async def update_account(
    payload: schema.AccountUpdate,
    account_id: UUID = Path(..., description="The account ID."),
) -> schema.Account:
    """Partially update an account."""
    account = await models.update_account(account_id, payload)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )
    return account


@accounts_router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: UUID = Path(..., description="The account ID."),
) -> None:
    """Delete an account."""
    deleted = await models.delete_account(account_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )


@accounts_router.get("/{account_id}/roles")
async def get_account_roles(
    account_id: UUID = Path(..., description="The account ID."),
) -> schema.AccountWithRoles:
    """Get all roles assigned to an account."""
    account = await models.get_account_with_roles(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )
    return account


@accounts_router.post(
    "/{account_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def assign_role_to_account(
    account_id: UUID = Path(..., description="The account ID."),
    role_id: UUID = Path(..., description="The role ID to assign."),
) -> None:
    """Assign a role to an account."""
    success = await models.assign_role(account_id, role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account or role not found.",
        )


@accounts_router.delete(
    "/{account_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_role_from_account(
    account_id: UUID = Path(..., description="The account ID."),
    role_id: UUID = Path(..., description="The role ID to remove."),
) -> None:
    """Remove a role from an account."""
    success = await models.remove_role(account_id, role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account or role assignment not found.",
        )


@accounts_router.post(
    "/{account_id}/api_keys/",
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key(
    account_id: UUID = Path(..., description="The account ID."),
) -> schema.ApiKey:
    """Create a new api key."""
    return await models.create_api_key(account_id=account_id)


@accounts_router.get("/{account_id}/api_keys/")
async def list_api_keys(
    account_id: UUID = Path(..., description="The account ID."),
) -> List[schema.ApiKey]:
    """List all api keys of the account."""
    return await models.list_api_keys(account_id=account_id)


@accounts_router.get("/{account_id}/api_keys/{api_key_id}")
async def get_api_key(
    account_id: UUID = Path(..., description="The account ID."),
    api_key_id: UUID = Path(..., description="The api key ID."),
) -> schema.ApiKey:
    """List all api keys of the account."""
    api_key: schema.ApiKey = await models.get_api_key(key_id=api_key_id)
    if not api_key or api_key.account_id != account_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Api Key not found.",
        )
    return api_key


@accounts_router.delete(
    "/{account_id}/api_keys/{api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_api_key(
    account_id: UUID = Path(..., description="The account ID."),
    api_key_id: UUID = Path(..., description="The api key ID."),
) -> None:
    """Delete an api key."""
    success = await models.delete_api_key(account_id=account_id, key_id=api_key_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Api Key not found.",
        )


# --------------------------------------------------------------------------- #
# Roles router  —  /api/roles
# --------------------------------------------------------------------------- #

roles_router = PrefectRouter(prefix="/roles", tags=["Roles"])


@roles_router.get("/")
async def list_roles() -> List[schema.Role]:
    """List all roles."""
    return await models.list_roles()


@roles_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    payload: schema.RoleCreate,
) -> schema.Role:
    """Create a new role."""
    return await models.create_role(payload)


@roles_router.get("/{role_id}")
async def get_role(
    role_id: UUID = Path(..., description="The role ID."),
) -> schema.Role:
    """Get a single role by ID, including its scopes."""
    role = await models.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )
    return role


@roles_router.patch("/{role_id}")
async def update_role(
    payload: schema.RoleUpdate,
    role_id: UUID = Path(..., description="The role ID."),
) -> schema.Role:
    """Partially update a role (name and/or scopes)."""
    role = await models.update_role(role_id, payload)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )
    return role


@roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID = Path(..., description="The role ID."),
) -> None:
    """Delete a role."""
    deleted = await models.delete_role(role_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )


@roles_router.post("/{role_id}/scopes")
async def update_role_scopes(
    payload: schema.RoleScopesUpdate,
    role_id: UUID = Path(..., description="The role ID."),
) -> schema.Role:
    """
    Replace the full list of scopes for a role.

    The provided list is treated as the new authoritative set —
    any scope not included is revoked.
    """
    role = await models.update_role_scopes(role_id, payload.scopes)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )
    return role

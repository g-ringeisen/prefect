# src/prefect/server/rbac/store.py

"""
RBAC store — persistence layer for accounts and roles.

Provides a single `RbacStore` class that wraps an async SQLAlchemy session
and implements all CRUD operations required by the RBAC routers.

Usage (via dependency injection in api/dependencies.py):

    from prefect.server.rbac.store import RbacStore

    async def provide_rbac_store(
        db: PrefectDBInterface = Depends(provide_database_interface),
    ) -> AsyncGenerator[RbacStore, None]:
        async with db.session_context() as session:
            yield RbacStore(session)
"""

from __future__ import annotations

import hashlib
import secrets
from typing import List, Optional, Sequence
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

import prefect.server.rbac.schemas as schemas
from prefect.server.database import PrefectDBInterface, db_injector
from prefect.server.database.orm_models import Base
from prefect.server.rbac.scopes import Scope
from prefect.server.utilities.database import JSON

# ----------------------------------------------------------------------- #
# Thin async persistence layer for RBAC entities.
# ----------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# Association table  (no ORM class needed — pure join table)
# --------------------------------------------------------------------------- #

rbac_account_role = sa.Table(
    "rbac_account_role",
    Base.registry.metadata,
    sa.Column(
        "account_id",
        sa.ForeignKey("rbac_account.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    sa.Column(
        "role_id",
        sa.ForeignKey("rbac_role.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


# --------------------------------------------------------------------------- #
# Role
# --------------------------------------------------------------------------- #


class RoleModel(Base):
    """SQLAlchemy model for an RBAC role."""

    __tablename__ = "rbac_role"

    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    # Scopes are stored as a JSON list of strings, e.g. ["see_flows", "run_flows"].
    # Validation against the Scope Enum is enforced at the Pydantic layer.
    scopes: Mapped[List[str]] = mapped_column(
        JSON,
        server_default="[]",
        default=list,
        nullable=False,
    )

    accounts: Mapped[List["AccountModel"]] = relationship(
        secondary=rbac_account_role,
        back_populates="roles",
        lazy="raise",
    )

    __table_args__ = (sa.UniqueConstraint("name", name="uq_rbac_role__name"),)


# --------------------------------------------------------------------------- #
# Api Key
# --------------------------------------------------------------------------- #
class ApiKeyModel(Base):
    """SQLAlchemy model for an RBAC account api key"""

    __tablename__ = "rbac_api_key"

    key: Mapped[str] = mapped_column(sa.String, nullable=False)

    account_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("rbac_account.id", ondelete="CASCADE"), nullable=False
    )
    account: Mapped["AccountModel"] = relationship(back_populates="api_keys")


# --------------------------------------------------------------------------- #
# Account
# --------------------------------------------------------------------------- #


class AccountModel(Base):
    """SQLAlchemy model for an RBAC account (user, service, or API key)."""

    __tablename__ = "rbac_account"

    # Human-readable display name (not necessarily unique)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    username: Mapped[str] = mapped_column(sa.String, nullable=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=True)
    email: Mapped[str] = mapped_column(sa.String, nullable=True)

    roles: Mapped[List[RoleModel]] = relationship(
        secondary=rbac_account_role,
        back_populates="accounts",
        lazy="selectin",
    )

    api_keys: Mapped[List[ApiKeyModel]] = relationship(back_populates="account")

    __table_args__ = (sa.Index("ix_rbac_account__name", "name"),)


# ----------------------------------------------------------------------- #
# Role Store
# ----------------------------------------------------------------------- #


@db_injector
async def list_roles(
    db: PrefectDBInterface,
) -> Sequence[schemas.Role]:

    async with db.session_context(begin_transaction=True) as session:
        result = await session.execute(sa.select(RoleModel))
        roles = result.scalars().all()
        return [schemas.Role.model_validate(r) for r in roles]


@db_injector
async def create_role(
    db: PrefectDBInterface, payload: schemas.RoleCreate
) -> schemas.Role:
    role = RoleModel(
        name=payload.name,
        scopes=[s.value for s in payload.scopes],
    )
    async with db.session_context(begin_transaction=True) as session:
        session.add(role)
        await session.flush()
        await session.refresh(role)
        return schemas.Role.model_validate(role)


@db_injector
async def get_role(db: PrefectDBInterface, role_id: UUID) -> Optional[schemas.Role]:
    async with db.session_context(begin_transaction=True) as session:
        role = await session.get(RoleModel, role_id)
        if role is None:
            return None
        return schemas.Role.model_validate(role)


@db_injector
async def update_role(
    db: PrefectDBInterface, role_id: UUID, payload: schemas.RoleUpdate
) -> Optional[schemas.Role]:
    async with db.session_context(begin_transaction=True) as session:
        role = await session.get(RoleModel, role_id)
        if role is None:
            return None
        if payload.name is not None:
            role.name = payload.name
        if payload.scopes is not None:
            role.scopes = [s.value for s in payload.scopes]
        await session.flush()
        await session.refresh(role)
        return schemas.Role.model_validate(role)


@db_injector
async def delete_role(db: PrefectDBInterface, role_id: UUID) -> bool:
    async with db.session_context(begin_transaction=True) as session:
        role = await session.get(RoleModel, role_id)
        if role is None:
            return False
        await session.delete(role)
        await session.flush()
        return True


@db_injector
async def update_role_scopes(
    db: PrefectDBInterface, role_id: UUID, scopes: List[Scope]
) -> Optional[schemas.Role]:
    async with db.session_context(begin_transaction=True) as session:
        role = await session.get(RoleModel, role_id)
        if role is None:
            return None
        role.scopes = [s.value for s in scopes]
        await session.flush()
        await session.refresh(role)
        return schemas.Role.model_validate(role)


# ----------------------------------------------------------------------- #
# Account Store
# ----------------------------------------------------------------------- #


@db_injector
async def list_accounts(db: PrefectDBInterface) -> List[schemas.Account]:
    async with db.session_context(begin_transaction=True) as session:
        result = await session.execute(sa.select(AccountModel))
        accounts = result.scalars().all()
        return [schemas.Account.model_validate(a) for a in accounts]


@db_injector
async def create_account(
    db: PrefectDBInterface, payload: schemas.AccountCreate
) -> schemas.Account:
    account = AccountModel(
        name=payload.name,
        username=payload.username,
        password=hashlib.sha256(payload.password.value.encode()).hexdigest(),
        email=payload.email,
    )
    async with db.session_context(begin_transaction=True) as session:
        session.add(account)
        await session.flush()
        await session.refresh(account)
        return schemas.Account.model_validate(account)


@db_injector
async def get_account(
    db: PrefectDBInterface, account_id: UUID
) -> Optional[schemas.Account]:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return None
        return schemas.Account.model_validate(account)


@db_injector
async def update_account(
    db: PrefectDBInterface, account_id: UUID, payload: schemas.AccountUpdate
) -> Optional[schemas.Account]:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return None
        if payload.name is not None:
            account.name = payload.name
        if payload.username is not None:
            account.username = payload.username
        if payload.password is not None:
            account.password = hashlib.sha256(payload.password.encode()).hexdigest()
        if payload.email is not None:
            account.email = payload.email
        await session.flush()
        await session.refresh(account)
        return schemas.Account.model_validate(account)


@db_injector
async def delete_account(db: PrefectDBInterface, account_id: UUID) -> bool:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return False
        await session.delete(account)
        await session.flush()
        return True


# ----------------------------------------------------------------------- #
# Api Key Store
# ----------------------------------------------------------------------- #
@db_injector
async def create_api_key(db: PrefectDBInterface, account_id: UUID) -> schemas.ApiKey:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return None
        api_key = ApiKeyModel(
            key=secrets.token_urlsafe(32),
            account=account,
        )
        session.add(api_key)
        await session.flush()
        await session.refresh(api_key)
        return schemas.ApiKey.model_validate(api_key)


@db_injector
async def list_api_keys(
    db: PrefectDBInterface, account_id: UUID
) -> List[schemas.ApiKey]:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(
            AccountModel,
            account_id,
            options=[selectinload(AccountModel.api_keys)],
        )
        if account is None:
            return None
        return [schemas.ApiKey.model_validate(k) for k in account.api_keys]


@db_injector
async def get_api_key(db: PrefectDBInterface, api_key_id: UUID) -> schemas.ApiKey:
    async with db.session_context(begin_transaction=True) as session:
        api_key = await session.get(ApiKeyModel, api_key_id)
        if api_key is None:
            return None
        return schemas.ApiKey.model_validate(api_key)


@db_injector
async def delete_api_key(
    db: PrefectDBInterface, account_id: UUID, key_id: UUID
) -> bool:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return False
        api_key = next([k for k in account.api_keys if k.id == key_id])
        if api_key is None:
            return False
        await session.delete(api_key)
        await session.flush()
        return True


# ----------------------------------------------------------------------- #
# Account ↔ Role assignments
# ----------------------------------------------------------------------- #


@db_injector
async def get_account_with_roles(
    db: PrefectDBInterface, account_id: UUID
) -> Optional[schemas.AccountWithRoles]:
    async with db.session_context(begin_transaction=True) as session:
        # roles are loaded via `lazy="selectin"` on ORMAccount
        account = await session.get(AccountModel, account_id)
        if account is None:
            return None
        return schemas.AccountWithRoles.model_validate(account)


@db_injector
async def assign_role(db: PrefectDBInterface, account_id: UUID, role_id: UUID) -> bool:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        role = await session.get(RoleModel, role_id)
        if account is None or role is None:
            return False
        # Avoid duplicates — SQLAlchemy relationship deduplicates in-memory
        # but the unique PK on the join table handles it at DB level too.
        if role not in account.roles:
            account.roles.append(role)
            await session.flush()
        return True


@db_injector
async def remove_role(db: PrefectDBInterface, account_id: UUID, role_id: UUID) -> bool:
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        role = await session.get(RoleModel, role_id)
        if account is None or role is None:
            return False
        if role not in account.roles:
            return False
        account.roles.remove(role)
        await session.flush()
        return True


# ----------------------------------------------------------------------- #
# Utility — used by the auth middleware to resolve scopes for an identity
# ----------------------------------------------------------------------- #


@db_injector
async def get_scopes_for_account(db: PrefectDBInterface, account_id: UUID) -> List[str]:
    """
    Return the consolidated list of scope values for a given account,
    deduplicating across all assigned roles.
    """
    async with db.session_context(begin_transaction=True) as session:
        account = await session.get(AccountModel, account_id)
        if account is None:
            return []
        seen: set[str] = set()
        result: list[str] = []
        for role in account.roles:
            for scope in role.scopes:
                if scope not in seen:
                    seen.add(scope)
                    result.append(scope)
        return result

"""Add RBAC tables (rbac_role, rbac_account, rbac_account_role).

Revision ID: a1b2c3d4e5f6
Revises: d20618ce678e
Create Date: 2026-07-23 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "bad1e352c597"
branch_labels = None
depends_on = None


def upgrade():
    # ------------------------------------------------------------------ #
    # rbac_role
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_role",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text("(GEN_RANDOM_UUID())"),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "scopes",
            prefect.server.utilities.database.JSON(astext_type=sa.Text()),
            server_default="[]",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rbac_role")),
        sa.UniqueConstraint("name", name=op.f("uq_rbac_role__name")),
    )
    op.create_index(
        op.f("ix_rbac_role__updated"), "rbac_role", ["updated"], unique=False
    )

    # ------------------------------------------------------------------ #
    # rbac_account
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_account",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text("(GEN_RANDOM_UUID())"),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rbac_account")),
    )
    op.create_index(
        op.f("ix_rbac_account__name"), "rbac_account", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_rbac_account__username"), "rbac_account", ["username"], unique=True
    )
    op.create_index(
        op.f("ix_rbac_account__updated"), "rbac_account", ["updated"], unique=False
    )

    # ------------------------------------------------------------------ #
    # rbac_api_key
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_api_key",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text("(GEN_RANDOM_UUID())"),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "account_id", prefect.server.utilities.database.UUID(), nullable=False
        ),
        sa.Column("key", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rbac_api_key")),
    )
    op.create_index(op.f("ix_rbac_api_key__key"), "rbac_api_key", ["key"], unique=True)

    # ------------------------------------------------------------------ #
    # rbac_account_role  (pure join table — no id/created/updated)
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_account_role",
        sa.Column(
            "account_id",
            prefect.server.utilities.database.UUID(),
            nullable=False,
        ),
        sa.Column(
            "role_id",
            prefect.server.utilities.database.UUID(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["rbac_account.id"],
            name=op.f("fk_rbac_account_role__account_id__rbac_account"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["rbac_role.id"],
            name=op.f("fk_rbac_account_role__role_id__rbac_role"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "account_id", "role_id", name=op.f("pk_rbac_account_role")
        ),
    )


def downgrade():
    op.drop_table("rbac_account_role")

    op.drop_index(op.f("ix_rbac_account__updated"), table_name="rbac_account")
    op.drop_index(op.f("ix_rbac_account__name"), table_name="rbac_account")
    op.drop_index(op.f("ix_rbac_account__username"), table_name="rbac_account")
    op.drop_table("rbac_account")

    op.drop_index(op.f("ix_rbac_api_key__key"), table_name="rbac_api_key")
    op.drop_table("rbac_api_key")

    op.drop_index(op.f("ix_rbac_role__updated"), table_name="rbac_role")
    op.drop_table("rbac_role")

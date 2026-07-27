"""Add RBAC tables (rbac_role, rbac_account, rbac_account_role).

Revision ID: a1b2c3d4e5f6
Revises: 3d46e23593d6
Create Date: 2026-07-23 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "79e7a60e43d8"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("PRAGMA foreign_keys=OFF")

    # ------------------------------------------------------------------ #
    # rbac_role
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_role",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text(
                "(lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2)))"
                " || '-4' || substr(lower(hex(randomblob(2))),2) || '-'"
                " || substr('89ab',abs(random()) % 4 + 1, 1)"
                " || substr(lower(hex(randomblob(2))),2) || '-'"
                " || lower(hex(randomblob(6))))"
            ),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
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
    with op.batch_alter_table("rbac_role", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_rbac_role__updated"), ["updated"], unique=False
        )

    # ------------------------------------------------------------------ #
    # rbac_account
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_account",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text(
                "(lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2)))"
                " || '-4' || substr(lower(hex(randomblob(2))),2) || '-'"
                " || substr('89ab',abs(random()) % 4 + 1, 1)"
                " || substr(lower(hex(randomblob(2))),2) || '-'"
                " || lower(hex(randomblob(6))))"
            ),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rbac_account")),
    )
    with op.batch_alter_table("rbac_account", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_rbac_account__name"), ["name"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_rbac_account__username"), ["username"], unique=True
        )
        batch_op.create_index(
            batch_op.f("ix_rbac_account__email"), ["email"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_rbac_account__updated"), ["updated"], unique=False
        )

    # ------------------------------------------------------------------ #
    # rbac_api_key
    # ------------------------------------------------------------------ #
    op.create_table(
        "rbac_api_key",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text(
                "(lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2)))"
                " || '-4' || substr(lower(hex(randomblob(2))),2) || '-'"
                " || substr('89ab',abs(random()) % 4 + 1, 1)"
                " || substr(lower(hex(randomblob(2))),2) || '-'"
                " || lower(hex(randomblob(6))))"
            ),
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
    with op.batch_alter_table("rbac_api_key", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_rbac_api_key__key"), ["key"], unique=True)

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

    op.execute("PRAGMA foreign_keys=ON")


def downgrade():
    op.execute("PRAGMA foreign_keys=OFF")

    op.drop_table("rbac_account_role")

    with op.batch_alter_table("rbac_account", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_rbac_account__updated"))
        batch_op.drop_index(batch_op.f("ix_rbac_account__username"))
        batch_op.drop_index(batch_op.f("ix_rbac_account__email"))
        batch_op.drop_index(batch_op.f("ix_rbac_account__name"))
    op.drop_table("rbac_account")

    with op.batch_alter_table("rbac_api_key", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_rbac_api_key__key"))
    op.drop_table("rbac_api_key")

    with op.batch_alter_table("rbac_role", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_rbac_role__updated"))
    op.drop_table("rbac_role")

    op.execute("PRAGMA foreign_keys=ON")

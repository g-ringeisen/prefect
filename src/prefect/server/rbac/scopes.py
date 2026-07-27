# src/prefect/server/rbac/scopes.py

"""
Defines the available RBAC scopes as an Enum.

A scope represents a single permission that can be granted to a role.
Roles aggregate multiple scopes, and accounts inherit the consolidated
set of scopes from all their assigned roles.
"""

from enum import Enum


class Scope(str, Enum):
    """
    Exhaustive list of scopes available in Prefect RBAC.

    Each value is a string of the form "<action>_<resource>" following
    the pattern already used by FastAPI / OAuth2 security schemes so
    that scopes can be forwarded to SecurityScopes dependencies without
    any transformation.

    Three-level convention for most resources:
      see_*    → read access
      write_*  → create / update
      manage_* → delete / admin operations
    Some resources add a dedicated action scope (run_*, etc.).
    """

    # ------------------------------------------------------------------ #
    # Flows
    # ------------------------------------------------------------------ #
    SEE_FLOWS = "see_flows"
    RUN_FLOWS = "run_flows"
    MANAGE_FLOWS = "manage_flows"

    # ------------------------------------------------------------------ #
    # Deployments
    # ------------------------------------------------------------------ #
    SEE_DEPLOYMENTS = "see_deployments"
    WRITE_DEPLOYMENTS = "write_deployments"
    RUN_DEPLOYMENTS = "run_deployments"
    MANAGE_DEPLOYMENTS = "manage_deployments"

    # ------------------------------------------------------------------ #
    # Work Pools
    # ------------------------------------------------------------------ #
    SEE_WORK_POOLS = "see_work_pools"
    WRITE_WORK_POOLS = "write_work_pools"
    MANAGE_WORK_POOLS = "manage_work_pools"

    # ------------------------------------------------------------------ #
    # Work Queues
    # ------------------------------------------------------------------ #
    SEE_WORK_QUEUES = "see_work_queues"
    WRITE_WORK_QUEUES = "write_work_queues"
    MANAGE_WORK_QUEUES = "manage_work_queues"

    # ------------------------------------------------------------------ #
    # Workers
    # ------------------------------------------------------------------ #
    SEE_WORKERS = "see_workers"
    WRITE_WORKERS = "write_workers"
    MANAGE_WORKERS = "manage_workers"

    # ------------------------------------------------------------------ #
    # Artifacts
    # ------------------------------------------------------------------ #
    SEE_ARTIFACTS = "see_artifacts"
    WRITE_ARTIFACTS = "write_artifacts"
    MANAGE_ARTIFACTS = "manage_artifacts"

    # ------------------------------------------------------------------ #
    # Assets
    # ------------------------------------------------------------------ #
    SEE_ASSETS = "see_assets"

    # ------------------------------------------------------------------ #
    # Blocks
    # ------------------------------------------------------------------ #
    SEE_BLOCKS = "see_blocks"
    MANAGE_BLOCKS = "manage_blocks"

    # ------------------------------------------------------------------ #
    # Variables
    # ------------------------------------------------------------------ #
    SEE_VARIABLES = "see_variables"
    WRITE_VARIABLES = "write_variables"
    MANAGE_VARIABLES = "manage_variables"

    # ------------------------------------------------------------------ #
    # Concurrency Limits
    # ------------------------------------------------------------------ #
    SEE_CONCURRENCY_LIMITS = "see_concurrency_limits"
    MANAGE_CONCURRENCY_LIMITS = "manage_concurrency_limits"

    # ------------------------------------------------------------------ #
    # Automations
    # ------------------------------------------------------------------ #
    SEE_AUTOMATIONS = "see_automations"
    MANAGE_AUTOMATIONS = "manage_automations"

    # ------------------------------------------------------------------ #
    # Saved Searches
    # ------------------------------------------------------------------ #
    MANAGE_SAVED_SEARCH = "manage_saved_search"

    # ------------------------------------------------------------------ #
    # Workspace Settings
    # ------------------------------------------------------------------ #
    SEE_WORKSPACE_SETTINGS = "see_workspace_settings"
    WRITE_WORKSPACE_SETTINGS = "write_workspace_settings"

    # ------------------------------------------------------------------ #
    # Workspace Users & Teams
    # ------------------------------------------------------------------ #
    SEE_WORKSPACE_USERS = "see_workspace_users"
    MANAGE_WORKSPACE_USERS = "manage_workspace_users"
    MANAGE_WORKSPACE_TEAMS = "manage_workspace_teams"

    # ------------------------------------------------------------------ #
    # RBAC administration
    # ------------------------------------------------------------------ #
    MANAGE_ACCOUNTS = "manage_accounts"
    MANAGE_ROLES = "manage_roles"

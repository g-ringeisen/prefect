from prefect.server.rbac.scopes import Scope

GUID = "__GUID__"
MGET = "__GET__"
MPOST = "__POST__"
MPUT = "__PUT__"
MPATCH = "__PATCH__"
MDELETE = "__DELETE__"

_route_tree = {
    "health": {
        MGET: [],
    },
    "hello": {
        MGET: [],
    },
    "version": {
        MGET: [],
    },
    "ready": {
        MGET: [],
    },
    "csrf-token": {
        MGET: [],
    },
    "me": {
        MGET: ["authenticated"],
    },
    "accounts": {
        GUID: {
            "roles": {
                GUID: {
                    MPOST: [Scope.MANAGE_ACCOUNTS],
                    MDELETE: [Scope.MANAGE_ACCOUNTS],
                },
                MGET: [Scope.MANAGE_ACCOUNTS],
            },
            MGET: [Scope.MANAGE_ACCOUNTS],
            MPATCH: [Scope.MANAGE_ACCOUNTS],
            MDELETE: [Scope.MANAGE_ACCOUNTS],
        },
        MGET: [Scope.MANAGE_ACCOUNTS],
        MPOST: [Scope.MANAGE_ACCOUNTS],
    },
    "roles": {
        GUID: {
            "scopes": {
                MPOST: [Scope.MANAGE_ROLES],
            },
            MGET: [Scope.MANAGE_ROLES],
            MPATCH: [Scope.MANAGE_ROLES],
            MDELETE: [Scope.MANAGE_ROLES],
        },
        MGET: [Scope.MANAGE_ROLES],
        MPOST: [Scope.MANAGE_ROLES],
    },
    "artifacts": {
        "count": {
            MPOST: [Scope.SEE_ARTIFACTS],
        },
        "filter": {
            MPOST: [Scope.SEE_ARTIFACTS],
        },
        "latest": {
            "count": {
                MPOST: [Scope.SEE_ARTIFACTS],
            },
            "filter": {
                MPOST: [Scope.SEE_ARTIFACTS],
            },
        },
        GUID: {
            "latest": {
                MGET: [Scope.SEE_ARTIFACTS],
            },
            MDELETE: [Scope.MANAGE_ARTIFACTS],
            MGET: [Scope.SEE_ARTIFACTS],
            MPATCH: [Scope.WRITE_ARTIFACTS],
        },
        MPOST: [Scope.WRITE_ARTIFACTS],
    },
    "block_capabilities": {
        MGET: [Scope.SEE_BLOCKS],
    },
    "block_documents": {
        "count": {
            MPOST: [Scope.SEE_BLOCKS],
        },
        "filter": {
            MPOST: [Scope.SEE_BLOCKS],
        },
        "my-access": {
            MPOST: [Scope.SEE_BLOCKS],
        },
        GUID: {
            "access": {
                MGET: [Scope.SEE_BLOCKS],
                MPUT: [Scope.MANAGE_BLOCKS],
            },
            MDELETE: [Scope.MANAGE_BLOCKS],
            MGET: [Scope.SEE_BLOCKS],
            MPATCH: [Scope.MANAGE_BLOCKS],
        },
        MPOST: [Scope.MANAGE_BLOCKS],
        MPUT: [Scope.MANAGE_BLOCKS],
    },
    "block_schemas": {
        "checksum": {
            GUID: {
                MGET: [Scope.SEE_BLOCKS],
            },
        },
        "filter": {
            MPOST: [Scope.SEE_BLOCKS],
        },
        GUID: {
            MDELETE: [Scope.MANAGE_BLOCKS],
            MGET: [Scope.SEE_BLOCKS],
        },
        MPOST: [Scope.MANAGE_BLOCKS],
    },
    "block_types": {
        "filter": {
            MPOST: [Scope.SEE_BLOCKS],
        },
        "install_system_block_types": {
            MPOST: [Scope.MANAGE_BLOCKS],
        },
        "slug": {
            GUID: {
                "block_documents": {
                    "name": {
                        GUID: {
                            MGET: [Scope.SEE_BLOCKS],
                        },
                    },
                    MGET: [Scope.SEE_BLOCKS],
                },
                MGET: [Scope.SEE_BLOCKS],
            },
        },
        GUID: {
            MDELETE: [Scope.MANAGE_BLOCKS],
            MGET: [Scope.SEE_BLOCKS],
            MPATCH: [Scope.MANAGE_BLOCKS],
        },
        MPOST: [Scope.MANAGE_BLOCKS],
    },
    "collections": {
        "work_pool_types": {
            MGET: [Scope.SEE_WORK_POOLS],
        },
    },
    "concurrency_limits": {
        "decrement": {
            MPOST: [Scope.RUN_FLOWS],
        },
        "filter": {
            MPOST: [Scope.SEE_CONCURRENCY_LIMITS],
        },
        "increment": {
            MPOST: [Scope.RUN_FLOWS],
        },
        "tag": {
            GUID: {
                "reset": {
                    MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
                },
                MDELETE: [Scope.MANAGE_CONCURRENCY_LIMITS],
                MGET: [Scope.SEE_CONCURRENCY_LIMITS],
            },
        },
        GUID: {
            MDELETE: [Scope.MANAGE_CONCURRENCY_LIMITS],
            MGET: [Scope.SEE_CONCURRENCY_LIMITS],
        },
        MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
    },
    "deployments": {
        "bulk_delete": {
            MPOST: [Scope.MANAGE_DEPLOYMENTS],
        },
        "count": {
            MPOST: [Scope.SEE_DEPLOYMENTS],
        },
        "filter": {
            MPOST: [Scope.SEE_DEPLOYMENTS],
        },
        "get_scheduled_flow_runs": {
            MPOST: [Scope.SEE_DEPLOYMENTS],
        },
        "my-access": {
            MPOST: [Scope.SEE_DEPLOYMENTS],
        },
        "name": {
            GUID: {
                GUID: {
                    MGET: [Scope.SEE_DEPLOYMENTS],
                },
            },
        },
        "paginate": {
            MPOST: [Scope.SEE_DEPLOYMENTS],
        },
        GUID: {
            "access": {
                MGET: [Scope.SEE_DEPLOYMENTS],
                MPUT: [Scope.MANAGE_DEPLOYMENTS],
            },
            "branch": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "create_flow_run": {
                "bulk": {
                    MPOST: [Scope.RUN_DEPLOYMENTS],
                },
                MPOST: [Scope.RUN_DEPLOYMENTS],
            },
            "disable": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "enable": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "pause_deployment": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "resume_deployment": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "schedule": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "schedules": {
                GUID: {
                    MDELETE: [Scope.WRITE_DEPLOYMENTS],
                    MPATCH: [Scope.WRITE_DEPLOYMENTS],
                },
                MGET: [Scope.SEE_DEPLOYMENTS],
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "set_schedule_active": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "set_schedule_inactive": {
                MPOST: [Scope.WRITE_DEPLOYMENTS],
            },
            "versions": {
                "paginate": {
                    MPOST: [Scope.SEE_DEPLOYMENTS],
                },
                GUID: {
                    "promote": {
                        MPOST: [Scope.MANAGE_DEPLOYMENTS],
                    },
                    MDELETE: [Scope.MANAGE_DEPLOYMENTS],
                    MGET: [Scope.SEE_DEPLOYMENTS],
                },
            },
            "work_queue_check": {
                MGET: [],
            },
            MDELETE: [Scope.MANAGE_DEPLOYMENTS],
            MGET: [Scope.SEE_DEPLOYMENTS],
            MPATCH: [Scope.WRITE_DEPLOYMENTS],
        },
        MPOST: [Scope.WRITE_DEPLOYMENTS],
    },
    "event-publications": {
        GUID: {
            "subscriptions": {
                MGET: [],
            },
            MDELETE: [],
            MGET: [],
            MPATCH: [],
        },
        MGET: [],
        MPOST: [],
    },
    "event-subscriptions": {
        GUID: {
            MDELETE: [],
            MGET: [],
            MPATCH: [],
        },
        MGET: [],
        MPOST: [],
    },
    "events": {
        "count-by": {
            GUID: {
                MPOST: [],
            },
        },
        "filter": {
            "next": {
                MGET: [],
            },
            MPOST: [],
        },
        MPOST: [],
    },
    "execution-plans": {
        "schema": {
            MGET: [],
        },
    },
    "flow_run_states": {
        GUID: {
            MGET: [Scope.SEE_FLOWS],
        },
        MGET: [Scope.SEE_FLOWS],
    },
    "flow_runs": {
        "bulk_delete": {
            MPOST: [Scope.MANAGE_FLOWS],
        },
        "bulk_set_state": {
            MPOST: [Scope.RUN_FLOWS],
        },
        "count": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "filter-minimal": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "history": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "lateness": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "paginate": {
            MPOST: [Scope.SEE_FLOWS],
        },
        GUID: {
            "artifacts": {
                MGET: [Scope.SEE_FLOWS],
            },
            "assets": {
                "materializations": {
                    MGET: [Scope.SEE_ASSETS],
                },
                "references": {
                    MGET: [Scope.SEE_ASSETS],
                },
            },
            "download-logs-csv": {
                MGET: [Scope.SEE_FLOWS],
            },
            "events": {
                MGET: [],
            },
            "graph": {
                MGET: [Scope.SEE_FLOWS],
            },
            "graph-v2": {
                MGET: [Scope.SEE_FLOWS],
            },
            "input": {
                "filter": {
                    MPOST: [Scope.SEE_FLOWS],
                },
                GUID: {
                    MDELETE: [Scope.MANAGE_FLOWS],
                    MGET: [Scope.SEE_FLOWS],
                },
                MPOST: [Scope.RUN_FLOWS],
            },
            "labels": {
                MPATCH: [Scope.RUN_FLOWS],
            },
            "logs": {
                "download": {
                    MGET: [Scope.SEE_FLOWS],
                },
                MGET: [Scope.SEE_FLOWS],
            },
            "resume": {
                MPOST: [Scope.RUN_FLOWS],
            },
            "set_state": {
                MPOST: [Scope.RUN_FLOWS],
            },
            MDELETE: [Scope.MANAGE_FLOWS],
            MGET: [Scope.SEE_FLOWS],
            MPATCH: [Scope.RUN_FLOWS],
        },
        MPOST: [Scope.RUN_FLOWS],
    },
    "flows": {
        "bulk_delete": {
            MPOST: [Scope.MANAGE_FLOWS],
        },
        "count": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "name": {
            GUID: {
                MGET: [Scope.SEE_FLOWS],
            },
        },
        "paginate": {
            MPOST: [Scope.SEE_FLOWS],
        },
        GUID: {
            MDELETE: [Scope.MANAGE_FLOWS],
            MGET: [Scope.SEE_FLOWS],
            MPATCH: [Scope.RUN_FLOWS],
        },
        MPOST: [Scope.RUN_FLOWS],
    },
    "logs": {
        "ai": {
            "flow_run_logs": {
                GUID: {
                    MGET: [Scope.SEE_FLOWS],
                },
            },
        },
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        MPOST: [Scope.RUN_FLOWS],
    },
    "metrics": {
        "deployments": {
            GUID: {
                "resource-peaks": {
                    MGET: [Scope.SEE_DEPLOYMENTS],
                },
            },
        },
        "flow-runs": {
            GUID: {
                "names": {
                    MGET: [Scope.SEE_FLOWS],
                },
                MGET: [Scope.SEE_FLOWS],
            },
        },
    },
    "observed-loggers": {
        MGET: [Scope.SEE_FLOWS],
    },
    "observed-states": {
        MGET: [Scope.SEE_FLOWS],
    },
    "pins": {
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        GUID: {
            MDELETE: [Scope.SEE_FLOWS],
        },
        MPOST: [Scope.SEE_FLOWS],
    },
    "saved_searches": {
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        GUID: {
            MDELETE: [Scope.MANAGE_SAVED_SEARCH],
            MGET: [Scope.SEE_FLOWS],
        },
        MPUT: [Scope.MANAGE_SAVED_SEARCH],
    },
    "settings": {
        MGET: [Scope.SEE_WORKSPACE_SETTINGS],
        MPATCH: [Scope.WRITE_WORKSPACE_SETTINGS],
    },
    "spans": {
        "lookup": {
            GUID: {
                MGET: [Scope.SEE_FLOWS],
            },
        },
        GUID: {
            "observed-tags": {
                MGET: [Scope.SEE_FLOWS],
            },
        },
    },
    "task_run_states": {
        GUID: {
            MGET: [Scope.SEE_FLOWS],
        },
        MGET: [Scope.SEE_FLOWS],
    },
    "task_runs": {
        "count": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "filter": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "history": {
            MPOST: [Scope.SEE_FLOWS],
        },
        "paginate": {
            MPOST: [Scope.SEE_FLOWS],
        },
        GUID: {
            "artifacts": {
                MGET: [Scope.SEE_FLOWS],
            },
            "assets": {
                "materializations": {
                    MGET: [Scope.SEE_ASSETS],
                },
                "references": {
                    MGET: [Scope.SEE_ASSETS],
                },
            },
            "set_state": {
                MPOST: [Scope.RUN_FLOWS],
            },
            MDELETE: [Scope.MANAGE_FLOWS],
            MGET: [Scope.SEE_FLOWS],
            MPATCH: [Scope.RUN_FLOWS],
        },
        MPOST: [Scope.RUN_FLOWS],
    },
    "task_workers": {
        "filter": {
            MPOST: [Scope.SEE_WORKERS],
        },
    },
    "team_access": {
        "filter": {
            MPOST: [Scope.MANAGE_WORKSPACE_TEAMS],
        },
        GUID: {
            MDELETE: [Scope.MANAGE_WORKSPACE_TEAMS],
        },
        MPUT: [Scope.MANAGE_WORKSPACE_TEAMS],
    },
    "traces": {
        GUID: {
            "context": {
                GUID: {
                    MGET: [Scope.SEE_FLOWS],
                },
            },
            "observed-loggers": {
                MGET: [Scope.SEE_FLOWS],
            },
            "observed-states": {
                MGET: [Scope.SEE_FLOWS],
            },
            "observed-tags": {
                MGET: [Scope.SEE_FLOWS],
            },
            "spans": {
                GUID: {
                    MGET: [Scope.SEE_FLOWS],
                },
                MGET: [Scope.SEE_FLOWS],
            },
            MGET: [Scope.SEE_FLOWS],
        },
    },
    "ui": {
        "flow_runs": {
            "count-task-runs": {
                MPOST: [Scope.SEE_FLOWS],
            },
            "history": {
                MPOST: [Scope.SEE_FLOWS],
            },
            "history-v2": {
                MPOST: [Scope.SEE_FLOWS],
            },
        },
        "flows": {
            "count-deployments": {
                MPOST: [Scope.SEE_FLOWS],
            },
            "next-runs": {
                MPOST: [Scope.SEE_FLOWS],
            },
        },
        "metrics": {
            "prefect": {
                GUID: {
                    "grouped": {
                        MPOST: [],
                    },
                    "timeseries": {
                        MPOST: [],
                    },
                    MPOST: [],
                },
            },
        },
        "schemas": {
            "validate": {
                MPOST: [],
            }
        },
        "task_runs": {
            "count": {
                MPOST: [Scope.SEE_FLOWS],
            },
            "dashboard": {
                "counts": {
                    MPOST: [Scope.SEE_FLOWS],
                },
            },
        },
        "work_pools": {
            "count-flow-runs": {
                MPOST: [Scope.SEE_FLOWS],
            },
        },
    },
    "user_access": {
        "filter": {
            MPOST: [Scope.SEE_WORKSPACE_USERS],
        },
        GUID: {
            MDELETE: [Scope.MANAGE_WORKSPACE_USERS],
            MGET: [Scope.SEE_WORKSPACE_USERS],
        },
        MPOST: [Scope.MANAGE_WORKSPACE_USERS],
    },
    "v2": {
        "concurrency_limits": {
            "decrement": {
                MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
            },
            "decrement-with-lease": {
                MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
            },
            "filter": {
                MPOST: [Scope.SEE_CONCURRENCY_LIMITS],
            },
            "increment": {
                MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
            },
            "increment-with-lease": {
                MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
            },
            "leases": {
                GUID: {
                    "renew": {
                        MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
                    },
                },
            },
            "paginate": {
                MPOST: [Scope.SEE_CONCURRENCY_LIMITS],
            },
            GUID: {
                MDELETE: [Scope.MANAGE_CONCURRENCY_LIMITS],
                MGET: [Scope.SEE_CONCURRENCY_LIMITS],
                MPATCH: [Scope.MANAGE_CONCURRENCY_LIMITS],
            },
            MPOST: [Scope.MANAGE_CONCURRENCY_LIMITS],
        },
    },
    "variables": {
        "count": {
            MPOST: [Scope.SEE_VARIABLES],
        },
        "filter": {
            MPOST: [Scope.SEE_VARIABLES],
        },
        "name": {
            GUID: {
                MDELETE: [Scope.MANAGE_VARIABLES],
                MGET: [Scope.SEE_VARIABLES],
                MPATCH: [Scope.WRITE_VARIABLES],
            },
        },
        GUID: {
            MDELETE: [Scope.MANAGE_VARIABLES],
            MGET: [Scope.SEE_VARIABLES],
            MPATCH: [Scope.WRITE_VARIABLES],
        },
        MPOST: [Scope.WRITE_VARIABLES],
    },
    "work_pools": {
        "configuration": {
            "preview": {
                MPOST: [],
            },
        },
        "count": {
            MPOST: [Scope.SEE_WORK_POOLS],
        },
        "filter": {
            MPOST: [Scope.SEE_WORK_POOLS],
        },
        "my-access": {
            MPOST: [Scope.SEE_WORK_POOLS],
        },
        "paginate": {
            MPOST: [Scope.SEE_WORK_POOLS],
        },
        GUID: {
            "access": {
                MGET: [Scope.SEE_WORK_POOLS],
                MPUT: [Scope.MANAGE_WORK_POOLS],
            },
            "concurrency_status": {
                MPOST: [Scope.SEE_WORK_POOLS, Scope.SEE_WORK_QUEUES],
            },
            "get_scheduled_flow_runs": {
                MPOST: [Scope.SEE_WORK_QUEUES],
            },
            "queues": {
                "filter": {
                    MPOST: [Scope.SEE_WORK_QUEUES],
                },
                "paginate": {
                    MPOST: [Scope.SEE_WORK_QUEUES],
                },
                GUID: {
                    MDELETE: [Scope.MANAGE_WORK_QUEUES],
                    MGET: [Scope.SEE_WORK_QUEUES],
                    MPATCH: [Scope.WRITE_WORK_QUEUES],
                },
                MPOST: [Scope.WRITE_WORK_QUEUES],
            },
            "workers": {
                "filter": {
                    MPOST: [Scope.SEE_WORKERS],
                },
                "heartbeat": {
                    MPOST: [Scope.WRITE_WORKERS],
                },
                "paginate": {
                    MPOST: [Scope.SEE_WORKERS],
                },
                GUID: {
                    MDELETE: [Scope.MANAGE_WORKERS],
                    MGET: [Scope.SEE_WORKERS],
                },
            },
            MDELETE: [Scope.MANAGE_WORK_POOLS],
            MGET: [Scope.SEE_WORK_POOLS],
            MPATCH: [Scope.WRITE_WORK_POOLS],
        },
        MPOST: [Scope.WRITE_WORK_POOLS],
    },
    "work_queues": {
        "filter": {
            MPOST: [Scope.SEE_WORK_QUEUES],
        },
        "name": {
            GUID: {
                MGET: [Scope.SEE_WORK_QUEUES],
            },
        },
        "paginate": {
            MPOST: [Scope.SEE_WORK_QUEUES],
        },
        GUID: {
            "concurrency_status": {
                MPOST: [Scope.SEE_WORK_QUEUES],
            },
            "get_runs": {
                MPOST: [Scope.SEE_WORK_QUEUES],
            },
            "status": {
                MGET: [Scope.SEE_WORK_QUEUES],
            },
            MDELETE: [Scope.MANAGE_WORK_QUEUES],
            MGET: [Scope.SEE_WORK_QUEUES],
            MPATCH: [Scope.WRITE_WORK_QUEUES],
        },
        MPOST: [Scope.WRITE_WORK_QUEUES],
    },
}


def resolve_api_scope(path: str, method: str = "get") -> list[str]:

    def _match(node: dict, segments: list[str], method: str, idx) -> list[str]:
        if idx == len(segments):
            return node.get(f"__{method.upper()}__", None)

        seg = segments[idx]
        # Priorité au match statique (évite qu'un wildcard "vole" une route plus précise)
        if seg in node:
            return _match(node[seg], segments, method, idx + 1)
        # Sinon on tente le wildcard
        elif GUID in node:
            return _match(node[GUID], segments, method, idx + 1)
        # Pour finir, on renvoi None si le chemin n'existe pas dans l'arbre
        return None

    segments = [s for s in path.split("/") if s]
    scopes = _match(_route_tree, segments, method, 0)
    return scopes if scopes is not None else ["admin"]

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
    "artifacts": {
        "count": {
            MPOST: ["see_artifacts"],
        },
        "filter": {
            MPOST: ["see_artifacts"],
        },
        "latest": {
            "count": {
                MPOST: ["see_artifacts"],
            },
            "filter": {
                MPOST: ["see_artifacts"],
            },
        },
        GUID: {
            "latest": {
                MGET: ["see_artifacts"],
            },
            MDELETE: ["manage_artifacts"],
            MGET: ["see_artifacts"],
            MPATCH: ["write_artifacts"],
        },
        MPOST: ["write_artifacts"],
    },
    "block_capabilities": {
        MGET: ["see_blocks"],
    },
    "block_documents": {
        "count": {
            MPOST: ["see_blocks"],
        },
        "filter": {
            MPOST: ["see_blocks"],
        },
        "my-access": {
            MPOST: ["see_blocks"],
        },
        GUID: {
            "access": {
                MGET: ["see_blocks"],
                MPUT: ["manage_blocks"],
            },
            MDELETE: ["manage_blocks"],
            MGET: ["see_blocks"],
            MPATCH: ["manage_blocks"],
        },
        MPOST: ["manage_blocks"],
        MPUT: ["manage_blocks"],
    },
    "block_schemas": {
        "checksum": {
            GUID: {
                MGET: ["see_blocks"],
            },
        },
        "filter": {
            MPOST: ["see_blocks"],
        },
        GUID: {
            MDELETE: ["manage_blocks"],
            MGET: ["see_blocks"],
        },
        MPOST: ["manage_blocks"],
    },
    "block_types": {
        "filter": {
            MPOST: ["see_blocks"],
        },
        "install_system_block_types": {
            MPOST: ["manage_blocks"],
        },
        "slug": {
            GUID: {
                "block_documents": {
                    "name": {
                        GUID: {
                            MGET: ["see_blocks"],
                        },
                    },
                    MGET: ["see_blocks"],
                },
                MGET: ["see_blocks"],
            },
        },
        GUID: {
            MDELETE: ["manage_blocks"],
            MGET: ["see_blocks"],
            MPATCH: ["manage_blocks"],
        },
        MPOST: ["manage_blocks"],
    },
    "collections": {
        "work_pool_types": {
            MGET: ["see_work_pools"],
        },
    },
    "concurrency_limits": {
        "decrement": {
            MPOST: ["run_flows"],
        },
        "filter": {
            MPOST: ["see_concurrency_limits"],
        },
        "increment": {
            MPOST: ["run_flows"],
        },
        "tag": {
            GUID: {
                "reset": {
                    MPOST: ["manage_concurrency_limits"],
                },
                MDELETE: ["manage_concurrency_limits"],
                MGET: ["see_concurrency_limits"],
            },
        },
        GUID: {
            MDELETE: ["manage_concurrency_limits"],
            MGET: ["see_concurrency_limits"],
        },
        MPOST: ["manage_concurrency_limits"],
    },
    "deployments": {
        "bulk_delete": {
            MPOST: ["manage_deployments"],
        },
        "count": {
            MPOST: ["see_deployments"],
        },
        "filter": {
            MPOST: ["see_deployments"],
        },
        "get_scheduled_flow_runs": {
            MPOST: ["see_deployments"],
        },
        "my-access": {
            MPOST: ["see_deployments"],
        },
        "name": {
            GUID: {
                GUID: {
                    MGET: ["see_deployments"],
                },
            },
        },
        "paginate": {
            MPOST: ["see_deployments"],
        },
        GUID: {
            "access": {
                MGET: ["see_deployments"],
                MPUT: ["manage_deployments"],
            },
            "branch": {
                MPOST: ["write_deployments"],
            },
            "create_flow_run": {
                "bulk": {
                    MPOST: ["run_deployments"],
                },
                MPOST: ["run_deployments"],
            },
            "disable": {
                MPOST: ["write_deployments"],
            },
            "enable": {
                MPOST: ["write_deployments"],
            },
            "pause_deployment": {
                MPOST: ["write_deployments"],
            },
            "resume_deployment": {
                MPOST: ["write_deployments"],
            },
            "schedule": {
                MPOST: ["write_deployments"],
            },
            "schedules": {
                GUID: {
                    MDELETE: ["write_deployments"],
                    MPATCH: ["write_deployments"],
                },
                MGET: ["see_deployments"],
                MPOST: ["write_deployments"],
            },
            "set_schedule_active": {
                MPOST: ["write_deployments"],
            },
            "set_schedule_inactive": {
                MPOST: ["write_deployments"],
            },
            "versions": {
                "paginate": {
                    MPOST: ["see_deployments"],
                },
                GUID: {
                    "promote": {
                        MPOST: ["manage_deployments"],
                    },
                    MDELETE: ["manage_deployments"],
                    MGET: ["see_deployments"],
                },
            },
            "work_queue_check": {
                MGET: [],
            },
            MDELETE: ["manage_deployments"],
            MGET: ["see_deployments"],
            MPATCH: ["write_deployments"],
        },
        MPOST: ["write_deployments"],
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
            MGET: ["see_flows"],
        },
        MGET: ["see_flows"],
    },
    "flow_runs": {
        "bulk_delete": {
            MPOST: ["manage_flows"],
        },
        "bulk_set_state": {
            MPOST: ["run_flows"],
        },
        "count": {
            MPOST: ["see_flows"],
        },
        "filter": {
            MPOST: ["see_flows"],
        },
        "filter-minimal": {
            MPOST: ["see_flows"],
        },
        "history": {
            MPOST: ["see_flows"],
        },
        "lateness": {
            MPOST: ["see_flows"],
        },
        "paginate": {
            MPOST: ["see_flows"],
        },
        GUID: {
            "artifacts": {
                MGET: ["see_flows"],
            },
            "assets": {
                "materializations": {
                    MGET: ["see_assets"],
                },
                "references": {
                    MGET: ["see_assets"],
                },
            },
            "download-logs-csv": {
                MGET: ["see_flows"],
            },
            "events": {
                MGET: [],
            },
            "graph": {
                MGET: ["see_flows"],
            },
            "graph-v2": {
                MGET: ["see_flows"],
            },
            "input": {
                "filter": {
                    MPOST: ["see_flows"],
                },
                GUID: {
                    MDELETE: ["manage_flows"],
                    MGET: ["see_flows"],
                },
                MPOST: ["run_flows"],
            },
            "labels": {
                MPATCH: ["run_flows"],
            },
            "logs": {
                "download": {
                    MGET: ["see_flows"],
                },
                MGET: ["see_flows"],
            },
            "resume": {
                MPOST: ["run_flows"],
            },
            "set_state": {
                MPOST: ["run_flows"],
            },
            MDELETE: ["manage_flows"],
            MGET: ["see_flows"],
            MPATCH: ["run_flows"],
        },
        MPOST: ["run_flows"],
    },
    "flows": {
        "bulk_delete": {
            MPOST: ["manage_flows"],
        },
        "count": {
            MPOST: ["see_flows"],
        },
        "filter": {
            MPOST: ["see_flows"],
        },
        "name": {
            GUID: {
                MGET: ["see_flows"],
            },
        },
        "paginate": {
            MPOST: ["see_flows"],
        },
        GUID: {
            MDELETE: ["manage_flows"],
            MGET: ["see_flows"],
            MPATCH: ["run_flows"],
        },
        MPOST: ["run_flows"],
    },
    "logs": {
        "ai": {
            "flow_run_logs": {
                GUID: {
                    MGET: ["see_flows"],
                },
            },
        },
        "filter": {
            MPOST: ["see_flows"],
        },
        MPOST: ["run_flows"],
    },
    "metrics": {
        "deployments": {
            GUID: {
                "resource-peaks": {
                    MGET: ["see_deployments"],
                },
            },
        },
        "flow-runs": {
            GUID: {
                "names": {
                    MGET: ["see_flows"],
                },
                MGET: ["see_flows"],
            },
        },
    },
    "observed-loggers": {
        MGET: ["see_flows"],
    },
    "observed-states": {
        MGET: ["see_flows"],
    },
    "pins": {
        "filter": {
            MPOST: ["see_flows"],
        },
        GUID: {
            MDELETE: ["see_flows"],
        },
        MPOST: ["see_flows"],
    },
    "saved_searches": {
        "filter": {
            MPOST: ["see_flows"],
        },
        GUID: {
            MDELETE: ["manage_saved_search"],
            MGET: ["see_flows"],
        },
        MPUT: ["manage_saved_search"],
    },
    "settings": {
        MGET: ["see_workspace_settings"],
        MPATCH: ["write_workspace_settings"],
    },
    "spans": {
        "lookup": {
            GUID: {
                MGET: ["see_flows"],
            },
        },
        GUID: {
            "observed-tags": {
                MGET: ["see_flows"],
            },
        },
    },
    "task_run_states": {
        GUID: {
            MGET: ["see_flows"],
        },
        MGET: ["see_flows"],
    },
    "task_runs": {
        "count": {
            MPOST: ["see_flows"],
        },
        "filter": {
            MPOST: ["see_flows"],
        },
        "history": {
            MPOST: ["see_flows"],
        },
        "paginate": {
            MPOST: ["see_flows"],
        },
        GUID: {
            "artifacts": {
                MGET: ["see_flows"],
            },
            "assets": {
                "materializations": {
                    MGET: ["see_assets"],
                },
                "references": {
                    MGET: ["see_assets"],
                },
            },
            "set_state": {
                MPOST: ["run_flows"],
            },
            MDELETE: ["manage_flows"],
            MGET: ["see_flows"],
            MPATCH: ["run_flows"],
        },
        MPOST: ["run_flows"],
    },
    "task_workers": {
        "filter": {
            MPOST: ["see_workers"],
        },
    },
    "team_access": {
        "filter": {
            MPOST: ["manage_workspace_teams"],
        },
        GUID: {
            MDELETE: ["manage_workspace_teams"],
        },
        MPUT: ["manage_workspace_teams"],
    },
    "traces": {
        GUID: {
            "context": {
                GUID: {
                    MGET: ["see_flows"],
                },
            },
            "observed-loggers": {
                MGET: ["see_flows"],
            },
            "observed-states": {
                MGET: ["see_flows"],
            },
            "observed-tags": {
                MGET: ["see_flows"],
            },
            "spans": {
                GUID: {
                    MGET: ["see_flows"],
                },
                MGET: ["see_flows"],
            },
            MGET: ["see_flows"],
        },
    },
    "ui": {
        "flow_runs": {
            "count-task-runs": {
                MPOST: ["see_flows"],
            },
            "history": {
                MPOST: ["see_flows"],
            },
            "history-v2": {
                MPOST: ["see_flows"],
            },
        },
        "flows": {
            "count-deployments": {
                MPOST: ["see_flows"],
            },
            "next-runs": {
                MPOST: ["see_flows"],
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
                MPOST: ["see_flows"],
            },
            "dashboard": {
                "counts": {
                    MPOST: ["see_flows"],
                },
            },
        },
        "work_pools": {
            "count-flow-runs": {
                MPOST: ["see_flows"],
            },
        },
    },
    "user_access": {
        "filter": {
            MPOST: ["see_workspace_users"],
        },
        GUID: {
            MDELETE: ["manage_workspace_users"],
            MGET: ["see_workspace_users"],
        },
        MPOST: ["manage_workspace_users"],
    },
    "v2": {
        "concurrency_limits": {
            "decrement": {
                MPOST: ["manage_concurrency_limits"],
            },
            "decrement-with-lease": {
                MPOST: ["manage_concurrency_limits"],
            },
            "filter": {
                MPOST: ["see_concurrency_limits"],
            },
            "increment": {
                MPOST: ["manage_concurrency_limits"],
            },
            "increment-with-lease": {
                MPOST: ["manage_concurrency_limits"],
            },
            "leases": {
                GUID: {
                    "renew": {
                        MPOST: ["manage_concurrency_limits"],
                    },
                },
            },
            "paginate": {
                MPOST: ["see_concurrency_limits"],
            },
            GUID: {
                MDELETE: ["manage_concurrency_limits"],
                MGET: ["see_concurrency_limits"],
                MPATCH: ["manage_concurrency_limits"],
            },
            MPOST: ["manage_concurrency_limits"],
        },
    },
    "variables": {
        "count": {
            MPOST: ["see_variables"],
        },
        "filter": {
            MPOST: ["see_variables"],
        },
        "name": {
            GUID: {
                MDELETE: ["manage_variables"],
                MGET: ["see_variables"],
                MPATCH: ["write_variables"],
            },
        },
        GUID: {
            MDELETE: ["manage_variables"],
            MGET: ["see_variables"],
            MPATCH: ["write_variables"],
        },
        MPOST: ["write_variables"],
    },
    "work_pools": {
        "configuration": {
            "preview": {
                MPOST: [],
            },
        },
        "count": {
            MPOST: ["see_work_pools"],
        },
        "filter": {
            MPOST: ["see_work_pools"],
        },
        "my-access": {
            MPOST: ["see_work_pools"],
        },
        "paginate": {
            MPOST: ["see_work_pools"],
        },
        GUID: {
            "access": {
                MGET: ["see_work_pools"],
                MPUT: ["manage_work_pools"],
            },
            "concurrency_status": {
                MPOST: ["see_work_pools", "see_work_queues"],
            },
            "get_scheduled_flow_runs": {
                MPOST: ["see_work_queues"],
            },
            "queues": {
                "filter": {
                    MPOST: ["see_work_queues"],
                },
                "paginate": {
                    MPOST: ["see_work_queues"],
                },
                GUID: {
                    MDELETE: ["manage_work_queues"],
                    MGET: ["see_work_queues"],
                    MPATCH: ["write_work_queues"],
                },
                MPOST: ["write_work_queues"],
            },
            "workers": {
                "filter": {
                    MPOST: ["see_workers"],
                },
                "heartbeat": {
                    MPOST: ["write_workers"],
                },
                "paginate": {
                    MPOST: ["see_workers"],
                },
                GUID: {
                    MDELETE: ["manage_workers"],
                    MGET: ["see_workers"],
                },
            },
            MDELETE: ["manage_work_pools"],
            MGET: ["see_work_pools"],
            MPATCH: ["write_work_pools"],
        },
        MPOST: ["write_work_pools"],
    },
    "work_queues": {
        "filter": {
            MPOST: ["see_work_queues"],
        },
        "name": {
            GUID: {
                MGET: ["see_work_queues"],
            },
        },
        "paginate": {
            MPOST: ["see_work_queues"],
        },
        GUID: {
            "concurrency_status": {
                MPOST: ["see_work_queues"],
            },
            "get_runs": {
                MPOST: ["see_work_queues"],
            },
            "status": {
                MGET: ["see_work_queues"],
            },
            MDELETE: ["manage_work_queues"],
            MGET: ["see_work_queues"],
            MPATCH: ["write_work_queues"],
        },
        MPOST: ["write_work_queues"],
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

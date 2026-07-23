from prefect.authorizations import resolve_api_scope


def test_existing_static_api_path():
    assert resolve_api_scope("/artifacts/latest/count", "POST") == ["see_artifacts"]
    assert resolve_api_scope("/artifacts/latest/count/", "POST") == ["see_artifacts"]


def test_existing_static_api_path_with_wrong_method():
    assert resolve_api_scope("/artifacts/latest/count", "GET") == ["admin"]


def test_non_existing_static_api_path():
    assert resolve_api_scope("/artifacts/fake/path", "POST") == ["admin"]


def test_existing_dynamic_api_path():
    assert resolve_api_scope(
        "/deployments/abcd-1234-efgh/schedules/5678-ijkl-0123", "PATCH"
    ) == ["write_deployments"]
    assert resolve_api_scope(
        "/deployments/abcd-1234-efgh/schedules/5678-ijkl-0123/", "PATCH"
    ) == ["write_deployments"]


def test_existing_dynamic_api_path_with_wrong_method():
    assert resolve_api_scope(
        "/deployments/abcd-1234-efgh/schedules/5678-ijkl-0123", "GET"
    ) == ["admin"]


def test_non_existing_dynamic_api_path():
    assert resolve_api_scope(
        "/deployments/abcd-1234-efgh/fake/5678-ijkl-0123", "PATCH"
    ) == ["admin"]


def test_public_path():
    assert resolve_api_scope("/health", "GET") == []
    assert resolve_api_scope("/ui/schemas/validate", "POST") == []

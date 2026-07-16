"""スモークテスト: 骨組みが壊れていないことの最低確認。

Claude Code はここにテストを足していく。
"""
from fastapi.testclient import TestClient

from app.main import app
from app.core.states import ProjectState, can_transition

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_project():
    r = client.post("/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"})
    assert r.status_code == 201
    pid = r.json()["project_id"]
    assert r.json()["state"] == ProjectState.CREATED

    r2 = client.get(f"/api/v1/projects/{pid}")
    assert r2.status_code == 200


def test_state_machine_rejects_illegal():
    # created から done へ直接飛ぶ遷移は許可されない
    assert not can_transition(ProjectState.CREATED, ProjectState.DONE)
    assert can_transition(ProjectState.CREATED, ProjectState.INTAKE_REVIEW)

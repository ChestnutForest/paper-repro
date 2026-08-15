"""スモークテスト: 骨組みが壊れていないことの最低確認。

Claude Code はここにテストを足していく。
"""

from app.core.db import Base, get_db
from app.core.states import ProjectState, can_transition
from app.main import app
from app.models.project import Project
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# テストでは in-memory SQLite を使い、同じエンジン接続を共有する。
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_project():
    r = client.post(
        "/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"}
    )
    assert r.status_code == 201
    pid = r.json()["project_id"]
    assert r.json()["state"] == ProjectState.CREATED

    r2 = client.get(f"/api/v1/projects/{pid}")
    assert r2.status_code == 200


def test_state_machine_rejects_illegal():
    # created から done へ直接飛ぶ遷移は許可されない
    assert not can_transition(ProjectState.CREATED, ProjectState.DONE)
    assert can_transition(ProjectState.CREATED, ProjectState.INTAKE_REVIEW)


def test_api_state_transition():
    # Create project
    r = client.post("/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"})
    pid = r.json()["project_id"]
    
    # Valid transition to INTAKE_REVIEW
    r2 = client.post(f"/api/v1/projects/{pid}/state", json={"state": "intake_review"})
    assert r2.status_code == 200
    assert r2.json()["state"] == "intake_review"
    
    # Invalid transition back to CREATED
    r3 = client.post(f"/api/v1/projects/{pid}/state", json={"state": "created"})
    assert r3.status_code == 400


def test_api_policy_transition():
    # Create project
    r = client.post("/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"})
    pid = r.json()["project_id"]
    
    # Invalid transition from CREATED to READING via policy directly
    r1 = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r1.status_code == 400
    
    # Advance state to intake_review
    client.post(f"/api/v1/projects/{pid}/state", json={"state": "intake_review"})
    
    # Valid transition to READING via set_policy
    r2 = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r2.status_code == 200
    assert r2.json()["state"] == "reading"

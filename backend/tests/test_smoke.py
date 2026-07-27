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

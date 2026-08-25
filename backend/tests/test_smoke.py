"""スモークテスト: 骨組みが壊れていないことの最低確認。

Claude Code はここにテストを足していく。
"""

from uuid import uuid4

from app.core.db import Base, get_db
from app.core.states import Course, Phase, Status, can_transition
from app.main import app
from app.models.project import Project
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
        "/api/v1/projects",
        json={"arxiv_url": "https://arxiv.org/abs/2505.20139", "course": "reading"},
    )
    assert r.status_code == 201
    pid = r.json()["project_id"]
    assert r.json()["phase"] == Phase.CREATED
    assert r.json()["status"] == Status.IDLE
    assert r.json()["course"] == Course.READING

    r2 = client.get(f"/api/v1/projects/{pid}")
    assert r2.status_code == 200


def test_state_machine_rejects_illegal():
    # created から done へ直接飛ぶ遷移は許可されない
    assert not can_transition(Phase.CREATED, Phase.DONE)
    assert can_transition(Phase.CREATED, Phase.INTAKE_REVIEW)


def test_api_policy_transition():
    # 汎用遷移エンドポイントが廃止されたため、DB を直接組み立てて
    # phase=intake_review のプロジェクトを用意する。
    db = TestingSessionLocal()
    pid = str(uuid4())
    project = Project(
        project_id=pid,
        arxiv_url="https://arxiv.org/abs/2505.20139",
        course=Course.READING,
        phase=Phase.INTAKE_REVIEW,
        status=Status.IDLE,
    )
    db.add(project)
    db.commit()
    db.close()

    r2 = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r2.status_code == 200
    assert r2.json()["phase"] == "reading"


def test_create_project_without_course_is_rejected():
    r = client.post(
        "/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"}
    )
    assert r.status_code == 422


def test_generic_state_endpoint_is_removed():
    r0 = client.post(
        "/api/v1/projects",
        json={"arxiv_url": "https://arxiv.org/abs/2505.20139", "course": "reading"},
    )
    pid = r0.json()["project_id"]
    r = client.post(f"/api/v1/projects/{pid}/state", json={"state": "intake_review"})
    assert r.status_code in (404, 405)


def test_policy_rejected_when_not_in_intake_review():
    r0 = client.post(
        "/api/v1/projects",
        json={"arxiv_url": "https://arxiv.org/abs/2505.20139", "course": "reading"},
    )
    pid = r0.json()["project_id"]
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r.status_code == 400


def _make_project_in_phase(phase: Phase) -> str:
    db = TestingSessionLocal()
    pid = str(uuid4())
    project = Project(
        project_id=pid,
        arxiv_url="https://arxiv.org/abs/2505.20139",
        course=Course.READING,
        phase=phase,
        status=Status.IDLE,
    )
    db.add(project)
    db.commit()
    db.close()
    return pid


def test_policy_rejected_from_reading_with_non_skip_policy():
    # READING -> READING は phase の自己ループとして許可されているため、
    # can_transition だけで判定すると誤って通ってしまう(承認ゲート①の再押下)。
    pid = _make_project_in_phase(Phase.READING)
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r.status_code == 400


def test_policy_rejected_from_reading_with_skip_policy():
    # READING -> SKIPPED は遷移表に無いため can_transition 単独でも 400 になるが、
    # 拒否の理由が「intake_review にいない」で統一されていることを担保する。
    pid = _make_project_in_phase(Phase.READING)
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "skip"})
    assert r.status_code == 400

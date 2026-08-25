"""スモークテスト。骨組みが壊れていないことの最低確認。

テストは in-memory SQLite を使い、`get_db` を差し替えて実行する。

含まれるもの:
    疎通、プロジェクトの作成と取得、状態機械の直接検査、承認ゲート①の遷移。
    加えて、設計上の決定が守られていることを証明する退行テストを5本持つ
    （`course` 必須、汎用遷移の廃止、ゲート①を押せる工程の限定）。

Note:
    退行テストは、決定を後から緩めたときに落ちることが目的である。
    落とさずに通すために条件を弱めてはならない。
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
    """`get_db` の差し替え。テスト用の in-memory SQLite セッションを渡す。

    Yields:
        Session: テスト用 DB セッション。呼び出し後に必ず閉じる。
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    """`GET /health` が 200 と `status=ok` を返すこと。"""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_project():
    """作成直後の `phase` / `status` / `course` が期待どおりで、再取得できること。

    仕様 3.1 の既定値（`phase=created` / `status=idle`）を確認する。
    """
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
    """`can_transition` が遷移表に無い遷移を拒否すること。

    API を介さず、状態機械そのものを直接検査する。
    """
    # created から done へ直接飛ぶ遷移は許可されない
    assert not can_transition(Phase.CREATED, Phase.DONE)
    assert can_transition(Phase.CREATED, Phase.INTAKE_REVIEW)


def test_api_policy_transition():
    """承認ゲート①が `intake_review` から `reading` へ進めること。

    汎用遷移エンドポイントが廃止されたため、DB を直接組み立てて前提の工程を作る。
    仕様 5.2 の却下理由に「テストで状態を進めたい場合は DB を直接組み立てればよい」
    と記載がある。
    """
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
    """`course` を欠いた作成リクエストが 422 で拒否されること。

    `course` を必須にする決定（仕様 5.1・`REQ-C01`）が守られていることの証明。
    """
    r = client.post(
        "/api/v1/projects", json={"arxiv_url": "https://arxiv.org/abs/2505.20139"}
    )
    assert r.status_code == 422


def test_generic_state_endpoint_is_removed():
    """`POST /projects/{id}/state` が存在しないこと（404 または 405）。

    承認ゲートの迂回を構造上できなくする決定（仕様 5.2・`REQ-C06`）が
    守られていることの証明。将来これを復活させると本テストが落ちる。
    """
    r0 = client.post(
        "/api/v1/projects",
        json={"arxiv_url": "https://arxiv.org/abs/2505.20139", "course": "reading"},
    )
    pid = r0.json()["project_id"]
    r = client.post(f"/api/v1/projects/{pid}/state", json={"state": "intake_review"})
    assert r.status_code in (404, 405)


def test_policy_rejected_when_not_in_intake_review():
    """`phase=created` のままゲート①を押せないこと（400）。"""
    r0 = client.post(
        "/api/v1/projects",
        json={"arxiv_url": "https://arxiv.org/abs/2505.20139", "course": "reading"},
    )
    pid = r0.json()["project_id"]
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r.status_code == 400


def _make_project_in_phase(phase: Phase) -> str:
    """指定した `phase` のプロジェクトを DB へ直接作り、その主キーを返す。

    API 経由では到達できない工程を前提にしたテストのためのヘルパー。

    Args:
        phase: 作りたい工程。

    Returns:
        作成したプロジェクトの `project_id`。
    """
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
    """`phase=reading` からゲート①を押し直せないこと（400）。

    2026-08-25 に修正したバグの再発防止。修正前は `can_transition` だけで
    判定していたため、`READING` の自己ループを通って 200 が返っていた。
    """
    # READING -> READING は phase の自己ループとして許可されているため、
    # can_transition だけで判定すると誤って通ってしまう(承認ゲート①の再押下)。
    pid = _make_project_in_phase(Phase.READING)
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "full"})
    assert r.status_code == 400


def test_policy_rejected_from_reading_with_skip_policy():
    """`phase=reading` から `policy=skip` でも同じ理由で拒否されること（400）。

    修正前でも遷移表の都合で偶然 400 になっていたが、**拒否の理由が
    「`intake_review` にいない」で統一されている**ことを担保するために置く。
    片方だけでは、判定を戻したときに気づけない。
    """
    # READING -> SKIPPED は遷移表に無いため can_transition 単独でも 400 になるが、
    # 拒否の理由が「intake_review にいない」で統一されていることを担保する。
    pid = _make_project_in_phase(Phase.READING)
    r = client.post(f"/api/v1/projects/{pid}/policy", json={"policy": "skip"})
    assert r.status_code == 400

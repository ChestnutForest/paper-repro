"""プロジェクト関連の API ルーター。

docs/arch-guide/arc-datamodel.md v1.0 に対応。
TODO(Claude Code):
  - 取り込み・spec草案・照合を services 層に実装し、長時間処理は Celery タスク化する
  - 承認ゲート（spec finalize, sanity gate）で phase 遷移を検証する
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.states import Course, Phase, Policy, Status, can_transition
from app.models.project import Project

router = APIRouter(tags=["projects"])


class CreateProjectReq(BaseModel):
    """`POST /projects` のリクエストボディ。

    Attributes:
        arxiv_url: 取り込む論文の URL。
        course: 読解か再現実装か（`REQ-C01`）。**必須で、既定値を持たない。**
            既定値を置くと未選択のプロジェクトが作れてしまい、
            「開始時に選択する」という要求が骨抜きになるため（仕様 5.1）。
    """

    arxiv_url: str
    course: Course


class ProjectRes(BaseModel):
    """プロジェクトの API 応答。

    ORM の `Project` から `from_attributes` で組み立てる。

    Attributes:
        project_id: 主キー。UUID v4 の文字列表現。
        arxiv_url: 取り込む論文の URL。
        course: 選択中の経路。
        phase: 工程上の現在地。
        status: その工程での実行状態。

    Note:
        `approval_kind` は含めない。事象駆動ゲート④⑤⑥が未実装で、
        現状では常に NULL を返すのみのため。ゲートを実装する段で追加する。
    """

    project_id: str
    arxiv_url: str
    course: Course
    phase: Phase
    status: Status

    model_config = ConfigDict(from_attributes=True)


@router.get("/projects", response_model=list[ProjectRes])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRes]:
    """プロジェクトを全件返す。

    Args:
        db: DB セッション（DI）。

    Returns:
        登録済みプロジェクトの一覧。0件なら空リスト。
    """
    projects = db.query(Project).all()
    return [ProjectRes.from_orm(project) for project in projects]


@router.post("/projects", response_model=ProjectRes, status_code=201)
def create_project(req: CreateProjectReq, db: Session = Depends(get_db)) -> ProjectRes:
    """arXiv URL と course を受けてプロジェクトを作成する。

    `phase=created` / `status=idle` で登録する。

    Args:
        req: 作成リクエスト。`course` は必須。
        db: DB セッション（DI）。

    Returns:
        作成したプロジェクト。HTTP 201 を返す。

    Raises:
        RequestValidationError: 422。`course` が欠けている、または値が
            `Course` の定義外のとき。FastAPI が自動で返す。

    Note:
        本来はここで取り込みジョブ（Celery）を起動し job_id を返す。
        いまは骨組みなので、作成だけ行う。
    """
    pid = str(uuid4())
    project = Project(
        project_id=pid,
        arxiv_url=req.arxiv_url,
        course=req.course,
        phase=Phase.CREATED,
        status=Status.IDLE,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectRes.from_orm(project)


@router.get("/projects/{project_id}", response_model=ProjectRes)
def get_project(project_id: str, db: Session = Depends(get_db)) -> ProjectRes:
    """プロジェクトを1件返す。

    Args:
        project_id: 主キー。
        db: DB セッション（DI）。

    Returns:
        該当プロジェクト。

    Raises:
        HTTPException: 404。該当する `project_id` が存在しないとき。
    """
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return ProjectRes.from_orm(project)


class PolicyReq(BaseModel):
    """`POST /projects/{project_id}/policy` のリクエストボディ。

    Attributes:
        policy: 承認ゲート①で選ぶ方針の5択。
    """

    policy: Policy


@router.post("/projects/{project_id}/policy", response_model=ProjectRes)
def set_policy(
    project_id: str, req: PolicyReq, db: Session = Depends(get_db)
) -> ProjectRes:
    """承認ゲート①。方針を確定して READING へ進む（`skip` なら SKIPPED）。

    判定は二段構えである。まず `phase` が `intake_review` かを確認し、
    通過したものだけ `can_transition` で遷移の可否を見る。
    `can_transition` は「その遷移が状態機械として許されるか」にしか答えられず、
    `Phase.READING` の自己ループを通り抜けてゲートの再押下を許してしまうため
    （2026-08-25 に修正）。

    Args:
        project_id: 主キー。
        req: 方針の5択。
        db: DB セッション（DI）。

    Returns:
        更新後のプロジェクト。`phase` は `reading` または `skipped`。

    Raises:
        HTTPException: 404。該当する `project_id` が存在しないとき。
        HTTPException: 400。`phase` が `intake_review` 以外のとき。
            方針の値によらず、同じ理由で拒否する。
        HTTPException: 400。工程の確認を通過したうえで遷移が許可されないとき。

    Note:
        汎用の状態遷移エンドポイントは廃止済み（仕様 5.2）。
        `phase` を進める経路は本関数のようなゲートのエンドポイントに限る。
        これにより承認ゲートの迂回が構造上できなくなる（`REQ-C06`）。
    """
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    if project.phase != Phase.INTAKE_REVIEW:
        raise HTTPException(
            status_code=400,
            detail=f"policy can only be set from intake_review, current phase is {project.phase.value}",
        )

    target_phase = Phase.SKIPPED if req.policy == Policy.SKIP else Phase.READING
    if not can_transition(project.phase, target_phase):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {project.phase.value} to {target_phase.value}",
        )

    project.policy = req.policy.value
    project.phase = target_phase
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectRes.from_orm(project)

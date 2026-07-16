"""プロジェクト関連の API ルーター。

docs/mvp-design.md の第3章「APIエンドポイント」に対応。
まずは骨組み（スタブ）。Claude Code に中身を実装してもらう。

TODO(Claude Code):
  - DB モデルと接続（app/models, app/core/db）を実装する
  - 取り込み・spec草案・照合を services 層に実装し、長時間処理は Celery タスク化する
  - 承認ゲート（policy 確定, spec finalize, sanity gate）で状態遷移を検証する
"""
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.states import Policy, ProjectState

router = APIRouter(tags=["projects"])

# --- 仮のインメモリ保存（MVP初期のみ。後で PostgreSQL に置き換える）---
_PROJECTS: dict[str, dict] = {}


class CreateProjectReq(BaseModel):
    arxiv_url: str


class ProjectRes(BaseModel):
    project_id: str
    arxiv_url: str
    state: ProjectState


@router.get("/projects", response_model=list[ProjectRes])
def list_projects() -> list[ProjectRes]:
    return [ProjectRes(**p) for p in _PROJECTS.values()]


@router.post("/projects", response_model=ProjectRes, status_code=201)
def create_project(req: CreateProjectReq) -> ProjectRes:
    """arXiv URL を受けてプロジェクトを作成する。

    本来はここで取り込みジョブ（Celery）を起動し job_id を返す。
    いまは骨組みなので、作成だけ行う。
    """
    pid = str(uuid4())
    rec = {"project_id": pid, "arxiv_url": req.arxiv_url, "state": ProjectState.CREATED}
    _PROJECTS[pid] = rec
    return ProjectRes(**rec)


@router.get("/projects/{project_id}", response_model=ProjectRes)
def get_project(project_id: str) -> ProjectRes:
    if project_id not in _PROJECTS:
        raise HTTPException(status_code=404, detail="project not found")
    return ProjectRes(**_PROJECTS[project_id])


class PolicyReq(BaseModel):
    policy: Policy


@router.post("/projects/{project_id}/policy", response_model=ProjectRes)
def set_policy(project_id: str, req: PolicyReq) -> ProjectRes:
    """承認ゲート①: 方針を確定して READING へ進む（または見送り）。"""
    if project_id not in _PROJECTS:
        raise HTTPException(status_code=404, detail="project not found")
    rec = _PROJECTS[project_id]
    rec["policy"] = req.policy
    rec["state"] = ProjectState.SKIPPED if req.policy == Policy.SKIP else ProjectState.READING
    return ProjectRes(**rec)

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
    arxiv_url: str
    course: Course


class ProjectRes(BaseModel):
    project_id: str
    arxiv_url: str
    course: Course
    phase: Phase
    status: Status

    model_config = ConfigDict(from_attributes=True)


@router.get("/projects", response_model=list[ProjectRes])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRes]:
    projects = db.query(Project).all()
    return [ProjectRes.from_orm(project) for project in projects]


@router.post("/projects", response_model=ProjectRes, status_code=201)
def create_project(req: CreateProjectReq, db: Session = Depends(get_db)) -> ProjectRes:
    """arXiv URL と course を受けてプロジェクトを作成する。

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
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return ProjectRes.from_orm(project)


class PolicyReq(BaseModel):
    policy: Policy


@router.post("/projects/{project_id}/policy", response_model=ProjectRes)
def set_policy(
    project_id: str, req: PolicyReq, db: Session = Depends(get_db)
) -> ProjectRes:
    """承認ゲート①: 方針を確定して READING へ進む（または見送り）。"""
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

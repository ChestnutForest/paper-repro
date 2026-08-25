from sqlalchemy import Column, Enum, String

from app.core.db import Base
from app.core.states import ApprovalKind, Course, Phase, Status


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String(36), primary_key=True, index=True)
    arxiv_url = Column(String, nullable=False)
    course = Column(
        Enum(Course, native_enum=False, validate_strings=True), nullable=False
    )
    phase = Column(
        Enum(Phase, native_enum=False, validate_strings=True),
        nullable=False,
        default=Phase.CREATED,
    )
    status = Column(
        Enum(Status, native_enum=False, validate_strings=True),
        nullable=False,
        default=Status.IDLE,
    )
    approval_kind = Column(
        Enum(ApprovalKind, native_enum=False, validate_strings=True), nullable=True
    )
    policy = Column(String, nullable=True)

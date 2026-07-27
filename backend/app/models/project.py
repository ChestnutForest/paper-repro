from sqlalchemy import Column, Enum, String

from app.core.db import Base
from app.core.states import ProjectState


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String(36), primary_key=True, index=True)
    arxiv_url = Column(String, nullable=False)
    state = Column(
        Enum(ProjectState, native_enum=False, validate_strings=True), nullable=False
    )
    policy = Column(String, nullable=True)

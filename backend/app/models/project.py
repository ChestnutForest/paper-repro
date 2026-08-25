"""プロジェクトの ORM モデル。

エクスポートするもの:
    Project: 論文1件の再現作業を表すテーブル `projects`。

列の型・NULL可否・既定値は docs/arch-guide/arc-datamodel.md v1.0 の 3.1 節を正本とする。
"""

from sqlalchemy import Column, Enum, String

from app.core.db import Base
from app.core.states import ApprovalKind, Course, Phase, Status


class Project(Base):
    """論文1件の再現作業を表す（テーブル `projects`）。

    Attributes:
        project_id: 主キー。UUID v4 の文字列表現。
        arxiv_url: 取り込む論文の URL。
        course: 読解か再現実装か。**NOT NULL で既定値を持たない。**
            既定値を置くと未選択のプロジェクトが作れてしまうため（`REQ-C01`・仕様 5.1）。
        phase: 工程上の現在地。既定は `Phase.CREATED`。
        status: その工程での実行状態。既定は `Status.IDLE`。
        approval_kind: 待っている承認ゲートの種別。`status` が
            `WAITING_APPROVAL` のときに限り非 NULL（仕様 3.5 の不変条件）。
        policy: 承認ゲート①で選んだ方針。ゲートを通る前は NULL。

    Note:
        Enum 列はすべて `native_enum=False` を指定する。テストが SQLite で動き、
        SQLite はネイティブ ENUM 型を持たないため。外すとテストは通るのに
        PostgreSQL で落ちる。

    Todo:
        次の段で `paper_type` / `title` / `course_changed_at` / `created_at` /
        `updated_at` の5列、`approval_kind` の CHECK 制約、`policy` の ENUM 化、
        既定値の `server_default` 化を加える（仕様 3.1・3.5）。
    """

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

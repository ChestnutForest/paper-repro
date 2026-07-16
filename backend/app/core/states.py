"""プロジェクトの状態機械。

docs/mvp-design.md の第1章「状態遷移」に対応する。
承認ゲートを通らないと次の状態に進めない。
"""
from enum import Enum


class ProjectState(str, Enum):
    CREATED = "created"                 # 作成直後
    INTAKE_REVIEW = "intake_review"     # 承認ゲート①: 方針を選ぶ
    READING = "reading"                 # spec・仮定台帳の作成
    IMPLEMENTING = "implementing"       # サニティ階段の実行
    SCORING = "scoring"                 # 論文値との照合
    DONE = "done"                       # 完了
    SKIPPED = "skipped"                 # 見送り（第1パスで打ち切り）
    FAILED = "failed"                   # 実行失敗（原因を提示して同状態へ戻す）


# 許可された遷移のみを定義する。ここに無い遷移は拒否する。
ALLOWED_TRANSITIONS: dict[ProjectState, set[ProjectState]] = {
    ProjectState.CREATED: {ProjectState.INTAKE_REVIEW, ProjectState.FAILED},
    ProjectState.INTAKE_REVIEW: {ProjectState.READING, ProjectState.SKIPPED},
    ProjectState.READING: {ProjectState.IMPLEMENTING, ProjectState.FAILED},
    ProjectState.IMPLEMENTING: {ProjectState.SCORING, ProjectState.FAILED},
    ProjectState.SCORING: {ProjectState.DONE, ProjectState.FAILED},
    ProjectState.FAILED: {ProjectState.READING, ProjectState.IMPLEMENTING, ProjectState.SCORING},
}


def can_transition(src: ProjectState, dst: ProjectState) -> bool:
    """src から dst への遷移が許可されているか。"""
    return dst in ALLOWED_TRANSITIONS.get(src, set())


class PaperType(str, Enum):
    A = "A"  # 学習あり（MVPスコープ外だが、判定は行う）
    B = "B"  # 学習なし（MVPの対象）


class Policy(str, Enum):
    FULL = "full"          # フル再現
    REDUCED = "reduced"    # 縮小版
    ADAPT = "adapt"        # 読解+改造
    PARTIAL = "partial"    # 部分採用
    SKIP = "skip"          # 見送り

"""プロジェクトの状態機械。

docs/arch-guide/arc-datamodel.md v1.0 の 3.3〜3.5 節に対応する。
`phase`（工程上の現在地）と `status`（その工程での実行状態）を分けて持つ。
承認ゲートを通らないと次の phase に進めない。
"""

from enum import Enum


class Course(str, Enum):
    READING = "reading"  # 読解
    REPRODUCTION = "reproduction"  # 再現実装


class Phase(str, Enum):
    CREATED = "created"  # 作成直後
    INTAKE_REVIEW = "intake_review"  # 承認ゲート①: 方針を選ぶ
    READING = "reading"  # spec・仮定台帳の作成
    IMPLEMENTING = "implementing"  # サニティ階段の実行
    SCORING = "scoring"  # 論文値との照合
    DONE = "done"  # 完了
    SKIPPED = "skipped"  # 見送り（第1パスで打ち切り）


class Status(str, Enum):
    IDLE = "idle"  # 待機中
    RUNNING = "running"  # ジョブ実行中
    WAITING_APPROVAL = "waiting_approval"  # 事象駆動ゲート待ち
    FAILED = "failed"  # 実行失敗（phase は変えない）


class ApprovalKind(str, Enum):
    POLICY = "policy"  # ゲート①
    SPEC = "spec"  # ゲート②
    SANITY = "sanity"  # ゲート③
    INTERPRETATION = "interpretation"  # ゲート④
    CONFLICT = "conflict"  # ゲート⑤
    COMPREHENSION = "comprehension"  # ゲート⑥


# 許可された phase 遷移のみを定義する。ここに無い遷移は拒否する。
# docs/arch-guide/arc-datamodel.md 3.4節の表に対応。
ALLOWED_TRANSITIONS: dict[Phase, set[Phase]] = {
    Phase.CREATED: {Phase.INTAKE_REVIEW},
    Phase.INTAKE_REVIEW: {Phase.READING, Phase.SKIPPED},
    Phase.READING: {Phase.READING, Phase.IMPLEMENTING},
    Phase.IMPLEMENTING: {Phase.SCORING},
    Phase.SCORING: {Phase.DONE},
}


def can_transition(src: Phase, dst: Phase) -> bool:
    """src から dst への phase 遷移が許可されているか。"""
    return dst in ALLOWED_TRANSITIONS.get(src, set())


class PaperType(str, Enum):
    A = "A"  # 学習あり（初期リリーススコープ外だが、判定は行う）
    B = "B"  # 学習なし（初期リリースの対象）


class Policy(str, Enum):
    FULL = "full"  # フル再現
    REDUCED = "reduced"  # 縮小版
    ADAPT = "adapt"  # 読解+改造
    PARTIAL = "partial"  # 部分採用
    SKIP = "skip"  # 見送り

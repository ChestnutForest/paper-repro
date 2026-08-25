"""プロジェクトの状態機械。

`phase`（工程上の現在地）と `status`（その工程での実行状態）を分けて持つ。
承認ゲートを通らないと次の phase に進めない。

エクスポートするもの:
    Course: 利用者が選ぶ主要経路。
    Phase: 工程上の現在地。`failed` を含めない。
    Status: その工程での実行状態。
    ApprovalKind: 待っている承認ゲートの種別。
    PaperType: 論文のタイプ判定結果。
    Policy: 承認ゲート①で選ぶ方針の5択。
    ALLOWED_TRANSITIONS: 許可された phase 遷移の表。
    can_transition: 遷移が許可されているかを返す。

値と遷移表は docs/arch-guide/arc-datamodel.md v1.0 の 3.3〜3.5 節を正本とする。
"""

from enum import Enum


class Course(str, Enum):
    """利用者が選ぶ主要経路（`REQ-C01`）。

    プロジェクト作成時に必須で、既定値を持たない。未選択の状態を存在させないため。
    値は DB の `course_enum`（仕様 3.3）と一対一に対応する。

    Attributes:
        READING: 読解・学習コース。`implementing` 以降へ進まない。
        REPRODUCTION: 再現実装コース。主経路をすべて通る。
    """

    READING = "reading"  # 読解
    REPRODUCTION = "reproduction"  # 再現実装


class Phase(str, Enum):
    """工程上の現在地（仕様 3.3 の `phase_enum`）。

    **`failed` を含めない。** 失敗は `Status.FAILED` で表し、`phase` は
    失敗した工程を保持し続ける。1列に混ぜるとどの工程で失敗したかが失われるため
    （仕様 2.1）。

    Note:
        `Phase.READING` と `Course.READING` は値がどちらも ``"reading"`` だが
        別の型である。取り違えた比較は常に偽になり気づきにくいので、
        `phase` の比較には必ず本 Enum を用いること。
    """

    CREATED = "created"  # 作成直後
    INTAKE_REVIEW = "intake_review"  # 承認ゲート①: 方針を選ぶ
    READING = "reading"  # spec・仮定台帳の作成
    IMPLEMENTING = "implementing"  # サニティ階段の実行
    SCORING = "scoring"  # 論文値との照合
    DONE = "done"  # 完了
    SKIPPED = "skipped"  # 見送り（第1パスで打ち切り）


class Status(str, Enum):
    """その工程での実行状態（仕様 3.3 の `status_enum`）。

    `phase` を変えずに実行の成否と待ち状態を表す。失敗からの復帰は
    `FAILED` から `IDLE` に戻すだけでよく、`phase` の遷移表を増やさない（仕様 3.5）。

    Attributes:
        IDLE: 待機中。
        RUNNING: ジョブ実行中。
        WAITING_APPROVAL: 事象駆動ゲート待ち。このときに限り `approval_kind` が非 NULL。
        FAILED: 実行失敗。`phase` は変えない。
    """

    IDLE = "idle"  # 待機中
    RUNNING = "running"  # ジョブ実行中
    WAITING_APPROVAL = "waiting_approval"  # 事象駆動ゲート待ち
    FAILED = "failed"  # 実行失敗（phase は変えない）


class ApprovalKind(str, Enum):
    """`status=WAITING_APPROVAL` のとき、どの承認ゲートで待つかを表す（仕様 3.3）。

    ゲート①〜③は工程の境目に来る遷移型、④〜⑥は作業中に不定期に発生する事象駆動型
    （`docs/product-design.md` 1.3）。

    Attributes:
        POLICY: ①方針の5択。Phase 0 の末。
        SPEC: ②spec とタイプの確定。Phase 1〜3 の末。
        SANITY: ③サニティの合格確認。Phase 4 の末。
        INTERPRETATION: ④重要な解釈の確認（`REQ-C10-S04`）。
        CONFLICT: ⑤重大な証拠矛盾の解決（`REQ-C07`）。
        COMPREHENSION: ⑥学習到達点の確認（`REQ-C04-S02`）。
    """

    POLICY = "policy"  # ゲート①
    SPEC = "spec"  # ゲート②
    SANITY = "sanity"  # ゲート③
    INTERPRETATION = "interpretation"  # ゲート④
    CONFLICT = "conflict"  # ゲート⑤
    COMPREHENSION = "comprehension"  # ゲート⑥


# 許可された phase 遷移のみを定義する。ここに無い遷移は拒否する。
# docs/arch-guide/arc-datamodel.md 3.4節の表に対応。
# 表に無い遷移は拒否される。`Phase.READING` の自己ループは `course=reading` の
# 反復（`docs/product-design.md` 1.2）を表す。
ALLOWED_TRANSITIONS: dict[Phase, set[Phase]] = {
    Phase.CREATED: {Phase.INTAKE_REVIEW},
    Phase.INTAKE_REVIEW: {Phase.READING, Phase.SKIPPED},
    Phase.READING: {Phase.READING, Phase.IMPLEMENTING},
    Phase.IMPLEMENTING: {Phase.SCORING},
    Phase.SCORING: {Phase.DONE},
}


def can_transition(src: Phase, dst: Phase) -> bool:
    """指定された phase 遷移が許可されているかを返す。

    Args:
        src: 遷移元の工程。
        dst: 遷移先の工程。

    Returns:
        `ALLOWED_TRANSITIONS` に定義があれば True、なければ False。

    Note:
        本関数が答えるのは「**その遷移が状態機械として許されるか**」であり、
        「**このゲートを押してよい工程にいるか**」ではない。
        `Phase.READING` には自己ループがあるため、承認ゲートの可否判定を
        本関数だけに委ねると作業中の再押下を通してしまう。
        ゲート側で `phase` を明示的に確認したうえで、二段目として本関数を用いること
        （`app/api/projects.py` の `set_policy` を参照）。
    """
    return dst in ALLOWED_TRANSITIONS.get(src, set())


class PaperType(str, Enum):
    """論文のタイプ判定結果。判定前は NULL。

    Attributes:
        A: 学習あり。初期リリースのスコープ外だが、判定は行う。
        B: 学習なし・公式実装あり。初期リリースの対象。
    """

    A = "A"  # 学習あり（初期リリーススコープ外だが、判定は行う）
    B = "B"  # 学習なし（初期リリースの対象）


class Policy(str, Enum):
    """承認ゲート①で選ぶ方針の5択（`docs/requirements.md` 1.2）。

    Attributes:
        FULL: フル再現。
        REDUCED: 縮小版。計算資源に合わせて設定を縮約する。
        ADAPT: 読解 + 改造。
        PARTIAL: 部分採用。
        SKIP: 見送り。`Phase.SKIPPED` へ進む終端。
    """

    FULL = "full"  # フル再現
    REDUCED = "reduced"  # 縮小版
    ADAPT = "adapt"  # 読解+改造
    PARTIAL = "partial"  # 部分採用
    SKIP = "skip"  # 見送り

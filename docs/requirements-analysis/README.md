# 要求分析資料

`paper-repro`の要件を検討するために、一次資料から抽出した示唆と現行要件との差分を記録する。
このディレクトリの文書は、要件を確定する前の分析資料であり、確定要件や決定台帳を直接置き換えない。

## 文書の位置づけ

| 種別 | 正本 | 役割 |
|---|---|---|
| 確定済み要件 | [`../requirements.md`](../requirements.md) | 実装と設計が従う要件定義 |
| 要件定義変更案 | [`../requirements-change-proposal.md`](../requirements-change-proposal.md) | 選択済み要求を統合した承認前の変更案 |
| 意思決定記録 | [`../requirements-decisions/`](../requirements-decisions/) | 5択、利用者の選択、理由、受入基準 |
| 一次資料分析 | 本ディレクトリ | 根拠範囲、現行要件との対応、新規要求候補 |
| 参考文献 | [`../references.md`](../references.md) | 一次資料の書誌情報と引用の方針 |

分析文書で見つかったメイン要求候補は、利用者が5択で方針を選ぶまで未確定とする。
既存要求を具体化するサブ要求も、変更案へ統合して承認されるまでは確定要件として扱わない。

## 分析文書一覧

| ファイル | 対象 | 状態 | 主な結果 |
|---|---|---|---|
| [`section-1.2-reading-techniques.md`](section-1.2-reading-techniques.md) | 菊田遥平『原論文から解き明かす生成AI』技術評論社, 2025 の「1.2 論文を読み解く技術」 | 分析完了・追加候補2件を選択済み | メイン要求候補2件、サブ要求候補10件 |
| [`section-1.2.1-reading-environment.md`](section-1.2.1-reading-environment.md) | 同書「1.2.1 論文を読む環境の構築」 | 詳細検証完了 | `REQ-C10`の根拠補強、既存サブ要求候補4件、新規IDなし |
| [`section-1.2.1.1-paper-acquisition.md`](section-1.2.1.1-paper-acquisition.md) | 同書「1.2.1.1 論文を入手する」 | 限定分析完了 | 新規メイン要求なし、`REQ-C03-S01`・`REQ-C07-S01`を要求文と受入基準まで具体化 |
| [`section-1.2.1.2-electronic-reading.md`](section-1.2.1.2-electronic-reading.md) | 同書「1.2.1.2 論文を電子媒体で読む」 | 限定分析完了 | 新規メイン要求なし、`REQ-C09-S01`を要求文と受入基準まで具体化 |
| [`section-1.2.1.3-human-authorship.md`](section-1.2.1.3-human-authorship.md) | 同書「1.2.1.3 論文は人間が書いたものであることを認識する」 | 限定分析完了 | 新規メイン要求なし、`REQ-C10`の根拠を補強し、`REQ-C10-S04`を具体化 |
| [`section-1.2.2-independent-reading-techniques.md`](section-1.2.2-independent-reading-techniques.md) | 同書「1.2.2 自分の力で論文を読み解くための技術」 | 限定分析完了 | 新規メイン要求なし、`REQ-C04`・`REQ-C05`・`REQ-C09`・`REQ-C10`のサブ要求候補8件を具体化 |
| [`section-1.2.2.1-discussion-conditions.md`](section-1.2.2.1-discussion-conditions.md) | 同書「1.2.2.1 議論が成立する条件を確認する」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C10-S01`〜`S03`を詳細化し、`REQ-C07-S01`・`REQ-C10-S04`の根拠を補強 |
| [`section-1.2.2.2-concrete-examples.md`](section-1.2.2.2-concrete-examples.md) | 同書「1.2.2.2 具体例を構成する」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C04-S01`・`REQ-C10-S03`を詳細化し、`REQ-C10-S01`の根拠を補強 |
| [`section-1.2.2.3-implementation-reading.md`](section-1.2.2.3-implementation-reading.md) | 同書「1.2.2.3 実装を読み解いて理解を深める」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C05-S01`を詳細化し、`REQ-C07:4`・`REQ-C08:4`・`REQ-C10-S04`の根拠を補強 |
| [`section-1.2.2.4-important-references.md`](section-1.2.2.4-important-references.md) | 同書「1.2.2.4 重要となる参考文献は踏み込んで調べる」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C09-S02`を詳細化し、`REQ-C03-S01`・`REQ-C04-S01`・`REQ-C07-S01`・`REQ-C08:4`の根拠を補強 |
| [`section-1.2.2.5-output-for-understanding.md`](section-1.2.2.5-output-for-understanding.md) | 同書「1.2.2.5 アウトプットすることで理解を深める」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C04-S02`・`REQ-C09-S03`を詳細化し、`REQ-C09-S02`・`REQ-C10-S01`・`REQ-C08:4`の根拠を補強 |
| [`section-1.2.3-external-help.md`](section-1.2.3-external-help.md) | 同書「1.2.3 自分以外の力も借りて論文を読み解くための技術」の導入部 | 導入部の検証完了・小節本文は未分析 | 新規メイン要求なし、暫定サブ要求候補`REQ-C07-S02`・`REQ-C09-S04`を提案 |
| [`section-1.2.3.1-small-group-discussion.md`](section-1.2.3.1-small-group-discussion.md) | 同書「1.2.3.1 少人数で深く議論する」 | 詳細検証完了 | 新規メイン要求・新規サブ要求ともになし、`REQ-C04-S02`と暫定の`REQ-C09-S04`の根拠を補強 |
| [`section-1.2.3.2-contacting-authors.md`](section-1.2.3.2-contacting-authors.md) | 同書「1.2.3.2 論文の著者に直接質問する」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C09-S05`を提案し、保留中の`REQ-C07-S02`の確定案を提示 |
| [`section-1.2.3.3-web-discussion.md`](section-1.2.3.3-web-discussion.md) | 同書「1.2.3.3 ウェブ上で議論する」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C07-S03`を提案し、`REQ-C07-S02`・`REQ-C09-S03`の根拠を補強 |
| [`section-1.2.3.4-using-generative-ai.md`](section-1.2.3.4-using-generative-ai.md) | 同書「1.2.3.4 生成AIを使う」 | 詳細検証完了 | 新規メイン要求なし、`REQ-C04-S03`・`REQ-C10-S05`を提案し、`REQ-C07:4`・`REQ-C10:4`・`REQ-C04-S02`・`REQ-C08:4`の根拠を補強 |
| [`academic-research-skills-frameworks.md`](academic-research-skills-frameworks.md) | SCONUL Seven Pillars・ACRL Framework・Vitae RDF・ACM Artifact Badging v1.1・ML再現性チェックリスト・FAIR原則・CRediT・ALLEA行動規範（REF-07〜REF-14） | 分析完了・5択未実施・現行要件との突合未実施 | メイン要求候補13件、サブ要求候補52件、非機能要求7件。再現の3水準の明示、成果物の4基準点検、実行回数と分散の記録が新規 |
| [`academic-research-skills.md`](academic-research-skills.md) | University of Sussex・University of Kent・University of Galway の「Academic and Research Skills」科目ページ（REF-04〜REF-06） | 分析完了・5択未実施・現行要件との突合未実施 | メイン要求候補3件（引用管理、研究倫理、プロジェクト計画）、サブ要求候補17件。7領域のうち4領域は既存要求の補強にとどまる |
| [`simclr-handson-deck.md`](simclr-handson-deck.md) | 角居雄太「論文再現実装ハンズオン #4 対照学習」DL COMMUNITY, 松尾・岩澤研究室, 東京大学, 2026（解説する原典: Chen, T.; Kornblith, S.; Norouzi, M.; Hinton, G. *Proc. 37th ICML*, 2020, 1597–1607. [arXiv:2002.05709](https://doi.org/10.48550/arxiv.2002.05709)） | 分析完了・5択未実施・現行要件との突合未実施 | メイン要求候補16件、サブ要求候補44件、非機能要求8件。暫定IDは`PR-M-xx`/`PR-S-xx-y`で、`REQ-Cxx`体系への合流は5択時に行う |

## 追加分析の共通手順

1. 対象節の開始・終了境界を本文とページ画像で確認する。
2. 本文、脚注、参考文献の範囲を分ける。
3. 現行要件と要件定義変更案へ対応付ける。
4. メイン要求、サブ要求、要求にしない記述へ分類する。
5. 新しいメイン要求候補は5択へ進める。
6. 選択後に変更案を更新し、利用者の承認後に確定要件へ反映する。

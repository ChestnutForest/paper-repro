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
| 要求突合表 | 本ディレクトリの `crosswalk-*.md` | 複数の分析文書の候補を統合し、現行要求への吸収を領域ごとに判定したもの。**5択の入力** |
| 参考文献 | [`../references.md`](../references.md) | 一次資料の書誌情報と引用の方針 |

分析文書で見つかったメイン要求候補は、利用者が5択で方針を選ぶまで未確定とする。
既存要求を具体化するサブ要求も、変更案へ統合して承認されるまでは確定要件として扱わない。

## 要求突合表

分析文書は一次資料ごとに独立して書かれるため、**同じ要求が別々のIDで重複する。**
突合表は、複数の分析文書の候補を統合したうえで、現行要求へ吸収されるかを領域ごとに判定する。

| ファイル | 対象領域 | 状態 | 主な結果 |
|---|---|---|---|
| [`crosswalk-01-reproduction.md`](crosswalk-01-reproduction.md) | 再現実装（`REQ-C05`・`REQ-C06`） | 突合完了・5択未実施 | 候補15件を13件へ統合。新規メイン要求候補3件（実行の再現条件の記録、スケールダウン、再現スコープ定義書）。`REQ-C06` に対応する候補は無し |
| [`crosswalk-02-reading.md`](crosswalk-02-reading.md) | 読解・学習（`REQ-C01`〜`REQ-C04`・`REQ-C10`） | 突合完了・5択未実施 | 候補16件。新規メイン要求候補2件（設計原理の抽象化、熟達段階の保持）。`REQ-C10-S01`〜`S04` の受け皿が厚く、多くが吸収された。**工程モデルが未確定のため2件を判定できず** |
| [`crosswalk-03-evidence.md`](crosswalk-03-evidence.md) | 証拠・由来（`REQ-C07`・`REQ-C08`） | 突合完了・5択未実施 | 候補3件。新規メイン要求候補1件（生成AIと人間の貢献の切り分け）。**現行に「CRediT」「貢献」の記述は皆無**。由来自体は `B-13` と `Provenance` が厚く扱う |
| [`crosswalk-04-artifacts.md`](crosswalk-04-artifacts.md) | 成果物・外部連携（`REQ-C09`・`REQ-C11`） | 突合完了・5択未実施 | 候補7件を6件へ統合。**新規メイン要求候補は0件**。第8章が段階2以降を第2フェーズへ先送りしているため3件を「時期尚早」とした。**4領域の総括を5節に置く** |

✅ **4領域すべての突合が完了した**（2026年9月2日）。総括は [`crosswalk-04-artifacts.md`](crosswalk-04-artifacts.md) 5節にある。

**36件の候補のうち、現行要求に収まらない新規メイン要求候補は6件**（X-01、`PR-M-08`、`PR-M-09`、`PR-M-13`、`ARF-M-12`、`ARF-M-08`）。
⚠️ **突合はすべて候補の要求文1行にもとづく。** 5択の前に、6件の全文を確認すること。
⚠️ **訂正（2026-09-02）**: 各分析文書の「重複要確認」（全11箇所）を読まずに突合していた。5件を訂正済み。
⚠️ **工程モデルが確定要件でないため、Y-01 と `AR-M-03` は判定できていない。**

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
| [`ml-research-practice-advice.md`](ml-research-practice-advice.md) | Karpathy「A Survival Guide to a PhD」・Marek Rei「Advice for students doing research projects in ML/NLP」・LiveResearchBench（arXiv:2510.14240）・Hadad ほか（J. Informetrics 20(3), 101816） | 分析完了・5択未実施・現行要件との突合未実施 | メイン要求候補3件（うち新規見込みは分割の由来の記録1件のみ）。実行回数と分散は`academic-research-skills-frameworks.md`の既出候補を第2の出典で補強。研究生活の管理と書誌計量は対象外と判断 |
| [`simclr-handson-deck.md`](simclr-handson-deck.md) | 角居雄太「論文再現実装ハンズオン #4 対照学習」DL COMMUNITY, 松尾・岩澤研究室, 東京大学, 2026（解説する原典: Chen, T.; Kornblith, S.; Norouzi, M.; Hinton, G. *Proc. 37th ICML*, 2020, 1597–1607. [arXiv:2002.05709](https://doi.org/10.48550/arxiv.2002.05709)） | 分析完了・5択未実施・現行要件との突合未実施 | メイン要求候補16件、サブ要求候補44件、非機能要求8件。暫定IDは`PR-M-xx`/`PR-S-xx-y`で、`REQ-Cxx`体系への合流は5択時に行う |

## 追加分析の共通手順

1. 対象節の開始・終了境界を本文とページ画像で確認する。
2. 本文、脚注、参考文献の範囲を分ける。
3. 現行要件と要件定義変更案へ対応付ける。
4. メイン要求、サブ要求、要求にしない記述へ分類する。
5. 新しいメイン要求候補は5択へ進める。
6. 選択後に変更案を更新し、利用者の承認後に確定要件へ反映する。

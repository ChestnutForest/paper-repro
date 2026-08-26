# ドキュメント索引

`paper-repro` のドキュメント一覧。目的から探せるように分類してある。

---

## 🔁 まず開くもの（日々の作業）

| ファイル | 内容 |
|---|---|
| [`daily-routine.md`](daily-routine.md) | **日々のルーチンワーク**。開発の開始〜終了までの手順 |
| [`dev-startup.md`](dev-startup.md) | 起動スクリプトの使い方・実行後の確認事項チェックリスト |

## 🤖 AI開発指示（Claude Code / Codex 共通）

| ファイル | 内容 |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | **共通正本**。設計原則、規約、検証、Claude Code ↔ Codex の引き継ぎ手順 |
| [`../CLAUDE.md`](../CLAUDE.md) | Claude Code用エントリーポイント。共通指示として `AGENTS.md` を読み込ませる |

## 🚀 環境構築（初回・OS別）

| ファイル | 内容 |
|---|---|
| [`getting-started-vscode-windows.md`](getting-started-vscode-windows.md) | **Windows版** Claude Code / Codex の開発開始・引き継ぎ手順 |
| [`getting-started-vscode.md`](getting-started-vscode.md) | Mac / Linux版の同手順 |

## 📐 設計（何を作るか）

| ファイル | 内容 |
|---|---|
| [`traceability-matrix.md`](traceability-matrix.md) | **トレーサビリティ・マトリクス（XDDP）**。仕様ごとに要求・設計・実装・テスト・画面・リリースの進捗を追う |
| [`requirements-usdm.md`](requirements-usdm.md) | **USDM 形式の要求仕様書**。要求を振る舞いとして書き、動詞ごとに仕様を導く。`REQ-C01` は24仕様まで展開済み |
| [`requirements.md`](requirements.md) | **要件定義の正本（v0.2）**。確定要求`REQ-C01`〜`REQ-C11`とサブ要求12件、受入基準、実装単位との対応表 |
| [`requirements-update-workflow.md`](requirements-update-workflow.md) | 一次資料の限定抽出、現行要件との比較、5択、変更案作成までの検討手順 |
| [`requirements-change-proposal.md`](requirements-change-proposal.md) | 選択済み11件と小節別サブ要求候補を統合した要件定義変更案。利用者の承認待ち |
| [`references.md`](references.md) | **参考文献**。一次資料の書誌情報と引用の方針。各分析文書は短縮形で引用する |
| [`arch-guide/arc-screen-rules.md`](arch-guide/arc-screen-rules.md) | **画面の共通ルール**。エリア構成・配色・フォント・エラー表示・多言語・承認ゲートの見せ方 |
| [`arch-guide/arc-screen-flow.md`](arch-guide/arc-screen-flow.md) | **画面遷移**。承認ゲートを通る線・異常系・引かなかった線とその理由 |
| [`arch-guide/arc-screen-list.md`](arch-guide/arc-screen-list.md) | **画面一覧**。7画面の識別子・分類・対応要求と階層構造 |
| [`arch-guide/screens/`](arch-guide/screens/) | **画面ごとのレイアウト設計書**（7ファイル） |
| [`arch-guide/arc-screen.md`](arch-guide/arc-screen.md) | **画面アーキテクチャ設計の枠組み（IPA 画面編準拠）**。6つの工程成果物、ID体系、合意成熟度の読み替え、6編の作成順序 |
| [`arch-guide/arc-datamodel.md`](arch-guide/arc-datamodel.md) | **データモデル仕様（v1.0 確定）**。フェーズ0の2テーブルのDDL、ENUM、状態遷移表、矛盾9件の解消、決定の記録3件 |
| [`references-usdm-ipa.md`](references-usdm-ipa.md) | **USDM と IPA ガイドラインの一次情報**。7分冊の個別URL、著作権上の使用条件、採用範囲。Processloop から移設 |
| [`requirements-analysis/README.md`](requirements-analysis/README.md) | 一次資料分析の索引と、確定要件・変更案・決定台帳との役割分担 |
| [`requirements-analysis/section-1.2-reading-techniques.md`](requirements-analysis/section-1.2-reading-techniques.md) | 「1.2 論文を読み解く技術」と現行要件の比較。`REQ-C10`・`REQ-C11`とサブ要求候補10件 |
| [`requirements-analysis/section-1.2.1-reading-environment.md`](requirements-analysis/section-1.2.1-reading-environment.md) | 「1.2.1 論文を読む環境の構築」の詳細検証。`REQ-C10`の根拠とサブ要求候補4件を具体化 |
| [`requirements-analysis/section-1.2.1.1-paper-acquisition.md`](requirements-analysis/section-1.2.1.1-paper-acquisition.md) | 「1.2.1.1 論文を入手する」の限定分析。新規メイン要求なし、`REQ-C03-S01`・`REQ-C07-S01`を具体化 |
| [`requirements-analysis/section-1.2.1.2-electronic-reading.md`](requirements-analysis/section-1.2.1.2-electronic-reading.md) | 「1.2.1.2 論文を電子媒体で読む」の限定分析。新規メイン要求なし、`REQ-C09-S01`を要求文と受入基準まで具体化 |
| [`requirements-analysis/section-1.2.1.3-human-authorship.md`](requirements-analysis/section-1.2.1.3-human-authorship.md) | 「1.2.1.3 論文は人間が書いたものであることを認識する」の限定分析。`REQ-C10`の根拠を補強し、`REQ-C10-S04`を具体化 |
| [`requirements-analysis/section-1.2.2-independent-reading-techniques.md`](requirements-analysis/section-1.2.2-independent-reading-techniques.md) | 「1.2.2 自分の力で論文を読み解くための技術」の限定分析。新規メイン要求なし、既存サブ要求候補8件を要求文と受入基準まで具体化 |
| [`requirements-analysis/section-1.2.2.1-discussion-conditions.md`](requirements-analysis/section-1.2.2.1-discussion-conditions.md) | 「1.2.2.1 議論が成立する条件を確認する」の限定分析。新規メイン要求なし、`REQ-C10-S01`〜`S03`を詳細化 |
| [`requirements-analysis/section-1.2.2.2-concrete-examples.md`](requirements-analysis/section-1.2.2.2-concrete-examples.md) | 「1.2.2.2 具体例を構成する」の限定分析。新規メイン要求なし、`REQ-C04-S01`・`REQ-C10-S03`を詳細化 |
| [`requirements-analysis/section-1.2.2.3-implementation-reading.md`](requirements-analysis/section-1.2.2.3-implementation-reading.md) | 「1.2.2.3 実装を読み解いて理解を深める」の限定分析。新規メイン要求なし、`REQ-C05-S01`を詳細化 |
| [`requirements-analysis/section-1.2.2.4-important-references.md`](requirements-analysis/section-1.2.2.4-important-references.md) | 「1.2.2.4 重要となる参考文献は踏み込んで調べる」の限定分析。新規メイン要求なし、`REQ-C09-S02`を詳細化 |
| [`requirements-analysis/section-1.2.2.5-output-for-understanding.md`](requirements-analysis/section-1.2.2.5-output-for-understanding.md) | 「1.2.2.5 アウトプットすることで理解を深める」の限定分析。新規メイン要求なし、`REQ-C04-S02`・`REQ-C09-S03`を詳細化 |
| [`requirements-analysis/section-1.2.3-external-help.md`](requirements-analysis/section-1.2.3-external-help.md) | 「1.2.3 自分以外の力も借りて論文を読み解くための技術」導入部の暫定分析。暫定サブ要求候補`REQ-C07-S02`・`REQ-C09-S04`を提案 |
| [`requirements-analysis/section-1.2.3.1-small-group-discussion.md`](requirements-analysis/section-1.2.3.1-small-group-discussion.md) | 「1.2.3.1 少人数で深く議論する」の限定分析。輪講や読み会は人間同士の活動のため新規要求なし、既存2件の根拠を補強 |
| [`requirements-analysis/section-1.2.3.2-contacting-authors.md`](requirements-analysis/section-1.2.3.2-contacting-authors.md) | 「1.2.3.2 論文の著者に直接質問する」の限定分析。`REQ-C09-S05`を提案し、保留中の`REQ-C07-S02`を確定案へ |
| [`requirements-analysis/section-1.2.3.3-web-discussion.md`](requirements-analysis/section-1.2.3.3-web-discussion.md) | 「1.2.3.3 ウェブ上で議論する」の限定分析。公開議論由来の情報を扱う`REQ-C07-S03`を提案 |
| [`requirements-analysis/section-1.2.3.4-using-generative-ai.md`](requirements-analysis/section-1.2.3.4-using-generative-ai.md) | 「1.2.3.4 生成AIを使う」の限定分析。製品の中核機能を直接扱う唯一の小節。`REQ-C04-S03`・`REQ-C10-S05`を提案 |
| [`requirements-analysis/academic-research-skills-frameworks.md`](requirements-analysis/academic-research-skills-frameworks.md) | 学術スキルの8枠組み（SCONUL・ACRL・Vitae RDF・ACM badging・ML再現性チェックリスト・FAIR・CRediT・ALLEA）からの詳細抽出。メイン要求候補13件 |
| [`requirements-analysis/academic-research-skills.md`](requirements-analysis/academic-research-skills.md) | 英国・アイルランドの大学科目「Academic and Research Skills」からの要求抽出。引用管理・研究倫理・プロジェクト計画の3件が新規メイン要求候補 |
| [`requirements-analysis/simclr-handson-deck.md`](requirements-analysis/simclr-handson-deck.md) | SimCLR解説資料からの要求抽出。メイン要求候補16件・サブ要求候補44件。5択と現行要件との突合は未実施 |
| [`requirements-decisions/batch-01-options.md`](requirements-decisions/batch-01-options.md) | 要件選択の第1バッチ。REQ-C01〜REQ-C05の5択、選択結果、理由、影響範囲、受入基準 |
| [`requirements-decisions/batch-02-options.md`](requirements-decisions/batch-02-options.md) | 要件選択の第2バッチ。REQ-C06〜REQ-C09の5択、選択結果、段階開発条件、受入基準 |
| [`requirements-decisions/batch-03-options.md`](requirements-decisions/batch-03-options.md) | 追加要件選択の第3バッチ。REQ-C10・REQ-C11の選択結果、理由、受入基準、段階開発条件 |
| [`product-design.md`](product-design.md) （**v0.2・要件v0.2準拠**） | 初期リリース設計。画面遷移・APIエンドポイント・技術スタック |
| [`tech-stack.md`](tech-stack.md) （**道具の一覧の正本**） | 技術スタック解説。各技術の役割と選定理由 |
| [`test-papers.md`](test-papers.md) | **動作確認に使うテスト論文**。基準論文の書誌・ライセンス・採用理由と、フェーズごとに画面で見えるべきこと |
| [`roadmap.md`](roadmap.md) （**進捗の正本**） | 開発ロードマップ。フェーズ0〜6と進捗、将来のDB候補 |

## 🧭 設計判断の指針（どう作るか）

| ディレクトリ | 内容 |
|---|---|
| [`arch-guide/`](arch-guide/) | CCAF（CCAR-F試験ガイド）由来の設計指針、AIコーディングエージェント依頼テンプレート、**適用率インジケーター** |

主要ファイル：
- [`arch-guide/README.md`](arch-guide/README.md) — 設計指針本体（フェーズ別の適用方針）
- [`arch-guide/ccaf-patterns.md`](arch-guide/ccaf-patterns.md) — CCAF 5ドメインとの対応表
- [`arch-guide/claude-code-playbook.md`](arch-guide/claude-code-playbook.md) — Claude Code / Codex 共通テンプレA〜DとClaude固有テンプレE
- [`arch-guide/coverage-rubric.md`](arch-guide/coverage-rubric.md) — 適用率の算定規則
- [`arch-guide/coverage-remeasure-howto.md`](arch-guide/coverage-remeasure-howto.md) — 再計測の運用手順
- `arch-guide/ccaf-coverage-YYYY-MM-DD.md` — 適用率レポート（節目ごとに追加）

## 📓 記録（何をやってきたか）

| ディレクトリ / ファイル | 内容 |
|---|---|
| [`devlog/`](devlog/) | **日次開発ログ**。Q&A知識カード、決定ログ、つまずき、画面キャプチャ記録 |
| [`history/project-history.md`](history/project-history.md) | **プロジェクト経緯**。指示と成果物の対応を日付順に整理 |
| [`worknotes/`](worknotes/) | **作業メモ**。分析をどう反映したか、なぜその方法を選んだか、何を保留したか |
| [`worknotes/pre-approval-screening.md`](worknotes/pre-approval-screening.md) | **承認前の矛盾スクリーニング**。新規32件と選択済み11件を突き合わせ、真の矛盾0件・要手当て2件・要注意4件と判定 |
| [`devlog/devlog-2026-08-25.md`](devlog/devlog-2026-08-25.md) | **フェーズ0-1の実装ログ**。状態表現の2列分割、`course`必須化、承認ゲートの迂回防止と、そのバグ修正 |
| [`worknotes/id-unification-and-phase-provisional.md`](worknotes/id-unification-and-phase-provisional.md) | **ID一本化とPhase暫定化の決定記録**。`REQ-Cxx`を一次識別子とし、`F-xx`等を二次識別子として維持する方針を確定 |

## 🔍 知識の活用

| ファイル | 内容 |
|---|---|
| [`notebooklm-prompts.md`](notebooklm-prompts.md) | NotebookLM 活用プロンプト集（スライド生成・テーマ別深掘り） |

---

## ディレクトリ構成の方針

現在は `docs/` 直下をフラットに保ち、**性質が異なり継続的に増えるものだけ**を
サブディレクトリに分けている（`arch-guide/`・`devlog/`・`history/`・`requirements-analysis/`・`requirements-decisions/`・`worknotes/`）。

ファイル数が増えて見通しが悪くなったら、`guide/`（手順）と `design/`（設計）への
分割を検討する。その際は README とドキュメント間の相互リンクの更新が必要になる。

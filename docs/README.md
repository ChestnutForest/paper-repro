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
| [`requirements.md`](requirements.md) | 要件定義。human-in-the-loop、サンドボックスのリスク |
| [`requirements-update-workflow.md`](requirements-update-workflow.md) | 一次資料の限定抽出、現行要件との比較、5択、変更案作成までの検討手順 |
| [`requirements-change-proposal.md`](requirements-change-proposal.md) | 選択済み11件と小節別サブ要求候補を統合した要件定義変更案。利用者の承認待ち |
| [`requirements-analysis/README.md`](requirements-analysis/README.md) | 一次資料分析の索引と、確定要件・変更案・決定台帳との役割分担 |
| [`requirements-analysis/section-1.2-reading-techniques.md`](requirements-analysis/section-1.2-reading-techniques.md) | 「1.2 論文を読み解く技術」と現行要件の比較。`REQ-C10`・`REQ-C11`とサブ要求候補10件 |
| [`requirements-analysis/section-1.2.1-reading-environment.md`](requirements-analysis/section-1.2.1-reading-environment.md) | 「1.2.1 論文を読む環境の構築」の詳細検証。`REQ-C10`の根拠とサブ要求候補4件を具体化 |
| [`requirements-analysis/section-1.2.1.1-paper-acquisition.md`](requirements-analysis/section-1.2.1.1-paper-acquisition.md) | 「1.2.1.1 論文を入手する」の限定分析。新規メイン要求なし、`REQ-C03-S01`・`REQ-C07-S01`を具体化 |
| [`requirements-analysis/section-1.2.1.2-electronic-reading.md`](requirements-analysis/section-1.2.1.2-electronic-reading.md) | 「1.2.1.2 論文を電子媒体で読む」の限定分析。新規メイン要求なし、`REQ-C09-S01`を要求文と受入基準まで具体化 |
| [`requirements-analysis/section-1.2.1.3-human-authorship.md`](requirements-analysis/section-1.2.1.3-human-authorship.md) | 「1.2.1.3 論文は人間が書いたものであることを認識する」の限定分析。`REQ-C10`の根拠を補強し、`REQ-C10-S04`を具体化 |
| [`requirements-analysis/section-1.2.2-independent-reading-techniques.md`](requirements-analysis/section-1.2.2-independent-reading-techniques.md) | 「1.2.2 自分の力で論文を読み解くための技術」の限定分析。新規メイン要求なし、既存サブ要求候補8件を要求文と受入基準まで具体化 |
| [`requirements-analysis/section-1.2.2.1-discussion-conditions.md`](requirements-analysis/section-1.2.2.1-discussion-conditions.md) | 「1.2.2.1 議論が成立する条件を確認する」の限定分析。新規メイン要求なし、`REQ-C10-S01`〜`S03`を詳細化 |
| [`requirements-analysis/section-1.2.2.2-concrete-examples.md`](requirements-analysis/section-1.2.2.2-concrete-examples.md) | 「1.2.2.2 具体例を構成する」の限定分析。新規メイン要求なし、`REQ-C04-S01`・`REQ-C10-S03`を詳細化 |
| [`requirements-decisions/batch-01-options.md`](requirements-decisions/batch-01-options.md) | 要件選択の第1バッチ。REQ-C01〜REQ-C05の5択、選択結果、理由、影響範囲、受入基準 |
| [`requirements-decisions/batch-02-options.md`](requirements-decisions/batch-02-options.md) | 要件選択の第2バッチ。REQ-C06〜REQ-C09の5択、選択結果、段階開発条件、受入基準 |
| [`requirements-decisions/batch-03-options.md`](requirements-decisions/batch-03-options.md) | 追加要件選択の第3バッチ。REQ-C10・REQ-C11の選択結果、理由、受入基準、段階開発条件 |
| [`product-design.md`](product-design.md) | 初期リリース設計。画面遷移・APIエンドポイント・技術スタック |
| [`tech-stack.md`](tech-stack.md) | 技術スタック解説。各技術の役割と選定理由 |
| [`roadmap.md`](roadmap.md) | 開発ロードマップ。フェーズ0〜6と進捗、将来のDB候補 |

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

## 🔍 知識の活用

| ファイル | 内容 |
|---|---|
| [`notebooklm-prompts.md`](notebooklm-prompts.md) | NotebookLM 活用プロンプト集（スライド生成・テーマ別深掘り） |

---

## ディレクトリ構成の方針

現在は `docs/` 直下をフラットに保ち、**性質が異なり継続的に増えるものだけ**を
サブディレクトリに分けている（`arch-guide/`・`devlog/`・`history/`・`requirements-analysis/`・`requirements-decisions/`）。

ファイル数が増えて見通しが悪くなったら、`guide/`（手順）と `design/`（設計）への
分割を検討する。その際は README とドキュメント間の相互リンクの更新が必要になる。

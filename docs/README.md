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
| [`requirements-decisions/batch-01-options.md`](requirements-decisions/batch-01-options.md) | 要件選択の第1バッチ。REQ-C01〜REQ-C05の5択と回答欄 |
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
サブディレクトリに分けている（`arch-guide/`・`devlog/`・`history/`・`requirements-decisions/`）。

ファイル数が増えて見通しが悪くなったら、`guide/`（手順）と `design/`（設計）への
分割を検討する。その際は README とドキュメント間の相互リンクの更新が必要になる。

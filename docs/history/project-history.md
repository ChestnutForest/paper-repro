# プロジェクト経緯（指示と対応の記録）

`paper-repro` の開発で、どんな指示に対して何を作ったかを日付順に整理したもの。
「なぜこの成果物があるのか」を後から辿るための資料。

- 日次の詳細は [`../devlog/`](../devlog/)
- 今後の計画は [`../roadmap.md`](../roadmap.md)

> 注：この一覧は特定のチャットで確認できた範囲をまとめたもので、
> 日付は作業時の記録に基づく。網羅性を保証するものではない。

---

## 2026-07-13：スキル整備とStructEval分析

| 指示 | 対応・成果物 |
|---|---|
| 論文再現手順のスキル化 | `arxiv-paper-repro` v2.0.0 作成（三段階読解法、タイプA/B分岐） |
| スキル名の変更・マスター運用 | `skill_refy.md`＋`build.sh` の二重構成を確立 |
| 発火の混線を解消したい | descriptionの書き分け（`english-parsing` との境界を明示） |
| StructEval論文の分析 | Phase 0〜3実施。公式実装（Apache-2.0）を発見、縮小版方針に決定 |

## 2026-07-15：スキル安全更新とStructEval-T解説

| 指示 | 対応・成果物 |
|---|---|
| 既存スキルを壊さず更新したい | `skill-safe-update` に「マスター運用」「出力規約」を追記（3保証を機械検証） |
| StructEval-Tを分かりやすく | 5形式・採点3段階・dot-path記法を解説 |

## 2026-07-16：要件定義・設計・雛形作成

| 指示 | 対応・成果物 |
|---|---|
| ツールの要件定義 | `requirements.md`（human-in-the-loop、サンドボックスが最大リスク） |
| MVPの詳細設計 | `product-design.md`（5画面・API・技術スタック。タイプB＋公式実装ありに限定） |
| VS Codeで開発する手順とフォルダ作成 | プロジェクト雛形一式（CLAUDE.md、backend、frontend、docs） |
| 拡張機能のインストール手順 | 推奨7拡張の一括導入手順 |
| Windows用の手順書がほしい | `getting-started-vscode-windows.md` を新規作成 |

## 2026-07-17：環境構築・GitHub・スキル生成

| 指示 | 対応・成果物 |
|---|---|
| `C:\Users\kazuy\projects` への配置方法 | 配置手順＋Windows特有の注意（二重フォルダ、隠しファイル） |
| `.env` の作り方 | `Copy-Item` での作成（`.env.txt` 問題の回避） |
| GitHubへリポジトリ追加 | `git init`〜`push -u origin main`、初回認証まで完走 |
| Gitのバージョン確認 | 2.53 → 2.55.0.windows.3 へ更新 |
| 多言語対応の方針 | i18n方針を `CLAUDE.md` に追記しpush |
| 「今日の分を資産化」のスキル化 | `paper-repro-devlog` 生成（RAG制約・捏造禁止つき） |
| 4日分のdevlog作成 | 7/13・15・16・17分を生成 |
| NotebookLM用スライドプロンプト | `slide-prompt.md` 作成 |
| 拡張機能の一括インストール | `@recommended` からの導入、7つ完了 |
| Docker起動〜Swagger UI | PostgreSQL/Redis起動、uvicorn起動、`/health`・`POST projects` 動作確認 |
| フロントエンド起動 | `npm run dev`、フロント↔バック連携を確認（土台完成） |
| 土台をコミット | `chore: scaffold running frontend and backend for MVP Step 1` |
| 画像も含めて資産化 | devlogスキルに「画面キャプチャ記録」章を追加、環境構築編を生成 |

## 2026-07-27：ライセンス・ロードマップ・PostgreSQL化

| 指示 | 対応・成果物 |
|---|---|
| MITかGPLか | MITを提案・採用。`LICENSE` 作成→混入修正→クリーンアップ |
| 開発ロードマップ | `roadmap.md`（フェーズ0〜6）作成 |
| TiDBに変更したい | 現時点は非推奨と説明。将来候補としてロードマップに記録 |
| フェーズ0-1の依頼方法 | Claude Codeへ「計画先行」で依頼→実装→テスト3 passed→コミット `733a359` |
| devlogを一元管理したい | `docs/devlog/` に6ファイル＋索引を配置、コミット `fd9065d` |
| その運用をスキル化 | devlogスキルに `docs/devlog/` 運用を追記 |

## 2026-07-28：NotebookLM活用

| 指示 | 対応・成果物 |
|---|---|
| テーマ別の深掘りプロンプト | 決定ログ／つまずき／i18n／PostgreSQL の4種を設計 |
| プロンプト集をファイル化 | `notebooklm-prompts.md`（スライド用A、チャット用B、テーマ別C） |

## 2026-08-03：CCAF適用・運用整備・プロフィール

| 指示 | 対応・成果物 |
|---|---|
| CCAF試験ガイドを開発に適用 | `paper-repro-arch-guide` スキル作成、`docs/arch-guide/` へ配置 |
| 適用状況を一目で見たい | v1.1へ。トレーサビリティ表＋適用率インジケーター（総合15.2%）を作成 |
| 「前回ファイル」とは | 再計測手順書 `coverage-remeasure-howto.md` を作成 |
| 日々のルーチン化 | `daily-routine.md` 作成、READMEから参照 |
| 起動スクリプトがほしい | `start-dev.ps1` / `start-dev.sh`＋`dev-startup.md`＋起動スキル |
| フレームワークの解説 | `tech-stack.md` 作成、READMEから参照 |
| 関連プロジェクトを示したい | READMEに「関連プロジェクト」節（学ぶ→実践する） |
| プロフィールREADME | `ChestnutForest/ChestnutForest` を作成、Mermaid図を採用 |
| リポジトリの整理 | Description・Topics設定、`docs/README.md` 索引と本ファイルを追加 |

## 2026-08-15：paper-reproへの改称・正式版開発への移行

| 指示 | 対応・成果物 |
|---|---|
| 製品名とリポジトリ名から `-mvp` 接尾辞を外したい | 製品名、ローカルフォルダ、GitHubリポジトリ、コード、手順書の表記を `paper-repro` に統一 |
| 最小実行可能製品だけで終わらせず正式版として開発したい | 現在のタイプB中心の範囲を「初期リリース」と再定義し、タイプA・GPU・レンダリング・LLM-as-a-Judgeを後続リリースの対象として明記 |
| 設計文書名を製品方針と同期したい | `product-design.md` へ改名し、初期リリース設計が製品全体の上限ではないことを明記 |
| 過去の判断履歴を保持したい | 過去devlogの当時の初期開発判断は履歴として維持し、製品名だけを現名称へ統一 |

## 2026-08-15：Claude Code / Codex 共通開発指示への統合

| 指示 | 対応・成果物 |
|---|---|
| Claude CodeとCodexの両方で継続開発したい | `AGENTS.md` をプロジェクト共通の正本として追加し、設計原則・規約・検証・引き継ぎ手順を一元化 |
| `CLAUDE.md` と `AGENTS.md` の内容ずれを防ぎたい | `CLAUDE.md` をClaude Code用エントリーポイントへ整理し、共通内容は `AGENTS.md` を全文参照する構成に変更 |
| 切り替え時に開発データを共有したい | 会話履歴ではなくGit・現行文書・devlogで、判断理由・未解決事項・次の一手を引き継ぐ手順を明記 |
| READMEと関連文書も同期したい | README、文書索引、日次手順、OS別開始手順、技術スタック、ロードマップ、設計指針を更新 |
| commit/push結果URLのスキルを登録したい | 登録済みの `github-result-urls` v1.3を確認し、重複するスキルは作成せず既存スキルを継続利用 |

## 2026-08-28：Claude Code / Codex / Antigravity IDE共通スキルへの統合

| 指示 | 対応・成果物 |
|---|---|
| paper-repro開発で作ったローカルスキルだけを一本化したい | プラグインキャッシュの`arxiv-paper-repro`と`paper-repro-devlog`をリポジトリへ正本化し、processloop由来の個人用`github-result-urls`は除外 |
| リポジトリ内のSkill関連ファイルを調査したい | 既存の2つの`SKILL.md`、`AGENTS.md`、`CLAUDE.md`、人間向け手順書を確認し、要件調査文書との違いも分類 |
| 3つのAI開発環境で共通利用したい | `.agents/skills`を本文正本、`.claude/skills`をClaude Code用の参照入口とする3スキル構成へ統合 |
| 矛盾を除去して検証したい | zip・`present_files`・架空SHA・URL件数制限を廃止し、`scripts/validate-agent-skills.ps1`で構造、参照、frontmatter、文字コードを検証可能にした |

## 2026-08-29：GitHub登録済みスキルだけを使用する方針

| 指示 | 対応・成果物 |
|---|---|
| GitHubリポジトリのスキルだけで仕事をしたい | `paper-repro-skill-source-policy`を追加し、他スキルより先にGit追跡・HEAD・必要時のリモートSHAを確認する規則を定義 |
| Windowsローカルの旧スキルを適切に扱いたい | 移行済みキャッシュは非アクティブな移行元とし、呼び出し・直接編集・直接削除を禁止。必要時はプラグイン単位で無効化する方針を記録 |
| 3環境で同じ制約を使いたい | `AGENTS.md`、`CLAUDE.md`、`.claude/skills`、README、文書索引、検証スクリプトを4スキル構成へ同期 |

## 2026-08-29：システム振舞い設計の具体化

| 指示 | 対応・成果物 |
|---|---|
| USDMで整理した要求全体からシステム振舞いを設計したい | 確定要求23件を6グループ47業務へ割り当て、一覧・フロー・業務説明・共通ルールを作成 |
| IPAのシステム振舞い編2冊で検査したい | 事前・事後条件、入出力データ種別、基本・代替・例外シナリオ、トリガー、共通ルールの構成項目を再点検して枠組みv0.3へ反映 |
| 既存実装との状態差を明らかにしたい | 状態遷移をガイド外の補助資料へ分離し、`Phase`・`Status`・`ApprovalKind`・遷移集合の一致と未実装箇所を記録 |
| READMEから進捗を確認したい | 設計工程表を4成果物作成済みに更新し、USDM未展開要求は再検査待ち、実装フェーズ0は不変と明記 |

## 2026-08-29：設計スキルの正本化とMermaid実描画検証

| 指示 | 対応・成果物 |
|---|---|
| 18件のシステム振舞い設計を支えたスキルを更新したい | `docs/arch-guide/README.md`に残っていた`paper-repro-arch-guide` v1.2を、`.agents/skills`正本と`.claude/skills`入口を持つv1.3.0へ移行 |
| Mermaid CLIを導入して描画検証したい | `@mermaid-js/mermaid-cli` 11.16.0を固定し、変更Markdownの全ブロックを一時SVGへ変換して件数一致まで確認する検証スクリプトを追加 |
| 3環境で同じ検証を使いたい | `package.json`の`validate:mermaid`を共通入口とし、AGENTS、Claude入口、文書索引、スキル検証を5スキル構成へ同期 |

## 2026-08-29：GitHub URLのチャット内個別コピー

| 指示 | 対応・成果物 |
|---|---|
| VS CodeのターミナルではなくチャットでURLをコピーしたい | `paper-repro-commit-output`をv2.2.0へ更新し、1 URLごとに独立した`text`コードブロックと見出しを出すことを必須化 |
| コマンドがURLを出す案内だけでは不足 | ターミナル出力を検証用の補助情報に限定し、チャット内URL一覧を省略できない禁止規則を追加 |
| 将来の退行を防ぎたい | 共通指示、人間向け運用ガイド、Claude入口、スキル検証を同じ出力契約へ同期 |

---

## 全体の流れ

**スキル整備（7/13-15）→ 設計（7/16）→ 環境構築と土台完成（7/17）
→ 永続化とライセンス（7/27）→ 知識活用（7/28）→ CCAF適用と運用整備（8/3）
→ paper-reproへの改称と正式版開発への移行（8/15）
→ Claude Code / Codex 共通開発指示への統合（8/15）
→ Claude Code / Codex / Antigravity IDE共通スキルへの統合（8/28）
→ GitHub登録済みスキル限定ポリシー（8/29）
→ システム振舞い設計の具体化（8/29）
→ 設計スキルの正本化とMermaid実描画検証（8/29）
→ GitHub URLのチャット内個別コピー（8/29）**

前半は「作るものを決める」、中盤は「動かす」、後半は「進め方を仕組みにする」
という重心の移り方をしている。

## 更新方針

- 節目（フェーズ完了、大きな方針転換）のタイミングで追記する。
- 日次の細かい記録は `docs/devlog/` が担当するため、ここには**指示と成果物の対応**だけを残す。

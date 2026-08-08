# プロジェクト経緯（指示と対応の記録）

`paper-repro-mvp` の開発で、どんな指示に対して何を作ったかを日付順に整理したもの。
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
| MVPの詳細設計 | `mvp-design.md`（5画面・API・技術スタック。タイプB＋公式実装ありに限定） |
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

---

## 全体の流れ

**スキル整備（7/13-15）→ 設計（7/16）→ 環境構築と土台完成（7/17）
→ 永続化とライセンス（7/27）→ 知識活用（7/28）→ CCAF適用と運用整備（8/3）**

前半は「作るものを決める」、中盤は「動かす」、後半は「進め方を仕組みにする」
という重心の移り方をしている。

## 更新方針

- 節目（フェーズ完了、大きな方針転換）のタイミングで追記する。
- 日次の細かい記録は `docs/devlog/` が担当するため、ここには**指示と成果物の対応**だけを残す。

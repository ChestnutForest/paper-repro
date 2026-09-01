# 開発ログ (devlog)

paper-repro の日次開発ログを一元管理する場所。
`paper-repro-devlog` スキルで「今日の分を資産化して」と生成したファイルをここに置く。
NotebookLM のソースとしても利用する。

## 一覧

| ファイル | 日付 | 内容 |
|---|---|---|
| devlog-2026-07-13.md | 2026-07-13 | 再現実装スキル作成、skill_refy運用、StructEval Phase 0〜3 |
| devlog-2026-07-15.md | 2026-07-15 | skill-safe-update追記、StructEval-Tの高校生向け説明 |
| devlog-2026-07-16.md | 2026-07-16 | 要件定義・MVP設計、VS Code雛形、Windows手順書 |
| devlog-2026-07-17.md | 2026-07-17 | GitHub初回push、Gitの更新、CLAUDE.mdへのi18n方針追記 |
| devlog-2026-07-17-env-setup.md | 2026-07-17 | 環境構築編（拡張機能〜フロント起動、画面キャプチャ20枚） |
| devlog-2026-07-27.md | 2026-07-27 | フェーズ0-1 PostgreSQL化、MITライセンス、ロードマップ |
| devlog-2026-08-15.md | 2026-08-15 | 再起動テスト、フェーズ0-2 状態遷移、アーキテクチャ仕様書の作成 |
| devlog-2026-08-25.md | 2026-08-25 | データモデル仕様v1.0確定、状態表現の2列分割、course必須化、汎用遷移の廃止、ゲートのバグ修正 |
| devlog-2026-09-01.md | 2026-09-01 | docs整合性作業（改名の取りこぼし修正、二重管理解消、worknotesの状態検証、-RequireRemoteSync追加、BR-13反映確認、外部インタフェース編の状態訂正、バッチ編・帳票編の非該当化、ML/NLP研究実践の要求分析） |

## 運用

1. 「今日の分を資産化して」で devlog を生成する
2. このフォルダ（docs/devlog/）に置く
3. `git add docs/devlog/ && git commit -m "docs: add devlog YYYY-MM-DD" && git push`
4. NotebookLM の「ソースを追加」からアップロードする

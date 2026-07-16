# CLAUDE.md — このプロジェクトの取扱説明書（Claude Code 用）

Claude Code はこのファイルを毎回読み込む。**作業を始める前に必ずここを参照すること。**

## このプロジェクトは何か

英語のAI論文（arXiv）を読み解いて再現実装まで支援するツールの **MVP**。
対象は「タイプB（学習なし・公式実装あり）の論文」に限定している。
GPU・レンダリング・LLM-as-a-Judge は MVP スコープ外。

詳しい要件と設計は次を読むこと：
- `docs/requirements.md` — 要件定義
- `docs/mvp-design.md` — 画面遷移・APIエンドポイント・技術スタック

## 技術スタック

- バックエンド: **FastAPI (Python 3.12)** + Celery + Redis + PostgreSQL
- フロントエンド: **Next.js (React) + TypeScript**
- 実行分離: サンドボックス（MVPは CPU のみ・ネットワーク遮断）

## 設計上の絶対原則（変更しないこと）

1. **human-in-the-loop。** 各 Phase 末に承認ゲートがあり、人間の承認なしに次へ進めない。
   全自動化しない。
2. **長時間処理は非同期ジョブ + WebSocket 進捗。** 同期RESTで待たせない。
3. **信頼できない第三者コードは必ずサンドボックスで実行。** ホスト直実行は禁止。
4. **成果物の zip 名は `files_reify_YYYYMMDD_hhmm.zip`（JST基準）。** UTCのまま作らない。
5. **将来的に日英の言語切り替え（i18n）に対応する。** フロントの画面文言は最初から `next-intl` の `t("キー")` 方式で書き、日本語・英語を直接ハードコードしないこと。

## ディレクトリ構成

```
backend/app/
  api/       … FastAPI のルーター（エンドポイント）
  core/      … 設定・DB接続・状態機械
  models/    … SQLAlchemy モデル / Pydantic スキーマ
  services/  … 論文取り込み・実装探索・LLM・スコア照合
  workers/   … Celery タスク（サンドボックス実行など）
frontend/src/
  pages/     … 画面（ダッシュボード, インテーク, 作業台, 検証台, レポート）
  components/… UI部品
  lib/       … API クライアント・WS クライアント
```

## コーディング規約

- Python: 型ヒント必須。`ruff` + `black` で整形。関数には docstring
- TypeScript: strict モード。`any` を避ける
- コミットは小さく。1つの論理変更 = 1コミット
- **秘密情報（APIキー等）を絶対にコミットしない。** `.env` は `.gitignore` 済み

## 作業の進め方（Claude Code への指示）

- 大きな変更の前に、まず変更計画を箇条書きで提示し、承認を得てから実装する
- テストがある機能はテストも同時に更新する
- `docs/` の設計と矛盾する実装をしそうなときは、勝手に進めず確認する
- 不明点は推測で埋めず質問する

## 現在の開発フェーズ

**Step 1: 骨組みを1本通す。**
「arXiv URL 投入 → 論文取り込み → spec 草案 → 手編集 → zip 出力」を、
サンドボックス無しで最短で動かす。まだ横に広げない（縦切り）。
`docs/mvp-design.md` の第6章「実装の着手順」に従う。

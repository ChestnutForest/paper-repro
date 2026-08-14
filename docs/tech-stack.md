# 技術スタック解説

`paper-repro` で使っている技術を、層ごとにまとめる。
「なぜそれを選んだか」も併記しているので、設計判断を振り返るときにも使う。

関連文書：[`product-design.md`](product-design.md)（設計）／[`roadmap.md`](roadmap.md)（導入時期）

---

## 全体構成（3層）

```
[ブラウザ] localhost:3000
    ↓ HTTP /（将来）WebSocket
[フロントエンド] Next.js + React + TypeScript
    ↓ REST API
[バックエンド] FastAPI（Python 3.13）  ← localhost:8000
    ↓ SQLAlchemy
[データ層] PostgreSQL 16 / Redis 7  ← Docker上
```

**設計意図：重い処理は Python、画面は TypeScript という分業。**
評価・スコア照合・ノートブック生成は既存の Python 資産（`t_scorer.py`）を流用したい。
一方で画面は React エコシステムで作るのが速い。
1言語に統一すると、どちらかを二重実装することになるため、あえて分けている。

---

## フロントエンド

### Next.js 14.2.35（フレームワーク本体）

React をベースにした Web アプリのフレームワーク。
ルーティング（URLと画面の対応）、開発サーバー、ビルドの仕組みが最初から揃っており、
素の React より手早く画面が作れる。

現在は **Pages Router** 構成（`src/pages/` にファイルを置くとURLになる方式）。
`index.tsx` が `/` に対応している。

### React 18

画面を「部品（コンポーネント）」の組み合わせで作るライブラリ。Next.js の土台。
現在のダッシュボードでは `useState`（入力欄の値を保持）と
`useEffect`（表示時に一覧を取得）を使用。

### TypeScript 5

JavaScript に「型」を足した言語。`strict` モードにしてあるため、
`Project` や `ProjectState` の形が違うとエディタが即座に指摘する。
初期リリース設計で決めたデータ構造を、コード上で守る仕組み。

### ESLint / Prettier

ESLint がコードの問題を検出し、Prettier が整形を担当。
VS Code の設定で**保存時に自動整形**されるようにしてある（`.vscode/settings.json`）。

---

## バックエンド

### FastAPI 0.115（フレームワーク本体）

Python の Web API フレームワーク。選定理由は3つ。

- **非同期（async）に対応** — 設計方針の「長時間処理を非同期でさばく」に必要
- **WebSocket 対応** — フェーズ2の進捗ストリーム表示に使う
- **Swagger UI を自動生成** — `localhost:8000/docs` の画面は FastAPI がコードから自動生成したもの

### uvicorn 0.32（ASGIサーバー）

FastAPI 自体は「窓口で応対する人」で、
**その窓口を開いて外からのアクセスを受け付けるのが uvicorn**。
`uvicorn app.main:app --reload` で起動しているのがこれ。
ASGI は非同期処理に対応したサーバーの規格を指す。

### Pydantic v2（データ検証）

「受け取るデータ・返すデータの形」を定義し、違反を自動で弾く。
Swagger UI に `422 Validation Error` が説明されているのは、Pydantic が入力を検証しているため。

> 補足：フェーズ0-1で発生した `orm_mode` → `from_attributes` のエラーは、
> Pydantic の v1 → v2 でのルール変更が原因だった。

### SQLAlchemy 2（ORM）

Python のオブジェクトと DB のテーブルを対応づける仕組み。**SQL を直接書かずに DB を操作できる。**

これは意図的な選択で、**DB を差し替えやすくする保険**である。
実際その効果が出ており、本番は PostgreSQL、テストは SQLite（使い捨て）に切り替えられている。
将来 TiDB を検討する際にも効く（→ [`roadmap.md`](roadmap.md) の技術選定メモ）。

### Celery 5 + Redis（非同期ジョブ）— **未実装・フェーズ2で導入**

Celery が「時間のかかる仕事を裏で処理する係」、Redis が「仕事を並べる待ち行列」を担当する。
論文取り込みや LLM 処理を、画面を固まらせずに実行するための仕組み。

### pytest 8（テスト）

`backend/tests/test_smoke.py` を走らせているのがこれ。

### Ruff / Black（整形・検査）

Python 版の ESLint / Prettier にあたる。Ruff は非常に高速なのが特徴。

---

## データ層（Docker上）

### PostgreSQL 16

本番用のデータベース。フェーズ0-1でここに保存する実装を導入した。
**初期リリースの規模には十分**で、枯れており情報が豊富なため詰まったときに調べやすい、という理由で選定。

### Redis 7

高速なメモリ上のデータストア。
現在は起動しているだけで、**フェーズ2で Celery の待ち行列として本格的に使う**。

### Docker / Docker Compose

PostgreSQL と Redis を「コンテナ」として動かす仕組み。
`docker-compose.yml` に構成を書いてあるため、`docker compose up -d` の一発で両方が立ち上がる。
自分のPCに直接インストールしないので、環境が汚れない。

---

## 開発を支える道具

### Claude Code / Codex（AIコーディングエージェント）

設計・実装・検証を支援する開発エージェント。フェーズ0-1の PostgreSQL 化は、
Claude Codeに計画を出させてから実装した。今後はCodexとも同じリポジトリを共有する。
共通の設計原則と作業規約は `AGENTS.md` を正本とし、Claude Codeは `CLAUDE.md` を入口に
その内容を読み、Codexは `AGENTS.md` を直接読む。頼み方のテンプレートは
[`arch-guide/claude-code-playbook.md`](arch-guide/claude-code-playbook.md)。

### Git / GitHub

バージョン管理と公開。MIT ライセンスで公開している。

---

## 将来使う予定（未実装）

| 技術 | 用途 | 導入フェーズ |
|---|---|---|
| Celery + Redis | 非同期ジョブと進捗ストリーム | フェーズ2 |
| next-intl | 日英切り替え（i18n）。共通方針は `AGENTS.md` に記載済み | フェーズ6 |
| gVisor 等のサンドボックス | 信頼できない第三者コードの隔離実行 | フェーズ4 |
| Alembic | DBテーブル構造のマイグレーション管理（`requirements.txt` には導入済み） | 必要時 |
| TiDB | 大規模化・ベクトル検索が必要になった場合のDB候補 | フェーズ6以降で再検討 |

---

## バージョン一覧（2026-08-03時点）

| 区分 | 技術 | バージョン |
|---|---|---|
| フロント | Next.js | 14.2.35 |
| フロント | React | 18 |
| フロント | TypeScript | 5 |
| バック | Python | 3.13.14 |
| バック | FastAPI | 0.115 |
| バック | uvicorn | 0.32 |
| バック | Pydantic | 2 |
| バック | SQLAlchemy | 2 |
| データ | PostgreSQL | 16 |
| データ | Redis | 7 |
| 開発 | Git | 2.55.0.windows.3 |

> 正確な依存バージョンは `backend/requirements.txt` と `frontend/package.json` を参照。

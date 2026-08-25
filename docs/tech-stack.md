# 技術スタック解説

`paper-repro` の開発で使う道具を、層ごとにまとめる。
「なぜそれを選んだか」も併記しているので、設計判断を振り返るときにも使う。
**まだ使っていないが導入済みのもの**も、状態を明記して載せる。

**本書が道具の一覧の正本である。** 同じ一覧を他の文書へ複製しない。

| 関連文書 | 本書との関係 |
|---|---|
| [`product-design.md`](product-design.md) | 設計。どの道具をどこで使うか（4章 技術スタック選定、5章 構成図） |
| [`roadmap.md`](roadmap.md) | 導入時期。未導入の道具がどのフェーズで入るか |
| [`arch-guide/arc-architecture.md`](arch-guide/arc-architecture.md) | 構造。層の分け方と道具の対応 |
| [`arch-guide/arc-datamodel.md`](arch-guide/arc-datamodel.md) | Alembic を当面導入しない決定と、導入する3条件（第4章） |
| [`../AGENTS.md`](../AGENTS.md) | 検査・整形の運用規約（§7 コーディング規約、§7.1 コメントと docstring、§9 検証） |
| [`references.md`](references.md) | 準拠する標準の書誌（PEP 257・PEP 8 は REF-18・REF-19） |
| [`dev-startup.md`](dev-startup.md)／[`daily-routine.md`](daily-routine.md) | 道具の起動と日々の使い方 |

---

## 道具の一覧

依存の実体は `backend/requirements.txt`、`frontend/package.json`、`docker-compose.yml` にある。
本表はそれを役割で読めるようにしたもの。**✅ は現在すでに使っているもの。**

### 実行に必要なもの（バックエンド）

| 道具 | 役割 | 状態 |
|---|---|---|
| Python 3.13 | 実行環境 | ✅ |
| FastAPI | Web API フレームワーク | ✅ |
| uvicorn | ASGI サーバー。FastAPI の窓口を開く | ✅ |
| Pydantic / pydantic-settings | 入出力の検証と設定の読み込み | ✅ |
| SQLAlchemy | ORM。Python オブジェクトと DB テーブルの対応づけ | ✅ |
| psycopg | PostgreSQL のドライバ | ✅ |
| httpx | HTTP クライアント。外部 API 呼び出し用 | 未使用 |
| anthropic | Claude API の SDK | 未使用 |
| python-dotenv | `.env` の読み込み | ✅ |
| Celery | 非同期ジョブの実行 | 未使用（フェーズ2） |
| redis（クライアント） | Celery のブローカーへの接続 | 未使用（フェーズ2） |
| **Alembic** | **DB スキーマのマイグレーション管理** | **導入済みだが未使用**（後述） |

### 評価・照合に使うもの

| 道具 | 役割 | 状態 |
|---|---|---|
| PyYAML / xmltodict / toml | 構造化データの読み書き。スコア照合で使う | 未使用（フェーズ5） |

### 開発を検査するもの

| 道具 | 役割 | 状態 |
|---|---|---|
| pytest | テスト実行 | ✅ |
| **Ruff** | **Python の静的検査（リンタ）** | ✅（後述） |
| **Black** | **Python の整形（フォーマッタ）** | ✅（後述） |

### フロントエンド

| 道具 | 役割 | 状態 |
|---|---|---|
| Next.js / React / TypeScript | 画面の構築 | ✅ |
| next-intl | 日英中の言語切り替え | ✅（`messages/` に3言語） |
| Tailwind CSS / PostCSS / autoprefixer | スタイル | ✅ |
| shadcn/ui 系（Radix Slot、CVA、clsx、tailwind-merge） | UI 部品の土台 | ✅ |
| lucide-react | アイコン | ✅ |
| ESLint / Prettier | 検査と整形 | ✅ |

### 基盤・運用

| 道具 | 役割 | 状態 |
|---|---|---|
| PostgreSQL 16 | 本番のデータベース | ✅ |
| Redis 7 | 待ち行列（起動のみ） | 起動のみ |
| Docker / Docker Compose | PostgreSQL と Redis をコンテナで動かす | ✅ |
| Git / GitHub | バージョン管理と公開 | ✅ |
| Claude Code / Codex | AI コーディングエージェント | ✅ |
| gVisor 等のサンドボックス | 第三者コードの隔離実行 | 未導入（フェーズ4） |

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

### Ruff 0.7（静的検査）

**コードを実行せずに問題を見つける道具（リンタ）。** Python 版の ESLint にあたる。
Rust 製で、同種の道具（Flake8 など）より桁違いに速いのが特徴。

検出するのは、未使用の import や変数、未定義の名前、書式の逸脱など。
実際に本プロジェクトでも `from fastapi import Depends` が未使用であることを検出し、
`F401` として報告した。**整形はしない。指摘するだけ**である点が Black との違い。

```powershell
backend\.venv\Scripts\python.exe -m ruff check backend
```

### Black 24（整形）

**コードの見た目を機械的に統一する道具（フォーマッタ）。** Prettier にあたる。
改行位置、空行、クォートの種類などを、設定ではなく **Black の決めた形**に揃える。
「どう書くか」を議論しなくて済むのが利点で、そのため設定項目がほとんど無い
（"uncompromising" を掲げている）。

既定の行長は88文字。本プロジェクトはこれに従う（PEP 8 の72文字からの逸脱は
[`../AGENTS.md`](../AGENTS.md) §7.1.5 に理由つきで記録）。

**`--check` は指摘するだけで直さない。** 必ず整形を実行してから確認する。
ファイルを絞ると触っていない既存の違反を見逃すため、対象は `backend` 全体にする。

```powershell
backend\.venv\Scripts\python.exe -m black backend; backend\.venv\Scripts\python.exe -m black --check backend
```

> 実例：2026-08-25 に docstring を追加した際、Black が
> 「モジュール docstring の後ろに空行を1つ入れよ」と要求した。
> PEP 257 はこれを明記していないため、規約側（`AGENTS.md` §7.1.2）に書き足した。

### Alembic 1（マイグレーション）— **導入済みだが当面使わない**

**DB のテーブル構造の変更履歴を管理する道具。** 列の追加や型の変更を「リビジョン」として
記録し、前後へ移動できる。`requirements.txt` には入っているが、**まだ使っていない。**

現在は `Base.metadata.create_all()` でテーブルを作り、
スキーマを変えるときは**テーブルごと作り直す**。

```powershell
docker compose down -v; docker compose up -d
```

`-v` はボリュームごと消す指定で、**入っているデータも消える。**

この方針は [`arch-guide/arc-datamodel.md`](arch-guide/arc-datamodel.md) 第4章で決めたもので、
理由は「公開前・利用者1名・捨ててよいデータしか無い段階では、マイグレーションを書く手間が
得られる安全に見合わない」こと。ただし先送りが続かないよう、**導入する条件を3つ**定めてある。

1. 捨てられないデータが入ったとき
2. 利用者が2名以上になったとき
3. フェーズ6の一般公開に着手するとき

`create_all()` は**既存テーブルを変更しない**点に注意する。列を足しても既存の DB には
反映されないため、上のコマンドで作り直すまで実行時エラーになる。

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
| Alembic | DBテーブル構造のマイグレーション管理。**導入済みだが当面使わない。**判断と3つの導入条件は [`arch-guide/arc-datamodel.md`](arch-guide/arc-datamodel.md) 第4章 | 条件を満たしたとき |
| TiDB | 大規模化・ベクトル検索が必要になった場合のDB候補 | フェーズ6以降で再検討 |

---

## バージョン一覧（2026-08-25時点）

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
| 開発 | pytest | 8 |
| 開発 | Ruff | 0.7 |
| 開発 | Black | 24 |
| 開発 | Git | 2.55.0.windows.3 |
| 未使用 | Alembic | 1 |
| 未使用 | Celery | 5 |
| 未使用 | anthropic（SDK） | 0.39 |

> 正確な依存バージョンは `backend/requirements.txt` と `frontend/package.json` を参照。
> **本表と実体が食い違ったら、実体が正しい。**依存を変えたら本書も同じ変更で直す。

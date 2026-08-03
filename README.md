# paper-repro-mvp

英語のAI論文（arXiv）を読み解いて再現実装まで支援するツールの MVP。
対象は「タイプB（学習なし・公式実装あり）」の論文に限定。

- 要件: [`docs/requirements.md`](docs/requirements.md)
- 設計: [`docs/mvp-design.md`](docs/mvp-design.md)
- **技術スタック**: [`docs/tech-stack.md`](docs/tech-stack.md)
- ロードマップ: [`docs/roadmap.md`](docs/roadmap.md)
- Claude Code 向け指示: [`CLAUDE.md`](CLAUDE.md)

---

## 🧱 技術スタック（概要）

| 層 | 技術 | ポート |
|---|---|---|
| フロントエンド | **Next.js 14 + React 18 + TypeScript 5** | 3000 |
| バックエンド | **FastAPI + uvicorn（Python 3.13）** | 8000 |
| データ層 | **PostgreSQL 16 / Redis 7**（Docker上） | 5432 / 6379 |

**重い処理は Python、画面は TypeScript** という分業。
評価・スコア照合の Python 資産を流用するため、バックエンドを Python に寄せている。

各技術の詳細と選定理由 👉 **[`docs/tech-stack.md`](docs/tech-stack.md)**

---

## ⚡ 開発環境の起動（ワンコマンド）

毎回コマンドを打ち分けずに、スクリプト1本で
**PostgreSQL 起動 → バックエンド起動 → Swagger UI を開く**まで実行できる。

**Windows**

```powershell
.\scripts\start-dev.ps1
```

**Mac / Linux**

```bash
./scripts/start-dev.sh
```

使い方・**実行後に確認する事項のチェックリスト**・つまずいたときの対処は
👉 **[`docs/dev-startup.md`](docs/dev-startup.md)**

---

## 🔁 日々のルーチンワーク（まずここを見る）

開発を始める前・終えるときは、**[`docs/daily-routine.md`](docs/daily-routine.md) を開いてなぞる。**

**毎日やること**

1. 前回の [`docs/devlog/`](docs/devlog/) 最新ファイルで「翌日の計画」を確認
2. **環境を起動**（上のワンコマンド → [`docs/dev-startup.md`](docs/dev-startup.md)）
3. 開発（設計で迷ったら [`docs/arch-guide/`](docs/arch-guide/)）
4. テストを回す → `git status` で `.env` が出ないことを確認 → コミット＆プッシュ
5. **「今日の分を資産化して」** で devlog を作り、コミット＆NotebookLMへ

**節目でやること**（フェーズ完了・大きな機能追加のとき）

- CCAF適用率の再計測 → [`docs/arch-guide/coverage-remeasure-howto.md`](docs/arch-guide/coverage-remeasure-howto.md)
- [`docs/roadmap.md`](docs/roadmap.md) の進捗更新

> 適用率の再計測は毎日ではない。数値は機能が実装されて初めて動くため、
> フェーズ完了などのトリガー時に測る。

---

## 必要なもの

- **Node.js 18 以上**（Claude Code と Next.js に必要）
- **Python 3.12 以上**
- **VS Code 1.98.0 以上**
- **Docker Desktop**（PostgreSQL / Redis をコンテナで動かす）
- **Anthropic の有料プラン**（Claude Code 用。Pro/Max/Team/Enterprise のいずれか。APIキーでも可）

## 初回セットアップ

2回目以降は上の「ワンコマンド起動」だけでよい。初回は次を実行する。

```bash
# 1. リポジトリのルートで、環境変数ファイルを用意
cp .env.example .env
#   → .env を開いて ANTHROPIC_API_KEY などを設定

# 2. バックエンドの仮想環境と依存関係
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. フロントエンドの依存関係
cd ../frontend
cp .env.local.example .env.local
npm install
```

以降は `scripts/start-dev.ps1`（または `.sh`）でバックエンドまで起動し、
画面も見るなら別ターミナルで `cd frontend && npm run dev`（http://localhost:3000）。

## VS Code + Claude Code での開発の始め方

**お使いのOSに合った手順書を参照すること**（コマンドが異なるため）:

- **Windows**: [`docs/getting-started-vscode-windows.md`](docs/getting-started-vscode-windows.md)
- **Mac / Linux**: [`docs/getting-started-vscode.md`](docs/getting-started-vscode.md)

要点（共通）：

1. VS Code で **このフォルダ（ルート）を開く**（File → Open Folder）
2. 拡張機能パネル（Ctrl/Cmd+Shift+X）で **"Claude Code"（発行元 Anthropic）** を検索してインストール
3. サイドバーの Spark アイコン（✱）をクリックしてサインイン
4. Claude Code に「`CLAUDE.md` と `docs/mvp-design.md` を読んで、Step 1 の骨組みから始めて」と依頼

## ディレクトリ構成

```
paper-repro-mvp/
├── CLAUDE.md              ← Claude Code が最初に読む指示書
├── README.md
├── .env.example          ← 環境変数のテンプレート（.env にコピーして使う）
├── docker-compose.yml    ← PostgreSQL + Redis
├── .vscode/              ← VS Code 推奨設定・拡張機能
├── scripts/
│   ├── start-dev.ps1         ← 開発環境の起動（Windows）
│   └── start-dev.sh          ← 開発環境の起動（Mac / Linux）
├── docs/
│   ├── tech-stack.md         ← 技術スタック解説
│   ├── dev-startup.md        ← 起動スクリプトの使い方・確認事項
│   ├── daily-routine.md      ← 日々のルーチンワーク
│   ├── requirements.md       ← 要件定義
│   ├── mvp-design.md         ← MVP設計
│   ├── roadmap.md            ← 開発ロードマップ
│   ├── notebooklm-prompts.md ← NotebookLM 活用プロンプト集
│   ├── devlog/               ← 日次開発ログ
│   └── arch-guide/           ← CCAF由来の設計指針と適用率レポート
├── backend/              ← FastAPI + Celery
└── frontend/             ← Next.js
```

## 開発の進め方

`docs/mvp-design.md` の第6章「実装の着手順」と [`docs/roadmap.md`](docs/roadmap.md) に従い、
**縦切り**で進める。まず1論文が最後まで通る細い線を作り、そこに機能を足す。

---

## 🔗 関連プロジェクト

このプロジェクトは、**Claude Certified Architect – Foundations（CCAR-F）で学んだ設計の型を、
実際のアプリ開発に適用する実践**という位置づけを持つ。

| リポジトリ | 役割 | このプロジェクトとの関係 |
|---|---|---|
| [ccar-f-study-skills](https://github.com/ChestnutForest/ccar-f-study-skills) | **学ぶ** — CCAR-F 試験対策の Custom Claude Skills 集 | そこで学んだ型を、本プロジェクトで実際に適用している |
| **paper-repro-mvp**（本リポジトリ） | **実践する** — 学んだ型を適用したアプリ開発 | 適用方針は [`docs/arch-guide/`](docs/arch-guide/)、適用度は `ccaf-coverage-*.md` に記録 |

### 適用の記録

「どのノウハウを、開発のどの工程で、どこまで使ったか」を計測して残している。

- 設計指針: [`docs/arch-guide/README.md`](docs/arch-guide/README.md)
- CCAF 5ドメインとの対応表: [`docs/arch-guide/ccaf-patterns.md`](docs/arch-guide/ccaf-patterns.md)
- 適用率インジケーター: [`docs/arch-guide/`](docs/arch-guide/) の `ccaf-coverage-YYYY-MM-DD.md`

## ライセンス

このプロジェクトは MIT ライセンスで公開している。詳細は [`LICENSE`](LICENSE) を参照。

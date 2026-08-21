# paper-repro

英語のAI論文（arXiv）を読み解き、再現実装まで支援する正式版プロダクト。
最初のリリースでは「タイプB（学習なし・公式実装あり）」の論文を縦切りで完成させ、
その後のリリースでタイプA、GPU実行、レンダリング、LLM-as-a-Judgeへ段階的に拡張する。

- **ドキュメント索引**: [`docs/README.md`](docs/README.md)
- 要件: [`docs/requirements.md`](docs/requirements.md)
- 要件定義の更新手順: [`docs/requirements-update-workflow.md`](docs/requirements-update-workflow.md)
- 要件定義変更案: [`docs/requirements-change-proposal.md`](docs/requirements-change-proposal.md)
- 要件選択・第1バッチ: [`docs/requirements-decisions/batch-01-options.md`](docs/requirements-decisions/batch-01-options.md)
- 要件選択・第2バッチ: [`docs/requirements-decisions/batch-02-options.md`](docs/requirements-decisions/batch-02-options.md)
- 設計: [`docs/product-design.md`](docs/product-design.md)
- 技術スタック: [`docs/tech-stack.md`](docs/tech-stack.md)
- ロードマップ: [`docs/roadmap.md`](docs/roadmap.md)
- プロジェクト経緯: [`docs/history/project-history.md`](docs/history/project-history.md)
- Claude Code / Codex 共通指示: [`AGENTS.md`](AGENTS.md)
- Claude Code 用エントリーポイント: [`CLAUDE.md`](CLAUDE.md)

## AI Agent 連携と共通スキル

当プロジェクトでは、複数のAI開発エージェント（Antigravity IDE, Gemini Gem, Codex, Claude Code）を併用したリレー開発を行っています。
エージェント設定の二重管理を防ぐため、すべてのエージェントのルールとスキルの正本（Single Source of Truth）は `AGENTS.md` に集約しています（`CLAUDE.md` などは `AGENTS.md` への参照指示のみを保持します）。

**実装済み共通スキル**
- **Auto Model Selector**: タスクの複雑度（Z言語やAlloyを用いた形式仕様の推論・複雑な設計 vs 単純な整形・翻訳作業）を分析し、最適な推論レベルのAIモデルを自動選択します。
- **Resource Limit Advisor**: トークン上限やAPI利用枠の超過による実行失敗を事前に検知し、処理の中断と具体的な代替案（タスク分割、軽量モデルへのダウングレード等）を提示するフェイルセーフ機能です。

## Claude Code と Codex の併用

プロジェクト共通の指示は `AGENTS.md` を正本とする。Codex は `AGENTS.md` を直接読み、
Claude Code は自動読込される `CLAUDE.md` から `AGENTS.md` を全文参照する。
共通方針を2ファイルへ重複させないため、どちらのツールに戻っても同じ基準で開発を再開できる。

会話履歴そのものは両ツール間で共有されない。切り替える前に変更を保存し、テスト結果、判断理由、
未解決事項、次の一手を Git と [`docs/devlog/`](docs/devlog/) に残す。切り替え後は
`git status`、最新コミット、`AGENTS.md`、最新devlogを確認してから作業する。

Codexの `AGENTS.md` 読み込み仕様は
[OpenAI公式ドキュメント](https://developers.openai.com/codex/guides/agents-md)を参照。

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
3. `AGENTS.md` の共通指示に従って開発（設計で迷ったら [`docs/arch-guide/`](docs/arch-guide/)）
4. テストを回す → `git status` で `.env` が出ないことを確認 → コミット＆プッシュ
5. **「今日の分を資産化して」** で devlog を作り、コミット＆NotebookLMへ

**節目でやること**（フェーズ完了・大きな機能追加のとき）

- CCAF適用率の再計測 → [`docs/arch-guide/coverage-remeasure-howto.md`](docs/arch-guide/coverage-remeasure-howto.md)
- [`docs/roadmap.md`](docs/roadmap.md) の進捗更新
- [`docs/history/project-history.md`](docs/history/project-history.md) に経緯を追記

> 適用率の再計測は毎日ではない。数値は機能が実装されて初めて動くため、
> フェーズ完了などのトリガー時に測る。

---

## 必要なもの

- **Node.js 18 以上**（Next.js に必要）
- **Python 3.12 以上**
- **VS Code 1.98.0 以上**
- **Docker Desktop**（PostgreSQL / Redis をコンテナで動かす）
- **Claude Code または Codex**（両方を併用可能）
- **Anthropic の利用環境**（Claude Codeを使う場合。対応プランまたはAPIキー）

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

## Claude Code / Codex での開発の始め方

**お使いのOSに合った手順書を参照すること**（コマンドが異なるため）:

- **Windows**: [`docs/getting-started-vscode-windows.md`](docs/getting-started-vscode-windows.md)
- **Mac / Linux**: [`docs/getting-started-vscode.md`](docs/getting-started-vscode.md)

要点（共通）：

1. VS Code で **このフォルダ（ルート）を開く**（File → Open Folder）
2. Claude Codeを使う場合は、拡張機能パネルで **"Claude Code"（発行元 Anthropic）** をインストールしてサインイン
3. Codexを使う場合は、Codexでこのリポジトリルートを開く
4. 「`AGENTS.md` と `docs/product-design.md` を読み、最新devlogを確認してから作業を始めて」と依頼

## ディレクトリ構成

```
paper-repro/
├── AGENTS.md              ← Claude Code / Codex 共通のAI開発指示（正本）
├── CLAUDE.md              ← Claude Code から AGENTS.md への入口
├── README.md
├── .env.example          ← 環境変数のテンプレート（.env にコピーして使う）
├── docker-compose.yml    ← PostgreSQL + Redis
├── .vscode/              ← VS Code 推奨設定・拡張機能
├── scripts/
│   ├── start-dev.ps1         ← 開発環境の起動（Windows）
│   └── start-dev.sh          ← 開発環境の起動（Mac / Linux）
├── docs/
│   ├── README.md             ← ドキュメント索引
│   ├── daily-routine.md      ← 日々のルーチンワーク
│   ├── dev-startup.md        ← 起動スクリプトの使い方・確認事項
│   ├── requirements.md       ← 要件定義
│   ├── requirements-update-workflow.md ← 要件定義を更新するための検討手順
│   ├── product-design.md     ← 製品設計（初期リリース範囲）
│   ├── tech-stack.md         ← 技術スタック解説
│   ├── roadmap.md            ← 開発ロードマップ
│   ├── notebooklm-prompts.md ← NotebookLM 活用プロンプト集
│   ├── getting-started-vscode-windows.md
│   ├── getting-started-vscode.md
│   ├── arch-guide/           ← CCAF由来の設計指針と適用率レポート
│   ├── devlog/               ← 日次開発ログ
│   └── history/              ← プロジェクト経緯
├── backend/              ← FastAPI + Celery
└── frontend/             ← Next.js
```

## 開発の進め方

`docs/product-design.md` の第6章「実装の着手順」と [`docs/roadmap.md`](docs/roadmap.md) に従い、
**縦切り**で進める。まず1論文が最後まで通る細い線を作り、そこに機能を足す。

---

## 🔗 関連プロジェクト

このプロジェクトは、**Claude Certified Architect – Foundations（CCAR-F）で学んだ設計の型を、
実際のアプリ開発に適用する実践**という位置づけを持つ。

| リポジトリ | 役割 | このプロジェクトとの関係 |
|---|---|---|
| [ccar-f-study-skills](https://github.com/ChestnutForest/ccar-f-study-skills) | **学ぶ** — CCAR-F 試験対策の Custom Claude Skills 集 | そこで学んだ型を、本プロジェクトで実際に適用している |
| **paper-repro**（本リポジトリ） | **実践する** — 学んだ型を適用したアプリ開発 | 適用方針は [`docs/arch-guide/`](docs/arch-guide/)、適用度は `ccaf-coverage-*.md` に記録 |

### 適用の記録

「どのノウハウを、開発のどの工程で、どこまで使ったか」を計測して残している。

- 設計指針: [`docs/arch-guide/README.md`](docs/arch-guide/README.md)
- CCAF 5ドメインとの対応表: [`docs/arch-guide/ccaf-patterns.md`](docs/arch-guide/ccaf-patterns.md)
- 適用率インジケーター: [`docs/arch-guide/`](docs/arch-guide/) の `ccaf-coverage-YYYY-MM-DD.md`

## ライセンス

このプロジェクトは MIT ライセンスで公開している。詳細は [`LICENSE`](LICENSE) を参照。

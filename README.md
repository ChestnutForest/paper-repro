# paper-repro

英語のAI論文（arXiv）を読み解き、再現実装まで支援する正式版プロダクト。
最初のリリースでは「タイプB（学習なし・公式実装あり）」の論文を縦切りで完成させ、
その後のリリースでタイプA、GPU実行、レンダリング、LLM-as-a-Judgeへ段階的に拡張する。

---

## 📍 開発ロードマップの進捗

**現在地: フェーズ0「土台の仕上げ」／ 全7フェーズ中 0 完了**

詳細と各フェーズの中身は **[`docs/roadmap.md`](docs/roadmap.md)** を参照。

| フェーズ | 内容 | 状態 |
|---|---|---|
| Step 1 土台 | プロジェクト作成 → 一覧表示、GitHub登録、MITライセンス設定 | ✅ 完了 |
| **▶ フェーズ0** | **データ永続化・状態遷移・`course`の導入（`REQ-C01`）** | 🔨 **進行中** |
| フェーズ1 | インテーク（論文取込・タイプ判定・方針選択ゲート） | ⬜ 未着手 |
| フェーズ2 | 非同期ジョブ（Celery/Redis）・WebSocket進捗 | ⬜ 未着手 |
| フェーズ3 | リーディング（spec草案・エディタ・仮定台帳） | ⬜ 未着手 |
| フェーズ4 | 検証（サンドボックス・サニティ階段・ノートブック生成） | ⬜ 未着手 |
| フェーズ5 | 照合・レポート（スコア照合・zip出力） | ⬜ 未着手 |
| フェーズ6 | 公開整備（README・i18n・一般公開） | ⬜ 未着手 |

### 進行中のフェーズ0の中身

| 項目 | 状態 |
|---|---|
| 0-0. データモデル仕様の確定（[`arc-datamodel.md`](docs/arch-guide/arc-datamodel.md) v1.0） | ✅ 完了（2026-08-25） |
| **0-1. `projects` / `papers` を作り PostgreSQL に永続化する** | **← 次の一手** |
| 0-2. 状態遷移を動かす（`state` 1列 → `phase` × `status` の2列） | ⬜ 未着手 |

> **進捗の正本は [`docs/roadmap.md`](docs/roadmap.md) である。**
> フェーズの状態を変えるときは、まず `roadmap.md` を更新し、同じ変更で本表も合わせる。
> 直近の作業内容は [`docs/devlog/`](docs/devlog/) の最新ファイルを見る。

### 🧪 動作確認の方針

**各開発項目には、それを画面で確かめる手段を必ず対にする。**
バックエンドだけを作って「テストが通ったので完了」とはしない。
各フェーズの確認画面は [`docs/roadmap.md`](docs/roadmap.md) の「◯◯の確認画面」を見る。

確認に投入する論文は **[`docs/test-papers.md`](docs/test-papers.md)** の基準論文を使う。

| | |
|---|---|
| **基準論文** | [StructEval（arXiv:2505.20139）](https://arxiv.org/abs/2505.20139) |
| 選定理由 | タイプB・GPU不要・公式実装あり・照合できる数値あり・CC BY 4.0 |

毎回同じ論文を使うことで、前回との違いが画面の差として現れる。

---

## ドキュメント

- **ドキュメント索引**: [`docs/README.md`](docs/README.md)
- **ロードマップ（進捗の正本・確認画面の対応表）**: [`docs/roadmap.md`](docs/roadmap.md)
- **動作確認用のテスト論文**: [`docs/test-papers.md`](docs/test-papers.md)
- 要件（**v0.2・確定要求23件を統合済み**）: [`docs/requirements.md`](docs/requirements.md)
- **USDM 形式の要求仕様書**: [`docs/requirements-usdm.md`](docs/requirements-usdm.md)
- **トレーサビリティ・マトリクス**: [`docs/traceability-matrix.md`](docs/traceability-matrix.md)
- 要件定義の更新手順: [`docs/requirements-update-workflow.md`](docs/requirements-update-workflow.md)
- 要件定義変更案: [`docs/requirements-change-proposal.md`](docs/requirements-change-proposal.md)
- ID一本化とPhase暫定化の決定記録: [`docs/worknotes/id-unification-and-phase-provisional.md`](docs/worknotes/id-unification-and-phase-provisional.md)
- 承認前の矛盾スクリーニング: [`docs/worknotes/pre-approval-screening.md`](docs/worknotes/pre-approval-screening.md)
- 画面アーキテクチャ設計の枠組み: [`docs/arch-guide/arc-screen.md`](docs/arch-guide/arc-screen.md)
- データモデル仕様（**v1.0 確定**）: [`docs/arch-guide/arc-datamodel.md`](docs/arch-guide/arc-datamodel.md)
- 参考文献: [`docs/references.md`](docs/references.md)
- USDM・IPAガイドラインの一次情報: [`docs/references-usdm-ipa.md`](docs/references-usdm-ipa.md)
- 要求分析資料: [`docs/requirements-analysis/README.md`](docs/requirements-analysis/README.md)
- 「1.2 論文を読み解く技術」の要求分析: [`docs/requirements-analysis/section-1.2-reading-techniques.md`](docs/requirements-analysis/section-1.2-reading-techniques.md)
- 「1.2.1 論文を読む環境の構築」の詳細分析: [`docs/requirements-analysis/section-1.2.1-reading-environment.md`](docs/requirements-analysis/section-1.2.1-reading-environment.md)
- 「1.2.1.1 論文を入手する」の詳細分析: [`docs/requirements-analysis/section-1.2.1.1-paper-acquisition.md`](docs/requirements-analysis/section-1.2.1.1-paper-acquisition.md)
- 「1.2.1.2 論文を電子媒体で読む」の詳細分析: [`docs/requirements-analysis/section-1.2.1.2-electronic-reading.md`](docs/requirements-analysis/section-1.2.1.2-electronic-reading.md)
- 「1.2.1.3 論文は人間が書いたものであることを認識する」の詳細分析: [`docs/requirements-analysis/section-1.2.1.3-human-authorship.md`](docs/requirements-analysis/section-1.2.1.3-human-authorship.md)
- 「1.2.2 自分の力で論文を読み解くための技術」の詳細分析: [`docs/requirements-analysis/section-1.2.2-independent-reading-techniques.md`](docs/requirements-analysis/section-1.2.2-independent-reading-techniques.md)
- 「1.2.2.1 議論が成立する条件を確認する」の詳細分析: [`docs/requirements-analysis/section-1.2.2.1-discussion-conditions.md`](docs/requirements-analysis/section-1.2.2.1-discussion-conditions.md)
- 「1.2.2.2 具体例を構成する」の詳細分析: [`docs/requirements-analysis/section-1.2.2.2-concrete-examples.md`](docs/requirements-analysis/section-1.2.2.2-concrete-examples.md)
- 「1.2.2.3 実装を読み解いて理解を深める」の詳細分析: [`docs/requirements-analysis/section-1.2.2.3-implementation-reading.md`](docs/requirements-analysis/section-1.2.2.3-implementation-reading.md)
- 「1.2.2.4 重要となる参考文献は踏み込んで調べる」の詳細分析: [`docs/requirements-analysis/section-1.2.2.4-important-references.md`](docs/requirements-analysis/section-1.2.2.4-important-references.md)
- 「1.2.2.5 アウトプットすることで理解を深める」の詳細分析: [`docs/requirements-analysis/section-1.2.2.5-output-for-understanding.md`](docs/requirements-analysis/section-1.2.2.5-output-for-understanding.md)
- 「1.2.3 自分以外の力も借りて論文を読み解くための技術」の詳細分析: [`docs/requirements-analysis/section-1.2.3-external-help.md`](docs/requirements-analysis/section-1.2.3-external-help.md)
- 「1.2.3.1 少人数で深く議論する」の詳細分析: [`docs/requirements-analysis/section-1.2.3.1-small-group-discussion.md`](docs/requirements-analysis/section-1.2.3.1-small-group-discussion.md)
- 「1.2.3.2 論文の著者に直接質問する」の詳細分析: [`docs/requirements-analysis/section-1.2.3.2-contacting-authors.md`](docs/requirements-analysis/section-1.2.3.2-contacting-authors.md)
- 「1.2.3.3 ウェブ上で議論する」の詳細分析: [`docs/requirements-analysis/section-1.2.3.3-web-discussion.md`](docs/requirements-analysis/section-1.2.3.3-web-discussion.md)
- 「1.2.3.4 生成AIを使う」の詳細分析: [`docs/requirements-analysis/section-1.2.3.4-using-generative-ai.md`](docs/requirements-analysis/section-1.2.3.4-using-generative-ai.md)
- 「Academic and Research Skills」の詳細要求分析（8つの確立された枠組み）: [`docs/requirements-analysis/academic-research-skills-frameworks.md`](docs/requirements-analysis/academic-research-skills-frameworks.md)
- 「Academic and Research Skills」の要求分析: [`docs/requirements-analysis/academic-research-skills.md`](docs/requirements-analysis/academic-research-skills.md)
- 「論文再現実装ハンズオン #4 対照学習（SimCLR）」の要求分析: [`docs/requirements-analysis/simclr-handson-deck.md`](docs/requirements-analysis/simclr-handson-deck.md)
- 要件選択・第1バッチ: [`docs/requirements-decisions/batch-01-options.md`](docs/requirements-decisions/batch-01-options.md)
- 要件選択・第2バッチ: [`docs/requirements-decisions/batch-02-options.md`](docs/requirements-decisions/batch-02-options.md)
- 追加要件選択・第3バッチ: [`docs/requirements-decisions/batch-03-options.md`](docs/requirements-decisions/batch-03-options.md)
- 設計: [`docs/product-design.md`](docs/product-design.md)
- 技術スタック: [`docs/tech-stack.md`](docs/tech-stack.md)
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

現在Gitで追跡している主要なファイルとディレクトリを示す。
仮想環境、依存パッケージ、ビルド生成物、`.env` などのGit管理外ファイルは省略している。

```text
paper-repro/
├── .env.example
├── .gitignore
├── AGENTS.md                    ← Claude Code / Codex 共通のAI開発指示（正本）
├── CLAUDE.md                    ← Claude Code から AGENTS.md への入口
├── LICENSE
├── README.md
├── docker-compose.yml           ← PostgreSQL + Redis
├── .vscode/
│   ├── extensions.json
│   └── settings.json
├── scripts/
│   ├── start-dev.ps1            ← 開発環境の起動（Windows）
│   └── start-dev.sh             ← 開発環境の起動（Mac / Linux）
├── backend/                      ← FastAPIバックエンド
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py              ← FastAPIエントリーポイント
│   │   ├── api/
│   │   │   └── projects.py      ← プロジェクトAPI
│   │   ├── core/
│   │   │   ├── config.py        ← アプリケーション設定
│   │   │   ├── db.py            ← データベース接続
│   │   │   └── states.py        ← 状態定義
│   │   ├── models/
│   │   │   └── project.py       ← プロジェクトモデル
│   │   ├── services/            ← サービス層
│   │   └── workers/             ← 非同期ワーカー層
│   └── tests/
│       └── test_smoke.py
├── frontend/                     ← Next.jsフロントエンド
│   ├── .env.local.example
│   ├── components.json
│   ├── next-env.d.ts
│   ├── next.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── messages/                 ← 多言語メッセージ
│   │   ├── en.json
│   │   ├── ja.json
│   │   └── zh-TW.json
│   └── src/
│       ├── components/
│       │   ├── LocaleSwitcher.tsx
│       │   ├── PaperInput.tsx
│       │   └── ui/
│       ├── lib/
│       │   ├── api.ts
│       │   └── utils.ts
│       ├── pages/
│       │   ├── _app.tsx
│       │   └── index.tsx
│       └── styles/
│           └── globals.css
└── docs/
    ├── README.md                 ← ドキュメント索引
    ├── daily-routine.md          ← 日々のルーチンワーク
    ├── dev-startup.md            ← 起動スクリプトの使い方・確認事項
    ├── getting-started-vscode-windows.md
    ├── getting-started-vscode.md
    ├── notebooklm-prompts.md     ← NotebookLM活用プロンプト集
    ├── product-design.md         ← 製品設計
    ├── references.md             ← 参考文献（一次資料の書誌と引用方針）
    ├── references-usdm-ipa.md    ← USDM・IPAガイドラインのURL一覧と使用条件
    ├── requirements.md           ← 確定済み要件の正本
    ├── requirements-change-proposal.md
    ├── requirements-update-workflow.md
    ├── roadmap.md                ← 開発ロードマップ（進捗の正本）
    ├── requirements-usdm.md      ← USDM形式の要求仕様書
    ├── traceability-matrix.md    ← トレーサビリティ・マトリクス
    ├── test-papers.md            ← 動作確認に使うテスト論文
    ├── tech-stack.md             ← 技術スタック解説
    ├── requirements-analysis/
    │   ├── README.md
    │   ├── section-1.2-reading-techniques.md
    │   ├── section-1.2.1-reading-environment.md
    │   ├── section-1.2.1.1-paper-acquisition.md
    │   ├── section-1.2.1.2-electronic-reading.md
    │   ├── section-1.2.1.3-human-authorship.md
    │   ├── section-1.2.2-independent-reading-techniques.md
    │   ├── section-1.2.2.1-discussion-conditions.md
    │   ├── section-1.2.2.2-concrete-examples.md
    │   ├── section-1.2.2.3-implementation-reading.md
    │   ├── section-1.2.2.4-important-references.md
    │   ├── section-1.2.2.5-output-for-understanding.md
    │   ├── section-1.2.3-external-help.md
    │   ├── section-1.2.3.1-small-group-discussion.md
    │   ├── section-1.2.3.2-contacting-authors.md
    │   ├── section-1.2.3.3-web-discussion.md
    │   ├── academic-research-skills-frameworks.md
    │   ├── academic-research-skills.md
    │   ├── section-1.2.3.4-using-generative-ai.md
    │   └── simclr-handson-deck.md
    ├── requirements-decisions/
    │   ├── batch-01-options.md
    │   ├── batch-02-options.md
    │   └── batch-03-options.md
    ├── arch-guide/               ← CCAF由来の設計指針と適用率レポート
    │   ├── README.md
    │   ├── arc-architecture.md
    │   ├── ccaf-coverage-2026-08-03.md
    │   ├── ccaf-patterns.md
    │   ├── claude-code-playbook.md
    │   ├── coverage-remeasure-howto.md
    │   └── coverage-rubric.md
    ├── devlog/                   ← 日次開発ログ
    │   ├── README.md
    │   └── devlog-YYYY-MM-DD*.md
    ├── history/
    │   └── project-history.md
    └── worknotes/            ← 反映メモ・保留記録・承認前スクリーニング・骨組み更新決定
        ├── README.md
        ├── pre-approval-screening.md
        ├── id-unification-and-phase-provisional.md
        └── ほか
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

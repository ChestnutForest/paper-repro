# paper-repro

英語のAI論文（arXiv）を読み解き、再現実装まで支援する正式版プロダクト。
最初のリリースでは「タイプB（学習なし・公式実装あり）」の論文を縦切りで完成させ、
その後のリリースでタイプA、GPU実行、レンダリング、LLM-as-a-Judgeへ段階的に拡張する。

---

## 📍 開発ロードマップの進捗

**現在地: フェーズ0「土台の仕上げ」／ 全7フェーズ中 0 完了。次の一手は 0-1 の永続化。**

フェーズの状態と各フェーズの内訳は **[`docs/roadmap.md`](docs/roadmap.md)** が正本である。
本書は表を複製しない。

### 📐 設計工程の進捗（IPA 6編）

**現在地: 現行確定要求について、データモデル編の4成果物と共通ルールを作成／ 全6編中 3 編**

詳細は **[`docs/arch-guide/arc-artifact-order.md`](docs/arch-guide/arc-artifact-order.md)**（作成順序の原則）を参照。

| 編 | 枠組み | 一覧 | 共通ルール | フロー・遷移 | 説明・レイアウト |
| --- | --- | --- | --- | --- | --- |
| 画面 | ✅ [v0.2.2](docs/arch-guide/arc-screen.md) | ✅ | ✅ | ✅ | ✅ 7画面 |
| **システム振舞い** | ✅ [v0.3](docs/arch-guide/arc-behavior.md) | ✅ [v0.2](docs/arch-guide/arc-behavior-list.md) | ✅ [v0.1](docs/arch-guide/arc-behavior-rules.md) | ✅ [フロー v0.1](docs/arch-guide/arc-behavior-flow.md)・[状態 v0.1](docs/arch-guide/arc-behavior-state.md) | ✅ [47業務 v0.1](docs/arch-guide/behaviors/) |
| **データモデル** | ✅ [v0.2](docs/arch-guide/arc-datamodel-framework.md) | ✅ [17エンティティ・要求23/23 v0.2](docs/arch-guide/arc-datamodel-list.md) | ✅ [v0.2](docs/arch-guide/arc-datamodel-rules.md) | ✅ [ER図 v0.1](docs/arch-guide/arc-datamodel-er.md)・[CRUD図 v0.2](docs/arch-guide/arc-datamodel-crud.md) | ✅ [論理定義 v0.2](docs/arch-guide/arc-datamodel-definitions.md)・[物理仕様 v1.0](docs/arch-guide/arc-datamodel.md) |
| 外部インタフェース | ✅ [v0.1.2](docs/arch-guide/arc-interface.md) | ✅ [v0.4](docs/arch-guide/arc-interface-list.md) | — | ✅ [関連図 v0.1.2](docs/arch-guide/arc-interface-map.md) | ⬜ **← 次の一手** |
| バッチ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 帳票 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

> **一覧が先である。** 詳細から書き始めると、完了を判定できず、粒度も揃わない。
> 根拠は [`docs/arch-guide/arc-artifact-order.md`](docs/arch-guide/arc-artifact-order.md) を参照。

> システム振舞い編とデータモデル編の✅は、**現行の確定要求を要求単位で設計した**ことを示す。
> データモデルは17エンティティの論理設計であり、物理仕様は`Project`／`Paper`だけが確定している。
> 4工程成果物は作成済みだが、レビュー結果は✅2・🔨11・⏳1で、全体成熟度は**仕掛**である。
> 注釈群と演習履歴群は、保持先未確定の2ギャップとしてUSDMへ戻している。
> `REQ-C02`〜`REQ-C11`はUSDM仕様未展開のため、両編とも仕様展開後に再検査する。
> ソフトウェア実装の現在地は変わらずフェーズ0である。

> **IPA 6編の設計工程の進捗は、本表が正本である。** 版数と✅は本表だけが持つ。
> ソフトウェア実装の進捗は [`docs/roadmap.md`](docs/roadmap.md) の管轄で、軸が異なる。
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

**[`docs/README.md`](docs/README.md) が索引の正本である。** 目的から文書を探すときはここから入る。

よく使う入口:

- 日々のルーチン: [`docs/daily-routine.md`](docs/daily-routine.md)
- 進捗: [`docs/roadmap.md`](docs/roadmap.md)
- 要件: [`docs/requirements.md`](docs/requirements.md)
- 設計: [`docs/product-design.md`](docs/product-design.md)
- AI開発指示: [`AGENTS.md`](AGENTS.md)

## AI Agent 連携と共通スキル

当プロジェクトでは、Claude Code、Codex、Antigravity IDEを併用したリレー開発を行っています。
共通ルールの正本は`AGENTS.md`、スキル本文の正本は`.agents/skills/`である。
Claude Codeは`.claude/skills/`の短い入口から同じ正本を読み、手順本文を重複管理しない。
paper-reproでは、GitHubへ登録されたリポジトリスキルだけを使用し、個人領域やプラグインキャッシュのスキルを適用しない。

**実装済み共通スキル**
- **[`paper-repro-skill-source-policy`](.agents/skills/paper-repro-skill-source-policy/SKILL.md)**: Git追跡・HEAD・リモート同期を確認し、リポジトリスキルだけを許可
- **[`paper-repro-arch-guide`](.agents/skills/paper-repro-arch-guide/SKILL.md)**: 要求から設計文書へ展開し、Mermaid CLIで図を実描画して検証
- **[`arxiv-paper-repro`](.agents/skills/arxiv-paper-repro/SKILL.md)**: AI/ML論文の再現実装、部分採用、スコア不一致の切り分け
- **[`paper-repro-devlog`](.agents/skills/paper-repro-devlog/SKILL.md)**: paper-repro開発の日次知識を`docs/devlog/`へ資産化
- **[`paper-repro-commit-output`](.agents/skills/paper-repro-commit-output/SKILL.md)**: commit/push、SHA照合、チャットで個別コピー可能なGitHub URL、実行結果検証

## Claude Code、Codex、Antigravity IDEの併用

CodexとAntigravity IDEは`.agents/skills/`を直接利用し、Claude Codeは`.claude/skills/`から
同じ本文を参照する。WindowsでのGit利用を安定させるため、シンボリックリンクではなく短い参照入口を使う。

会話履歴そのものは3環境間で共有されない。切り替える前に変更を保存し、テスト結果、判断理由、
未解決事項、次の一手を Git と [`docs/devlog/`](docs/devlog/) に残す。切り替え後は
`git status`、最新コミット、`AGENTS.md`、最新devlogを確認してから作業する。

仕様は[OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)、
[Claude Code Skills](https://code.claude.com/docs/en/slash-commands)、
[Google Antigravity Skills](https://antigravity.google/docs/skills)を参照。

---

## 🧱 技術スタック（概要）

| 層 | 技術 | ポート |
|---|---|---|
| フロントエンド | **Next.js 14 + React 18 + TypeScript 5** | 3000 |
| バックエンド | **FastAPI + uvicorn（Python）** | 8000 |
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
- **Python**（開発環境の版は [`docs/tech-stack.md`](docs/tech-stack.md) を参照）
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

```text
paper-repro/
├── AGENTS.md          ← AI開発指示の正本
├── CLAUDE.md          ← AGENTS.md への入口
├── README.md
├── docker-compose.yml ← PostgreSQL + Redis
├── scripts/           ← 起動スクリプト・検証スクリプト
├── backend/           ← FastAPI（Python）
├── frontend/          ← Next.js（TypeScript）
├── .agents/skills/    ← リポジトリスキルの正本
├── .claude/skills/    ← Claude Code 用の入口
└── docs/              ← 設計・要件・記録
```

`docs/` 配下の構成と各文書の内容は **[`docs/README.md`](docs/README.md)** を参照。
本書はファイル一覧を複製しない。

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

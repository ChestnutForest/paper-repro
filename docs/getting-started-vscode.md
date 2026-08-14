# Claude Code / Codex で開発を始める手順

このプロジェクトを、Claude CodeとCodexのどちらからでも継続開発するための手順書。
初めての人でも迷わないよう、順番どおりに進めれば動くように書いている。

（情報は 2026年7月時点の公式ドキュメントに基づく。バージョン要件は変わることがあるので、
うまくいかないときは https://code.claude.com/docs/en/vs-code を確認する）

---

## 全体の流れ（10ステップ）

1. 前提ソフトを入れる（Node.js / Python / Docker / VS Code）
2. VS Code でこのフォルダを開く
3. Claude Code を使う場合は拡張機能を入れる
4. Claude Code を使う場合はサインインする／Codexではリポジトリを開く
5. 推奨拡張機能を入れる
6. 環境変数ファイル（.env）を用意する
7. DB と Redis を起動する（Docker）
8. バックエンドを起動する
9. フロントエンドを起動する
10. Claude Code または Codex に最初の実装を依頼する

---

## ステップ1：前提ソフトを入れる

以下を先に入れておく。すでにあるものは飛ばしてよい。

| ソフト | 必要バージョン | 確認コマンド | 入手先 |
|---|---|---|---|
| Node.js | **18 以上** | `node --version` | https://nodejs.org |
| Python | **3.12 以上** | `python --version` | https://python.org |
| Docker Desktop | 最新 | `docker --version` | https://docker.com |
| VS Code | **1.98.0 以上** | Help → About | https://code.visualstudio.com |

**VS Code のバージョンが 1.98.0 未満だと Claude Code 拡張が動かない。** 先に更新すること。

さらに **Anthropic の有料プラン**（Pro / Max / Team / Enterprise のいずれか）が要る。
Claude Code に無料枠はない。API キーでの従量課金でも使える。

---

## ステップ2：VS Code でこのフォルダを開く

**重要：Claude CodeとCodexのどちらでも、リポジトリのルートを開く。** ばらばらのファイルではない。

1. VS Code を開く
2. File → Open Folder（ファイル → フォルダーを開く）
3. **このプロジェクトのルート**（`paper-repro` フォルダ）を選ぶ

ルートを開くのが大事。`backend` だけ・`frontend` だけを開くと、
`AGENTS.md`、`CLAUDE.md`、`docs/` をまとめて参照できず、全体像を掴めない。

---

## ステップ3：Claude Code 拡張機能を入れる

1. 拡張機能パネルを開く（`Ctrl+Shift+X` / Mac は `Cmd+Shift+X`）
2. 検索欄に **「Claude Code」** と入力
3. **発行元が「Anthropic」** のものを選んで Install（似た名前の別物に注意）

うまく表示されないときは、コマンドパレット（`Ctrl+Shift+P` / `Cmd+Shift+P`）で
**「Developer: Reload Window」** を実行してから、もう一度開く。

> このプロジェクトには `.vscode/extensions.json` があるので、フォルダを開いた時点で
> 「推奨拡張機能をインストールしますか？」と聞かれることがある。そこから入れてもよい。

---

## ステップ4：Claude Code にサインインする

1. 左のアクティビティバー、または エディタ右上の **Spark アイコン（✱）** をクリック
   （✱ はファイルを開いているときだけ右上に出る）
2. パネルが開いたら **Sign in** を押す
3. ブラウザが開くので、Anthropic アカウントで認証する

これでチャットパネルが使えるようになる。拡張機能は CLI を内蔵しているので、
チャットパネルを使うだけなら別途 CLI を入れる必要はない。

> API キーを使いたい場合は、環境変数 `ANTHROPIC_API_KEY` を設定し、
> **ターミナルから `code .` で VS Code を起動**すると環境変数が引き継がれる。
> （普通にアイコンから起動すると引き継がれず、サインイン画面が出ることがある）

### Codexを使う場合

Codexでリポジトリルート `paper-repro` を開く。Codexはルートの `AGENTS.md` を
作業前に読み込む。Claude Codeは `CLAUDE.md` を入口として同じ `AGENTS.md` を読むため、
共通指示を二重管理しない。詳細は
[OpenAI公式ドキュメント](https://developers.openai.com/codex/guides/agents-md)を参照。

---

## ステップ5：推奨拡張機能を入れる

Python・Ruff・ESLint・Prettier・Docker があると開発が快適になる。
`.vscode/extensions.json` に列挙してあるので、
コマンドパレットで「Extensions: Show Recommended Extensions」から一括で入れられる。

---

## ステップ6：環境変数ファイル（.env）を用意する

ルートで次を実行（またはエクスプローラでコピー）：

```bash
cp .env.example .env
```

`.env` を開いて、少なくとも `ANTHROPIC_API_KEY` を自分の値にする。
**`.env` は `.gitignore` 済みなのでコミットされない。** 秘密情報はここだけに置く。

---

## ステップ7：DB と Redis を起動する（Docker）

ルートで：

```bash
docker compose up -d
```

PostgreSQL（5432番）と Redis（6379番）がコンテナで立ち上がる。
`docker compose ps` で稼働を確認できる。止めるときは `docker compose down`。

---

## ステップ8：バックエンドを起動する

VS Code の統合ターミナルを開く（`Ctrl+@` / `Cmd+@`）。

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows は .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

ブラウザで **http://localhost:8000/docs** を開くと、API の一覧（Swagger UI）が見える。
`/health` が `{"status":"ok"}` を返せば成功。

---

## ステップ9：フロントエンドを起動する

**別の**ターミナルを開いて：

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

ブラウザで **http://localhost:3000** を開く。arXiv URL を入れて「作成」を押すと、
バックエンドにプロジェクトが作られ、一覧に出る。ここまで動けば土台は完成。

---

## ステップ10：Claude Code または Codex に最初の実装を依頼する

ここからが本番。使用するツールのパネルで、たとえばこう頼む：

```
AGENTS.md と docs/product-design.md、docs/roadmap.md、最新のdevlogを読んで。
いまは Step 1（骨組みを1本通す）の段階。
backend/app/api/projects.py のインメモリ保存を、
PostgreSQL + SQLAlchemy の実装に置き換えたい。
まず変更計画を箇条書きで出してから実装して。
```

**うまく使うコツ：**

- **まず計画を出させてから実装させる。** 共通方針は `AGENTS.md` に記載してある
- **`@ファイル名`** でファイルを指定すると、そのファイルを文脈に読み込む
- 変更は **diff（差分）ビュー**で表示される。Accept / Reject / Accept Hunk（部分採用）を選べる。
  勝手に書き換わらないので安心してよい
- ビルドエラーやテスト失敗は、そのファイルをエディタで開いてから頼むと、
  AI開発ツールが診断情報を直接読める
- 会話が長くなって文脈が一杯になったら、プロンプト欄で **`/compact`** を実行して圧縮する

**動作確認の習慣：**

```bash
# バックエンドのテスト
cd backend && python -m pytest tests/ -q
```

AI開発ツールが実装したら、必ずテストを回す。緑になってから次へ進む。
これは論文再現の「サニティチェック」と同じ思想 — 小さく確かめてから積み上げる。

ツールを切り替える前には、テスト結果、判断理由、未解決事項、次の一手をGit管理下へ残す。
切り替え後は `git status`、最新コミット、`AGENTS.md`、最新devlogを確認して再開する。

---

## つまずいたとき

| 症状 | 対処 |
|---|---|
| 拡張が出てこない | VS Code を 1.98.0 以上に更新。「Developer: Reload Window」 |
| サインインを何度も求められる | ターミナルから `code .` で起動して環境変数を引き継ぐ |
| `uvicorn` が見つからない | 仮想環境を有効化したか確認（`source .venv/bin/activate`） |
| フロントが API に繋がらない | バックエンドが 8000 番で起動しているか、`.env.local` の API_BASE を確認 |
| Docker が起動しない | Docker Desktop 本体が起動しているか確認 |
| AI開発ツールが的外れな実装をする | `AGENTS.md` を読ませたか確認。`@docs/product-design.md` で設計を指定する |

---

## 開発の進め方（再掲）

`docs/product-design.md` 第6章「実装の着手順」に従い、**縦切り**で進める。
横に機能を広げる前に、まず「1論文が最後まで通る細い線」を完成させること。

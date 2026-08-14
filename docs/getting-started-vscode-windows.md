# 【Windows版】Claude Code / Codex で開発を始める手順

**この手順書は Windows 専用。** Mac / Linux の人は `getting-started-vscode.md` を見ること。
コマンド（仮想環境の有効化、ファイルコピー等）が OS で異なるため、混同しないよう分けている。
Claude Codeのセットアップに加え、同じリポジトリをCodexへ引き継ぐ方法も扱う。

配置先の例: `C:\Users\kazuy\projects\paper-repro`
（情報は 2026年7月時点の公式ドキュメントに基づく。要件が変わったら https://code.claude.com/docs/en/vs-code を確認）

---

## 全体の流れ（11ステップ）

0. プロジェクトを正しい場所に配置する（Windows特有の注意）
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

## ステップ0：プロジェクトを正しい場所に配置する

zip を展開し、**`paper-repro` フォルダごと** `C:\Users\kazuy\projects` の直下に置く。

```
C:\Users\kazuy\projects\
└── paper-repro\        ← この1フォルダにまとめる（中身をバラで置かない）
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── backend\
    ├── frontend\
    └── docs\
```

### Windows特有の注意（3つ）

**① 二重フォルダに注意**
エクスプローラーの「すべて展開」は、zip名と同じフォルダを1階層余分に作ることがある。

```
✗ 悪い例: projects\files_reify_xxxx\paper-repro\AGENTS.md
✓ 良い例: projects\paper-repro\AGENTS.md
```

**目印は「`AGENTS.md` と `CLAUDE.md` が `projects\paper-repro\` の直下に見えるか」。**
二重になっていたら、内側の `paper-repro` を `projects` 直下へ移動し、外側の空フォルダを削除する。

**② ドット始まりのファイルが見えない**
`.env.example` `.gitignore` `.vscode` などは、エクスプローラーの初期状態では隠れている。
「表示」タブ →「隠しファイル」にチェックを入れると見える。
（VS Code 内では普通に見えるので、実害はほぼない）

**③ 日本語ユーザー名・パスのままでよい**
`C:\Users\kazuy` のようなパスは問題ない。ただし後述のコマンドは、
**必ず VS Code の統合ターミナルで実行**する（パスのずれを防げる）。

---

## ステップ1：前提ソフトを入れる

| ソフト | 必要バージョン | 確認コマンド | 入手先 |
|---|---|---|---|
| Node.js | **18 以上** | `node --version` | https://nodejs.org |
| Python | **3.12 以上** | `python --version` | https://python.org |
| Docker Desktop | 最新 | `docker --version` | https://docker.com |
| VS Code | **1.98.0 以上** | Help → About | https://code.visualstudio.com |

**VS Code が 1.98.0 未満だと Claude Code 拡張が動かない。** 先に更新すること。

### Windows でのインストールの勘所

- **Python は「Add python.exe to PATH」に必ずチェック**を入れてインストールする。
  入れ忘れると、ターミナルで `python` が見つからないと言われる。
- Python を Microsoft Store 版で入れていると挙動が不安定なことがある。
  うまくいかないときは python.org のインストーラ版を使う。
- Docker Desktop は WSL2 バックエンドを使う。初回起動で WSL2 の導入を促されたら従う。
- 確認コマンドは **PowerShell**（スタート →「PowerShell」）で実行できる。

さらに **Anthropic の有料プラン**（Pro / Max / Team / Enterprise）が必要。
Claude Code に無料枠はない。API キーでの従量課金でも使える。

---

## ステップ2：VS Code でこのフォルダを開く

**重要：Claude CodeとCodexのどちらでも、リポジトリのルートを開く。**

1. VS Code を起動
2. File → Open Folder（ファイル → フォルダーを開く）
3. **`C:\Users\kazuy\projects\paper-repro`** を選ぶ
   （`projects` ではなく、その中の `paper-repro` を開く）

ルートを開くのが大事。`backend` だけを開くと、`AGENTS.md`、`CLAUDE.md`、`docs\` を
まとめて参照できず、全体像を掴めない。

> 初回は「このフォルダー内のファイルの作成者を信頼しますか？」と聞かれる。
> 自分の作ったプロジェクトなので「はい、作成者を信頼します」を選ぶ。

---

## ステップ3：Claude Code 拡張機能を入れる

1. 拡張機能パネルを開く（`Ctrl+Shift+X`）
2. 検索欄に **「Claude Code」** と入力
3. **発行元が「Anthropic」** のものを選んで Install（似た名前の別物に注意）

表示されないときは、コマンドパレット（`Ctrl+Shift+P`）で
**「Developer: Reload Window」** を実行してから、もう一度開く。

> このプロジェクトには `.vscode\extensions.json` があるので、フォルダを開いた時点で
> 「推奨拡張機能をインストールしますか？」と右下に出ることがある。そこから入れてもよい。

---

## ステップ4：Claude Code にサインインする

1. 左のアクティビティバー、または エディタ右上の **Spark アイコン（✱）** をクリック
   （✱ はファイルを開いているときだけ右上に出る）
2. パネルが開いたら **Sign in** を押す
3. ブラウザが開くので、Anthropic アカウントで認証する

拡張機能は CLI を内蔵しているので、チャットパネルを使うだけなら別途 CLI を入れる必要はない。

> API キーを使う場合は、環境変数 `ANTHROPIC_API_KEY` を設定する。
> Windows では PowerShell で次のように設定できる（恒久設定）：
> ```powershell
> setx ANTHROPIC_API_KEY "sk-ant-xxxx"
> ```
> 設定後は VS Code を再起動して反映させる。

### Codexを使う場合

Codexで `C:\Users\kazuy\projects\paper-repro` をプロジェクトとして開く。
Codexはリポジトリルートの `AGENTS.md` を作業前に読み込む。Claude Codeは
`CLAUDE.md` を入口として同じ `AGENTS.md` を読むため、共通指示を二重管理しない。
詳細は [OpenAI公式ドキュメント](https://developers.openai.com/codex/guides/agents-md) を参照。

---

## ステップ5：推奨拡張機能を入れる

`.vscode\extensions.json` に列挙済み。コマンドパレット（`Ctrl+Shift+P`）で
**「Extensions: Show Recommended Extensions」** を開き、一括で入れる。

入る拡張（発行元IDで確実に）:
`anthropic.claude-code` / `ms-python.python` / `ms-python.vscode-pylance` /
`charliermarsh.ruff` / `dbaeumer.vscode-eslint` / `esbenp.prettier-vscode` /
`ms-azuretools.vscode-docker`

---

## ステップ6：環境変数ファイル（.env）を用意する

**ここが Windows で最もつまずく所。** メモ帳で作ると `.env.txt` になってしまう。
**必ず VS Code の統合ターミナルでコマンドを使う。**

統合ターミナルを開く（`Ctrl+@`）。**既定が PowerShell なら**：

```powershell
Copy-Item .env.example .env
```

**既定が コマンドプロンプト(cmd) なら**：

```bat
copy .env.example .env
```

作成した `.env` を VS Code で開き、少なくとも `ANTHROPIC_API_KEY` を自分の値にする。
`.env` は `.gitignore` 済みなのでコミットされない。秘密情報はここだけに置く。

> ターミナルの種類は、統合ターミナル右上のドロップダウンで確認・切替できる。
> この手順書では以降 **PowerShell** を前提にする。

---

## ステップ7：DB と Redis を起動する（Docker）

**先に Docker Desktop 本体を起動しておく**（タスクトレイのクジラアイコンが安定するまで待つ）。

統合ターミナル（プロジェクトのルートにいること）で：

```powershell
docker compose up -d
```

PostgreSQL（5432番）と Redis（6379番）が立ち上がる。
`docker compose ps` で稼働確認。止めるときは `docker compose down`。

> 「docker: command not found」が出たら Docker Desktop が起動していない。
> 起動してからやり直す。

---

## ステップ8：バックエンドを起動する

統合ターミナルで、**Windows 用のコマンド**を使う（Mac の `source ...` とは違う）：

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### PowerShell で有効化できないとき

`.venv\Scripts\Activate.ps1` 実行時に「スクリプトの実行が無効」というエラーが出たら、
PowerShell の実行ポリシーを一度だけ緩める：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

それでも面倒なら、コマンドプロンプト(cmd)版の有効化を使う：

```bat
.venv\Scripts\activate.bat
```

起動したら、ブラウザで **http://localhost:8000/docs** を開く。
`/health` が `{"status":"ok"}` を返せば成功。

---

## ステップ9：フロントエンドを起動する

**別の**統合ターミナルを開く（ターミナルパネルの「＋」で新規）。PowerShell で：

```powershell
cd frontend
Copy-Item .env.local.example .env.local
npm install
npm run dev
```

ブラウザで **http://localhost:3000** を開く。arXiv URL を入れて「作成」を押すと、
バックエンドにプロジェクトが作られ、一覧に出る。ここまで動けば土台は完成。

---

## ステップ10：Claude Code または Codex に最初の実装を依頼する

使用するツールのパネルで、たとえばこう頼む：

```
AGENTS.md と docs\product-design.md、docs\roadmap.md、最新のdevlogを読んで。
いまは Step 1（骨組みを1本通す）の段階。
backend\app\api\projects.py のインメモリ保存を、
PostgreSQL + SQLAlchemy の実装に置き換えたい。
まず変更計画を箇条書きで出してから実装して。
```

**うまく使うコツ：**

- **まず計画を出させてから実装させる。** 共通方針は `AGENTS.md` に記載してある
- **`@ファイル名`** でファイルを指定すると、そのファイルを文脈に読み込む
- 変更は **diff（差分）ビュー**で表示される。Accept / Reject / Accept Hunk を選べる。
  勝手に書き換わらないので安心してよい
- 会話が長くなって文脈が一杯になったら、プロンプト欄で **`/compact`** を実行して圧縮する

**動作確認の習慣**（バックエンドのテスト）：

```powershell
cd backend
.venv\Scripts\Activate.ps1
python -m pytest tests\ -q
```

AI開発ツールが実装したら、必ずテストを回す。緑になってから次へ進む。
これは論文再現の「サニティチェック」と同じ思想 — 小さく確かめてから積み上げる。

ツールを切り替える前には、テスト結果、判断理由、未解決事項、次の一手をGit管理下へ残す。
切り替え後は `git status`、最新コミット、`AGENTS.md`、最新devlogを確認して再開する。

---

## つまずいたとき（Windows版）

| 症状 | 対処 |
|---|---|
| `python` が見つからない | インストール時に「Add python.exe to PATH」を入れ忘れ。入れ直すか環境変数PATHに追加 |
| `.env.txt` になってしまう | メモ帳で作らない。VS Code ターミナルで `Copy-Item .env.example .env` |
| `Activate.ps1` が実行できない | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`、または `activate.bat` を使う |
| `docker` コマンドが無い | Docker Desktop 本体を起動してから再実行 |
| 拡張が出てこない | VS Code を 1.98.0 以上に更新 →「Developer: Reload Window」 |
| サインインを繰り返す | `setx` でキーを設定後、VS Code を再起動して環境変数を反映 |
| フロントが API に繋がらない | バックエンドが 8000 番で起動しているか、`.env.local` の API_BASE を確認 |
| パスに日本語が含まれて不安 | `C:\Users\kazuy` は問題ない。コマンドは統合ターミナルで実行すればよい |

---

## 開発の進め方

`docs\product-design.md` 第6章「実装の着手順」に従い、**縦切り**で進める。
横に機能を広げる前に、まず「1論文が最後まで通る細い線」を完成させること。

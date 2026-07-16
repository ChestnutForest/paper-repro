# paper-repro-mvp

英語のAI論文（arXiv）を読み解いて再現実装まで支援するツールの MVP。
対象は「タイプB（学習なし・公式実装あり）」の論文に限定。

- 要件: [`docs/requirements.md`](docs/requirements.md)
- 設計: [`docs/mvp-design.md`](docs/mvp-design.md)
- Claude Code 向け指示: [`CLAUDE.md`](CLAUDE.md)

---

## 必要なもの

- **Node.js 18 以上**（Claude Code と Next.js に必要）
- **Python 3.12 以上**
- **VS Code 1.98.0 以上**
- **Docker Desktop**（PostgreSQL / Redis をコンテナで動かす）
- **Anthropic の有料プラン**（Claude Code 用。Pro/Max/Team/Enterprise のいずれか。APIキーでも可）

## クイックスタート

```bash
# 1. リポジトリのルートで、環境変数ファイルを用意
cp .env.example .env
#   → .env を開いて ANTHROPIC_API_KEY などを設定

# 2. DB と Redis を起動（Docker）
docker compose up -d

# 3. バックエンド
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload    # http://localhost:8000/docs で API 確認

# 4. フロントエンド（別ターミナル）
cd frontend
npm install
npm run dev                      # http://localhost:3000
```

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
├── docs/                 ← 要件・設計・手順書
├── backend/              ← FastAPI + Celery
└── frontend/             ← Next.js
```

## 開発の進め方

`docs/mvp-design.md` の第6章「実装の着手順」に従い、**縦切り**で進める。
まず1論文が最後まで通る細い線を作り、そこに機能を足す。

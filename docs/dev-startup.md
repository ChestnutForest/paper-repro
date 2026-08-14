# 開発環境の起動（ワンコマンド）

毎回 Docker → 仮想環境 → uvicorn と順に打つ代わりに、
スクリプト1本で **PostgreSQL 起動 → バックエンド起動 → Swagger UI を開く** までを実行する。

日々の作業手順は [`daily-routine.md`](daily-routine.md) を参照。

---

## 使い方

### Windows（PowerShell）

VS Code のターミナルで、プロジェクトのルートから実行する。

```powershell
cd C:\Users\kazuy\projects\paper-repro
```

```powershell
.\scripts\start-dev.ps1
```

> **初回だけ**「スクリプトの実行が無効」と出たら、実行ポリシーを一度緩める:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Mac / Linux（bash）

```bash
cd ~/projects/paper-repro
```

```bash
chmod +x scripts/start-dev.sh   # 初回のみ
```

```bash
./scripts/start-dev.sh
```

---

## スクリプトが行うこと

| ステップ | 内容 |
|---|---|
| 事前チェック | `.env` と `backend/.venv` の存在を確認（無ければ対処法を表示して停止） |
| ステップ1 | Docker 本体の稼働を確認 → `docker compose up -d` → **PostgreSQL(5432) に実際に接続できるまで待つ** |
| ステップ2 | 仮想環境を有効化して `uvicorn app.main:app --reload` を起動 |
| ステップ3 | `/health` が応答したのを検知して、Swagger UI を既定ブラウザで開く |

「コンテナが起動した」ことと「DBに接続できる」ことは別なので、**ポートを直接叩いて待つ**ようにしてある。

---

## 実行して確認する事項（チェックリスト）

上から順に確認する。1つでも欠けたら、下の「つまずいたとき」を見る。

- [ ] **`[OK] .env を確認`** が出た
- [ ] **`[OK] backend\.venv を確認`** が出た
- [ ] `docker compose up -d` で **postgres と redis が起動**した（`Started` または `Running`）
- [ ] **`[OK] PostgreSQL に接続できました`** が出た
- [ ] uvicorn のログに **`Application startup complete.`** が出た
- [ ] ブラウザが自動で開き、**Swagger UI が表示**された
- [ ] Swagger UI に **`/health`** と **`/api/v1/projects`** が並んでいる
- [ ] `/health` を Try it out → Execute で **Code 200 と `{"status":"ok"}`** が返る

最後の1つまで確認できれば、バックエンドは完全に正常です。

### フロントエンドも使う場合（別ターミナル）

このスクリプトはバックエンドまで。画面も見るなら、**別のターミナル**で:

```powershell
cd frontend
npm run dev
```

その後 `http://localhost:3000` を開く。

---

## 止め方

- **バックエンドを止める**：スクリプトを実行しているターミナルで `Ctrl + C`
- **DB も止める**：別のターミナルで

```powershell
docker compose down
```

（`down` してもデータは残る。PostgreSQL のデータは Docker ボリューム `pgdata` に保存されているため）

---

## つまずいたとき

| 表示・症状 | 意味と対処 |
|---|---|
| `[NG] .env がありません` | `Copy-Item .env.example .env`（Mac: `cp .env.example .env`）を実行 |
| `[NG] backend\.venv がありません` | `cd backend` → `python -m venv .venv` → 有効化 → `pip install -r requirements.txt` |
| `[NG] Docker に接続できません` | Docker Desktop 本体を起動し、クジラアイコンが緑（Engine running）になるまで待つ |
| `[NG] PostgreSQL に接続できませんでした` | `docker compose ps` で状態確認。ポート5432を別のPostgreSQLが使っていないかも確認 |
| ブラウザが `ERR_CONNECTION_REFUSED` | uvicorn がまだ起動していない。`Application startup complete.` を待ってから再読み込み |
| uvicorn 起動時に赤いトレースバック | DB接続まわりの可能性。エラー全文を確認する |
| 実行ポリシーのエラー（Windows） | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` を一度実行 |

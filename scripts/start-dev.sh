#!/usr/bin/env bash
# =============================================================================
# start-dev.sh — 開発環境の起動（Mac / Linux 用）
#
# やること:
#   ステップ1: Docker で PostgreSQL と Redis を起動し、接続できるまで待つ
#   ステップ2: Python 仮想環境を有効化してバックエンド（uvicorn）を起動
#   ステップ3: 起動を検知したら Swagger UI (http://localhost:8000/docs) を自動で開く
#
# 使い方（初回のみ実行権限を付ける）:
#   chmod +x scripts/start-dev.sh
#   ./scripts/start-dev.sh
#
# 止め方:
#   このターミナルで Ctrl + C （uvicorn が止まる）
#   DB も止めるなら別途: docker compose down
#
# 前提:
#   - Docker Desktop が起動していること
#   - backend/.venv が作成済みであること
#   - ルートに .env が存在すること
# =============================================================================

set -euo pipefail

# --- スクリプトの位置からプロジェクトのルートを求める（どこから呼んでも動くように）---
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "[info] プロジェクトルート: $ROOT"

# --- 事前チェック: .env があるか ---------------------------------------------
if [ ! -f "./.env" ]; then
  echo "[NG] .env がありません。次を実行してから再試行してください:"
  echo "     cp .env.example .env"
  exit 1
fi
echo "[OK] .env を確認"

# --- 事前チェック: 仮想環境があるか ------------------------------------------
if [ ! -f "./backend/.venv/bin/activate" ]; then
  echo "[NG] backend/.venv がありません。次を実行してから再試行してください:"
  echo "     cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi
echo "[OK] backend/.venv を確認"

# =============================================================================
# ステップ1: Docker で PostgreSQL / Redis を起動
# =============================================================================
echo ""
echo "=== ステップ1: Docker (PostgreSQL / Redis) を起動 ==="

# Docker 本体が動いているか確認（動いていないと以降が全部失敗する）
if ! docker info >/dev/null 2>&1; then
  echo "[NG] Docker に接続できません。Docker Desktop を起動してから再実行してください。"
  exit 1
fi

docker compose up -d

# PostgreSQL(5432) が実際に受け付けるまで待つ。
# コンテナが「起動した」ことと「接続できる」ことは別なので、ポートを直接叩いて確認する。
echo "[info] PostgreSQL(5432) の待ち受けを確認中..."
db_ready=0
for _ in $(seq 1 30); do
  if (exec 3<>/dev/tcp/localhost/5432) 2>/dev/null; then
    exec 3<&- 3>&-
    db_ready=1
    break
  fi
  sleep 1
done
if [ "$db_ready" -ne 1 ]; then
  echo "[NG] PostgreSQL に接続できませんでした（30秒待機）。"
  echo "     docker compose ps で状態を確認してください。"
  exit 1
fi
echo "[OK] PostgreSQL に接続できました"

# =============================================================================
# ステップ3の準備: 起動を検知したらブラウザを開く処理を裏で走らせる
#   （uvicorn は起動すると前面を占有するため、待ち受け役をバックグラウンドに置く）
# =============================================================================
(
  for _ in $(seq 1 40); do
    if curl -sf "http://localhost:8000/health" >/dev/null 2>&1; then
      if command -v open >/dev/null 2>&1; then
        open "http://localhost:8000/docs"          # macOS
      elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:8000/docs"      # Linux
      fi
      break
    fi
    sleep 1
  done
) &

# =============================================================================
# ステップ2: バックエンド（uvicorn）を起動
#   このターミナルはログ表示のため占有される。止めるときは Ctrl + C。
# =============================================================================
echo ""
echo "=== ステップ2: バックエンド (uvicorn) を起動 ==="
echo "[info] 起動後、Swagger UI が自動で開きます (http://localhost:8000/docs)"
echo "[info] 止めるときは Ctrl + C"

cd "$ROOT/backend"
# shellcheck disable=SC1091
source ./.venv/bin/activate
uvicorn app.main:app --reload

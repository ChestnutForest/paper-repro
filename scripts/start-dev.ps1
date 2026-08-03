# =============================================================================
# start-dev.ps1 — 開発環境の起動（Windows / PowerShell 用）
#
# やること:
#   ステップ1: Docker で PostgreSQL と Redis を起動し、接続できるまで待つ
#   ステップ2: Python 仮想環境を有効化してバックエンド（uvicorn）を起動
#   ステップ3: 起動を検知したら Swagger UI (http://localhost:8000/docs) を自動で開く
#
# 使い方（プロジェクトのルートで実行）:
#   .\scripts\start-dev.ps1
#
# 止め方:
#   このターミナルで Ctrl + C （uvicorn が止まる）
#   DB も止めるなら別途: docker compose down
#
# 前提:
#   - Docker Desktop 本体が起動していること（クジラアイコンが緑 = Engine running）
#   - backend\.venv が作成済みであること
#   - ルートに .env が存在すること
# =============================================================================

$ErrorActionPreference = "Stop"

# --- スクリプトの位置からプロジェクトのルートを求める（どこから呼んでも動くように）---
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Write-Host "[info] プロジェクトルート: $Root" -ForegroundColor Cyan

# --- 事前チェック: .env があるか ---------------------------------------------
if (-not (Test-Path ".\.env")) {
    Write-Host "[NG] .env がありません。次を実行してから再試行してください:" -ForegroundColor Red
    Write-Host "     Copy-Item .env.example .env" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] .env を確認" -ForegroundColor Green

# --- 事前チェック: 仮想環境があるか ------------------------------------------
if (-not (Test-Path ".\backend\.venv\Scripts\Activate.ps1")) {
    Write-Host "[NG] backend\.venv がありません。次を実行してから再試行してください:" -ForegroundColor Red
    Write-Host "     cd backend; python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] backend\.venv を確認" -ForegroundColor Green

# =============================================================================
# ステップ1: Docker で PostgreSQL / Redis を起動
# =============================================================================
Write-Host "`n=== ステップ1: Docker (PostgreSQL / Redis) を起動 ===" -ForegroundColor Cyan

# Docker Desktop 本体が動いているか確認（動いていないと以降が全部失敗する）
try {
    docker info *> $null
} catch {
    Write-Host "[NG] Docker に接続できません。Docker Desktop を起動し、" -ForegroundColor Red
    Write-Host "     クジラアイコンが緑 (Engine running) になってから再実行してください。" -ForegroundColor Yellow
    exit 1
}

docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[NG] docker compose up に失敗しました。" -ForegroundColor Red
    exit 1
}

# PostgreSQL(5432) が実際に受け付けるまで待つ。
# コンテナが「起動した」ことと「接続できる」ことは別なので、ポートを直接叩いて確認する。
Write-Host "[info] PostgreSQL(5432) の待ち受けを確認中..." -ForegroundColor Cyan
$dbReady = $false
for ($i = 1; $i -le 30; $i++) {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect("localhost", 5432)
        $client.Close()
        $dbReady = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $dbReady) {
    Write-Host "[NG] PostgreSQL に接続できませんでした（30秒待機）。" -ForegroundColor Red
    Write-Host "     docker compose ps で状態を確認してください。" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] PostgreSQL に接続できました" -ForegroundColor Green

# =============================================================================
# ステップ3の準備: 起動を検知したらブラウザを開くジョブを先に仕込む
#   （uvicorn は起動すると前面を占有するため、待ち受け役を裏で走らせておく）
# =============================================================================
Start-Job -ScriptBlock {
    for ($i = 1; $i -le 40; $i++) {
        try {
            Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
            Start-Process "http://localhost:8000/docs"   # Swagger UI を既定ブラウザで開く
            break
        } catch {
            Start-Sleep -Seconds 1
        }
    }
} | Out-Null

# =============================================================================
# ステップ2: バックエンド（uvicorn）を起動
#   このターミナルはログ表示のため占有される。止めるときは Ctrl + C。
# =============================================================================
Write-Host "`n=== ステップ2: バックエンド (uvicorn) を起動 ===" -ForegroundColor Cyan
Write-Host "[info] 起動後、Swagger UI が自動で開きます (http://localhost:8000/docs)" -ForegroundColor Cyan
Write-Host "[info] 止めるときは Ctrl + C" -ForegroundColor Cyan

Set-Location "$Root\backend"
& ".\.venv\Scripts\Activate.ps1"
uvicorn app.main:app --reload

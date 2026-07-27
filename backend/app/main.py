"""FastAPI エントリポイント。

まずは起動確認できる最小構成。
Claude Code にここから api/ のルーターを足していってもらう。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import projects
from app.core.db import init_db

app = FastAPI(
    title="paper-repro-mvp",
    version="0.1.0",
    description="英語AI論文の読解〜再現実装 支援ツール（MVP: タイプB・公式実装あり）",
)

# フロントエンド（Next.js: localhost:3000）からのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    """疎通確認用。"""
    return {"status": "ok"}

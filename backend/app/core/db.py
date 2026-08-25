"""SQLAlchemy の接続とセッション。

エクスポートする主なもの:
    engine: 設定の `database_url` から作るエンジン。
    SessionLocal: セッションのファクトリ。
    Base: ORM モデルが継承する宣言的ベース。
    init_db: 登録済みモデルのテーブルを作成する。
    get_db: FastAPI の依存性注入へ渡すセッション。

Note:
    マイグレーションツール（Alembic）は当面導入しない。スキーマを変えるときは
    テーブルを作り直す。導入する条件は docs/arch-guide/arc-datamodel.md 第4章に定めた。
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def init_db() -> None:
    """Create database tables for all registered ORM models."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """リクエスト1件ぶんの DB セッションを渡し、終了時に必ず閉じる。

    FastAPI の `Depends` から呼ぶことを想定する。

    Yields:
        Session: DB セッション。

    Note:
        テストでは `app.dependency_overrides` により in-memory SQLite の
        セッションへ差し替える。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

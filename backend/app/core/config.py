"""アプリ設定。環境変数（.env）から読み込む。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    anthropic_api_key: str = ""

    database_url: str = "postgresql+psycopg://repro:changeme@localhost:5432/paperrepro"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    # API コストの上限（USD）。超えたら実行を止める（要件 N-03）。
    cost_limit_usd: float = 5.0
    # 出力 zip のタイムゾーン（規約: JST）。
    output_tz: str = "Asia/Tokyo"


settings = Settings()

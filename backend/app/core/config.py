"""アプリ設定。環境変数（.env）から読み込む。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数（`.env`）から読み込むアプリ設定。

    Attributes:
        app_env: 実行環境の名前。既定は ``"development"``。
        anthropic_api_key: Claude API のキー。ログへ出さないこと（要件 N-02）。
        database_url: PostgreSQL への接続文字列。
        redis_url: Redis への接続文字列。
        celery_broker_url: Celery のブローカー。
        celery_result_backend: Celery の結果バックエンド。
        cost_limit_usd: API コストの上限（USD）。超えたら実行を止める（要件 N-03）。
        output_tz: 出力 zip のタイムゾーン。規約により JST 固定。
    """

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

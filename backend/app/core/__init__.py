"""アプリ横断の基盤。

モジュール:
    config: 環境変数から読み込む設定。
    db: SQLAlchemy のエンジン・セッション・宣言的ベース。
    states: プロジェクトの状態機械（phase・status・承認ゲート）。
"""

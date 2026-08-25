"""paper-repro のバックエンドアプリケーション本体。

英語AI論文の読解から再現実装までを支援する FastAPI アプリを構成する。
サブパッケージは api（ルーター）、core（設定・DB・状態機械）、models（ORM）、
services（取り込み・探索・LLM・照合）、workers（Celery タスク）。
"""

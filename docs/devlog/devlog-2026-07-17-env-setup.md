# 開発ログ: paper-repro-mvp — 2026-07-17（JST・環境構築編）

## メタ情報
- 日付（JST）: 2026-07-17
- 本日の作業範囲: VS Code拡張機能の一括インストール、Docker（PostgreSQL/Redis）起動、Python 3.13.14への更新と仮想環境構築、バックエンド（uvicorn）起動と動作確認、フロントエンド（Next.js）起動と画面表示、フロント↔バック連携の確認、動く土台のGitへのコミット&push、開発ログ資産化スキルへの画面キャプチャ記録機能の追加
- 参照したソース URL:
  - https://www.python.org/downloads/windows/ （Python 3.13.14のダウンロード）
  - https://www.docker.com/products/docker-desktop/ （Docker Desktop）

## Q&A 知識カード

### Q. VS Codeで推奨拡張機能の通知が出ないとき、一括インストールするにはどうするか？
A. コマンドパレット（Ctrl+Shift+P）で「Extensions: Show Recommended Extensions（拡張機能: 推奨事項を表示）」を実行し、「ワークスペースの推奨事項」グループの雲アイコン（下向き矢印つき）で一括インストールする。通知が出ないのは以前スキップしたか一部が既に入っているためで、この方法が本来の確実な入口である。
（出典: 本日の作業から）

### Q. VS Codeの「ワークスペースの推奨事項」と「その他の推奨事項」の違いは何か？
A. 「ワークスペースの推奨事項」はプロジェクトの.vscode/extensions.jsonで指定した必要な拡張（このプロジェクトでは7つ）である。「その他の推奨事項」はVS Codeが一般論で薦める別物（Azure Toolsなど）で、このプロジェクトとは無関係なため入れる必要はない。
（出典: 本日の作業から）

### Q. docker compose up -d の -d は何を意味するか？
A. -d は detached（デタッチ、バックグラウンド実行）の意味で、コマンドを打ち終わってもターミナルが使える状態でコンテナを動かす。docker compose up -d はdocker-compose.ymlに書かれたPostgreSQLとRedisをバックグラウンドで起動する。実行後にStartedが2つ出れば成功である。
（出典: 本日の作業から）

### Q. Windowsで「python は認識されません」と出る原因は何か？
A. ターミナルの種類の問題ではなく、PythonがPATH（実行ファイルの検索パス）に登録されていないことが原因である。Linux用ターミナル（WSL）に切り替えても解決しない。対処はPythonインストール時に「Add python.exe to PATH」にチェックを入れることで、Windowsでは開発をPowerShellで統一するのが最もシンプルである。
（出典: 本日の作業から）

### Q. uvicorn app.main:app --reload の各部分は何を意味するか？
A. uvicornはWebサーバー（ブラウザからのアクセスを受けてPythonコードに渡す窓口）である。app.main:appはコロンの前がファイル（app/main.py）、後が変数（main.py内のapp=FastAPI()で作った変数）を指す。--reloadはコードを保存すると自動で再起動する開発用オプションである。
（出典: 本日の作業から）

### Q. なぜエンドポイントに /health という名前を使うのか？
A. ヘルスチェック（health check、サービスが生きて動いているかの確認）という確立した概念に由来する。/healthは世界中の開発者が同じ意味で使う事実上の標準的な名前で、見ただけで「生存確認用の窓口」と理解できる。監視システムやロードバランサーが自動で叩いてサーバーの生死を判定するのに使う。
（出典: 本日の作業から）

### Q. HTTPステータスコードの200と201の違いは何か？
A. 200は単なる成功、201は特に「新しくリソースを作成できた」ことを表す成功である。GET /health（情報を取りに行くだけ）は200を返し、POST /api/v1/projects（プロジェクトを新規作成する）は201を返す。422は送られたデータが正しくないときの入力エラーを表す。
（出典: 本日の作業から）

### Q. POSTのSwagger UIにRequest bodyがあり、GETに無いのはなぜか？
A. POSTはデータを作る窓口なので「何を作るか」の材料（このプロジェクトではarxiv_url）を送る必要があり、その入力欄がRequest bodyである。GETは情報を取りに行くだけで材料が不要なため、Request bodyは無い。
（出典: 本日の作業から）

### Q. npm installで出るdeprecatedやvulnerabilitiesの警告は対処が必要か？
A. 対処不要である。deprecated（非推奨）警告は、自分が指定した部品が内部で使う「部品の部品」が古い、という将来向けのお知らせで、開発元が管理する領域である。vulnerabilities（脆弱性）もローカル開発では影響しないことがほとんど。npm audit fix --forceは動作を壊す変更を含むため実行しないのが正解。
（出典: 本日の作業から）

### Q. 仮想環境（.venv）を作る場所を間違えたらどう直すか？
A. deactivateで抜け、間違った場所のRemove-Item -Recurse -Force .venvで消し、正しいフォルダ（backend）にcdしてからpython -m venv .venvで作り直す。成功の目印はターミナル先頭が(.venv) ...\backend>になり、エクスプローラーでbackendの中に.venvがあること。
（出典: 本日の作業から）

## 開発の型の出現記録
本日分のみ。累積更新には前日の devlog を貼ってください。

### 決定ログ（なぜその技術・設計を選んだか）
| 決定した事項 | 選んだ理由 | 却下した代替案 | 本日/累積 |
|---|---|---|---|
| 開発をPowerShellで統一する | Docker/DB/ファイルがWindows側で動いており、環境を分けると混乱するため | Linux用ターミナル(WSL)に切替→WindowsとLinuxで扱いが分かれ却下 | 本日1 / 累積1 |
| Pythonを3.13.14に更新 | プロジェクト要件が3.12以上で、3.8.3では最新ライブラリが入らないため | 3.8.3のまま進める→pip installやコードでエラーの恐れがあり却下 | 本日1 / 累積1 |
| npm audit fix --forceは実行しない | breaking changes（動作を壊す変更）を含み構成が壊れる恐れがあるため | 警告を消すため強制修正→起動不能リスクで却下 | 本日1 / 累積1 |
| .env.localをGitに含めない | .env系は秘密情報を入れうるため慣習的にコミットしない | そのままコミット→秘密漏洩リスクの習慣が付き却下 | 本日1 / 累積1 |

### つまずき→解決の記録
| つまずき | 原因 | 解決方法 | 本日/累積 |
|---|---|---|---|
| VS Codeで推奨拡張の通知が出ない | 以前スキップor一部導入済み | コマンドパレットのShow Recommended Extensionsから一括導入 | 本日1 / 累積1 |
| python が認識されない | PythonがPATH未登録（3.8.3も古い） | 3.13.14を「Add to PATH」付きで導入しVS Code再起動 | 本日1 / 累積1 |
| .venvをbackendでなくルートに作った | cd backendせずに実行した | deactivate→ルートの.venv削除→cd backend→作り直し | 本日1 / 累積1 |
| .env.localがgit statusに出た | .gitignoreにfrontend/.env.localの除外行が無かった | .gitignoreに除外を追記しstatusから消えたのを確認 | 本日1 / 累積1 |

### Git・環境操作の記録
| 操作 | コマンド/手順 | 効果 | 本日/累積 |
|---|---|---|---|
| DBとRedisの起動 | docker compose up -d | PostgreSQL(5432)とRedis(6379)をバックグラウンド起動 | 本日1 / 累積1 |
| 仮想環境の作成と有効化 | python -m venv .venv / .venv\Scripts\Activate.ps1 | backend専用のPython環境を用意し有効化 | 本日1 / 累積1 |
| 依存インストール(backend) | pip install -r requirements.txt | FastAPI等を導入、Successfully installed | 本日1 / 累積1 |
| バックエンド起動 | uvicorn app.main:app --reload | localhost:8000でAPIを起動、/docsで確認 | 本日1 / 累積1 |
| 依存インストール(frontend) | npm install | 331パッケージ導入、node_modules生成 | 本日1 / 累積1 |
| フロントエンド起動 | npm run dev | localhost:3000で画面表示、Ready | 本日1 / 累積1 |
| .gitignoreへの除外追記 | Add-Content .gitignore "frontend/.env.local" | .env.localをGit管理から除外 | 本日1 / 累積1 |
| 土台のコミット&push | git add . / git commit / git push | 動く土台(4ファイル)をGitHubに反映(3 Commits, d12abae) | 本日1 / 累積1 |

## 語彙・用語リスト（プロジェクト固有）
| 用語 | 定義 |
|---|---|
| uvicorn | Python製のASGI Webサーバー。ブラウザ等のリクエストを受けてFastAPIのコードに渡す窓口。既定でポート8000を使う |
| Swagger UI | FastAPIがコードから自動生成するAPIの「説明書兼試乗場」の画面。localhost:8000/docsで見られ、その場でAPIを試せる |
| OpenAPI | APIの仕様を決まった形式で書き表す世界共通ルール。Swagger UIはこれを人間向けの画面に変換して表示する |
| ヘルスチェック | サービスが生きて動いているかを確認する仕組み。/healthエンドポイントで{"status":"ok"}を返す |
| ステータスコード200/201/422 | 200=成功、201=作成成功、422=入力エラー。POSTでの作成成功は201が返る |
| Request body | POSTでデータを送るときの本体。このプロジェクトではarxiv_urlを送る。GETには無い |
| deprecated | 非推奨・古いの意味。npm installで「部品の部品」が古いと出る将来向けの警告。動作には影響しない |
| .env.local | フロント用の環境設定ファイル。NEXT_PUBLIC_API_BASEでバック接続先を指定。秘密を含みうるためGitに含めない |
| project_id (UUID) | プロジェクトに自動で振られる世界で一意な識別子。projects.pyのuuid4()が生成する |

## 未解決の疑問と翌日の開発計画
- 未解決の疑問:
  - 現状はインメモリ保存のため、uvicorn再起動で作成したプロジェクトが消える（PostgreSQL保存への置き換えが必要）
- 翌日の計画:
  - Claude CodeにStep 1の本命「projects.pyのインメモリ保存をPostgreSQLに置き換える（再起動でも消えないようにする）」を依頼する
  - 余力があればフロントの画面文言をi18n（t("キー")方式）で書き始める

## 画面キャプチャ記録
本日ユーザーがアップロードした画面キャプチャを、アップロード順に実行ログ風に記録する（画像自体は埋め込まず、何の画面か＋結果をテキストで残す）。

| # | 何の画面か | 結果・状態 |
|---|---|---|
| 1 | VS Codeでpaper-repro-mvpを開いた直後（ようこそ画面） | ルートが正しく開けている。エクスプローラーに.vscode/backend/docs/frontend等が見える |
| 2 | VS Codeで.envを開いた画面（CLAUDE.mdタブあり） | Copy-Itemで.envを作成成功、817バイト。.env.txt問題を回避 |
| 3 | GitHubログイン後のDashboard（アカウントChestnutForest） | ログイン成功。空リポジトリ作成の直前 |
| 4 | Authorize Git Credential Managerの認証画面 | git push途中の認証。緑のAuthorizeボタンで承認する段階 |
| 5 | GitHubのpaper-repro-mvpリポジトリ（push後） | 初回push成功。Private、1 Commit、初回コミット:MVP雛形が反映 |
| 6 | 拡張機能パネル @recommended（推奨一覧） | ワークスペースの推奨事項7つが表示、一括インストールの直前 |
| 7 | 拡張機能Dockerの詳細画面 | 7つの推奨拡張がすべてインストール済み（インストールボタンが消え歯車表示） |
| 8 | Docker Desktopのcontainers画面（Sign in有無の質問） | Sign in不要と判断。左下クジラが緑=Engine running、v4.12.0 |
| 9 | ターミナルでpython -m venv .venvのエラー | python未認識。原因はPATH未登録（py --versionは3.8.3と判明） |
| 10 | python.org Windows版ダウンロードページ | 3.12系が無く、Stable Releasesの3.13.14を選ぶ判断 |
| 11 | Python 3.13.14インストール後のVS Code（venvエラー画面） | py --versionは3.13.14に更新成功。VS Code再起動の案内段階 |
| 12 | VS Code再起動後、.venvがルートにできた画面 | python --versionが3.13.14。ただし.venvをbackend外に作る誤り発覚 |
| 13 | .venvを正しい場所に作り直した画面 | (.venv) ...\backend> になり、backend内に.venv。「パッケージ更新中エラー」通知は無視でよい |
| 14 | Swagger UI（localhost:8000/docs）表示 | バックエンド起動成功。/healthや/api/v1/projectsが並ぶ |
| 15 | GET /health を Try it out で展開した画面 | Execute直前。Example Valueは見本（本物ではない）と確認 |
| 16 | GET /health を Execute 実行後 | Code 200、{"status":"ok"}、server: uvicorn。疎通確認成功 |
| 17 | POST /api/v1/projects を開いた画面 | Try it out未押下のためExecute無し。Request bodyにarxiv_url |
| 18 | POST /api/v1/projects の入力編集画面 | Edit Valueにarxiv_url入力済み、Execute直前 |
| 19 | POST /api/v1/projects を Execute 実行後 | Code 201、project_id自動生成(UUID)、state:created。作成成功 |
| 20 | フロント画面 localhost:3000 表示 | プロジェクト一覧に2件表示。フロント↔バック連携成功、土台が全部つながった |

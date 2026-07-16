# MVP 詳細設計：画面遷移・APIエンドポイント・技術スタック

- 対象: 要件定義書 v0.1 の MVP スコープ（タイプB・公式実装あり）
- 版: v0.1

前提（要件定義書より）: **human-in-the-loop の伴走型パイプライン。**
GPU 不要・レンダリング不要・LLM-as-a-Judge 不要に絞った範囲。

---

## 0. 設計の背骨（3つの原則）

1. **非同期ジョブ + WebSocket 進捗。** 取り込み・読解・推論・実行はすべて長時間。
   REST で「投げてジョブID受領」、進捗は WS でストリーム。同期で待たせない。
2. **サンドボックスは別プロセスに隔離。** 信頼できないコードを実行するワーカーを、
   API サーバと同じ空間に置かない。ネットワーク遮断・使い捨て。
3. **プロジェクトはステートマシン。** Phase 0〜6 は承認ゲートで進む状態遷移。
   `phase`（現在地）× `status`（idle / running / waiting_approval / failed）で管理。

---

## 1. 状態遷移（プロジェクトのライフサイクル）

```
created
  │ POST /intake（取り込み・第1パス・タイプ判定・実装探索）
  ▼
intake_review        ← 承認ゲート①：方針を5択で確定
  │ POST /policy
  ▼
reading              ← spec 編集・仮定台帳作成（公式コード読解で埋める）
  │ POST /spec:finalize（承認ゲート②：タイプ判定と spec を確定）
  ▼
implementing         ← サニティ階段を下から実行
  │  段3(オラクル満点) と 段4(異常系0点) の pass が必須
  │ POST /sanity:gate（承認ゲート③：評価器の正しさを確認）
  ▼
scoring              ← 識別力の高い2タスクで論文値と照合
  │ POST /artifacts/zip
  ▼
done
```

**失敗系**: どの状態でも実行ジョブが失敗すれば `failed` に落ち、原因ログを提示して同じ状態へ戻す。
`skip`（見送り）は intake_review からいつでも選べる終端。

---

## 2. 画面遷移

```
┌─────────────┐
│ ダッシュボード │ プロジェクト一覧・進捗・コスト
└──────┬──────┘
       │「新規」→ arXiv URL 入力
       ▼
┌─────────────┐
│  インテーク   │ 第1パス要約 / 公式実装の有無 / タイプA・B判定
│             │ ★承認ゲート①: 方針5択（フル/縮小/改造/部分/見送り）
└──────┬──────┘
       ▼
┌─────────────────────────┐
│  リーディング作業台（3ペイン）  │
│ [論文ビューア][specエディタ][仮定台帳] │
│ タイプ判定の確認・上書き        │
│ ★承認ゲート②: spec と タイプ を確定 │
└──────┬──────────────────┘
       ▼
┌─────────────────────────┐
│  実装・検証台               │
│ [ノートブック/コード][実行コンソール] │
│ [サニティ階段: 段1..7 の pass/fail]  │
│ ★承認ゲート③: 段3満点・段4=0 を確認  │
└──────┬──────────────────┘
       ▼
┌─────────────┐
│ 照合・レポート │ 再現値 vs 論文値（±5判定・色分け）
│             │ 規約名 zip ダウンロード
└─────────────┘
```

### 画面別の主要UI要素

| 画面 | 主要要素 |
|---|---|
| ダッシュボード | プロジェクトカード（状態バッジ・進捗率・累計コスト）、新規ボタン |
| インテーク | Abstract要約、公式リポジトリへのリンク、A/Bバッジ+根拠、**方針5択ラジオ+確定ボタン**、コスト見積もり |
| リーディング作業台 | 左:論文HTML/PDFビューア（KaTeX）、中:Markdownエディタ（Monaco・プレビュー）、右:台帳テーブル（疑わしさ 高/中/低 タグ、状態） |
| 実装・検証台 | ノートブックプレビュー、**サニティ階段（段ごとに pass/fail/未実行、段3・段4を強調）**、実行コンソール（stdout・生成ファイルの目視リンク）、コスト |
| 照合・レポート | タスク別スコア表（再現/論文/差/判定）、サチュレーション側・崩壊側のラベル、zipダウンロード |

---

## 3. APIエンドポイント（MVP）

規約: REST は `/api/v1`。長時間処理は **202 Accepted + `{job_id}`** を返し、進捗は WS。
認証は MVP では単一ユーザー想定（Bearer トークン）。

### 3.1 プロジェクト / 状態

| メソッド | パス | 役割 | 返却 |
|---|---|---|---|
| GET | `/projects` | 一覧（状態・進捗・コスト） | `Project[]` |
| POST | `/projects` | 作成。arXiv URL を受け、取り込みジョブ起動 | `{project_id, job_id}` |
| GET | `/projects/{id}` | 詳細（現在の phase/status を含む） | `Project` |
| DELETE | `/projects/{id}` | 削除（コンテナ・成果物も破棄） | `204` |

### 3.2 Phase 0：インテーク

| メソッド | パス | 役割 |
|---|---|---|
| POST | `/projects/{id}/intake` | 第1パス要約 + タイプ判定 + 実装探索（GitHub/PwC/OpenReview）をジョブ実行 |
| GET | `/projects/{id}/intake` | 結果取得（要約・official_repo_url・type・cost見積もり） |
| POST | `/projects/{id}/policy` | **承認ゲート①**。`{policy: full/reduced/adapt/partial/skip}` を確定 → `reading` へ |

### 3.3 Phase 1〜3：リーディング（spec・台帳・Δ）

| メソッド | パス | 役割 |
|---|---|---|
| POST | `/projects/{id}/spec:draft` | LLM で spec 草案生成（ジョブ）。**公式リポジトリ読解の結果を反映** |
| GET / PUT | `/projects/{id}/spec` | spec.md 取得 / 人手編集の保存 |
| GET | `/projects/{id}/assumptions` | 仮定台帳の一覧 |
| POST | `/projects/{id}/assumptions` | 行追加 |
| PUT / DELETE | `/projects/{id}/assumptions/{aid}` | 行更新（疑わしさ・状態）/ 削除 |
| GET / PUT | `/projects/{id}/deltas` | Δリスト取得/更新（5超で警告フラグ） |
| POST | `/projects/{id}/repo:read` | 公式リポジトリを clone し、抽出関数・スコア計算・パーサ・プロンプトを静的抽出（ジョブ） |
| POST | `/projects/{id}/spec:finalize` | **承認ゲート②**。type と spec を確定 → `implementing` へ |

### 3.4 Phase 4：サニティ階段（サンドボックス）

| メソッド | パス | 役割 |
|---|---|---|
| POST | `/projects/{id}/notebook:generate` | Colab `.ipynb` を生成（環境ピン留め・サニティ段・照合を含む） |
| POST | `/projects/{id}/sanity/{rung}` | 指定段を**サンドボックスで実行**（ジョブ）。rung=data/parse/oracle/adversarial/e2e/subset |
| GET | `/projects/{id}/sanity` | 各段の pass/fail/ログ参照 |
| POST | `/projects/{id}/sanity:gate` | **承認ゲート③**。段3(oracle)満点・段4(adversarial)=0 を確認 → `scoring` へ |

### 3.5 Phase 5〜6：照合・成果物

| メソッド | パス | 役割 |
|---|---|---|
| POST | `/projects/{id}/scores` | 再現値と論文値を照合（±5判定）。`{tasks:[{name,mine,paper}]}` |
| GET | `/projects/{id}/scores` | 照合結果 |
| POST | `/projects/{id}/artifacts/zip` | **規約名 zip（files_reify_YYYYMMDD_hhmm.zip, JST）**生成 |
| GET | `/projects/{id}/artifacts` | 成果物一覧（notebook/code/spec/zip） |
| GET | `/projects/{id}/cost` | Phase 別コストと合計 |

### 3.6 ジョブ / ストリーム

| メソッド | パス | 役割 |
|---|---|---|
| GET | `/jobs/{job_id}` | ジョブ状態（queued/running/done/failed）とサマリ |
| WS | `/ws/jobs/{job_id}` | 進捗率・ログ行・stdout・生成物イベントをストリーム |

### 3.7 エンドポイント共通仕様

- 長時間ジョブ: `202 { job_id }` → クライアントは `/ws/jobs/{job_id}` 購読
- 実行前に**ドライラン見積もり**（例数×モデル数×単価）を返し、上限超過は起動拒否（N-03）
- 冪等: 同一段の再実行は前結果を上書きし履歴に残す（N-05）

---

## 4. 技術スタック選定

### 4.1 推奨構成

| 層 | 推奨 | 主な代替 | 選定理由 |
|---|---|---|---|
| フロントエンド | **Next.js (React) + TypeScript** | SvelteKit, Vue/Nuxt | WS/SSE容易、Monaco・KaTeX 等の資産が揃う、型安全 |
| エディタ | **Monaco Editor** | CodeMirror | spec/コード編集。VSCode同等の体験 |
| 数式表示 | **KaTeX** | MathJax | 高速・軽量 |
| APIサーバ | **FastAPI (Python)** | Node/NestJS, Go | **ML/評価資産がPython。** async・型・WS・OpenAPI自動生成。`t_scorer.py` 等を直接流用 |
| ジョブキュー | **Redis + Celery** | RQ, Arq, Dramatiq | 非同期ジョブの定番。進捗は Redis Pub/Sub → WS 中継 |
| DB | **PostgreSQL** | MySQL | 台帳の可変列は JSONB。承認履歴・状態遷移に強い |
| オブジェクトストレージ | **S3互換（MinIO/AWS S3）** | ローカルFS(初期) | 生成物・中間ファイル・zip |
| **サンドボックス** | **gVisor もしくは Firecracker 上の使い捨てコンテナ** | Docker+seccomp/ネットns, nsjail | **信頼できないコードの実行分離。ここは最優先で妥協しない** |
| LLM | **Claude API（抽象化層で包む）** | 他プロバイダ差替可 | spec抽出・数式→コード下訳・翻訳。プロバイダ非依存に |
| 認証(MVP) | 単一ユーザー + Bearer | OAuth(将来) | MVPは最小限 |
| デプロイ | Docker Compose（MVP）→ k8s（拡張時） | — | まず1ホストで、実行ワーカーだけ隔離 |

### 4.2 なぜ FastAPI（バックエンドを Python に寄せる）か

- サニティチェック・スコア照合・ノートブック生成は**すべて Python 資産**。
  今回作成した `t_scorer.py`・オラクル生成・照合ロジックが**そのまま流用できる**。
- 公式リポジトリの読解（AST 解析・関数抽出）も Python で完結。
- フロントを TS、バックを Python に分けても、**「重い処理は Python 一貫」**が最も無駄がない。

### 4.3 サンドボックスの構成（最重要・再掲）

```
[APIサーバ]──(ジョブ投入)──▶[実行ワーカー]
                              └─ 1実行 = 1 使い捨てコンテナ
                                 ├─ ネットワーク: 原則遮断（許可リストproxy経由のみ）
                                 ├─ リソース上限: CPU/mem/時間/書込量
                                 ├─ FS隔離: ホスト・他PJへ到達不可
                                 └─ 実行後: コンテナ破棄、生成物のみストレージへ退避
```

- MVP は **CPU のみ・ネットワーク遮断**で十分（タイプBに絞ったため）。
- gVisor/Firecracker で**カーネル分離**まで行うと、任意コード実行前提でも安全度が上がる。
- **中間生成物（画像・ファイル）は必ず退避し、UI で目視できるように**（タイプBの教訓）。

### 4.4 却下した選択肢と理由

| 却下案 | 理由 |
|---|---|
| バックエンドも Node/TS で統一 | 評価・ML 資産が Python にあり、二重実装になる |
| 同期 REST で処理を待たせる | 数十分ジョブで破綻。タイムアウト・UX崩壊 |
| サンドボックス無しでホスト実行 | **信頼できない第三者コードの実行。論外**（セキュリティ致命傷） |
| 素の Docker のみ（分離なし） | コンテナ脱出リスク。任意コード前提なら gVisor/Firecracker 相当が要る |
| DB を持たずファイルだけで管理 | 状態遷移・台帳・承認履歴・冪等再開が破綻 |

---

## 5. MVP 構成図（デプロイ）

```
                 [ブラウザ: Next.js]
                        │ HTTPS / WSS
                 ┌──────▼──────┐
                 │  FastAPI     │  REST + WS
                 │  (APIサーバ)  │
                 └──┬────┬───┬──┘
       ┌────────────┘    │   └────────────┐
   [PostgreSQL]      [Redis]          [S3/MinIO]
   状態・台帳・履歴   キュー/進捗Pub/Sub  成果物・中間物
                       │
                 ┌─────▼─────┐
                 │ 実行ワーカー │ Celery
                 │ (Python)   │
                 └─────┬─────┘
                       │ 1実行=1コンテナ（隔離・使い捨て）
                 ┌─────▼─────────────┐
                 │ サンドボックス       │ gVisor/Firecracker
                 │ ネット遮断・上限・破棄 │ CPUのみ(MVP)
                 └───────────────────┘
```

---

## 6. 実装の着手順（サニティの精神で、縦に薄く貫く）

1. **骨組み1本を貫通させる**: arXiv URL 投入 → 取り込み → spec 草案 → 手編集 → zip 出力（サンドボックス無し）
2. **サンドボックスを足す**: CPU・ネット遮断の使い捨てコンテナで、段3(オラクル満点)・段4(異常系0点)だけ動かす
3. **照合を足す**: 2タスクの再現値 vs 論文値、±5 判定
4. **承認ゲートと状態機械を締める**: 各 Phase 末のゲートを必須化、失敗系の復帰を整える

**いきなり全機能を横に広げない。** まず1本の縦線（1論文が done まで通る）を最短で通し、そこに機能を足す。
これは Phase 4 のサニティチェックと同じ思想（縦切り実装）である。

# paper-repro データモデル仕様

`paper-repro` の永続化層を定める。**フェーズ0（データ永続化・状態遷移）の実装は本書を仕様とする。**

- 版: v0.1（草案・未承認）
- 作成日: 2026年8月25日
- 状態: **草案。第5章の未決事項3件を利用者が判断するまで、実装に着手しない。**

## 1. 本書の位置づけ

### 1.1 目的

要件定義とプロダクト設計に散在するデータ構造の記述を、**DDL に落とせる粒度で1か所に確定させる**。
型・NULL可否・既定値・外部キー・インデックス・ENUM の値までを決める。

### 1.2 上位文書との関係

| 文書 | 関係 |
|---|---|
| [`../requirements.md`](../requirements.md) 6.1〜6.4 | 17エンティティのER図。本書はそのうちフェーズ0で作るものを DDL 化する |
| [`../product-design.md`](../product-design.md) 1.1〜1.4 | 状態機械とスキーマ差分。本書は状態の持ち方を確定する |
| [`arc-architecture.md`](arc-architecture.md) | 全体構造。本書は永続化層のみを扱う |
| [`../roadmap.md`](../roadmap.md) | フェーズ0の作業項目。本書はその 0-1・0-2 の仕様 |

### 1.3 対象範囲

**フェーズ0では `projects` と `papers` の2テーブルのみを作る。**
残る15エンティティは、それを使う機能を実装するフェーズで追加する
（`assumptions` はフェーズ3、`sanity_runs` はフェーズ4、`score_compares` はフェーズ5など）。

先にテーブルだけ作っても、使われないまま定義が古びる。**使う直前に作る。**

---

## 2. 既存記述との矛盾（実装前に解消が必要）

要件定義・プロダクト設計・現行コード（`backend/app/`）を突き合わせた結果、**9件の食い違い**が見つかった。
本書は各件について解消案を示す。⚠️ が付く3件は利用者の判断を要する。

| # | 論点 | 要件定義 / プロダクト設計 | 現行コード | 本書の解消案 |
|---|---|---|---|---|
| 1 | ⚠️ 状態の持ち方 | `phase` × `status` の**2列**（設計 原則3） | `state` **1列**に混在 | 2列に分ける（3.3節） |
| 2 | ⚠️ 汎用遷移API | 定義なし。承認ゲートは**迂回不可能**（`REQ-C06`） | `POST /projects/{id}/state` で任意遷移が可能 | 廃止する（5.2節） |
| 3 | ⚠️ `course` 列 | `NOT NULL`・既定値なし（設計 1.4、`REQ-C01`） | 列が存在しない | 追加。API 変更を伴う（5.1節） |
| 4 | `approval_kind` 列 | 事象駆動ゲート④⑤⑥用（設計 1.3） | 列が存在しない | 追加する |
| 5 | 失敗からの復帰 | 「原因ログを提示し**同じ状態へ戻す**」（設計 1.1） | `FAILED` が phase を潰すため、どこへ戻るか判別不能 | #1 の2列化で解決 |
| 6 | `CREATED` での失敗 | どの状態でも失敗しうる | `FAILED → CREATED` の遷移が無く復帰不能 | #1 の2列化で解決 |
| 7 | `reading` の自己ループ | `course=reading` のとき反復（設計 1.2） | 定義なし | 3.4節の遷移表に含める |
| 8 | `policy` の型 | ENUM（ER図 6.1） | `Policy` Enum を定義しつつ列は `String` | ENUM 制約を列に適用 |
| 9 | 主キー名と欠落列 | `id` PK、`paper_type`・`created_at`・`updated_at` あり | `project_id`、3列とも欠落 | 列名は `project_id` を維持（5.3節）、欠落列は追加 |

### 2.1 特に重い矛盾：#1 状態の持ち方

現行コードは `created` `intake_review` `reading` `implementing` `scoring` `done` `skipped` `failed`
を**1つの列**に入れている。しかし `failed` は工程ではなく**実行結果**である。

このため次の不整合が生じている。

- `reading` で失敗すると `state = failed` となり、**どの工程で失敗したかが失われる**
- 結果として `ALLOWED_TRANSITIONS` は `FAILED → {READING, IMPLEMENTING, SCORING}` と
  **どこへでも戻れる**定義になっている。設計が言う「同じ状態へ戻す」を実現できない
- `created` で取り込みジョブが失敗した場合、`FAILED → CREATED` が無いため**復帰不能**

プロダクト設計 原則3 の「`phase`（現在地）× `status`（idle / running / waiting_approval / failed）」
に従い、2列へ分けることで3つとも解消する。

---

## 3. テーブル定義

### 3.1 `projects`

| 列 | 型 | NULL | 既定値 | 説明 | 根拠 |
|---|---|---|---|---|---|
| `project_id` | `VARCHAR(36)` | NOT NULL | — | 主キー。UUID v4 の文字列表現 | 現行コード |
| `course` | `course_enum` | **NOT NULL** | **なし** | 読解 / 再現実装 | `REQ-C01`、設計 1.4 |
| `arxiv_url` | `TEXT` | NOT NULL | — | 入力された論文の URL | 現行コード |
| `phase` | `phase_enum` | NOT NULL | `created` | 工程上の現在地 | 設計 原則3 |
| `status` | `status_enum` | NOT NULL | `idle` | その工程での実行状態 | 設計 原則3 |
| `approval_kind` | `approval_kind_enum` | NULL | `NULL` | `status='waiting_approval'` のとき、どのゲートで待つか | 設計 1.3 |
| `paper_type` | `paper_type_enum` | NULL | `NULL` | A / B。判定前は NULL | ER図 6.1 |
| `policy` | `policy_enum` | NULL | `NULL` | 方針5択。ゲート①の前は NULL | ER図 6.1、#8 |
| `title` | `TEXT` | NULL | `NULL` | 取り込み後に埋まる | ER図 6.1 |
| `course_changed_at` | `TIMESTAMPTZ` | NULL | `NULL` | コース切替の時刻 | 設計 1.4 |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | | ER図 6.1 |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | 更新時に更新する | ER図 6.1 |

**インデックス**: `project_id`（主キー）、`(phase, status)`（一覧のフィルタ用）。

**`course` に既定値を置かない理由。** 既定値があると、利用者が選ばないまま片方の経路に入り、
「開始時に選択する」という `REQ-C01` が骨抜きになる（設計 1.4 の判断を踏襲）。

### 3.2 `papers`

`projects` と 1 対 1。取り込み結果を保持する。

| 列 | 型 | NULL | 既定値 | 説明 | 根拠 |
|---|---|---|---|---|---|
| `paper_id` | `VARCHAR(36)` | NOT NULL | — | 主キー | — |
| `project_id` | `VARCHAR(36)` | NOT NULL | — | `projects.project_id` への外部キー。`UNIQUE` | 1対1 |
| `source` | `TEXT` | NOT NULL | — | 入手元（`arxiv` / `pdf` / `doi` など） | `REQ-C03-S01` |
| `identifier` | `TEXT` | NULL | `NULL` | arXiv ID・DOI など | `REQ-C03-S01` |
| `version` | `TEXT` | NULL | `NULL` | v1 / v2 など | `REQ-C03-S01` |
| `category` | `TEXT` | NULL | `NULL` | arXiv のカテゴリー | `REQ-C03-S01` |
| `publication_status` | `JSONB` | NOT NULL | `'[]'` | プレプリント・査読・採択の**履歴**。配列 | `REQ-C03-S01` |
| `abstract` | `TEXT` | NULL | `NULL` | | ER図 6.1 |
| `official_repo_url` | `TEXT` | NULL | `NULL` | 公式実装 | ER図 6.1 |
| `fetched_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | 取得日時 | `REQ-C03-S01` |

**外部キー**: `project_id → projects.project_id`（`ON DELETE CASCADE`）。
プロジェクトを消したら論文も消える（設計 3.1 の `DELETE /projects/{id}` は成果物も破棄する）。

**`NULL` の意味。** `REQ-C03-S01` は「不明な情報を推測で補わない」を要求する。
取得できなかった項目は `NULL` のままとし、**空文字や推測値で埋めない。**

### 3.3 ENUM の値

| ENUM 名 | 値 | 根拠 |
|---|---|---|
| `course_enum` | `reading`, `reproduction` | 設計 1.2 |
| `phase_enum` | `created`, `intake_review`, `reading`, `implementing`, `scoring`, `done`, `skipped` | 設計 1.1。**`failed` を含めない** |
| `status_enum` | `idle`, `running`, `waiting_approval`, `failed` | 設計 原則3 |
| `approval_kind_enum` | `policy`, `spec`, `sanity`, `interpretation`, `conflict`, `comprehension` | 設計 1.3 のゲート①〜⑥ |
| `paper_type_enum` | `A`, `B` | 現行コード |
| `policy_enum` | `full`, `reduced`, `adapt`, `partial`, `skip` | 現行コード、要件 1.2 |

**`phase_enum` から `failed` を除いたことが #1・#5・#6 の解消そのものである。**
失敗は `status='failed'` で表し、`phase` は失敗した工程を保持し続ける。
復帰は `status` を `idle` に戻すだけでよく、遷移表を増やさない。

### 3.4 状態遷移表

`phase` の遷移のみを定義する。`status` の遷移は工程に依存しないため、3.5節で別に定める。

| 遷移元 `phase` | 遷移先 `phase` | 契機 | ゲート |
|---|---|---|---|
| `created` | `intake_review` | `POST /projects/{id}/intake` の完了 | — |
| `intake_review` | `reading` | `POST /projects/{id}/policy`（`skip` 以外） | ①`policy` |
| `intake_review` | `skipped` | `POST /projects/{id}/policy`（`skip`） | ①`policy` |
| `reading` | `reading` | `course=reading` のときの反復（#7） | — |
| `reading` | `implementing` | `POST /projects/{id}/spec:finalize` | ②`spec` |
| `implementing` | `scoring` | `POST /projects/{id}/sanity:gate` | ③`sanity` |
| `scoring` | `done` | `POST /projects/{id}/artifacts/zip` | — |

**上記以外の `phase` 遷移は拒否する。** `done` と `skipped` は終端。

`course=reading` のプロジェクトは `implementing` へ進まない（設計 1.2）。
**この制約は遷移表ではなく、`spec:finalize` の実行時に `course` を見て判定する。**
遷移表に条件を持ち込むと、表が状態と属性の両方に依存して読めなくなるためである。

### 3.5 `status` の遷移

| 遷移元 | 遷移先 | 契機 |
|---|---|---|
| `idle` | `running` | ジョブ起動 |
| `running` | `idle` | ジョブ正常終了 |
| `running` | `failed` | ジョブ失敗。`phase` は**変えない** |
| `running` | `waiting_approval` | 事象駆動ゲート④⑤⑥の発生。`approval_kind` を設定 |
| `failed` | `idle` | 利用者が再実行を選択。`phase` は変えない |
| `waiting_approval` | `idle` | `:resolve` または `:defer`。`approval_kind` を `NULL` に戻す |

**不変条件**: `status = 'waiting_approval'` のときに限り `approval_kind IS NOT NULL`。
それ以外では `approval_kind IS NULL`。CHECK 制約で表現する。

---

## 4. マイグレーション方針

**フェーズ0では Alembic を導入せず、`Base.metadata.create_all()` で作成する。**

理由は、公開前かつ利用者が1名で、**捨ててよいデータしか無い**ため。
スキーマを変えるときはテーブルを作り直す。この段階でマイグレーションを書く手間は、得る安全に見合わない。

**Alembic を導入する条件**を先に決めておく。次のいずれかを満たしたとき導入する。

1. 捨てられないデータが入ったとき（実際の論文プロジェクトを継続運用し始めたとき）
2. 利用者が2名以上になったとき
3. フェーズ6の一般公開に着手するとき

導入時に既存テーブルから初期リビジョンを起こす。**それまでは `create_all()` を使う。**

---

## 5. 未決事項（利用者の判断が要る）

### 5.1 ⚠️ `course` を必須にすると `POST /projects` が変わる

`course` を `NOT NULL`・既定値なしにすると、プロジェクト作成時に必ず受け取る必要がある。
現行の `POST /projects` は `arxiv_url` のみを受け取るため、**リクエストの形が変わる**。

| 案 | 内容 | 長所 | 短所 |
|---|---|---|---|
| **A** | `POST /projects` が `course` を必須で受け取る | 不正な状態が一瞬も存在しない。`REQ-C01` に最も忠実 | 既存 API の破壊的変更。フロントの作成画面も変える |
| B | `course` を NULL 許容にし、選択後に `POST /course` で埋める | API を変えずに済む | 「開始時に選択する」が守られず、未選択のプロジェクトが残りうる |
| C | 作成前にコース選択画面を置き、`course` 込みで1回だけ POST する | 設計 2章の画面遷移（コース選択→インテーク）と一致 | フロントの実装順が変わる |

**本書の推奨は A（実質 C と同じ）。** 設計 2章が既にコース選択画面をインテークの前に置いており、
画面の流れと API の形が一致する。破壊的変更といっても利用者は開発者本人のみで、影響は小さい。

### 5.2 ⚠️ 汎用の状態遷移エンドポイントを廃止してよいか

現行の `POST /projects/{id}/state` は、任意の遷移を直接指定できる。
`can_transition` で遷移の妥当性は見るが、**承認ゲートを通さずに `reading → implementing` へ進める。**

これは `REQ-C06` の「迂回不可能な承認ゲート」に反する。

| 案 | 内容 |
|---|---|
| **A** | 廃止する。遷移は `policy` / `spec:finalize` / `sanity:gate` など**ゲートのエンドポイント経由のみ** |
| B | 開発用として残し、`app_env=development` のときだけ有効にする |

**本書の推奨は A。** B は「開発では通るが本番では通らない経路」を作り、テストの意味を薄める。
テストで状態を進めたい場合は、ゲートのエンドポイントを順に呼ぶか、DB を直接組み立てればよい。

### 5.3 主キーの列名を `id` と `project_id` のどちらにするか

ER図（要件 6.1）は `id`、現行コードは `project_id` である。

**本書は `project_id` を推奨する。** 既にコードとテストが存在し、変更すると
`papers.project_id` との対応も分かりにくくなる。要件定義の ER 図側を `project_id` に合わせる。

---

## 6. 本書に含まれないもの

- `assumptions` `claims` `evidences` など、フェーズ1以降で使う15テーブルの定義（1.3節）
- Celery のジョブ状態の永続化（フェーズ2で扱う）
- オブジェクトストレージ上の成果物の配置規約（フェーズ4以降）
- 認証・マルチユーザー（要件 10.1 の未決事項）

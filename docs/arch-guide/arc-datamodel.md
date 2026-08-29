# paper-repro フェーズ0データモデル物理仕様

`paper-repro` の永続化層を定める。**フェーズ0（データ永続化・状態遷移）の実装は本書を仕様とする。**

- 版: **v1.0（確定）**
- 前版: v0.1（草案）
- 作成日: 2026年8月25日
- 確定日: 2026年8月25日
- 文書構成更新日: 2026年8月29日
- 状態: **確定。フェーズ0（0-1・0-2）の実装は本書を仕様とする。**
- 外部設計の枠組み: [`arc-datamodel-framework.md`](arc-datamodel-framework.md) v0.1

> **v1.0 で確定したこと。** v0.1 が未決としていた3件を、いずれも本書の推奨どおりに決めた。
> 決定の内容と理由は第5章に残す。あわせて第2章の矛盾9件の解消方針を確定とした。

## 1. 本書の位置づけ

### 1.1 目的

要件定義とプロダクト設計に散在するデータ構造の記述を、**DDL に落とせる粒度で1か所に確定させる**。
型・NULL可否・既定値・外部キー・インデックス・ENUM の値までを決める。

本書はDDLへ落とす物理仕様に責務を限定する。REF-15／REF-16データモデル編が想定する
ER図、エンティティ一覧、エンティティ定義、CRUD図とレビュー基準は、
[`arc-datamodel-framework.md`](arc-datamodel-framework.md)以下の論理設計文書を正本とする。
これにより、外部設計の合意成果物と、フェーズ0で必要な型・NULL・制約を混在させない。

### 1.2 上位文書との関係

| 文書 | 関係 |
|---|---|
| [`../requirements.md`](../requirements.md) 6.1〜6.4 | 17エンティティのER図。本書はそのうちフェーズ0で作るものを DDL 化する |
| [`../product-design.md`](../product-design.md) 1.1〜1.4 | 状態機械とスキーマ差分。本書は状態の持ち方を確定する |
| [`arc-architecture.md`](arc-architecture.md) | 全体構造。本書は永続化層のみを扱う |
| [`arc-datamodel-framework.md`](arc-datamodel-framework.md) | 17エンティティ全体の論理設計と4工程成果物の枠組み |
| [`../roadmap.md`](../roadmap.md) | フェーズ0の作業項目。本書はその 0-1・0-2 の仕様 |

### 1.3 対象範囲

**フェーズ0では `projects` と `papers` の2テーブルのみを作る。**
残る15エンティティは、それを使う機能を実装するフェーズで追加する
（`assumptions` はフェーズ3、`sanity_runs` はフェーズ4、`score_compares` はフェーズ5など）。

先にテーブルだけ作っても、使われないまま定義が古びる。**使う直前に作る。**

---

## 2. 既存記述との矛盾と、その解消（確定）

要件定義・プロダクト設計・現行コード（`backend/app/`）を突き合わせた結果、**9件の食い違い**が見つかった。
本書は各件について解消方針を定める。**9件すべて、本章の方針で確定である。**
⚠️ が付く3件は利用者の判断を要したもので、第5章に決定を記録した。

| # | 論点 | 要件定義 / プロダクト設計 | 現行コード | 解消方針（確定） |
|---|---|---|---|---|
| 1 | ⚠️ 状態の持ち方 | `phase` × `status` の**2列**（設計 原則3） | `state` **1列**に混在 | 2列に分ける（3.3節） |
| 2 | ⚠️ 汎用遷移API | 定義なし。承認ゲートは**迂回不可能**（`REQ-C06`） | `POST /projects/{id}/state` で任意遷移が可能 | **廃止する**（5.2節で確定） |
| 3 | ⚠️ `course` 列 | `NOT NULL`・既定値なし（設計 1.4、`REQ-C01`） | 列が存在しない | **追加し、`POST /projects` を変更する**（5.1節で確定） |
| 4 | `approval_kind` 列 | 事象駆動ゲート④⑤⑥用（設計 1.3） | 列が存在しない | 追加する |
| 5 | 失敗からの復帰 | 「原因ログを提示し**同じ状態へ戻す**」（設計 1.1） | `FAILED` が phase を潰すため、どこへ戻るか判別不能 | #1 の2列化で解決 |
| 6 | `CREATED` での失敗 | どの状態でも失敗しうる | `FAILED → CREATED` の遷移が無く復帰不能 | #1 の2列化で解決 |
| 7 | `reading` の自己ループ | `course=reading` のとき反復（設計 1.2） | 定義なし | 3.4節の遷移表に含める |
| 8 | `policy` の型 | ENUM（ER図 6.1） | `Policy` Enum を定義しつつ列は `String` | ENUM 制約を列に適用 |
| 9 | 主キー名と欠落列 | `id` PK、`paper_type`・`created_at`・`updated_at` あり | `project_id`、3列とも欠落 | **`project_id` に統一**し、要件のER図を合わせる（5.3節で確定）。欠落列は追加 |

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

道具としての Alembic の説明は [`../tech-stack.md`](../tech-stack.md) を参照する。

理由は、公開前かつ利用者が1名で、**捨ててよいデータしか無い**ため。
スキーマを変えるときはテーブルを作り直す。この段階でマイグレーションを書く手間は、得る安全に見合わない。

**Alembic を導入する条件**を先に決めておく。次のいずれかを満たしたとき導入する。

1. 捨てられないデータが入ったとき（実際の論文プロジェクトを継続運用し始めたとき）
2. 利用者が2名以上になったとき
3. フェーズ6の一般公開に着手するとき

導入時に既存テーブルから初期リビジョンを起こす。**それまでは `create_all()` を使う。**

---

## 5. 決定の記録

v0.1 が未決としていた3件を、2026年8月25日に利用者が判断した。**いずれも v0.1 の推奨どおり。**

### 5.1 `course` は必須。`POST /projects` を変更する【確定：A案】

`course` を `NOT NULL`・既定値なしとし、**プロジェクト作成時に必ず受け取る**。

| 案 | 内容 | 採否 |
|---|---|---|
| **A** | `POST /projects` が `course` を必須で受け取る | **採用** |
| B | `course` を NULL 許容にし、選択後に `POST /course` で埋める | 却下 |
| C | 作成前にコース選択画面を置き、`course` 込みで1回だけ POST する | A と同義のため A に統合 |

**採用の理由。** 不正な状態が一瞬も存在せず、`REQ-C01`（開始時に選択する）に最も忠実である。
プロダクト設計 2章が既にコース選択画面をインテークの前に置いており、画面の流れと API の形が一致する。

**却下の理由（B）。** 未選択のプロジェクトが残りうる。`course` に既定値を置かない判断（3.1節）と
同じ理由で、「開始時に選択する」が骨抜きになる。

**この決定に伴う変更。**

| 対象 | 変更内容 |
|---|---|
| `POST /api/v1/projects` | リクエストに `course` を必須で追加する（**破壊的変更**） |
| `CreateProjectReq` | `arxiv_url` に加え `course: Course` を持つ |
| フロントエンドの作成画面 | コース選択を経てから作成 API を呼ぶ |
| `POST /api/v1/projects/{id}/course` | 作成後の**切替**専用として残す（設計 3.1） |

破壊的変更にあたるが、利用者は開発者本人のみであり、影響は小さい。

### 5.2 汎用の状態遷移エンドポイントは廃止する【確定：A案】

`POST /projects/{id}/state` を**削除する**。`phase` の遷移は、承認ゲートのエンドポイント経由のみとする。

| 案 | 内容 | 採否 |
|---|---|---|
| **A** | 廃止する。遷移は `policy` / `spec:finalize` / `sanity:gate` 経由のみ | **採用** |
| B | 開発用として残し、`app_env=development` のときだけ有効にする | 却下 |

**採用の理由。** 現行の汎用エンドポイントは `can_transition` で遷移の妥当性は見るが、
**承認ゲートを通さずに `reading → implementing` へ進める**。これは `REQ-C06` の
「迂回不可能な承認ゲート」に反する。経路を1つに絞れば、迂回が構造上できなくなる。

**却下の理由（B）。** 「開発では通るが本番では通らない経路」を作ると、テストが本番と違う道を通り、
テストの意味が薄れる。テストで状態を進めたい場合は、ゲートのエンドポイントを順に呼ぶか、
DB を直接組み立てればよい。

**この決定に伴う変更。**

| 対象 | 変更内容 |
|---|---|
| `POST /api/v1/projects/{id}/state` | **削除する** |
| `StateTransitionReq` | 削除する |
| `can_transition` | 残す。各ゲートのエンドポイントが内部で呼ぶ |
| 既存テスト | 汎用遷移を使っている箇所を、ゲート経由へ書き換える |

### 5.3 主キーの列名は `project_id` に統一する【確定】

要件定義の ER 図（6.1）が `id`、現行コードが `project_id` と割れていた。**`project_id` に統一する。**

**採用の理由。** 既にコードとテストが `project_id` で書かれており、変更すると
`papers.project_id` との対応も分かりにくくなる。**要件定義の ER 図側を `project_id` に合わせる。**

**この決定に伴う変更。**

| 対象 | 変更内容 |
|---|---|
| [`../requirements.md`](../requirements.md) 6.1 の ER 図 | `Project` の PK を `id` から `project_id` へ変更する |
| 現行コード | 変更なし |

---

## 6. 本書に含まれないもの

- `assumptions` `claims` `evidences` など、フェーズ1以降で使う15テーブルの定義（1.3節）
- Celery のジョブ状態の永続化（フェーズ2で扱う）
- オブジェクトストレージ上の成果物の配置規約（フェーズ4以降）
- 認証・マルチユーザー（要件 10.1 の未決事項）

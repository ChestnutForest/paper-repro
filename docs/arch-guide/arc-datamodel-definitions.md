# エンティティ定義

- 対象プロダクト: `paper-repro`
- 版: **v0.2**
- 作成日: 2026年8月29日
- 更新日: 2026年8月29日
- 枠組み: [`arc-datamodel-framework.md`](arc-datamodel-framework.md)
- 一覧: [`arc-datamodel-list.md`](arc-datamodel-list.md)

## 0. 記法

本書は論理属性を定義する。型、NULL、既定値、索引、DB制約を確定済みとして扱うのは、
[`arc-datamodel.md`](arc-datamodel.md) v1.0に物理仕様がある`Project`／`Paper`だけである。

| 状態 | 意味 |
| --- | --- |
| 確定 | 確定要求または既存物理仕様に明記されている |
| 候補 | エンティティを識別・関連付けるために必要だが、物理名・型は未決 |
| 未決 | USDM展開または利用フェーズ直前の物理設計で決める |

## 1. 中核

### DM-E01 Project

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| `project_id` | プロジェクト識別子 | 確定 | 物理仕様3.1 |
| `course` | `reading`／`reproduction` | 確定 | `REQ-C01` |
| `arxiv_url` | 初期リリースで指定する論文URL | 確定 | `REQ-C03` |
| `phase` | 工程上の現在地 | 確定 | 状態設計 |
| `status` | 工程内の実行状態 | 確定 | 状態設計 |
| `approval_kind` | 待機中の承認種別 | 確定 | `REQ-C06` |
| `paper_type` | A／B。判定前は不明 | 確定 | `REQ-C03` |
| `policy` | 方針5択 | 確定 | ゲート① |
| `title` | 論文タイトル | 確定 | 物理仕様3.1 |
| `course_changed_at` | 最後のコース切替日時 | 確定 | `REQ-C01-R3.20` |
| `created_at`／`updated_at` | 作成・更新日時 | 確定 | 物理仕様3.1 |

物理制約と実装差分は`arc-datamodel.md`第3章と`arc-behavior-state.md`第6章を参照する。

### DM-E02 Paper

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| `paper_id`／`project_id` | 論文識別子と所属プロジェクト | 確定 | 物理仕様3.2 |
| `source` | arXiv、PDF、DOI等の入手元 | 確定 | `REQ-C03-S01` |
| `identifier` | arXiv ID、DOI等 | 確定 | `REQ-C03-S01` |
| `version` | 対象版 | 確定 | `REQ-C03-S01` |
| `category` | 入手元が返す分類 | 確定 | `REQ-C03-S01` |
| `publication_status` | プレプリント、査読、採択等の履歴 | 確定 | `REQ-C03-S01` |
| `abstract`／本文参照 | 概要と保存した本文への参照 | 確定／未決 | 要求第6章 |
| `official_repo_url` | 候補となる公式実装 | 確定 | `REQ-C05-S01` |
| `fetched_at` | 取得日時 | 確定 | `REQ-C03-S01` |

取得できない値は空文字や推測値で埋めず、`DMR-02`に従う。
`Project`は取り込み前にも存在できるため、`Project`から見た`Paper`の多重度は0..1である。
`Paper.project_id`は必須かつ一意とし、`Paper`から見た`Project`の多重度は1とする。

### DM-E03 Spec

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 版付きspecと所属 | 候補 | `REQ-C08` |
| `body` | spec本文 | 確定 | 要求第6章 |
| 版・作成条件 | 生成・編集・承認した版を区別する | 確定 | `REQ-C08` |
| 状態・承認参照 | 草案／確定と承認を関連付ける | 未決 | `REQ-C06` USDM展開待ち |

### DM-E04 Assumption

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 仮定と所属 | 候補 | `REQ-C05` |
| `topic` | 仮定の対象 | 確定 | 要求第6章 |
| `paper_says` | 原論文に明記された内容 | 確定 | `REQ-C07` |
| `chosen`／`rationale` | 採用内容と理由 | 確定 | `REQ-C07` |
| `suspicion`／`status` | 疑わしさと確認状態 | 確定 | 要求第6章 |

### DM-E05 Delta

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 差分と所属 | 候補 | `REQ-C05-S01` |
| `body` | 差分内容 | 確定 | 要求第6章 |
| 対象版・分類・理由 | 一致、実装詳細、省略、版差等 | 確定 | `REQ-C05-S01` |
| 状態・承認参照 | 解決、保留、採用理由 | 未決 | `REQ-C05-S01` USDM展開待ち |

## 2. 批判的検証と由来

### DM-E06 Claim

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 主張と所属 | 候補 | `REQ-C10` |
| `kind` | 事実、結果、解釈、仮説、予測、宣伝的表現 | 確定 | `REQ-C10-S04` |
| `premises`／`consequences`／`scope` | 前提、帰結、成立範囲 | 確定 | `REQ-C10-S01` |
| `reading_depth` | 利用者が選ぶ読解深度 | 確定 | `REQ-C10-S01` |
| `direct_support_range` | 根拠が直接支持する範囲 | 確定 | `REQ-C10-S04` |
| 原文位置・分類主体 | 対象版の位置と分類者 | 確定 | `REQ-C10-S04` |

### DM-E07 Evidence

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`claim_id` | 証拠と対象主張 | 候補 | `REQ-C07` |
| `source_type`／版／著者性 | 情報源の属性 | 確定 | `REQ-C07`, `REQ-C07-S01` |
| `directness`／`agreement` | 直接性と一致・矛盾 | 確定 | `REQ-C07` |
| `confidence` | 確信度 | 確定 | `REQ-C07` |
| 人間承認・理由 | 採用判断と根拠 | 確定 | `REQ-C07` |
| 取得日時・対象版 | いつ何を確認したか | 確定 | `REQ-C07-S01` |

### DM-E08 ExperimentCond

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 実験条件と所属 | 候補 | `REQ-C10-S02` |
| data／preprocessing／model | データ、前処理、モデル | 確定 | `REQ-C10-S02` |
| hyperparams／seed／runs | 設定、乱数、試行回数 | 確定 | `REQ-C10-S02` |
| metric／error_bar | 評価指標と不確実性 | 確定 | `REQ-C10-S02` |
| compute／comparison | 計算資源と比較条件 | 確定 | `REQ-C10-S02` |
| `state` | 記載済み、未報告、推定、外部確認済み | 確定 | `REQ-C10-S02` |

### DM-E09 Provenance

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 由来関係と所属 | 候補 | `REQ-C08` |
| source／target参照 | 原文、分析、実装、成果物間の両端 | 確定／物理未決 | `REQ-C08` |
| 対象版・位置 | 版、コミット、ファイル、行、セル等 | 確定 | `REQ-C05-S01` |
| 変換条件 | モデル、プロンプト、処理、意図的変更 | 確定 | `REQ-C08` |
| 支持・反証・分類 | 両端の関係 | 確定 | `REQ-C08` |
| 訂正・レビュー履歴 | 人間の訂正と承認 | 確定 | `REQ-C08` |

## 3. 実行・照合・成果物

### DM-E10 SanityRun

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 実行と所属 | 候補 | `REQ-C05` |
| paper type／rung | 論文タイプとサニティ段階 | 確定 | 要求第6章 |
| status／log参照 | pass／failとログ | 確定 | 要求第6章 |
| 入力、資源制限、実行環境 | 再実行に必要な条件 | 確定／物理未決 | `REQ-C05`, `REQ-C06` |
| 開始・終了日時 | 実行時刻 | 候補 | 非同期処理の追跡 |

### DM-E11 ScoreCompare

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 照合と所属 | 候補 | `REQ-C05` |
| task／mine／paper／diff | 対象、再現値、論文値、差 | 確定 | 要求第6章 |
| verdict | ok／investigate | 確定 | 要求第6章 |
| 条件参照・人間注記 | 比較条件と最終判断 | 確定／物理未決 | `REQ-C10-S02`, `REQ-C10-S04` |

### DM-E12 Artifact

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 成果物と所属 | 候補 | `REQ-C05` |
| kind | code、notebook、report、zip等 | 確定 | `REQ-C05`, `REQ-C09-S01` |
| 版・保存参照・ハッシュ | 同一性と実体の所在 | 確定／物理未決 | `REQ-C08` |
| 生成条件・由来参照 | 何からどう作ったか | 確定 | `REQ-C08` |
| 公開範囲・権利情報 | 非公開、限定共有、公開と条件 | 確定 | `REQ-C09-S03` |

### DM-E13 Approval

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 承認履歴と所属 | 候補 | `REQ-C06` |
| gate／対象参照 | 承認の種類と対象 | 確定 | `REQ-C06` |
| 選択・理由・承認者・時刻 | 人間の最終判断 | 確定 | `REQ-C01`, `REQ-C07` |
| before／after | コース切替等の前後値 | 確定 | `REQ-C01-R3.30` |

### DM-E14 CostRecord

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | コスト記録と所属 | 候補 | `REQ-C05` |
| phase／job参照 | どの工程・実行か | 確定／物理未決 | 要求第6章 |
| 資源種別・量・単位 | CPU時間、API利用量等 | 未決 | 実装フェーズで確定 |
| 期間・時刻・タイムゾーン | 計測範囲 | 候補 | `BR-04` |

## 4. 学習と質問

### DM-E15 SelfExplanation

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 自己説明と所属 | 候補 | `REQ-C04-S02` |
| text／anchor | 説明本文と原文・概念の根拠 | 確定 | `REQ-C04-S02` |
| state | 理解済み、部分理解、未理解、要再確認 | 確定 | `REQ-C04-S02` |
| visibility | 公開範囲 | 確定 | `REQ-C09-S03` |
| フィードバック・訂正履歴 | 根拠付き応答と利用者訂正 | 確定／物理未決 | `REQ-C04-S02` |

### DM-E16 DeepDiveQueue

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 候補と所属 | 候補 | `REQ-C09-S02` |
| 対象参照・関係・推薦信号 | 候補化の材料 | 確定 | `REQ-C09-S02` |
| priority／理由 | 利用者が決める順序と理由 | 確定 | `REQ-C09-S02` |
| state | 候補、優先、深掘り中、読解済み、保留等 | 確定 | `REQ-C09-S02` |
| 取得・検査可能性 | 公開、取得、検査の状態 | 確定 | `REQ-C09-S02` |

### DM-E17 Question

| 論理属性 | 意味 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 識別子／`project_id` | 質問と所属 | 候補 | `REQ-C11` |
| body | 疑問本文 | 確定 | `REQ-C11` |
| answers／respondent | 回答履歴と回答主体 | 確定／物理未決 | `REQ-C11` |
| source／medium／datetime | 情報源、媒体、日時 | 確定 | `REQ-C11` |
| original／summary | 原文と要約の区別 | 確定 | `REQ-C11` |
| visibility／history | 公開範囲と送信・訂正履歴 | 確定 | `REQ-C11`, `REQ-C09-S03` |
| state | 未解決、解決、保留等 | 未決 | `REQ-C11` USDM展開待ち |

## 5. 物理設計へ渡す未決事項

- 将来15エンティティの主キー型、テーブル名、FK、NULL、索引
- 版管理を同一表の複数行で行うか、版エンティティへ分けるか
- `Provenance`のsource／target参照をRDBでどう制約するか
- 本文、ログ、コード、Notebook、zipをDBとオブジェクトストレージのどちらへ置くか
- 履歴を追記専用にする範囲と訂正の表現
- 保存期間、最大件数、増加率、容量見積の根拠
- 認証導入後の所有者、共有主体、アクセス制御モデル

これらは要件がない状態で確定せず、該当フェーズのUSDM仕様と実測値を入力にする。

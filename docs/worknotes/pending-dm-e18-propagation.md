# 未整備の追随：`DM-E18 LearningProfile` の依存関係

- 対象プロダクト: `paper-repro`
- 文書種別: 未整備事項の記録
- 作成日: 2026年9月2日
- 発見の契機: [`batch-06-options.md`](../requirements-decisions/batch-06-options.md) 選択肢3の採用により
  `DM-E18` を新設し、他成果物への追随を検討したとき
- 状態: **未着手。次の作業単位で対応する**
- 影響先: [`../arch-guide/arc-datamodel-er.md`](../arch-guide/arc-datamodel-er.md)、
  [`../arch-guide/arc-datamodel-crud.md`](../arch-guide/arc-datamodel-crud.md)、
  [`../arch-guide/arc-datamodel-definitions.md`](../arch-guide/arc-datamodel-definitions.md)、
  [`../arch-guide/arc-behavior-list.md`](../arch-guide/arc-behavior-list.md)

---

## 0. 何が未整備か

`DM-E18 LearningProfile` は [`../arch-guide/arc-datamodel-list.md`](../arch-guide/arc-datamodel-list.md) v0.3 に
追加したが、**他の成果物には反映していない。**

⚠️ **追随は件数の書き換えではなく、設計判断を含む。** 本書はその判断すべき点を記録する。

---

## 1. 構造上の位置：ER図のどこにも収まらない

[`../arch-guide/arc-datamodel-er.md`](../arch-guide/arc-datamodel-er.md) は4枚のER図で構成される。

| 図 | 名称 | 起点 |
|---|---|---|
| `DM-ER-01` | 中核 | `PROJECT` |
| `DM-ER-02` | 批判的検証と由来 | `PROJECT` |
| `DM-ER-03` | 実行・照合・成果物 | `PROJECT` |
| `DM-ER-04` | 学習と質問 | `PROJECT` |

**4枚すべてが `PROJECT` を起点とし、17エンティティは例外なくそこから線が伸びる。**

`DM-E18` にはその線が無い。意味的には `DM-ER-04`（学習と質問）が近いが、
あの図は `PROJECT ||--o{ SELF_EXPLANATION` のような関係で構成されており、
**プロジェクトを持たないエンティティを置くと図の一貫性が崩れる。**

### 1.1 選択肢

| 案 | 内容 | 注意点 |
|---|---|---|
| A | **5枚目のER図を作る**（`DM-ER-05` 利用者） | エンティティ1件のために図を1枚増やす |
| B | **`DM-ER-04` に独立した島として描く** | 図の中に起点が2つできる。読み手が関係の有無を誤解しうる |
| C | **`USER` を新設し、`USER ||--o| LEARNING_PROFILE` と `USER ||--o{ PROJECT` を描く** | **19エンティティ目を生む。** 認証・アカウント管理は要求に無く、単一利用者を前提としている以上、根拠が薄い |

⚠️ **C は採りにくい。** 要求に無いエンティティを図の都合で足すことになる。

---

## 2. 下流の依存：Scope 段階が参照する

要件 v0.3.1 第1.1節が「Scope の結果は `REQ-C02-S01` により横断で保持する」と定めた。

実装単位は `F-16`（前提知識の説明画面）、`B-04`（LLMオーケストレータ）、`B-09`（台帳・PJ 永続化）。

⚠️ **依存の向きが他と逆になる。** 通常の工程はプロジェクトの中で完結するが、
Scope は「この論文に何が足りないか」を評価したあと、`DM-E18` を読んで既習分を差し引く。
**プロジェクトの外を参照する初めての工程である。**

---

## 3. ⚠️ 最も注意が要る点：`Paper` との重複

**「既読論文」は2種類の実体を指しうる。**

| 種別 | 状態 | 例 |
|---|---|---|
| **内部の履歴** | `Paper` と `Project` が既に存在する | 過去に paper-repro で読んだ論文 |
| **外部の申告** | 識別子しかない | 他所で読んだ論文、受講した講座 |

**同じ論文が両方に現れる可能性がある。** この区別を設計しないと、同じ論文が二重に記録される。

[`../requirements-analysis/simclr-handson-deck.md`](../requirements-analysis/simclr-handson-deck.md) の
`PR-S-14-2` が「前提知識ごとに、**内部の過去成果物（過去の再現実装）と外部教材の両方**をリンクする」と
定めていたのは、この区別のことだと読める。

### 3.1 決めるべきこと

- `DM-E18` の既読論文が `Paper` を参照するのか、識別子だけを持つのか
- 内部の履歴と外部の申告を、同じ項目で扱うのか分けるのか
- 同一論文が両方に現れたときの扱い

---

## 4. 振舞い編への波及

CRUD図は6つの業務グループで構成される。`DM-E18` への操作は主に2箇所で発生する。

| グループ | 操作 | 内容 |
|---|---|---|
| 04 読解・学習・仕様化 | R | Scope 段階が既習分を参照する |
| 01 プロジェクトとポートフォリオ | C・U | 利用者が既読資料を登録する |

⚠️ **現在の47業務に「既読資料を登録する」業務が無い。**
[`../arch-guide/arc-behavior-list.md`](../arch-guide/arc-behavior-list.md) への追加が要る可能性がある。

**データモデル編だけでなく、システム振舞い編にも追随が要る。**

---

## 5. 追随が必要な文書

| 文書 | 内容 | 判断を要するか |
|---|---|---|
| [`../arch-guide/arc-datamodel-er.md`](../arch-guide/arc-datamodel-er.md) | `DM-E18` の描画 | ✅ **1.1節の案A〜Cから選ぶ** |
| [`../arch-guide/arc-datamodel-definitions.md`](../arch-guide/arc-datamodel-definitions.md) | 論理属性の定義 | ✅ **3.1節を決めてから** |
| [`../arch-guide/arc-datamodel-crud.md`](../arch-guide/arc-datamodel-crud.md) | 47業務との対応 | ✅ **4節の業務追加の要否を決めてから** |
| [`../arch-guide/arc-behavior-list.md`](../arch-guide/arc-behavior-list.md) | 既読資料の登録業務 | ✅ 追加の要否 |
| 各文書の「17エンティティ」の記述 | 18へ更新 | — 機械的 |

### 5.1 「17エンティティ」の記述がある文書

⚠️ **すべてを直すのではない。** 当時の記録（devlog、選択記録、凍結済みの worknotes）は残す。

直すのは、現在の設計を説明している次の文書である。

- `arc-datamodel-framework.md`（4箇所）
- `arc-datamodel-er.md`（1箇所）
- `arc-datamodel-crud.md`（2箇所）
- `arc-datamodel-rules.md`（2箇所）
- `arc-datamodel.md`（2箇所）
- `arc-architecture.md`・`arc-artifact-order.md`・`arc-interface.md`
- `docs/README.md`・`arch-guide/README.md`・ルート `README.md`
- `requirements.md` 428行・`traceability-matrix.md`

⚠️ **定義が17件しかない状態で件数だけ18へ書き換えない。**
ER図・CRUD図・論理属性定義を先に整えること。

---

## 6. 次に行うこと

1. 1.1節の案A〜Cから選び、ER図へ `DM-E18` を描く。
2. 3.1節を決め、論理属性を定義する。
3. 4節の業務追加の要否を決め、CRUD図を更新する。
4. 1〜3が済んでから、5.1節の「17エンティティ」を18へ更新する。
5. `arc-datamodel-list.md` 1.1節の「本書以外の成果物への反映は未了である」という注記を外す。

⚠️ **1〜3は設計判断を含む。** 機械的な置換で済むのは4だけである。

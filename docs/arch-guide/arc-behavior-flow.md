# システム化業務フロー

- 対象プロダクト: `paper-repro`
- 版: **v0.1**
- 作成日: 2026年8月29日
- 準拠: REF-15／REF-16 システム振舞い編
- 一覧: [`arc-behavior-list.md`](arc-behavior-list.md) v0.2
- 共通ルール: [`arc-behavior-rules.md`](arc-behavior-rules.md)

## 0. 図の読み方と範囲

各図は「利用者」「Paper-repro」「外部サービス」のレーンを持つ。`B-xx-xxx`を付けた節点が
開発対象のシステム化業務であり、外部サービス内部の処理は対象外である。承認ゲートは必ず
利用者レーンに置く。実線は処理、点線はデータまたは通知、破線枠相当の注記は将来機能を表す。

| 記号 | 意味 |
| --- | --- |
| 角丸節点 | 開始・終了 |
| 長方形 | 業務または機能 |
| ひし形 | 分岐・人の判断 |
| `[(...)]` | 保存データ |

## BF-01 プロジェクトとポートフォリオ

```mermaid
flowchart LR
    subgraph U[利用者]
        U0([開始]) --> U1[B-01-002 再開]
        U0 --> U2[B-01-003 検索・絞り込み]
        U0 --> U3[B-01-004 バックアップ・復元・移行]
        U0 --> U4[B-01-005 確認付き削除]
    end
    subgraph S[Paper-repro]
        S1[B-01-001 一覧取得] --> DB[(プロジェクト・成果物)]
        S2[B-01-006 ポートフォリオ更新] --> DB
    end
    U0 --> S1
    S1 -.一覧.-> U1
    U1 --> DB
    U2 --> S1
    U3 --> DB
    U4 --> DB
```

## BF-02 コース選択と切替

```mermaid
flowchart LR
    subgraph U[利用者]
        U0([新規作成]) --> U1[B-02-001 コース選択・作成]
        U2[B-02-003 コース切替]
    end
    subgraph S[Paper-repro]
        V{入力は妥当か}
        E[B-02-002 拒否理由を返す]
        H[B-02-004 切替履歴を保存]
        G[B-02-005 ゲート②の遷移先を決定]
        O[B-02-006 読解成果を出力可能にする]
        DB[(course・履歴・成果物)]
    end
    U1 --> V
    V -- いいえ --> E --> U1
    V -- はい --> DB
    U2 --> H --> DB
    DB --> G
    G -- reproduction --> I([実装工程])
    G -- reading --> R([読解継続])
    R --> O
```

## BF-03 取り込みと方針決定

```mermaid
flowchart LR
    subgraph U[利用者]
        U0([created]) --> U1[B-03-001 入手元を指定]
        U2[B-03-006 取り込み結果を確認] --> D{方針}
        D -- 続行 --> U3[B-03-007 方針を承認]
        D -- 見送り --> U4[B-03-008 見送り]
    end
    subgraph S[Paper-repro]
        S1[B-03-002 論文・メタデータ取得]
        S2[B-03-003 版・公開状態・履歴保存]
        S3[B-03-004 公式実装・参考情報探索]
        S4[B-03-005 タイプ・検査可能性判定]
        DB[(論文・証拠・取得履歴)]
    end
    subgraph X[外部サービス・対象外]
        X1[arXiv・出版社]
        X2[GitHub・OpenReview等]
    end
    U1 --> S1
    S1 --> X1
    S1 --> S2 --> DB
    S2 --> S3 --> X2
    S3 --> S4 -.結果.-> U2
    U3 --> R([reading])
    U4 --> K([skipped])
```

## BF-04 読解・学習・仕様化

```mermaid
flowchart LR
    subgraph U[利用者]
        U1[B-04-001 原論文・注釈]
        U5[B-04-005 自己説明]
        U7[B-04-007 spec編集]
        U8[B-04-008 論文・実装対応付け]
        U9[B-04-009 主張・証拠・条件の構造化]
        U10[B-04-010 深掘りキュー]
        U11[B-04-011 質問・外部回答]
        U12[B-04-012 解決・保留]
        U13[B-04-013 spec承認]
    end
    subgraph S[Paper-repro]
        S2[B-04-002 前提説明]
        S3[B-04-003 課題提示]
        S4[B-04-004 再計算・フィードバック]
        S6[B-04-006 spec草案生成]
        DB[(原文・spec・台帳・質問)]
        P{解決待ちがあるか}
    end
    U1 --> S2 --> S3 --> S4 --> U5 --> S6 --> U7
    U7 --> U8 --> U9 --> P
    U9 --> U10 --> U11 --> DB
    P -- ある --> U12 --> DB --> U7
    P -- ない --> U13
    U13 -- reading --> U1
    U13 -- reproduction --> I([実装工程])
```

## BF-05 再現実装・検証・照合

```mermaid
flowchart LR
    subgraph U[利用者]
        U2[B-05-002 実行計画・制限確認]
        U6[B-05-006 例・反例・境界条件を記録]
        U7[B-05-007 サニティ通過を承認]
    end
    subgraph S[Paper-repro]
        S1[B-05-001 実装・Notebook草案生成]
        S3[B-05-003 サンドボックス実行]
        S4[B-05-004 進捗・失敗通知]
        S5[B-05-005 サニティ段階実行]
        S8[B-05-008 論文値・再現値照合]
        OK{サニティ合格か}
    end
    subgraph X[隔離実行環境]
        X1[使い捨てコンテナ]
    end
    S1 --> U2 --> S3 --> X1
    X1 -.進捗・ログ.-> S4
    X1 --> S5 --> OK
    OK -- いいえ --> U6 --> S1
    OK -- はい --> U7 --> S8 --> R([レポート工程])
```

## BF-06 レポート・成果物・共有

```mermaid
flowchart LR
    subgraph U[利用者]
        U2[B-06-002 差異・最終判断を注記]
        U5[B-06-005 公開範囲・送信内容を確認]
        U6[B-06-006 明示操作で共有・公開]
    end
    subgraph S[Paper-repro]
        S1[B-06-001 結果・根拠表示]
        S3[B-06-003 成果物パッケージ化]
        S4[B-06-004 完了記録]
        DB[(成果物・承認・共有履歴)]
    end
    subgraph X[外部サービス・対象外]
        X1[共有先・公開先]
    end
    S1 --> U2 --> S3 --> DB --> S4 --> D([done])
    D --> U5
    U5 -- 中止 --> D
    U5 -- 承認 --> U6 --> X1
    U6 --> DB
```

## 7. 異常系の共通フロー

```mermaid
flowchart LR
    A[非同期機能を開始] --> B{成功したか}
    B -- はい --> C[成果物と履歴を保存]
    B -- いいえ --> D[status=failed]
    D --> E[失敗工程・理由・ログを保持]
    E --> F{利用者が再実行するか}
    F -- はい --> G[status=idleへ復帰] --> A
    F -- いいえ --> H[未解決として保持]
```

失敗しても`phase`を失わない。自動的に次工程へ進めず、承認ゲートと
[`arc-behavior-state.md`](arc-behavior-state.md)の遷移条件を再適用する。

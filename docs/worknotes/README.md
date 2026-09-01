# 作業メモ（worknotes）

要求分析と設計工程の作業で使った指示書・変更記録・検討資料を保存する場所。
**分析結果そのものは [`../requirements-analysis/`](../requirements-analysis/) が正本**であり、
本フォルダは「どう反映したか」「なぜその方法を選んだか」「何を保留したか」を扱う。

## 一覧

| ファイル | 内容 | 対応する分析 |
| --- | --- | --- |
| [`reflection-1.2.2.5.md`](reflection-1.2.2.5.md) | 「1.2.2.5」初版の判定結果と反映箇所、作業上の教訓 | `section-1.2.2.5-output-for-understanding.md` |
| [`workflow-patch-v0.19.md`](workflow-patch-v0.19.md) | ワークフロー文書 v0.18→v0.19 の変更4箇所と適用方法の記録 | 同上 |
| [`reflection-1.2.2.5-v2.md`](reflection-1.2.2.5-v2.md) | 脚注31・32を反映した更新内容と、脚注31の設計上の含意 | 同上 |
| [`reflection-1.2.3.md`](reflection-1.2.3.md) | 「1.2.3」導入部の暫定分析に伴う反映指示（案A／案Bの判断含む） | `section-1.2.3-external-help.md` |
| [`reflection-1.2.3.1.md`](reflection-1.2.3.1.md) | 「1.2.3.1」の判定（新規要求なし）と`REQ-C07-S02`保留の記録 | `section-1.2.3.1-small-group-discussion.md` |
| [`reflection-1.2.3.2.md`](reflection-1.2.3.2.md) | 「1.2.3.2」の判定、`REQ-C07-S02`確定と`REQ-C09-S05`候補化 | `section-1.2.3.2-contacting-authors.md` |
| [`reflection-1.2.3.3.md`](reflection-1.2.3.3.md) | 「1.2.3.3」の判定と`REQ-C07-S03`を分けた理由 | `section-1.2.3.3-web-discussion.md` |
| [`reflection-1.2.3.4.md`](reflection-1.2.3.4.md) | 「1.2.3.4」の判定と既存文書への追記記録 | `section-1.2.3.4-using-generative-ai.md` |
| [`pending-req-c09-s04.md`](pending-req-c09-s04.md) | 未確定の要求候補`REQ-C09-S04`の状態管理と判断保留の経緯 | `section-1.2.3-external-help.md` ほか |
| [`pre-approval-screening.md`](pre-approval-screening.md) | 変更案v0.12の承認前に、新規32件と選択済み11件の矛盾だけを確認した記録 | `simclr-handson-deck.md`、`academic-research-skills.md`、`academic-research-skills-frameworks.md` |
| [`id-unification-and-phase-provisional.md`](id-unification-and-phase-provisional.md) | ID体系を`REQ-Cxx`へ一本化し、Phase 0〜6を暫定と明記した決定記録（v0.2骨組み更新） | `requirements.md` v0.2-draft |
| [`readme-progress-table.md`](readme-progress-table.md) | ルートREADMEへ設計工程の進捗表を追加した提案と反映の記録（凍結） | — |
| [`reflection-arc-screen-v02.md`](reflection-arc-screen-v02.md) | `arc-screen.md` v0.1→v0.2 の原文突合せの検証記録（凍結） | `arc-screen.md` |
| [`reflection-arc-behavior-v02.md`](reflection-arc-behavior-v02.md) | `arc-behavior.md` v0.1→v0.2 の原文突合せの検証記録（凍結） | `arc-behavior.md` |
| [`reflection-arc-interface.md`](reflection-arc-interface.md) | 外部インタフェース編の枠組み作成の記録。4成果物、共通ルール不在の扱い（凍結） | `arc-interface.md` |
| [`reflection-arc-interface-list.md`](reflection-arc-interface-list.md) | 外部IF一覧・関連図の作成記録（凍結） | `arc-interface-list.md`、`arc-interface-map.md` |
| [`decision-arxiv-acknowledgement.md`](decision-arxiv-acknowledgement.md) | 設計判断の記録。arXiv 謝辞の文言と表示箇所 | — |
| [`decision-github-auth.md`](decision-github-auth.md) | 設計判断の記録。GitHub API の認証を必須とする | — |
| [`decision-pwc-replacement.md`](decision-pwc-replacement.md) | 設計判断の記録。Papers with Code 終了への対応 | — |
| [`br13-draft.md`](br13-draft.md) | 共通ルールの追記案。`BR-13` 外部API呼び出しの規則 | — |
| [`pending-br13-external-api.md`](pending-br13-external-api.md) | 未整備事項の記録。外部API呼び出しの共通ルール`BR-13` | — |
| [`pending-sota-comparison.md`](pending-sota-comparison.md) | 将来の変更要求の候補。第三者の再現結果との比較 | — |

## 保存する理由

- 反映作業でどのファイルのどこを変えたかを、後から追跡できるようにする。
- 同じ失敗を繰り返さないための教訓を残す（長文ファイルの全文差し替えを避ける、
  日本語を含むPowerShellスクリプトを避ける、など）。
- 暫定版として保留した判断（例：「1.2.3」の案A／案B）の経緯を残す。
- **未確定のまま残っている要求候補と、判断を保留した理由を記録する。**
  判断の先送りを記録しないと、後から見た人が検討漏れと誤解するため。

## 運用

### 文書の2種類

本フォルダには性格の異なる2種類がある。混ぜると、永久に「反映待ち」のまま残る文書が生まれる。

**反映メモ** — 設計や要件へ反映すべき差分を持つ。状態行を持ち、反映の完了まで追う。
**記録** — 設計判断の記録、検証記録、作成記録、未整備事項の記録、将来の変更要求の候補など。
なぜそう判断したかの経緯であり、反映すべき差分を持たない。各文書の冒頭に「文書種別」として明記する。
状態行を置く場合は「記録・凍結（日付）」とし、以後更新しない。

### 状態行の規則

- 分析1件につき、反映メモ1件を目安とする。
- 反映が完了したら、**反映と同じコミットで**「状態: 反映完了（コミットSHA）」へ更新する。
  別コミットにすると更新を忘れる。
- 状態の語は次から選ぶ。反映待ち／反映完了／判断保留／未着手／記録・凍結／開発しない。
- 文書を追加・改名したら、上の一覧表も同じコミットで更新する。
- 分析文書を更新した場合は、`-v2` のように版を分けて追加する（上書きしない）。
- 未確定の要求候補が生じた場合は、`pending-<要求ID>.md` として状態管理の記録を作る。

# 作業メモ（worknotes）

要求分析の反映作業で使った指示書・変更記録・検討資料を保存する場所。
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
| [`pending-req-c09-s04.md`](pending-req-c09-s04.md) | 未確定の要求候補`REQ-C09-S04`の状態管理と判断保留の経緯 | `section-1.2.3-external-help.md` ほか |

## 保存する理由

- 反映作業でどのファイルのどこを変えたかを、後から追跡できるようにする。
- 同じ失敗を繰り返さないための教訓を残す（長文ファイルの全文差し替えを避ける、
  日本語を含むPowerShellスクリプトを避ける、など）。
- 暫定版として保留した判断（例：「1.2.3」の案A／案B）の経緯を残す。
- **未確定のまま残っている要求候補と、判断を保留した理由を記録する。**
  判断の先送りを記録しないと、後から見た人が検討漏れと誤解するため。

## 運用

- 分析1件につき、反映メモ1件を目安とする。
- 反映が完了したら、メモの冒頭に「状態: 反映完了（コミットSHA）」を記録する。
- 分析文書を更新した場合は、`-v2` のように版を分けて追加する（上書きしない）。
- 未確定の要求候補が生じた場合は、`pending-<要求ID>.md` として状態管理の記録を作る。

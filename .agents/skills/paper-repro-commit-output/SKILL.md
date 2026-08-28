---
name: paper-repro-commit-output
description: paper-reproリポジトリで、変更ファイルのcommit/pushコマンドを求められたとき、実際のcommit/pushを依頼されたとき、push結果のGitHub URLを求められたとき、またはGit実行結果の検証を求められたときに使う。明示したファイルだけをステージし、Conventional Commits、検証、ローカルとリモートのSHA照合、リポジトリ・コミット・ブランチ・全コミット対象ファイル・履歴のコピー可能なURL出力を行う。コマンド提示だけの依頼ではcommit/pushを実行しない。paper-repro以外には使わない。
---

# paper-repro commit/push・結果URL

## 正本と対応環境

この`SKILL.md`がスキル本文の唯一の正本である。

| 環境 | 読み込み方法 |
|---|---|
| Codex | `.agents/skills/paper-repro-commit-output/`を直接読む |
| Antigravity IDE | `.agents/skills/paper-repro-commit-output/`を直接読む |
| Claude Code | `.claude/skills/paper-repro-commit-output/`の入口から本ファイルを全文読む |

対象は`https://github.com/ChestnutForest/paper-repro`だけである。ローカルの既定位置は
`C:\Users\kazuy\projects\paper-repro`だが、実行時は`git rev-parse --show-toplevel`と
`git remote get-url origin`で実体を確認する。

## 変更履歴

| 版 | 日付 | 変更内容 |
|---|---|---|
| 2.0.0 | 2026-08-28 | 個人用URL出力規約とリポジトリ内の重複手順を統合。3環境共通の正本、権限境界、全ファイルURL、SHA照合を明文化し、環境固有のzip・提示ツール依存を廃止 |
| 1.1 | 2026-08-23 | commit URLと実行結果検証を追加 |
| 1.0 | 2026-08-23 | 初版 |

## 最初に依頼を分類する

| 依頼 | 動作 |
|---|---|
| 「commit/pushするコマンドを出して」 | 読み取り確認だけ行い、コマンドと到達可能なURLを出す。commit/pushは実行しない |
| 「commit/pushして」 | 検証後に実行し、リモートSHA一致まで確認して完全な結果URLを出す |
| 「push後のURLを出して」 | 実在するリモート状態を確認してURLを出す。未pushならその事実を報告する |
| 実行結果を貼って「検証して」 | 期待値、実出力、飛ばされた手順、残作業を照合する |

ユーザーの明示的な依頼なしにcommit、push、pull、履歴改変を行わない。

## 実行順序

具体的なPowerShellコマンドと検証マトリクスは、必要になった時点で
[`references/commit-workflow.md`](references/commit-workflow.md)を全文読む。

1. リポジトリルート、ブランチ、origin、作業ツリーを確認する。
2. 変更ファイルを実測し、ユーザーの既存変更と今回の変更を分離する。
3. 文書索引・進捗表を同期すべきか判断する。
4. 変更種別に応じて検証し、`git diff --check`を通す。
5. 対象パスを列挙してステージする。`git add .`は使わない。
6. 英語のConventional Commitを作る。件名は50字程度、本文は2〜3文かつ50語以内とし、差分で分からない理由を書く。
7. 依頼が実行まで含む場合だけpushする。
8. `HEAD`と`origin/<branch>`の完全SHAを照合する。
9. GitHub URLを生成し、存在する値だけを出す。

## 文書同期の判断

- フェーズ状態が変わる場合は`docs/roadmap.md`を先に直し、同じコミットでルート`README.md`の進捗表を合わせる。
- 新規・改名した現行文書は`docs/README.md`へ追加し、ルートREADMEの関連箇所も確認する。
- 既存文書の版更新、作業メモ、分析文書、スキル、devlogだけの変更では、進捗表のマス目を変えない。
- 判断基準は「今回の変更で進捗表のマス目が実際に変わるか」である。

## 成果物の示し方

共有ローカルワークスペース内のファイルは、その場で編集し、絶対パスのファイルリンクで示す。
特定のチャット環境だけが持つ成果物提示ツールや一時出力ディレクトリ、zipの展開・再配置を前提にしない。
ダウンロード用zipはユーザーが明示的に求めた場合だけ作る。

## コマンド出力

- Windows PowerShell 5.1でそのまま実行できる形にする。
- 番号付きの工程ごとに、関連コマンドを1つの`powershell`ブロックへまとめる。
- 各ブロックの直前に目的と期待値を書く。
- 変更ファイルは実測したパスを明示し、プレースホルダーのまま渡さない。
- 日本語本文を生成するPowerShellヒアストリングは避ける。BOMなしUTF-8とLFを維持する。

## GitHub URL出力

実際にpushした後は、次の順で省略せず出す。

1. リポジトリ
2. 実在する完全SHAのコミット
3. pushしたブランチ
4. そのコミットに含まれる全ファイルのコミット固定URL
5. コミット履歴

URLは1件ずつ独立した`text`コードブロックに入れ、直前に内容を示す見出しを付ける。
ファイル数が多くても省略しない。空のSHA、プレースホルダー、架空値を出さない。

コマンドだけを提示する段階では、リポジトリ、ブランチ、対象ファイルの`blob/main` URL、履歴URLは出してよい。
コミット固有URLはまだ生成せず、実行コマンド内でpush後の完全SHAとURLを表示させる。

## 実行結果の検証

利用者がPowerShellやVS Codeの結果を貼った場合は、次を短い表で照合する。

- 各コマンドの期待値と実出力
- 飛ばされた工程と後続への影響
- 変更件数やMermaid数などの実測内訳
- 文書だけの変更が`backend/`や`frontend/`へ波及していないこと
- commit、push、ローカルSHA、リモートSHAの一致

不一致を利用者の操作ミスと決めつけない。先に自分の期待値と数え方を再検証する。

## 禁止事項

- `git add .`で無関係な変更を巻き込む
- dirtyな作業ツリーへ自動的に`git pull`する
- `git checkout --`、`git reset --hard`、stashで既存変更を隠す・破棄する
- push前にコミットURLを捏造する
- 実際にpushしたのに変更ファイルURLを一部だけ省く
- 他プロジェクトへこのスキルを適用する
- 同じ本文を`.claude/skills`や`docs/skills`へ複製する

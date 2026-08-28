# paper-repro commit/pushワークフロー

`paper-repro-commit-output`を適用するときだけ読む詳細手順である。
コマンド提示だけの依頼では、下記の読み取り確認は行ってよいが、`git add`以降は実行しない。

## 1. 事前確認

```powershell
Set-Location 'C:\Users\kazuy\projects\paper-repro'
git rev-parse --show-toplevel
git remote get-url origin
git status --short --branch
git diff --stat
git diff --name-status
```

期待値:

- ルートが`C:/Users/kazuy/projects/paper-repro`
- originが`https://github.com/ChestnutForest/paper-repro.git`
- ブランチと変更ファイルが依頼範囲に一致

一覧に依頼と無関係な変更があれば、対象から外す。重なるファイルは勝手に上書きせず、差分を確認する。

## 2. 変更内容の確認

```powershell
git diff -- AGENTS.md CLAUDE.md README.md docs/README.md
git diff -- .agents/skills .claude/skills docs/skills scripts/validate-agent-skills.ps1
git diff --check
```

`git diff --check`は出力がないことを期待する。長文ファイルの差分が意図より大きい場合は、
改行・文字コード・表の再整形による置換を疑い、内容を実測してから進む。

## 3. 変更種別ごとの検証

| 変更 | 必須確認 | 期待値 |
|---|---|---|
| スキル | `scripts/validate-agent-skills.ps1`とskill validator | すべて成功 |
| 文書のみ | `git diff --name-only`でコード領域を検索 | `backend/`、`frontend/`が出ない |
| Python | 対象テスト、ruff、black確認 | 全成功 |
| フロントエンド | `npm --prefix frontend run build`と関連テスト | 全成功 |
| Mermaid | リポジトリ既定のMermaid検証 | 構文エラーなし |
| 新規文書 | `docs/README.md`と関連索引 | 掲載漏れなし |

`black --check`は修正しない。整形が必要なら、明示的な整形コマンドを先に実行する。

## 4. ステージ前の文書同期

次の順で判断する。

1. フェーズ状態が変わったか。変わった場合は`docs/roadmap.md`を正本として更新する。
2. ルート`README.md`の進捗表のマス目が実際に変わるか。変わる場合だけ同じコミットで更新する。
3. 現行文書を追加・改名したか。該当する場合は`docs/README.md`とルートREADMEの関連箇所を確認する。
4. スキル、devlog、分析、作業メモだけの変更なら進捗表は変更しない。

更新した場合は、表全体を再生成せず、該当するマス目と要約値だけを変更する。

## 5. ステージとコミット

実測したファイルを1つずつ列挙する。次は形式例であり、実際の変更一覧へ置き換える。

```powershell
git add -- 'AGENTS.md' 'CLAUDE.md' 'README.md' 'docs/README.md'
git add -- '.agents/skills/paper-repro-commit-output/SKILL.md'
git status --short
git diff --cached --check
git diff --cached --stat
git commit -m 'docs(skills): unify agent skills' -m 'A repository-owned source prevents client-specific copies from drifting. Shared discovery paths keep the workflow portable across supported agents.'
```

コミットメッセージの規則:

- 英語のConventional Commits
- 件名は命令形で50字程度
- 本文は2〜3文、合計50語以内、1文20語程度
- ファイル名や差分の要約ではなく、変更理由を書く

## 6. pushとSHA照合

実行依頼がある場合だけ行う。

```powershell
$branch = git branch --show-current
git push origin $branch
$localSha = git rev-parse HEAD
$remoteLine = git ls-remote --heads origin "refs/heads/$branch"
$remoteSha = ($remoteLine -split "`t")[0]
"local=$localSha"
"remote=$remoteSha"
if ($localSha -ne $remoteSha) { throw 'Local and remote SHA do not match.' }
```

`git log --oneline`の省略SHA同士だけで判断しない。完全SHAが一致することを確認する。

## 7. push後のURL生成

実在するSHAを使い、コミット対象ファイルを機械的に列挙する。

```powershell
$repoUrl = 'https://github.com/ChestnutForest/paper-repro'
$branch = git branch --show-current
$sha = git rev-parse HEAD
$files = git diff-tree --no-commit-id --name-only -r $sha
$urls = @()
$urls += $repoUrl
$urls += "$repoUrl/commit/$sha"
$urls += "$repoUrl/tree/$branch"
$urls += $files | ForEach-Object { "$repoUrl/blob/$sha/$($_ -replace '\\','/')" }
$urls += "$repoUrl/commits/$branch"
$urls | ForEach-Object { $_ }
```

エージェントの最終応答では、出力されたURLを1件ずつ独立した`text`コードブロックへ入れる。
ファイル数による省略をしない。

## 8. commit前に案内するURL

commitをまだ作っていない段階ではSHAを推測しない。次だけを案内できる。

- `https://github.com/ChestnutForest/paper-repro`
- `https://github.com/ChestnutForest/paper-repro/tree/main`
- `https://github.com/ChestnutForest/paper-repro/blob/main/<実在する対象パス>`
- `https://github.com/ChestnutForest/paper-repro/commits/main`

コミット固有URLは第7節のコマンドでpush後に生成する。

## 9. 貼り付けられた実行結果の検証

| 順 | 確認すること |
|---|---|
| 1 | 期待値と実出力をコマンドごとに照合する |
| 2 | 飛ばされた工程と後続結果への影響を確認する |
| 3 | 自分が示した期待件数・期待値を実データで再計算する |
| 4 | 追加・変更・削除の内訳を説明する |
| 5 | 文書変更がコードへ波及していないか確認する |
| 6 | commit SHAとpush先、ローカル・リモートSHAを照合する |
| 7 | 途中なら残コマンド、完了なら完全なURLを示す |

よくある食い違い:

| 症状 | 先に調べること |
|---|---|
| `git status --short`が空 | 変更が既に反映・コミット済みか、別ルートにいるか |
| `nothing to commit` | 既存コミット、ステージ対象の誤り、別ブランチ |
| Mermaid数が予告の2倍 | 描画用とソース表示用の両方を数えていないか |
| 件数が予告と違う | 手計算を捨て、実ファイルを再集計する |
| `black --check`失敗 | 整形を実行していない可能性 |

利用者の操作ミスと断定しない。自分の期待値が誤っていた場合は明言し、正しい確認方法を示す。

## 10. PowerShell 5.1の注意

- 日本語を含むPowerShellスクリプトやヒアストリングを成果物として生成しない。
- MarkdownをPowerShellで再生成しない。既存ファイルの局所編集を使う。
- BOMなしUTF-8、LFを維持する。
- `$HOME`、`$home`、`$CODEX_HOME`を作業変数として再定義しない。
- 一時ファイルを使った場合は、対象パスを確認してからその一時ファイルだけを削除する。

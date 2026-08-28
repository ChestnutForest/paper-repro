---
name: paper-repro-skill-source-policy
description: paper-reproでスキルを選択・呼び出す前に、GitHubリポジトリで追跡・登録されたスキルだけを使用するための検証を行う。Windows個人領域、Codexプラグインキャッシュ、他リポジトリのスキルをpaper-repro作業へ適用しない。利用候補のSKILL.mdが.agents/skills配下にあり、Git追跡済みでHEADに存在し、originの完全SHAと同期していることを確認する。ローカルにしかない機能が必要な場合は使用せず、リポジトリへの移行案を提示する。
---

# paper-reproスキル利用元ポリシー

## 目的

paper-reproの作業で、GitHubリポジトリに登録されているスキルだけを使用する。
スキル本文の正本は`.agents/skills/<skill>/SKILL.md`であり、ローカル個人領域や
プラグインキャッシュの同名・類似スキルを知識源または手順源にしない。

このスキルは、他のpaper-reproスキルを選択する前に適用する。

## 変更履歴

| 版 | 日付 | 変更内容 |
|---|---|---|
| 1.0.0 | 2026-08-29 | GitHub登録済みスキルだけを使用する選択規則、確認手順、ローカル旧スキルの扱いを定義 |

## 現在許可されている正本スキル

| スキル | 正本パス | 責務 |
|---|---|---|
| `paper-repro-skill-source-policy` | `.agents/skills/paper-repro-skill-source-policy/SKILL.md` | スキル利用元の検証 |
| `arxiv-paper-repro` | `.agents/skills/arxiv-paper-repro/SKILL.md` | 論文の再現実装・部分採用 |
| `paper-repro-devlog` | `.agents/skills/paper-repro-devlog/SKILL.md` | 開発ログの資産化 |
| `paper-repro-commit-output` | `.agents/skills/paper-repro-commit-output/SKILL.md` | commit/push・結果URL・実行結果検証 |

`.claude/skills/`はGit管理下のClaude Code用入口であり、独立した本文正本ではない。
入口から上表の`.agents/skills/`を全文参照する場合だけ使用できる。

## 呼び出し前の確認

### 1. リポジトリを特定する

```powershell
$repoRoot = git rev-parse --show-toplevel
$origin = git remote get-url origin
$repoRoot
$origin
```

期待値:

- ルートが`C:/Users/kazuy/projects/paper-repro`
- originが`https://github.com/ChestnutForest/paper-repro.git`

一致しなければ、このポリシーとpaper-reproスキルを適用しない。

### 2. 候補スキルがGit追跡済みか確認する

`<skill-name>`を実際の候補名へ置き換える。

```powershell
$skillName = '<skill-name>'
$skillPath = ".agents/skills/$skillName/SKILL.md"
git ls-files --error-unmatch -- $skillPath
git cat-file -e "HEAD:$skillPath"
git status --short -- $skillPath
```

合格条件:

- `git ls-files`がパスを1件返す
- `git cat-file`が終了コード0になる
- `git status`が空で、呼び出す本文に未コミット差分がない

いずれかが不合格なら、そのスキルを呼び出さない。新規・更新中のスキルはcommit/pushと検証が終わるまで
通常作業へ適用しない。

### 3. GitHub登録状態を必ず確認する

GitHub登録済みのスキルとして使用する前に、完全SHAを比較する。

```powershell
$branch = git branch --show-current
$localSha = git rev-parse HEAD
$remoteLine = git ls-remote --heads origin "refs/heads/$branch"
$remoteSha = ($remoteLine -split "`t")[0]
"local=$localSha"
"remote=$remoteSha"
if ($localSha -ne $remoteSha) { throw 'Local and remote SHA do not match.' }
```

SHAが不一致、またはリモートを確認できない場合は「GitHub登録済み」と断定しない。

## Windowsローカル環境のスキルの扱い

| 場所・種類 | 扱い |
|---|---|
| `C:\Users\kazuy\.agents\skills` | paper-reproでは呼び出さない |
| `C:\Users\kazuy\.claude\skills` | paper-reproでは呼び出さない |
| `C:\Users\kazuy\.gemini\config\skills` | paper-reproでは呼び出さない |
| Codexプラグインキャッシュ | 移行元・配布キャッシュとしてのみ扱い、呼び出し・直接編集・直接削除をしない |
| 他リポジトリのスキル | paper-reproへ適用しない |
| 個人用`github-result-urls` | processloop由来のためpaper-reproでは呼び出さない |

プラグインキャッシュは更新で再生成され、他プロジェクト用スキルも含み得る。重複発火を完全に止める必要がある場合は、
キャッシュを手作業で削除せず、元のプラグインを無効化またはアンインストールする。

個人所有の重複スキルを自動探索対象外へ移す場合は、対象を確認し、ユーザーの明示的な承認を得てから行う。
移動前にリポジトリ正本へ必要な内容が移行済みであることを検証する。

## ローカルにしかない機能が必要な場合

1. ローカルスキルを呼び出さない。
2. 必要な機能、根拠、ライセンス、既存リポジトリスキルとの重複を調べる。
3. `.agents/skills/`へ追加する変更案を提示する。
4. Claude Codeが必要なら`.claude/skills/`へ参照入口を追加する。
5. `scripts/validate-agent-skills.ps1`と関連索引を更新する。
6. レビュー、commit、push、リモートSHA照合が完了した後から使用する。

## 出力規則

スキルを使用するときは、最初の短い進捗報告で次を示す。

- 使用するリポジトリスキル名
- 正本のリポジトリ相対パス
- ローカル・プラグイン版を使用していないこと

毎回長い検証ログを出す必要はない。検証失敗時だけ、失敗した条件と代替案を報告する。

## プロジェクトスキルと実行機能の区別

ターミナル、Git、ファイル編集、ブラウザーなど、AI開発環境が提供する実行機能はプロジェクトスキルではない。
これらは作業に使用できるが、paper-repro固有の判断・手順・知識は必ずGit管理下の正本スキルと`AGENTS.md`から得る。

## 禁止事項

- 個人領域やプラグインキャッシュのスキルをpaper-reproの正本として扱う
- 同名だからという理由だけでローカルスキルを優先する
- 未追跡・未コミット・未pushのスキルを「GitHub登録済み」と説明する
- プラグインキャッシュを直接編集して同期を試みる
- ローカルスキルを使った後で、出典をリポジトリスキルだったことにする

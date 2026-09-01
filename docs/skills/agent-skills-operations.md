# paper-repro AI Agent Skills運用ガイド

> 版: 2.4.0
> 更新日: 2026-09-01

Claude Code、Codex、Antigravity IDEで同じスキルを使い、本文の重複による内容ずれを防ぐための運用ガイドである。
この文書は人間向けの案内であり、スキル本文ではない。

## 調査結果

### Windowsローカル環境

| 場所・スキル | 判定 | 対応 |
|---|---|---|
| `C:\Users\kazuy\.agents\skills` | paper-repro専用スキルなし | マージ対象なし |
| `C:\Users\kazuy\.claude\skills` | ディレクトリなし | マージ対象なし |
| `C:\Users\kazuy\.gemini\config\skills` | ディレクトリなし | マージ対象なし |
| Codexプラグインキャッシュの`arxiv-paper-repro` | paper-repro開発履歴と一致 | リポジトリへ正本化 |
| Codexプラグインキャッシュの`paper-repro-devlog` | paper-repro開発履歴と一致 | リポジトリへ正本化し、旧名`paper-repro-mvp`を修正 |
| 個人用`github-result-urls` | processloop開発時に作成 | paper-repro以外のため除外。変更・削除なし |

プラグインキャッシュはインストール済みパッケージの派生配置であり、プロジェクトの正本にはしない。

### リポジトリ内のSkill関連ファイル

調査前に存在したSkill関連ファイルは、次の5件だけだった。

- `AGENTS.md`
- `CLAUDE.md`
- `.agents/skills/paper-repro-commit-output/SKILL.md`
- `.claude/skills/paper-repro-commit-output/SKILL.md`
- `docs/skills/agent-skills-operations.md`

`docs/requirements-analysis/academic-research-skills.md`と
`docs/requirements-analysis/academic-research-skills-frameworks.md`にも「skills」が含まれるが、
これらはアプリ要件の調査文書であり、AI Agent Skillではない。

## 統合後の正本構成

```text
.agents/skills/
├── paper-repro-skill-source-policy/
│   └── SKILL.md
├── paper-repro-arch-guide/
│   └── SKILL.md
├── arxiv-paper-repro/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── paper-repro-devlog/
│   └── SKILL.md
└── paper-repro-commit-output/
    ├── SKILL.md
    └── references/

.claude/skills/
├── paper-repro-skill-source-policy/SKILL.md
├── paper-repro-arch-guide/SKILL.md
├── arxiv-paper-repro/SKILL.md
├── paper-repro-devlog/SKILL.md
└── paper-repro-commit-output/SKILL.md
```

`.agents/skills`の5ファイルが本文の正本である。`.claude/skills`の5ファイルは正本への短い入口だけを持ち、
手順本文を複製しない。WindowsでGitのシンボリックリンクが通常ファイルへ変わる問題を避けるため、
シンボリックリンクではなく参照入口を採用した。

## 対応環境

| 環境 | 読み込み先 | 備考 |
|---|---|---|
| Codex | `.agents/skills` | リポジトリスキルの標準探索場所 |
| Antigravity IDE | `.agents/skills` | ワークスペーススキルの標準探索場所 |
| Claude Code | `.claude/skills` | 入口から`.agents/skills`の正本を全文参照 |

各`SKILL.md`のfrontmatterは、移植性を保つため`name`と`description`だけを使う。

## 5スキルの責務

| スキル | 責務 | 使わない場面 |
|---|---|---|
| `paper-repro-skill-source-policy` | GitHub登録済みのリポジトリスキルだけを許可 | paper-repro以外のプロジェクト |
| `paper-repro-arch-guide` | 要求からアーキテクチャ設計へ展開し、Mermaid CLIで実描画検証 | 論文そのものの再現実装、日次ログ |
| `arxiv-paper-repro` | AI/ML論文の再現、部分採用、スコア不一致の切り分け | 単純な要約・英文解釈 |
| `paper-repro-devlog` | paper-repro開発の日次知識を`docs/devlog/`へ保存 | 他アプリ、論文そのものの実装 |
| `paper-repro-commit-output` | commit/pushコマンド、実行、SHA照合、チャットで個別コピー可能なGitHub URL、結果検証 | 他リポジトリ |

用途の異なる機能は別スキルのまま保ち、保存場所、正本、参照方法だけを一本化する。

## スキル利用元の制限

他のスキルを選ぶ前に`paper-repro-skill-source-policy`を適用する。候補の`SKILL.md`が
`.agents/skills/`配下にあり、Git追跡済みで、`HEAD`に存在し、未コミット差分がないことを確認する。
GitHub登録済みとして利用する前に、ローカルとoriginの完全SHAも必ず照合する。

Windows個人領域、Codexプラグインキャッシュ、他リポジトリのスキルはpaper-reproへ適用しない。
移行済みのローカル旧スキルは非アクティブな移行元として残し、呼び出し・直接編集・直接削除をしない。
重複発火を止める必要がある場合は、キャッシュ削除ではなく元プラグインの無効化またはアンインストールを選ぶ。

ローカルにしかない機能が必要な場合は使用を中止し、リポジトリスキルとして追加・検証・commit/pushしてから利用する。

## 更新規則

1. 本文は`.agents/skills/<name>/SKILL.md`だけを編集する。
2. 詳細資料は同じスキル配下の`references/`または`assets/`に置く。
3. `.claude/skills/<name>/SKILL.md`には、名前・発火条件・正本リンクだけを置く。
4. `docs/skills/`へスキル本文を複製しない。
5. スキルを追加・改名したら、この文書、`README.md`、`docs/README.md`、検証スクリプトを同期する。
6. 改名した場合は、同期の直後に `git grep <旧名>` を実行し、出力がゼロであることを確認する。上の一覧は網羅を保証しない。
7. プラグインキャッシュや個人用スキルを呼び出し・直接編集しない。
8. 新規・更新中のスキルは、commit/pushとリモートSHA照合が終わるまで通常作業へ適用しない。

## 検証

PowerShell 5.1から次を実行する。

```powershell
Set-Location 'C:\Users\kazuy\projects\paper-repro'
powershell -NoProfile -ExecutionPolicy Bypass -File '.\scripts\validate-agent-skills.ps1'
git diff --check
```

検証は、正本とClaude入口の1対1対応、標準frontmatter、参照先、禁止された古い環境依存語、
BOMなしUTF-8、LF、関連文書の参照を確認する。

設計文書のMermaidを追加・変更した場合は、リポジトリ固定のCLIで実描画も確認する。

```powershell
npm ci
npm run validate:mermaid
```

全Markdownを描画検証するときは`npm run validate:mermaid:all`を使う。

commit後は、Git追跡・`HEAD`登録・未コミット差分なしも確認する。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\scripts\validate-agent-skills.ps1' -RequireGitTracked
```

## commit/pushと確認URL

コマンド提示、実際のcommit/push、push後のURL、実行結果検証では、リポジトリ内の
[`paper-repro-commit-output`](../../.agents/skills/paper-repro-commit-output/SKILL.md)を使う。
詳細コマンドは
[`commit-workflow.md`](../../.agents/skills/paper-repro-commit-output/references/commit-workflow.md)を参照する。

コマンドだけを求められた場合はcommit/pushを実行しない。実際にpushした後は完全SHAを照合し、
リポジトリ、コミット、ブランチ、全コミット対象ファイル、履歴のURLを省略せず出す。
ターミナルへURLを表示しただけでは完了とせず、このチャットで1 URLずつ独立した`text`コードブロックへ入れる。
各ブロックにはURLだけを置き、チャットUIのコピーアイコンで個別コピーできる形にする。

## 公式仕様

- [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Google Antigravity Skills](https://antigravity.google/docs/skills)

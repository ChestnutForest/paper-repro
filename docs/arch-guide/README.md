# paper-reproアーキテクチャ設計文書

paper-reproの要求を、アーキテクチャ、画面、システム振舞い、データモデルへ展開した
現行設計文書の索引である。AI Agent Skillの本文は
[`../../.agents/skills/paper-repro-arch-guide/SKILL.md`](../../.agents/skills/paper-repro-arch-guide/SKILL.md)
を正本とし、この文書には複製しない。

## 設計成果物

| 文書 | 内容 |
|---|---|
| [`arc-artifact-order.md`](arc-artifact-order.md) | 成果物の作成順、責務、相互参照 |
| [`arc-architecture.md`](arc-architecture.md) | システム全体のアーキテクチャ |
| [`arc-screen.md`](arc-screen.md) | 画面設計の枠組み |
| [`arc-screen-list.md`](arc-screen-list.md) | 画面一覧 |
| [`arc-screen-flow.md`](arc-screen-flow.md) | 画面遷移 |
| [`arc-screen-rules.md`](arc-screen-rules.md) | 画面共通ルール |
| [`arc-behavior.md`](arc-behavior.md) | システム振舞い設計の枠組み |
| [`arc-behavior-list.md`](arc-behavior-list.md) | 要求から導いた業務・自動処理の一覧 |
| [`arc-behavior-flow.md`](arc-behavior-flow.md) | 振舞いフロー |
| [`arc-behavior-rules.md`](arc-behavior-rules.md) | 振舞い共通ルール |
| [`arc-behavior-state.md`](arc-behavior-state.md) | 実装と照合した状態遷移 |
| [`behaviors/README.md`](behaviors/README.md) | グループ別システム振舞い説明の索引 |
| [`arc-datamodel.md`](arc-datamodel.md) | データモデル設計 |

## CCAF適用資料

| 文書 | 内容 |
|---|---|
| [`ccaf-patterns.md`](ccaf-patterns.md) | paper-reproへ適用するCCAFパターン |
| [`claude-code-playbook.md`](claude-code-playbook.md) | Claude Code / Codexへの設計・実装依頼例 |
| [`coverage-rubric.md`](coverage-rubric.md) | CCAF適用率の算定規則 |
| [`coverage-remeasure-howto.md`](coverage-remeasure-howto.md) | 適用率の再計測手順 |
| [`ccaf-coverage-2026-08-03.md`](ccaf-coverage-2026-08-03.md) | 2026-08-03時点の適用率 |

## Mermaid描画検証

Mermaidを含む設計文書を追加・変更したら、構造検査に加えてリポジトリ固定の
Mermaid CLIで実際にSVGへ描画する。

```powershell
npm ci
npm run validate:mermaid
```

全Markdownを検査する場合は次を使う。

```powershell
npm run validate:mermaid:all
```

検証スクリプトは一時SVGを検査後に削除するため、生成物はリポジトリへ残らない。

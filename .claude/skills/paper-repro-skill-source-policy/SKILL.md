---
name: paper-repro-skill-source-policy
description: paper-reproでスキルを選択・呼び出す前に、GitHubリポジトリで追跡された正本だけを使うための検証を行う。本文の正本は.agents/skillsにある。
---

# Claude Code entrypoint: paper-repro-skill-source-policy

他のpaper-reproスキルを選択する前に、正本の
[`../../../.agents/skills/paper-repro-skill-source-policy/SKILL.md`](../../../.agents/skills/paper-repro-skill-source-policy/SKILL.md)
を全文読み、その指示に従う。

このファイルへ手順本文を複製しない。変更は正本だけに行う。

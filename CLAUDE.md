# CLAUDE.md — Claude Code 用エントリーポイント

Claude Code はこのファイルを自動的に読み込む。
**paper-reproの共通AI開発ルールは`AGENTS.md`、スキル本文は`.agents/skills/`を正本とする。**

## 作業開始時に必ず行うこと

1. `AGENTS.md` を全文読み、その指示に従う。
2. `docs/requirements.md`、`docs/product-design.md`、`docs/roadmap.md` のうち作業に関係する文書を読む。
3. `git status --short --branch` と `docs/devlog/` の最新ファイルを確認する。
4. `.claude/skills/paper-repro-skill-source-policy/`の入口から利用元を確認する。
5. 依頼に該当する場合だけ、`arxiv-paper-repro`、`paper-repro-devlog`、
   `paper-repro-commit-output`の正本を全文読む。

## 共有ルール

- プロジェクト共通の方針は `AGENTS.md` に記録し、このファイルへ重複させない。
- Claude Code 固有のコマンドや設定だけを、このファイルまたは `.claude/` に置く。
- CodexまたはAntigravity IDEへ引き継ぐ判断・未解決事項・次の作業は、会話内だけで終わらせずGit管理下の文書へ残す。
- `.claude/skills/`はClaude Code用の入口だけを保持し、`.agents/skills/`の本文を複製しない。
- Windows個人領域やプラグインキャッシュのスキルをpaper-reproへ適用しない。
- `AGENTS.md` を変更した場合は、`README.md` と関連文書の参照も同じ変更で確認する。

上位のシステム指示やユーザーの明示的な依頼と矛盾しない範囲で、`AGENTS.md` を
paper-repro のプロジェクト固有ルールとして適用する。

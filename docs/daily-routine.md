# 日々のルーチンワーク

開発を始めるとき・終えるときに、この手順をなぞる。
**毎日やること**と**節目でやること**を分けている。迷ったらこのファイルを開けばよい。

---

## 1. 開発を始めるとき（5分）

### 1-1. 前回の続きを確認する

```
docs/devlog/ の最新ファイルを開き、「未解決の疑問と翌日の開発計画」を読む
```

前回の自分が残した「次にやること」がここに書いてある。ここから再開する。

### 1-2. 環境を起動する（ワンコマンド）

Docker Desktop 本体を起動しておいてから、プロジェクトのルートで実行する。

**Windows**

```powershell
.\scripts\start-dev.ps1
```

**Mac / Linux**

```bash
./scripts/start-dev.sh
```

PostgreSQL 起動 → バックエンド起動 → Swagger UI が自動で開く。
**実行後に確認する事項のチェックリスト**は [`dev-startup.md`](dev-startup.md) を参照。

画面（フロントエンド）も使うなら、**別のターミナル**で：

```powershell
cd frontend
npm run dev
```

### 1-3. 今日やることを決める

`docs/roadmap.md` で現在フェーズを確認し、今日の範囲を1つに絞る（縦切り）。

---

## 2. 開発中（都度）

- 設計で迷ったら → [`arch-guide/README.md`](arch-guide/README.md)（CCAF設計指針）
- Claude Code への頼み方 → [`arch-guide/claude-code-playbook.md`](arch-guide/claude-code-playbook.md)（依頼テンプレA〜E）
- 大きな変更は「まず計画を出させてから実装」

---

## 3. 開発を終えるとき（10分）

### 3-1. テストを回す

```powershell
cd backend
.venv\Scripts\Activate.ps1
python -m pytest tests\ -q
```

緑（passed）を確認してからコミットする。

### 3-2. コミット＆プッシュ

```powershell
cd C:\Users\kazuy\projects\paper-repro-mvp
git status
```

`.env` や `.env.local` が出ていないことを目視確認してから：

```powershell
git add .
git commit -m "<英文メッセージ。例: feat: add paper intake endpoint>"
git push
```

### 3-3. 今日の分を資産化する（毎日）

Claude に **「今日の分を資産化して」** と言う。
生成された `devlog-YYYY-MM-DD.md` を配置してコミットする：

```powershell
git add docs/devlog/
git commit -m "docs: add devlog YYYY-MM-DD"
git push
```

### 3-4. NotebookLM に入れる（毎日）

生成した devlog を NotebookLM の「ソースを追加」からアップロードする。
深掘りやスライド化のプロンプトは [`notebooklm-prompts.md`](notebooklm-prompts.md) を使う。

### 3-5. 環境を止める（任意）

バックエンドは起動中のターミナルで `Ctrl + C`。DB も止めるなら：

```powershell
docker compose down
```

---

## 4. 節目でやること（毎日ではない）

以下は**毎日やっても意味が薄い**ため、トリガーが来たときだけ実施する。

### 4-1. CCAF適用率の再計測

**トリガー**：ロードマップのフェーズが1つ完了したとき／大きな機能が入ったとき／報告資料を作るとき

**理由**：適用率は機能が実装されて初めて動く。毎日測っても同じ数値が並ぶだけで、
指標としての意味が薄れる。

**手順**：[`arch-guide/coverage-remeasure-howto.md`](arch-guide/coverage-remeasure-howto.md) に従う（要点は下記）。

1. 前回ファイル（`docs/arch-guide/` の最新 `ccaf-coverage-*.md`）を Claude に添付する
2. 「CCAF適用率を出して」と言う
3. 生成されたレポートを配置してコミットする：

```powershell
git add docs/arch-guide/
git commit -m "docs: update CCAF coverage indicator YYYY-MM-DD"
git push
```

### 4-2. ロードマップの更新

フェーズが完了したら `docs/roadmap.md` の進捗サマリーにチェックを入れる。

---

## チェックリスト（印刷・コピー用）

**毎日**

- [ ] 前回の devlog の「翌日の計画」を読んだ
- [ ] `start-dev` スクリプトで環境を起動し、Swagger UI を確認した
- [ ] 今日の範囲を1つに絞った
- [ ] テストが緑になった
- [ ] `git status` で `.env` が出ないことを確認してコミット＆プッシュした
- [ ] 「今日の分を資産化して」で devlog を作り、コミットした
- [ ] devlog を NotebookLM にアップロードした

**節目（フェーズ完了・大きな機能追加のとき）**

- [ ] 前回ファイルを添付して CCAF適用率を再計測した
- [ ] レポートをコミット＆プッシュした
- [ ] `docs/roadmap.md` の進捗を更新した

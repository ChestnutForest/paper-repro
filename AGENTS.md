# AGENTS.md — paper-repro 共通AI開発指示

このファイルはリポジトリ全体に適用する、**Claude Code と Codex の共通正本**である。
Codex はこのファイルを直接読み、Claude Code は `CLAUDE.md` を入口としてこのファイルを全文読む。

## 基本方針: SSOT（Single Source of Truth）について

当プロジェクトでは、開発プロセスおよびシステム設計において **SSOT（Single Source of Truth：信頼できる唯一の情報源）** の原則を厳格に適用します。

SSOTとは、組織内のあらゆるデータ要素を「たった1つの場所」にのみ保存・編集するように構造化する概念です。
情報が複数の場所に点在・重複することを防ぐことで、「どのデータが最新で正しいのか」という迷いや、同期漏れによる不整合（バグ）を根本から排除します。

**【当プロジェクトにおけるSSOTの適用例】**
*   **開発ルール・AIエージェントのスキル**: 本ファイル（`AGENTS.md`）をSSOTとします。他のすべての環境（Claude Codeの `CLAUDE.md` 等）は、個別にルールを持たず、本ファイルへの参照指示のみを保持します。
*   **バックエンド/フロントエンドのデータモデル**: データベースのスキーマやAPIの型定義においても、情報の重複管理を避け、一箇所で定義したものを各所で参照・再利用する設計を徹底してください。

## 1. 指示と開発データの共有方針

- プロジェクト共通の方針・設計原則・作業手順は、この `AGENTS.md` だけで管理する。
- `CLAUDE.md` には Claude Code 固有の入口情報だけを置き、共通内容を複製しない。
- Claude Code と Codex の会話履歴や一時的な内部状態は共有されない。引き継ぐ情報は Git、`docs/`、
  `docs/devlog/` に残す。
- エージェントを切り替えるときは、未解決事項・判断理由・次の作業を文書化し、作業ツリーの状態を確認する。
- このファイルを変更したら、同じ変更で `CLAUDE.md`、`README.md`、関連する現行文書の参照も確認する。

## 2. 作業開始時の読み順

1. `git status --short --branch` で作業ツリーを確認し、既存のユーザー変更を保護する。
2. この `AGENTS.md` を全文読む。
3. `docs/requirements.md`、`docs/product-design.md`、`docs/roadmap.md` を読む。
4. `docs/daily-routine.md` と `docs/devlog/` の最新ファイルで、未解決事項と次の作業を確認する。
5. ユーザーの依頼範囲を確認し、その範囲を越える変更は行わない。

## 3. このプロジェクトは何か

**paper-repro** は、英語のAI論文（arXiv）を読み解き、再現実装まで支援する正式版プロダクト。
現在は正式版の第1段階として、「タイプB（学習なし・公式実装あり）」の論文を対象に
初期リリースを縦切りで構築している。GPU・レンダリング・LLM-as-a-Judge は
製品全体から除外せず、後続リリースで対応する。

## 4. 技術スタック

- バックエンド: **FastAPI (Python 3.12+)** + Celery + Redis + PostgreSQL
- フロントエンド: **Next.js (React) + TypeScript**
- 実行分離: サンドボックス（初期リリースは CPU のみ・ネットワーク遮断）

## 5. 設計上の絶対原則

1. **human-in-the-loop。** 各 Phase 末に承認ゲートを置き、人間の承認なしに次へ進めない。
   全自動化しない。
2. **長時間処理は非同期ジョブ + WebSocket 進捗。** 同期RESTで待たせない。
3. **信頼できない第三者コードは必ずサンドボックスで実行。** ホスト直実行は禁止。
4. **成果物の zip 名は `files_reify_YYYYMMDD_hhmm.zip`（JST基準）。** UTCのまま作らない。
5. **将来的に日英の言語切り替え（i18n）に対応する。** フロントの画面文言は最初から
   `next-intl` の `t("キー")` 方式で書き、日本語・英語を直接ハードコードしない。

## 6. ディレクトリ構成

```text
backend/app/
  api/        FastAPI のルーター（エンドポイント）
  core/       設定・DB接続・状態機械
  models/     SQLAlchemy モデル / Pydantic スキーマ
  services/   論文取り込み・実装探索・LLM・スコア照合
  workers/    Celery タスク（サンドボックス実行など）
frontend/src/
  pages/      画面（ダッシュボード、インテーク、作業台、検証台、レポート）
  components/ UI部品
  lib/        API クライアント・WebSocket クライアント
docs/         要件、設計、ロードマップ、運用手順、開発履歴
```

## 7. コーディング規約

- Python: 型ヒント必須。`ruff` + `black` で整形する。
- **インターフェース情報の記載は必須。** 公開するクラス・関数・メソッドには、
  次を含む docstring を必ず付ける（詳細は §7.1）。
- TypeScript: strict モードを維持し、`any` を避ける。
- 1つの論理変更を1コミットにまとめ、無関係な差分を混ぜない。
- 秘密情報（APIキー等）を絶対にコミットしない。`.env` と `.env.local` は追跡対象にしない。
- 既存のAPI入出力や状態遷移を変える場合は、理由を設計文書または履歴に記録する。

### 7.1 インターフェース情報のコメント（必須）

コードを追加・変更したときは、**同じ変更の中で** インターフェース情報を記載する。
「あとで書く」は残らない。レビューではこの記載の有無も見る。

**クラスに書くこと**

- そのクラスが何を表すか（1文）
- `Attributes:` — 各属性の意味。列や項目に制約（NOT NULL、既定値なし、必須など）があれば明記する
- 根拠となる要求ID（`REQ-Cxx`）や仕様の節番号

**関数・メソッドに書くこと**

- 何をするか（1文）
- `Args:` — 各引数の意味
- `Returns:` — 戻り値の意味。HTTP を返す場合はステータスコードも
- `Raises:` — 送出しうる例外と、**その条件**。条件が複数あるなら分けて書く
- `Note:` — 誤用しやすい点、他の関数との境界、過去に起きた不具合

**特に必ず書くもの**

| 対象 | 書く理由 |
|---|---|
| 似た名前で意味が違うもの | 例: `Course.READING` と `Phase.READING` は値が同じ文字列だが別の型。取り違えた比較は常に偽になり気づきにくい |
| 何に答え、何に答えないか | 例: `can_transition` は遷移の可否には答えるが、ゲートを押せる工程かには答えない |
| 制約とその根拠 | 例: `course` に既定値を置かない理由（`REQ-C01`） |
| 過去の不具合 | 再発防止のテストには、何を守るテストかを書く |

**やってはいけないこと**

- 型注釈をそのまま日本語にしただけの記述（`db: DB セッション` だけで終わる等）
- 実装の手順をなぞるだけの記述。**呼び出す側が知りたいこと**を書く
- docstring を足すついでに実行コードを変えること。**別のコミットに分ける**

**実行コードを変えずに docstring だけを足したことの証明**

docstring を除いた抽象構文木（AST）を追加前後で比較し、一致することを確認する。

```powershell
backend\.venv\Scripts\python.exe -c "import ast,sys;
def s(p):
    t=ast.parse(open(p,encoding='utf-8').read())
    for n in ast.walk(t):
        if isinstance(n,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
            b=n.body
            if b and isinstance(b[0],ast.Expr) and isinstance(b[0].value,ast.Constant) and isinstance(b[0].value.value,str): n.body=b[1:]
    return ast.dump(t)
print('same' if s(sys.argv[1])==s(sys.argv[2]) else 'DIFFER')" before.py after.py
```

## 8. 作業の進め方

- 大きな変更の前に、変更対象・方針・検証方法を箇条書きで示す。
- ユーザーが実装範囲を明示して依頼済みなら、その範囲は承認済みとして進める。
  範囲を広げる必要がある場合だけ、追加の確認を取る。
- テストがある機能は、実装と同時にテストも更新する。
- `docs/` の要件・設計と矛盾しそうな場合は、推測で進めず確認する。
- 既存の未コミット変更はユーザーのものとして扱い、勝手に破棄・上書きしない。
- README以外の現行文書を追加・改名した場合は、`README.md` と `docs/README.md` の索引を同期する。
- commit / push はユーザーが依頼した場合に実行し、実行後はローカルとリモートのSHA一致を確認する。

## 9. 検証

変更範囲に応じて、少なくとも次を実行する。

```powershell
# バックエンド
backend\.venv\Scripts\python.exe -m pytest backend\tests -q

# フロントエンド
npm --prefix frontend run build

# リポジトリ差分
git diff --check
git status --short --branch
```

実行できない検証がある場合は、理由と未検証範囲を報告する。

## 10. Claude Code ↔ Codex の引き継ぎ

作業を渡す側：

1. 変更内容とテスト結果を確認する。
2. 未解決事項・判断理由・次の一手を `docs/devlog/` または適切な現行文書へ記録する。
3. `git status` を確認し、依頼されている場合は commit / push する。

作業を受け取る側：

1. 同じリポジトリルートを開き、`git status` と `git log -1 --oneline` を確認する。
2. この `AGENTS.md`、関連設計、最新devlogを読む。
3. 会話履歴ではなく、リポジトリに記録された状態を基準に再開する。

## 11. 現在の開発フェーズ

**Step 1: 骨組みを1本通す。**
「arXiv URL 投入 → 論文取り込み → spec 草案 → 手編集 → zip 出力」を、
サンドボックス無しで最短で動かす。まだ横に広げない（縦切り）。
`docs/product-design.md` の第6章「実装の着手順」に従う。

## 12. エージェントの出力フォーマット（GitHub URL等）

`commit` や `push` を実行した後は、その結果として生成されたGitHubのURLを**必ず一行ずつ独立したコードブロックで出力**し、人間が個別に簡単にコピーできるようにすること。
「commit/pushしたURLを教えて」と指示された場合も同様の形式で出力する。

対象とするURLは以下の通り：
*   対象ファイルごとのブランチのURL（例: `https://github.com/.../blob/main/filename.md`）
*   特定のコミットに紐づくファイルのURL（例: `https://github.com/.../blob/<commit-hash>/filename.md`）
*   コミット自体のURL（例: `https://github.com/.../commit/<commit-hash>`）

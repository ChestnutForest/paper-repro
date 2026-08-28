# AGENTS.md — paper-repro 共通AI開発指示

このファイルはリポジトリ全体に適用する、**Claude Code、Codex、Antigravity IDEの共通ルール正本**である。
CodexとAntigravity IDEはこのファイルをプロジェクト指示として読み、Claude Codeは`CLAUDE.md`を入口として全文読む。

## 基本方針: SSOT（Single Source of Truth）について

当プロジェクトでは、開発プロセスおよびシステム設計において **SSOT（Single Source of Truth：信頼できる唯一の情報源）** の原則を厳格に適用します。

SSOTとは、組織内のあらゆるデータ要素を「たった1つの場所」にのみ保存・編集するように構造化する概念です。
情報が複数の場所に点在・重複することを防ぐことで、「どのデータが最新で正しいのか」という迷いや、同期漏れによる不整合（バグ）を根本から排除します。

**【当プロジェクトにおけるSSOTの適用例】**
*   **開発ルール**: 本ファイル（`AGENTS.md`）をSSOTとします。`CLAUDE.md`等は環境固有の入口だけを保持します。
*   **AI Agent Skills**: `.agents/skills/<skill>/SKILL.md`を本文のSSOTとします。`.claude/skills/`はClaude Code用の参照入口だけを保持し、本文を複製しません。
*   **バックエンド/フロントエンドのデータモデル**: データベースのスキーマやAPIの型定義においても、情報の重複管理を避け、一箇所で定義したものを各所で参照・再利用する設計を徹底してください。

## 1. 指示と開発データの共有方針

- プロジェクト共通の方針・設計原則・作業手順は、この `AGENTS.md` だけで管理する。
- `CLAUDE.md`と`.claude/skills/`にはClaude Code固有の入口情報だけを置き、共通内容を複製しない。
- Claude Code、Codex、Antigravity IDEの会話履歴や一時的な内部状態は共有されない。引き継ぐ情報はGit、`docs/`、
  `docs/devlog/` に残す。
- エージェントを切り替えるときは、未解決事項・判断理由・次の作業を文書化し、作業ツリーの状態を確認する。
- このファイルを変更したら、同じ変更で `CLAUDE.md`、`README.md`、関連する現行文書の参照も確認する。

## 2. 作業開始時の読み順

1. `git status --short --branch` で作業ツリーを確認し、既存のユーザー変更を保護する。
2. この `AGENTS.md` を全文読む。
3. `docs/requirements.md`、`docs/product-design.md`、`docs/roadmap.md` を読む。
4. `docs/daily-routine.md` と `docs/devlog/` の最新ファイルで、未解決事項と次の作業を確認する。
5. 依頼が該当する場合は、`.agents/skills/`の`arxiv-paper-repro`、`paper-repro-devlog`、`paper-repro-commit-output`を読む。
6. ユーザーの依頼範囲を確認し、その範囲を越える変更は行わない。

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

### 7.1 コメントと docstring（PEP 257 / PEP 8 準拠・必須）

**Python のコメントは PEP 257（Docstring Conventions）と PEP 8（Style Guide for Python Code）に従う。**
両者は Python 公式の情報提供 PEP であり、書誌は `docs/references.md` の REF-18・REF-19。

コードを追加・変更したときは、**同じ変更の中で** docstring を書く。「あとで書く」は残らない。

#### 7.1.1 どこに書くか（PEP 8）

公開するモジュール・関数・クラス・メソッドには docstring を書く。
非公開（`_` 始まり）には docstring は必須でないが、**何をするかのコメントは置く**。
パッケージは `__init__.py` のモジュール docstring で文書化する（PEP 257）。

#### 7.1.2 書式（PEP 257）

- 常に `"""三重ダブルクォート"""` で囲む。バックスラッシュを含むなら `r"""..."""`。
- **1行 docstring**: 本当に自明な場合だけ。閉じクォートは開きクォートと同じ行に置き、
  前後に空行を入れない。末尾はピリオド（日本語なら句点）で終える。
- **複数行 docstring**: 要約行 → **空行** → 詳細、の順。要約行は1行に収める。
  要約行は開きクォートと同じ行に置く。閉じクォートは独立した行に置く。
- クラスの docstring の**後ろに空行**を1行入れ、最初のメソッドと離す。
- **モジュール docstring の後ろにも空行**を1行入れ、最初の import と離す。
  PEP 257 は明記していないが、`black` がこれを要求する。空行が無いと整形で落ちる。
- 1行 docstring に**シグネチャを書かない**。引数は内省で得られるため。
  ただし**戻り値の性質**は内省で分からないので書く。
- 要約行は効果を**命令形**で述べる。「〜を返す」と書き、「〜を返します」とは書かない。

#### 7.1.3 何を書くか（PEP 257）

| 対象 | 書く内容 |
|---|---|
| モジュール | エクスポートするクラス・例外・関数を、それぞれ1行の要約つきで列挙する |
| パッケージ | 上に加えて、エクスポートするモジュールとサブパッケージを列挙する |
| クラス | 振る舞いの要約、公開メソッドとインスタンス変数。継承元と主に振る舞いが同じなら、その旨と差分 |
| 関数・メソッド | 振る舞いの要約、**引数・戻り値・副作用・送出する例外・呼び出せる条件の制限**（該当するものすべて）。省略可能な引数はその旨を示す |

**節見出しの書式は Google スタイル**（`Args:` / `Returns:` / `Yields:` / `Raises:` /
`Attributes:` / `Note:` / `Todo:`）を用いる。PEP 257 は「マークアップ構文には立ち入らない」と
明言しており、節見出しの形式は PEP が定めていない。**プロジェクトとして Google スタイルを選ぶ。**

#### 7.1.4 コメント（PEP 8）

- ブロックコメントは、説明する**コードと同じインデント**に置き、各行を `# ` で始める。
  段落の区切りは `#` だけの行にする。
- インラインコメントは控えめに使う。文と**2つ以上のスペース**で離し、`# ` で始める。
  自明なことを書かない。
- **コードと矛盾するコメントは、コメントが無いより悪い。** コードを変えたらコメントも変える。

#### 7.1.5 このプロジェクトの逸脱（意図的）

| PEP の記述 | 本プロジェクトの扱い | 理由 |
|---|---|---|
| コメントは英語で書く（PEP 8） | **日本語で書く。**コミットメッセージは英語 | 読み手が日本語話者に限られる。PEP 8 も「その言語を話さない人に読まれないと120%確信できる場合」は例外としている |
| docstring とコメントは72文字まで（PEP 8） | `black` の既定（88文字）に合わせる | PEP 8 自身がチームの合意による延長を認めている。日本語では文字数の意味も異なる |
| 要約行はピリオドで終わる（PEP 257） | **句点「。」で終える。**Ruff の `D400` は無効化する | `D400` は ASCII のピリオドだけを認めるため、日本語では必ず誤検出になる。規則自体は §7.1.2 で守り、検査は §7.1.8 の自作スクリプトが担う |

**要約行を識別子や固有名詞で始めない。** Ruff の `D403` は先頭語の大文字化を求めるが、
PEP 8 は識別子の大小を変えることを禁じており、`arXiv` のように意図的に小文字で始まる
固有名詞もある。**大文字化するのではなく、そもそもそれらで始まらない要約行に書き換える。**

#### 7.1.6 特に必ず書くもの

| 対象 | 書く理由 |
|---|---|
| 似た名前で意味が違うもの | 例: `Course.READING` と `Phase.READING` は値が同じ文字列だが別の型。取り違えた比較は常に偽になり気づきにくい |
| 何に答え、何に答えないか | 例: `can_transition` は遷移の可否には答えるが、ゲートを押せる工程かには答えない |
| 制約とその根拠 | 例: `course` に既定値を置かない理由（`REQ-C01`） |
| 過去の不具合 | 退行テストには、何を守るテストかを書く |

#### 7.1.7 やってはいけないこと

- 型注釈をそのまま日本語にしただけの記述（`db: DB セッション` だけで終える等）
- 実装の手順をなぞるだけの記述。**呼び出す側が知りたいこと**を書く
- docstring を足すついでに実行コードを変えること。**別のコミットに分ける**

#### 7.1.8 検証

**PEP 257 の規則を Ruff で検査する。** 検査対象は `backend/ruff.toml` が定める。
設定が無いと Ruff は `D` 規則を見ないため、**この設定ファイルを消さないこと。**

```powershell
backend\.venv\Scripts\python.exe -m ruff check backend
```

**整形を通す。** `--check` は失敗を知らせるだけで直さない。
**必ず `black` を実行してから `--check` で確認する。** 対象はファイル単位ではなく
`backend` 全体にする。ファイルを絞ると、触っていない既存の違反を見逃す。

```powershell
backend\.venv\Scripts\python.exe -m black backend; backend\.venv\Scripts\python.exe -m black --check backend
```

整形で実行コードが変わっていないことは、下の AST 比較で改めて確認する。

**docstring の欠落を検出する。**

```powershell
backend\.venv\Scripts\python.exe -c "import ast,pathlib
for p in sorted(pathlib.Path('backend').rglob('*.py')):
    if '.venv' in str(p): continue
    t=ast.parse(p.read_text(encoding='utf-8'))
    m=[] if ast.get_docstring(t) else ['module']
    for n in ast.walk(t):
        if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and not (n.name.startswith('_') and n.name!='__init__') and not ast.get_docstring(n): m.append(n.name)
    if m: print(p, m)"
```

**実行コードを変えずに docstring だけを足したことを証明する。**
docstring を除いた抽象構文木（AST）が追加前後で一致することを確認する。
比較元は `git show` で取り出す。**`git stash` は使わない。** 未追跡ファイルを退避せず、
`pop` に失敗すると変更が stash に残って気づきにくいため。

```powershell
git show HEAD:backend/app/core/states.py > $env:TEMP\before.py
```

```powershell
backend\.venv\Scripts\python.exe -c "import ast,sys
def s(p):
    t=ast.parse(open(p,encoding='utf-8').read())
    for n in ast.walk(t):
        if isinstance(n,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
            b=n.body
            if b and isinstance(b[0],ast.Expr) and isinstance(b[0].value,ast.Constant) and isinstance(b[0].value.value,str): n.body=b[1:]
    return ast.dump(t)
print('same' if s(sys.argv[1])==s(sys.argv[2]) else 'DIFFER')" $env:TEMP\before.py backend\app\core\states.py
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

## 8.1 進捗の更新

フェーズの状態が変わったときは、**`docs/roadmap.md` を正本として先に直し、
同じ変更でルート `README.md` 冒頭の進捗表も合わせる。**
README はリポジトリを開いた人が最初に見る場所であり、そこが古いと誤解が生じる。

## 9. 検証

各道具の役割と選定理由は [`docs/tech-stack.md`](docs/tech-stack.md) を参照する。
変更範囲に応じて、少なくとも次を実行する。

**加えて、機能を追加・変更したときは画面で確かめる。**
テストが通ることと、利用者が操作できることは別である。
確認する画面は [`docs/roadmap.md`](docs/roadmap.md) の各フェーズの「確認画面」の表、
投入する論文は [`docs/test-papers.md`](docs/test-papers.md) の基準論文を使う。

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

## 10. Claude Code ↔ Codex ↔ Antigravity IDE の引き継ぎ

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

commit/pushコマンド、実行、結果URL、Git実行結果の検証には、リポジトリ内の
`.agents/skills/paper-repro-commit-output/SKILL.md`を使う。コマンド提示だけの依頼ではcommit/pushを実行しない。

実際にpushした後は完全SHAをリモートと照合し、リポジトリ、コミット、ブランチ、
全コミット対象ファイル、履歴のURLを1件ずつ独立したコードブロックで出力する。
空または架空のSHAを使用せず、ファイル数を理由にURLを省略しない。

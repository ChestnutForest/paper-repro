---
name: paper-repro-commit-steps
description: paper-repro プロジェクト（C:\Users\kazuy\projects\paper-repro、GitHub は ChestnutForest/paper-repro）で作成した md ファイルやスクリプトを、Windows PowerShell 5.1 から配置して GitHub にコミット・プッシュするまでの手順を、番号ごとに1つのコピー可能なコマンドブロックとして出力する。ユーザーが「コミットするコマンドを示して」「配置手順を教えて」「GitHub にコミットしたい」「番号付きの手順で」「コマンドラインをコピーできる形式で」と言ったときに従うこと。さらに重要な発火条件として、paper-repro 向けのファイルを create_file や str_replace で作成・修正したときは、ユーザーが求めなくても必ず同じ応答の中で present_files による提示と、配置・コミット・確認の手順まで続けること。ファイルを作って説明だけで終えてはならない。提示しなければユーザーはダウンロードできず、手順がなければ配置できないためである。zip の展開方式、配置後の取り違えの検証、Conventional Commits 形式の英語コミットメッセージ、プッシュ後の確認 URL までを含む。確認 URL には、変更後のファイルやフォルダに加えて、今回のコミットの差分を見る commit ログの URL を必ず含める。コミット SHA は Claude 側では分からないため、コミットのブロックに git log でSHAを表示するコマンドを組み込み、ユーザーがその値を URL に差し込む形で案内する。確認 URL は1つずつ別ブロックにして、コピーボタンでそのままブラウザへ貼れる形にする。コミットメッセージの本文は2〜3文かつ50語以内に収め、1文は20語程度にとどめる。差分やコミットした文書に書いてあることを繰り返さない。paper-repro 以外のプロジェクト（Processloop は processloop-commit-steps を使う）や、Linux/macOS 環境の手順には使わない。
---

# paper-repro 配置・コミット手順の出力形式

## 変更履歴

| 版 | 変更内容 |
| --- | --- |
| 1.1 | 確認 URL に commit ログの URL を追加（第「確認 URL」章）。SHA の入手をコミットのブロックへ組み込む規約を追加 |
| 1.0 | 初版。`processloop-commit-steps` の規約を `paper-repro` の前提へ移した |

## ★ 発火条件 — ファイルを作ったら必ず提示と手順まで続ける

`paper-repro` 向けのファイルを作成・修正したら、**ユーザーが求めなくても**
同じ応答の中で提示と手順まで続ける。

### 応答を終える前の確認

| 欠けているもの | ユーザーに起きること |
| --- | --- |
| `present_files` による提示 | **ダウンロードできない** |
| 番号付きの配置・コミット手順 | 自分でパスを調べることになる |
| 確認 URL | 反映されたか確かめられない |

### 手順を省いてよい場合

- ファイルを作らず、説明や検証だけで終わるとき
- ユーザーが明示的に「手順は不要」と言ったとき

### 応答の構成

```
1. 何をしたかの説明（簡潔に）
2. 判断の根拠・注意点
3. present_files による提示
4. 番号付きの配置・コミット手順
5. 確認 URL
```

## 適用範囲

`paper-repro` プロジェクトで、Claude が作成したファイルをユーザーの Windows 環境に配置し、
GitHub へコミット・プッシュするまでの手順を示すときに使う。

**環境の前提**

| 項目 | 値 |
| --- | --- |
| リポジトリ | `C:\Users\kazuy\projects\paper-repro` |
| GitHub | `https://github.com/ChestnutForest/paper-repro` |
| シェル | Windows PowerShell 5.1 |
| ダウンロード先 | `C:\Users\kazuy\Downloads` |
| 出力 zip 名 | `files_reify_YYYYMMDD_hhmm.zip`（**JST 基準**） |
| バックエンド | Python 3.13 / FastAPI（`backend/.venv`） |
| フロントエンド | Next.js（`frontend/`） |

⚠️ **仮想環境が有効なターミナルでも Git 操作はできる。** プロンプトに `(.venv)` が
付いていても問題ない。無効化を促さない。

---

## 出力の原則

### 1. 番号ごとに1ブロック

**1つの番号に対してコマンドブロックは1つだけ**にする。
関連するコマンドは同じブロックにまとめ、コピーして一度に貼れる形にする。

````markdown
## 3. 配置

```powershell
Copy-Item "$tmp\docs\arch-guide\arc-screen.md" ".\docs\arch-guide\" -Force
Copy-Item "$tmp\docs\worknotes\reflection.md" ".\docs\worknotes\" -Force
```
````

**やってはいけないこと**

- 1つの番号の中でブロックを分割する（コピーの手間が増える）
- 1行ずつ別ブロックにする
- 説明文をブロックの間に挟んで分断する

### 2. 番号の粒度

工程の区切りで分ける。目安は6〜9番程度。

| 番号 | 典型的な内容 |
| --- | --- |
| 1 | ルートへ移動、zip の展開 |
| 2 | 展開結果の確認 |
| 3 | 配置（フォルダ作成を含む） |
| 4 | `git status` と差分の確認 |
| 5 | 手編集が必要な場合（該当時） |
| 6 | コミットとプッシュ |
| 7 | 片付け |
| 8 | 確認 URL（**commit ログを先頭に**） |

⚠️ **Processloop より番号が少ない。** `paper-repro` は `README.md` が
ルートと `docs/` の2箇所だけで、退避方式を要する場面が少ないためである。

### 3. 各番号に見出しを付ける

`## 3. 配置` のように、何をする段階か一目で分かる見出しにする。

---

## 展開と配置

### 基本形

zip 名と展開先を変数に置き、以降で使い回す。

```powershell
cd C:\Users\kazuy\projects\paper-repro
$zip = "$HOME\Downloads\files_reify_YYYYMMDD_hhmm.zip"
$tmp = "$HOME\Downloads\<用途>-tmp"
Expand-Archive -Path $zip -DestinationPath $tmp -Force
```

**`$tmp` の名前は用途が分かるものにする**（`scr-tmp`、`beh-tmp` など）。
毎回同じ名前にすると、前回の残骸と混ざる。

### 展開結果の確認を必ず入れる

配置の前に、独立した番号として入れる。

```powershell
Get-ChildItem $tmp -Recurse -File | Select-Object FullName
```

**これを省くと、空の `$tmp` に気づかないまま `Copy-Item` が失敗し、
`git status` に何も出ない状態で混乱する。** 実際に起きた。

### フォルダが無い場合

配置先が存在しないときは、同じブロックで作る。

```powershell
New-Item -ItemType Directory -Force -Path ".\docs\worknotes"
Copy-Item "$tmp\docs\worknotes\*.md" ".\docs\worknotes\" -Force
```

---

## 取り違えの検証ブロック

配置後、独立した番号として必ず入れる。

```powershell
git status
git diff --stat
```

**差分の行数を見て、想定と合うか確かめるよう促す。**

⚠️ **長文ファイルを全文差し替えたときは特に注意する。** 実際に、
517行の文書を差し替えて **141行の差分**が出た。内容は同じでも、
改行位置・表の桁揃え・末尾スラッシュが変わっていた。

意図した変更が数行なのに差分が数十行を超えたら、**元ファイルを受け取って
該当箇所だけ置換する方式に切り替える。**

---

## コマンド作成時の注意

### エンコーディング

⚠️ **日本語を含む PowerShell スクリプトを作らない。**
UTF-8 のファイルを PowerShell 5.1 が Shift-JIS として読み、文字化けする。
ヒアストリング（`@' ... '@`）の中に日本語の表があると、
Markdown の `| --- |` がパイプ演算子として解釈され、構文エラーになる。

**実際に起きた失敗である。** 追記を自動化しようとして破綻した。
**手作業での編集を案内するほうが確実である。**

### ファイル作成

`.env` のようなドット始まりのファイルは、メモ帳で作ると `.env.txt` になる。

```powershell
Copy-Item .env.example .env
```

### 手編集が必要な場合

コマンドで完結しないときは、番号を分けて明示する。

````markdown
## 5. 既存文書の1行を修正

`docs/arch-guide/arc-screen.md` を開き、第9章の表の次の行を置き換えてください。

**変更前**

```markdown
| 2 | システム振舞い | `arc-behavior.md` | ⬜ |
```

**変更後**

```markdown
| 2 | システム振舞い | [`arc-behavior.md`](arc-behavior.md) | 🔨 枠組み作成中 |
```
````

**表の桁揃えは元のファイルに合わせるよう添える。**

---

## コミットメッセージ

### 形式

Conventional Commits に従う。`git add` `git commit` `git push` は同じブロックにまとめる。

| 型 | 用途 |
| --- | --- |
| `feat` / `fix` | 機能の追加 / 不具合の修正 |
| `docs` / `test` | ドキュメント / テスト |
| `refactor` / `chore` | 挙動を変えない整理 / 設定・依存 |

スコープは `docs(arch-guide):` のように付ける。

### ★ 長さの上限

| 部分 | 上限 |
| --- | --- |
| 件名 | 50字程度。命令形 |
| 本文 | **2〜3文。50語以内** |
| 1文 | 20語程度 |

**文数が範囲内でも、1文が長ければ守っていない。**

### 何を書き、何を書かないか

判断の基準は「**差分を見ても分からないか**」の一点にある。

| 書く | 書かない |
| --- | --- |
| なぜこの変更が必要になったか | 何を書いたか（差分で分かる） |
| 却下した案と、その理由 | コミットした文書に既にある説明 |
| 後で問題になりそうな判断 | 仕様の件数、行数、章の数 |

⚠️ **ドキュメントのコミットで、その文書の内容を要約しない。**
読み手は文書そのものを開ける。答えるべきは「なぜ今これを書いたのか」である。

### 良い例

```
docs(arch-guide): verify screen design against primary sources

The v0.1 framework was written without the source PDFs. Reading them
confirmed no errors but revealed six omitted concerns, including the
cross-artifact consistency chapter that the predecessor guide had.
```

**2文・約35語。** 検証した理由と、その結果だけを述べている。

### その他

**英語で書く。** 箇条書きにしない。ファイル名を列挙しない。

`git add` は**対象を明示指定する。** `git add .` は作業メモを巻き込む。

### ★ SHA の表示をブロックに組み込む

**コミットのブロックの末尾に `git log --oneline -1` を必ず入れる。**
確認 URL で commit ログを開くために SHA が要るが、
**Claude は push 後の SHA を知らない。** ユーザーが自分で取得できるようにする。

```powershell
git add docs/arch-guide/arc-screen.md docs/worknotes/reflection.md
git commit -m "docs(arch-guide): ..." -m "..."
git push
git log --oneline -1
```

⚠️ **`git log` を別の番号に分けない。** コミットと同じブロックに置くことで、
一度の貼り付けで SHA まで得られる。

---

## 片付け

コミットの後、独立した番号として入れる。

```powershell
Remove-Item -Recurse -Force $tmp
```

**作業メモをリポジトリに置かない方針の場合は、ここで削除する。**
ただし `paper-repro` では `docs/worknotes/` へコミットする方針である
（2026-08-23 の決定）。**削除するのは `$tmp` だけにする。**

---

## 確認 URL

最後の番号として、GitHub の確認先を示す。

### ★ 必ず含める2種類

| 種類 | 用途 |
| --- | --- |
| **commit ログ** | **今回の変更だけを差分で見る。最初に置く** |
| 変更後のファイル | 描画や表示を確認する |

**commit ログを先に置く。** 何が変わったかを差分で見るのが先で、
描画の確認は後である。順序が逆だと、変更点を把握しないまま個別ファイルを開くことになる。

### commit ログの URL

| 見たいもの | URL の形 |
| --- | --- |
| **今回のコミットの差分** | `.../commit/<SHA>` |
| コミット履歴（全体） | `.../commits/main` |
| 特定ファイルの変更履歴 | `.../commits/main/<path>` |
| 2コミット間の差分 | `.../compare/<A>...<B>` |

**基本は1つ目である。** 残り3つは、履歴を追いたいときや複数コミットにまたがるときに使う。

### ⚠️ SHA が分からない場合の書き方

**Claude は push 後の SHA を知らない。** 推測で書いてはならない。
コミットのブロックに組み込んだ `git log --oneline -1` の出力を使うよう案内する。

**正しい形**

````markdown
## 7. 確認 URL

**今回のコミットの差分**

手順5で表示された SHA を、次の URL の末尾に差し込んでください。

```
https://github.com/ChestnutForest/paper-repro/commit/
```

**画面編の設計（v0.2）**

```
https://github.com/ChestnutForest/paper-repro/blob/main/docs/arch-guide/arc-screen.md
```
````

**やってはいけない形**

````markdown
```
https://github.com/ChestnutForest/paper-repro/commit/abc1234
```
````

⚠️ **`abc1234` のような架空の SHA を書かない。** 実在しない URL は 404 になり、
ユーザーが自分で SHA を調べ直すことになる。**末尾を空けて差し込ませるほうが速い。**

### SHA が分かっている場合

会話の中でユーザーが `git log` の出力を貼ってくれたときや、
過去のコミットを参照するときは、**実在する SHA を使って完全な URL を書く。**

```
https://github.com/ChestnutForest/paper-repro/commit/4551722
```

### ★ URL は1つずつ別ブロックにする

**複数の URL を1つのブロックにまとめない。** ブラウザのアドレスバーに貼るとき、
まとめてあると1件ずつ選び直す手間が生じる。1ブロック1URL にすれば、
コピーボタンを押してそのまま貼れる。

コマンドブロックは番号ごとに1つにまとめる原則と、ここだけ扱いが逆になる。
理由は用途の違いにある。コマンドは順に実行するため一括が速く、
URL は1件ずつブラウザへ移すため個別のほうが速い。

**正しい形**

````markdown
## 8. 確認 URL

**画面編の設計（v0.2）**

```
https://github.com/ChestnutForest/paper-repro/blob/main/docs/arch-guide/arc-screen.md
```

**検証の記録**

```
https://github.com/ChestnutForest/paper-repro/blob/main/docs/worknotes/reflection-arc-screen-v02.md
```
````

**やってはいけない形**

````markdown
```
https://github.com/.../a.md
https://github.com/.../b.md
```
````

### 各 URL に見出しを添える

何のファイルか、太字の見出しで示す。URL だけを並べない。

### 何を見てほしいか書く

Mermaid の図を含むなら描画を、表を含むなら崩れていないかを確認するよう促す。

### URL の数が多い場合

5件を超えるときは、**最も確認すべきもの3件程度に絞る。**
残りはフォルダの URL で代替する。

```
https://github.com/ChestnutForest/paper-repro/tree/main/docs/arch-guide
```

---

## やってはいけないこと

- ❌ ファイルを作って `present_files` を呼ばずに終える
- ❌ 手順を示さずに「コミットしてください」とだけ書く
- ❌ 1つの番号でブロックを分割する
- ❌ 複数の URL を1ブロックにまとめる
- ❌ **確認 URL に commit ログを含めない**（何が変わったか差分で見られない）
- ❌ **架空のコミット SHA を書く**（404 になる。末尾を空けて差し込ませる）
- ❌ **`git log --oneline -1` を別の番号に分ける**（コミットと同じブロックに置く）
- ❌ 日本語を含む PowerShell スクリプトで自動化する
- ❌ `git add .` を使う（作業メモを巻き込む）
- ❌ コミットメッセージで、コミットした文書の内容を要約する
- ❌ 展開結果の確認を省く

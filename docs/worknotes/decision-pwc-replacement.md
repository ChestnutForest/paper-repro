# 決定記録：Papers with Code 終了への対応

- 対象プロダクト: `paper-repro`
- 文書種別: 設計判断の記録
- 決定日: 2026年8月31日
- 契機: [`../arch-guide/arc-interface-list.md`](../arch-guide/arc-interface-list.md) 作成時の公式仕様調査
- 影響先: [`../product-design.md`](../product-design.md) 201行、`IF-03`

---

## 1. 何が起きたか

`product-design.md` 201行は、実装探索の接続先を次のように定めている。

> 第1パス要約 + タイプ判定 + 実装探索（**GitHub/PwC/OpenReview**）をジョブ実行

**このうち PwC（Papers with Code）は、2025年7月に Meta が終了させた。**
ドメインは Hugging Face の Trending Papers へリダイレクトされ、リーダーボードは失われている。

**設計が成立しない状態にある。**

## 2. PwC に何を期待していたか

`product-design.md` の記述は「実装探索」である。PwC が提供していた機能のうち、
`paper-repro` が必要としていたのは**論文と公式実装の紐付け**だけである。

| PwC の機能 | `paper-repro` での必要性 |
| --- | --- |
| **論文 ⇔ 公式実装の紐付け** | **必要**（`REQ-C05-S01`） |
| ベンチマークのリーダーボード | 不要 |
| SOTA スコアの追跡 | 不要 |

⚠️ **失われた機能のうち、必要なのは1つだけである。** 代替を探す範囲もそこに限られる。

### 2.1 ⚠️ この判断の前提

**リーダーボードと SOTA 追跡を不要としたのは、比較機能を要求としないためである。**

利用者は既に「この論文を読みたい」と決めて arXiv URL を投入する。
**論文を選ぶ段階が製品の外にある**ため、複数論文を比較する場面が現状は無い。

将来、第三者の再現結果と比較したくなる可能性は記録した
（[`pending-sota-comparison.md`](pending-sota-comparison.md)）。
**その案が要求になれば、本決定の前提が変わる。**

## 3. 検討した選択肢

| 案 | 内容 | 評価 |
| --- | --- | --- |
| A | 実装探索を GitHub と OpenReview の2つに減らす | 紐付けの情報源が減る |
| B | **Hugging Face Papers API へ差し替える** | **採用** |
| C | CodeSOTA へ差し替える | 第三者サービス。継続性が不明 |
| D | 凍結アーカイブ（paperswithcode-data）を使う | 更新されない。新しい論文に対応できない |

### 3.1 案Bを採用する理由

Hugging Face Papers API は、次の点で `paper-repro` の用途に合う。

| 観点 | 内容 |
| --- | --- |
| **提供する情報** | 著者、リンクされた models/datasets/spaces、**GitHubリポジトリURL**、プロジェクトページ |
| **引き方** | **arXiv ID で直接引ける**（`paper-repro` は arXiv URL が起点） |
| 対象範囲 | arXiv の AI/CS 論文。Hugging Face 上のリンクの95%が arXiv |
| 索引の仕組み | model card や README に arXiv URL があると**自動で索引される** |
| 認証 | 読み取りは不要 |
| 提供元 | Hugging Face 本体。第三者ではない |

**arXiv ID で直接引ける点が決め手である。** `IF-01` で取得した arXiv ID を、
そのまま `IF-03` の入力にできる。追加の名寄せが要らない。

### 3.2 案Aを採らない理由

GitHub の検索だけでは、**論文と実装の対応が保証されない。** 論文名で検索して
似た名前のリポジトリが見つかっても、それが公式実装とは限らない。

`REQ-C07-S01`（情報源の種類と時点）と `BR-10`（推測で埋めない）に従えば、
**紐付けの根拠がある情報源**を持つ方がよい。

### 3.3 案C・Dを採らない理由

- **CodeSOTA**：第三者が PwC の後継を名乗るサービスである。継続性を判断する材料がない。
- **凍結アーカイブ**：2025年7月以降の論文に対応できない。`paper-repro` は新しい論文も扱う。

## 4. 決定

**`IF-03` の接続先を Papers with Code から Hugging Face Papers API へ差し替える。**

| 項目 | 変更前 | 変更後 |
| --- | --- | --- |
| 外部システム | `EX-03` Papers with Code | `EX-03` **Hugging Face** |
| インタフェース名 | 公式実装の探索（PwC） | **論文と実装の紐付けの取得** |
| 状態 | 要判断 | **採用** |
| エンドポイント | — | `https://huggingface.co/api/papers/{arxiv_id}` |
| 認証 | — | 不要 |
| 課金 | — | 無償 |

### 4.1 ⚠️ 制約として記録すること

| 制約 | 内容 |
| --- | --- |
| **索引の網羅性** | **全論文が索引されているわけではない。** 見つからない場合がある |
| **紐付けの依存** | GitHubリポジトリの紐付けは、著者または利用者の登録に依存する |
| 対象分野 | AI/CS が中心。他分野は手薄な可能性がある |

⚠️ **「見つからない」を「実装が存在しない」と解釈しない。** `BR-10` に従い、
**未索引と実装なしを区別する。** これは `IF-04`（OpenReview）の空結果問題と同じ性質である。

## 5. 影響範囲

| 対象 | 変更 |
| --- | --- |
| [`../arch-guide/arc-interface-list.md`](../arch-guide/arc-interface-list.md) | `EX-03`・`IF-03` の記述。1.1節の「要判断」を解消 |
| [`../arch-guide/arc-interface-map.md`](../arch-guide/arc-interface-map.md) | `IF-03` の線を点線から実線へ。図とソースの両方 |
| [`../product-design.md`](../product-design.md) 201行 | 「GitHub/PwC/OpenReview」の記述 |

⚠️ **`product-design.md` の修正は本決定の範囲外とする。** 設計文書の正本であり、
実装方式の記述を含む。**別途の判断を要する。**

本決定では、外部インタフェース編の2文書のみを更新する。

## 6. 未確定の事項

- **Hugging Face API のレート制限。** 公式ドキュメントに明示が見当たらなかった。
  実装時に実測するか、問い合わせる。
- **索引率。** 対象論文のどれだけが索引されているかは未計測である。
  テスト論文（[`../test-papers.md`](../test-papers.md)）で確かめる。
- **比較機能を要求とするか。** 本決定は要求としない前提に立つ（2.1節）。
  記録は [`pending-sota-comparison.md`](pending-sota-comparison.md) にある。
- **GitHub 検索との併用。** `IF-02` と `IF-03` の役割分担。
  紐付けが得られない場合に GitHub 検索へ落とすかは未定。

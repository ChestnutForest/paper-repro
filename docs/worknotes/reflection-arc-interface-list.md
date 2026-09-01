# 外部IF一覧・関連図の作成記録

- 作成日: 2026年8月31日
- 対応する設計: [`../arch-guide/arc-interface-list.md`](../arch-guide/arc-interface-list.md)、
  [`../arch-guide/arc-interface-map.md`](../arch-guide/arc-interface-map.md)
- 状態: **記録・凍結**（2026年9月1日）。本書は外部IF一覧・関連図の作成時点の検証・判断の記録であり、設計へ反映すべき差分は持たない。以後更新しない。

---

## 外部システムの確定経路

業務説明からは導けなかった。経緯は次のとおり。

| 調査 | 結果 |
| --- | --- |
| `arc-behavior-list.md` の47業務 | 外部サービス名は `B-03-001` の1件のみ |
| `behaviors/*.md` の業務説明 | 3件ヒットしたが、いずれも外部連携の記述ではない |
| **`product-design.md`** | **185・201・281行に明記されていた** |

`behaviors/README.md` が「API、回数、閾値等が未決なら`未決`とし、設計側で補わない」と
定めており、**方針どおり書かれていない**状態だった。欠陥ではない。

## ⚠️ 調査で判明した重大な事実

### Papers with Code は2025年7月に終了している

`product-design.md` 201行は実装探索先に「GitHub/PwC/OpenReview」を挙げるが、
**PwC は Meta が終了させ、ドメインは Hugging Face へリダイレクトされている。**

一覧には `IF-03` として載せたが、**状態を「要判断」とした。**
削除するか代替へ差し替えるかは、要求または設計の変更にあたるため、承認が要る。

### arXiv に謝辞の文言義務がある

> Thank you to arXiv for use of its open access interoperability.

**製品への表示が求められている。** 画面編の対応が必要になる。
あわせて、arXiv のブランド名・ロゴ・配色を製品に使わないことも求められる。

### GitHub は認証の有無で83倍の差

未認証 60/時 に対し、認証すれば 5,000/時 である。
実装探索は1論文あたり複数回の呼び出しを要するため、**未認証では実用に耐えない。**

### OpenReview は誤りが検出されない

誤ったベースURL（v1/v2）や `invitation` 文字列を使っても、
**エラーではなく空の結果が返る。**

「結果ゼロ」を「該当なし」と解釈すると誤る。`BR-10`（`unknown` を推測で埋めない）に従い、
空の結果と取得失敗を区別する必要がある。

## 設計上の判断

### `EX-05` を「Claude API」と書かなかった

`product-design.md` 281行が「抽象化層で包む／他プロバイダ差替可／プロバイダ非依存に」と
定めている。**特定プロバイダ名で固定すると設計意図に反する。**

一覧・関連図とも「LLM プロバイダ」と表記した。

### 対応業務を推測で埋めなかった

`IF-01` を除き「未特定」とした。業務説明が具体化された段階で対応づける。
`behaviors/README.md` の方針に倣った。

### 承認を要する判断を分離した

一覧6章に、次の3件を分けて記した。

- PwC 終了への対応
- GitHub 認証の必須化
- 謝辞の文言の表示

**いずれも本書では決定しない。** 要求または設計の変更にあたるためである。

## 既存文書への追記

### 1. `docs/README.md`（索引）

`arc-interface.md` の行の直後へ2行追加する。

```markdown
| [`arch-guide/arc-interface-list.md`](arch-guide/arc-interface-list.md) | **外部IF一覧**。5外部システム・6インタフェース。レート制限、課金、失敗時の影響、代替の可否 |
| [`arch-guide/arc-interface-map.md`](arch-guide/arc-interface-map.md) | **外部システム関連図**。依存の強さと、止まったときに何が進まないか |
```

### 2. ルート `README.md`（進捗表）

外部インタフェースの行を更新する。

**変更前**

```markdown
| 外部インタフェース | ✅ [v0.1](docs/arch-guide/arc-interface.md) | ⬜ | — | ⬜ | ⬜ |
```

**変更後**

```markdown
| 外部インタフェース | ✅ [v0.1.2](docs/arch-guide/arc-interface.md) | ✅ [v0.1](docs/arch-guide/arc-interface-list.md) | — | ✅ [関連図 v0.1](docs/arch-guide/arc-interface-map.md) | ⬜ **← 次の一手** |
```

⚠️ **共通ルール列は「—」のままとする。** 本編に共通ルールの成果物は無く、
`arc-behavior-rules.md` へ `BR-13` を追記する形になる（未着手）。

---

## 次の作業

| 順 | 作業 |
| --- | --- |
| 1 | **一覧6章の判断を仰ぐ**（PwC、GitHub認証、謝辞の表示） |
| 2 | `arc-behavior-rules.md` へ `BR-13` を追記 |
| 3 | `interfaces/` の項目説明・処理説明 |

**1が先である。** PwC の扱いが決まらないと、`IF-03` の項目説明を書けない。

# 決定記録：arXiv 謝辞の文言と表示箇所

- 対象プロダクト: `paper-repro`
- 文書種別: 設計判断の記録
- 決定日: 2026年9月1日
- 契機: [`../arch-guide/arc-interface-list.md`](../arch-guide/arc-interface-list.md) 6章の未決事項
- 影響先: 画面編（`arc-screen-rules.md`）、`IF-01`

---

## 1. 何が求められているか

arXiv は API 利用者に対し、**製品への謝辞の表示**を求めている。

> Acknowledge arXiv data usage with this statement on your product

⚠️ **`on your product`** とある。ドキュメントではなく**製品そのもの**への表示である。

## 2. ⚠️ 文言は2文である

調査の結果、**これまで記録していた文言は不完全であった。**

| 出典 | 文言 |
| --- | --- |
| API Access ページ | 第1文のみ |
| **Brand Use Guidelines** | **第1文＋第2文** |

Brand Use Guidelines は `on your product` として次を示している。

```
Thank you to arXiv for use of its open access interoperability.
This [service/product] was not reviewed or approved by, nor does it
necessarily express or reflect the policies or opinions of, arXiv.
```

### 2.1 第2文が重要である

第2文は「**arXiv による審査も承認も受けておらず、arXiv の方針や見解を表すものでもない**」という否認である。

**第1文だけでは、arXiv が関与しているように読まれうる。** `paper-repro` は
論文を読解・再現するツールであり、arXiv の見解と誤解されると問題が生じる。

**両方を表示する。**

### 2.2 採用する文言

`[service/product]` を `service` に置き換える。

```
Thank you to arXiv for use of its open access interoperability.
This service was not reviewed or approved by, nor does it necessarily
express or reflect the policies or opinions of, arXiv.
```

⚠️ **原文のまま表示する。翻訳しない。** 否認の効力は原文にある。
多言語化の対象外とする（`BR-07` の例外）。

## 3. `paper-repro` は独立プロジェクトに該当する

arXiv は、次の4条件をすべて満たすプロジェクトを **entirely independent** として扱う。

| # | 条件 | `paper-repro` |
| --- | --- | --- |
| 1 | 公開APIを使う | ✅ arXiv API のみ |
| 2 | arXiv の支援を必要としない | ✅ |
| 3 | **名称・ロゴ・URL・配色を使わない** | ✅ 使わない（4章） |
| 4 | 無償・オープンアクセス、または研究・教育目的 | ✅ MITライセンス、研究目的 |

**4条件を満たすため、arXiv との関係は生じない。** 謝辞の表示だけが求められる。

## 4. ロゴは使わない

Brand Use Guidelines は、**API利用だけではロゴ使用は通常許諾されない**としている。

> Typically logo usage beyond the above is not granted for API use.

例外として、arXiv の PDF や abstract ページへ**直接リンクする場合**は使用できる。

| 条件 | 内容 |
| --- | --- |
| 幅 | 50〜100px（ロゴマークは15px以上） |
| 目的 | **リンクのためであり、ブランディングではない** |
| 動作 | **必ず arXiv へリンクする** |

`paper-repro` は論文へリンクするため、使用の余地はある。**しかし使わない。**

理由は、3章の条件3（名称・ロゴを使わない）を満たし続けることで、
**独立プロジェクトの立場を保てる**ためである。ロゴを使えば、サイズや配置の制約が加わり、
将来のブランド指針の変更にも追随する必要が生じる。

⚠️ **`arXiv` という名称も、ブランドとして使わない。** 論文の出典を示す文脈
（「arXiv から取得した」「arXiv URL を入力」）は情報の記述であり、ブランド利用ではない。
**製品名やロゴ的な扱いをしない**という意味である。

## 5. 表示箇所

| 箇所 | 表示 | 理由 |
| --- | --- | --- |
| **全画面のフッタ** | **常時** | `on your product` の要求を満たす最小構成 |
| 論文を表示する画面 | フッタで足りる | 個別画面への追加は不要 |
| 出力する成果物（zip、レポート） | **含める** | 製品の一部として配布されるため |
| リポジトリの README | 任意 | 製品ではないが、記載してよい |

### 5.1 フッタとする理由

**全画面に出る場所が1箇所あれば足りる。** 個別画面ごとに置くと、
画面編の共通ルール（`arc-screen-rules.md`）の「ページの構成要素」と衝突する。

⚠️ **画面編の共通ルールへ追記が必要である。** フッタの構成要素として定める。
本決定では外部インタフェース編のみを更新し、**画面編の変更は別途とする。**

### 5.2 成果物へ含める理由

照合レポートや zip は、**製品が生成して利用者が持ち出すもの**である。
arXiv 由来のデータを含むため、`on your product` の範囲に入ると解する。

## 6. 影響範囲

| 対象 | 変更 | 本決定の範囲 |
| --- | --- | --- |
| [`../arch-guide/arc-interface-list.md`](../arch-guide/arc-interface-list.md) | 文言を2文へ修正。6章の未決を解消 | ✅ 含む |
| `arc-screen-rules.md` | フッタの構成要素へ謝辞を追加 | ⬜ **別途** |
| 成果物の生成処理 | レポート・zip へ文言を含める | ⬜ 実装時 |

## 7. 未確定の事項

- **フッタの具体的な配置。** 画面編の判断。
- **成果物への含め方。** レポートの末尾か、別ファイルか。実装時に決める。
- **他の外部システムの謝辞。** GitHub、Hugging Face、OpenReview に同様の要求があるかは未確認。

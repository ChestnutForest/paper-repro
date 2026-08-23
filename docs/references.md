# 参考文献

- 対象プロダクト: `paper-repro`
- 位置づけ: 要件検討で一次資料として用いた文献の書誌情報を一元管理する
- 作成日: 2026年8月23日

各分析文書は本ファイルの**短縮形**（著者・書名・出版社・発行年）で引用する。
版、ページ数、ISBN、入手先などの詳細は本ファイルだけに置き、各文書へ重複させない。

---

## 引用の方針

- 一次資料は**要約と言い換え**で扱い、本文をそのまま転載しない。
- 章・節のタイトルは、**参照箇所を特定する目的にのみ**用いる。
- 図表、数式、コードは複製せず、出典を示して参照先を案内する。
- 分析文書に書く示唆は、一次資料の記述そのものではなく、`paper-repro` への適用として書き起こす。

---

## 書誌一覧

| 略号 | 短縮形（各文書での表記） | 書誌 |
|---|---|---|
| REF-01 | 菊田遥平『原論文から解き明かす生成AI』技術評論社, 2025 | 菊田遥平『原論文から解き明かす生成AI』技術評論社、2025年8月18日、304ページ、B5変形判、ISBN 978-4-297-15078-5（電子版 ISBN 978-4-297-15079-2）。書誌情報: https://gihyo.jp/book/2025/978-4-297-15078-5 |
| REF-02 | 角居雄太「論文再現実装ハンズオン #4 対照学習」DL COMMUNITY, 松尾・岩澤研究室, 東京大学, 2026 | 角居雄太「論文再現実装ハンズオン #4 対照学習」DL COMMUNITY、松尾・岩澤研究室、東京大学、2026年。講義解説資料。 |
| REF-03 | Chen et al., *Proc. 37th ICML*, 2020 | Chen, T.; Kornblith, S.; Norouzi, M.; Hinton, G. "A Simple Framework for Contrastive Learning of Visual Representations." *Proceedings of the 37th International Conference on Machine Learning*, 2020, 1597–1607. https://doi.org/10.48550/arxiv.2002.05709 |

---

## 略号ごとの利用箇所

| 略号 | 利用している文書 |
|---|---|
| REF-01 | [`requirements-update-workflow.md`](requirements-update-workflow.md)、[`requirements-change-proposal.md`](requirements-change-proposal.md)、[`requirements-decisions/batch-03-options.md`](requirements-decisions/batch-03-options.md)、[`requirements-analysis/`](requirements-analysis/) の `section-1.2*.md` 各文書 |
| REF-02 | [`requirements-analysis/simclr-handson-deck.md`](requirements-analysis/simclr-handson-deck.md) |
| REF-03 | [`requirements-analysis/simclr-handson-deck.md`](requirements-analysis/simclr-handson-deck.md)（REF-02 が解説する原典） |

---

## 文献を追加するときの手順

1. 本ファイルの書誌一覧へ、略号・短縮形・書誌の3列を追記する。
2. 発行元の公式ページなど、**一次情報の URL** を書誌に含める。二次的な紹介記事は使わない。
3. 分析文書側は短縮形だけで引用し、書誌の詳細は本ファイルへ参照させる。
4. 「略号ごとの利用箇所」へ、その文献を使う文書を追記する。

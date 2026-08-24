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
| REF-04 | University of Sussex「Academic and Research Skills MAIED (883X4)」2025 | University of Sussex, "Academic and Research Skills MAIED (883X4)", Postgraduate module, 2025/26. 修士（Level 7）60単位の通年科目。https://www.sussex.ac.uk/study/modules/postgraduate/2025/101236-academic-and-research-skills-maied （2026年8月23日閲覧） |
| REF-05 | University of Kent「Academic and Research Skills (ANTS3080)」 | University of Kent, "Academic and Research Skills - ANTS3080", Module page. 人類学・環境科学系の学部科目。**2023/24年度は開講していない旨がページに明記されている**。https://www.kent.ac.uk/courses/modules/module/ANTS3080 （2026年8月23日閲覧） |
| REF-06 | University of Galway「Reading and Research Skills」 | University of Galway, "Reading and Research Skills", Academic Skills. https://www.universityofgalway.ie/academic-skills/readingandresearch/ （2026年8月23日閲覧） |
| REF-07 | SCONUL「Seven Pillars of Information Literacy: Core Model」2011 | SCONUL Working Group on Information Literacy, "The SCONUL Seven Pillars of Information Literacy: Core Model for Higher Education", 2011. Research Lens を含む。https://www.sconul.ac.uk/page/seven-pillars-of-information-literacy （2026年8月23日確認） |
| REF-08 | ACRL「Framework for Information Literacy for Higher Education」2015 | Association of College and Research Libraries, "Framework for Information Literacy for Higher Education", ACRL理事会承認 2015年2月2日。6つのフレームで構成。https://www.ala.org/acrl/standards/ilframework （2026年8月23日確認） |
| REF-09 | Vitae「Researcher Development Framework」 | Vitae (CRAC), "Researcher Development Framework". 2010年版は4ドメイン・12サブドメイン・63記述子。**2025年改訂版へ移行中で両版が併存する**。https://vitae.ac.uk/vitae-researcher-development-framework/ （2026年8月23日確認） |
| REF-10 | ACM「Artifact Review and Badging」Version 1.1, 2020 | Association for Computing Machinery, "Artifact Review and Badging - Version 1.1", 2020年8月24日. https://www.acm.org/publications/policies/artifact-review-and-badging-current （2026年8月23日に本文を確認） |
| REF-11 | Pineau et al., *JMLR* 22, 2021 | Pineau, J. et al. "Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)." *Journal of Machine Learning Research*, 22, 2021. https://jmlr.org/papers/volume22/20-303/20-303.pdf （2026年8月23日確認） |
| REF-12 | Wilkinson et al., *Scientific Data* 3, 160018, 2016 | Wilkinson, M. D. et al. "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data*, 3, 160018, 2016. 15の原則からなる。https://doi.org/10.1038/sdata.2016.18 （2026年8月23日確認） |
| REF-13 | CRediT (Contributor Roles Taxonomy), ANSI/NISO, 2022 | National Information Standards Organization, "CRediT (Contributor Roles Taxonomy)", ANSI/NISO標準として2022年承認。14の貢献役割。CC BY 4.0。https://credit.niso.org/ （2026年8月23日確認） |
| REF-14 | ALLEA「The European Code of Conduct for Research Integrity」2023年改訂版 | ALLEA (All European Academies), "The European Code of Conduct for Research Integrity", Revised Edition 2023. 欧州委員会がEU資金研究の第一基準として認める。https://allea.org/code-of-conduct/ （2026年8月23日確認） |
| REF-03 | Chen et al., *Proc. 37th ICML*, 2020 | Chen, T.; Kornblith, S.; Norouzi, M.; Hinton, G. "A Simple Framework for Contrastive Learning of Visual Representations." *Proceedings of the 37th International Conference on Machine Learning*, 2020, 1597–1607. https://doi.org/10.48550/arxiv.2002.05709 |

---

## 略号ごとの利用箇所

| 略号 | 利用している文書 |
|---|---|
| REF-01 | [`requirements-update-workflow.md`](requirements-update-workflow.md)、[`requirements-change-proposal.md`](requirements-change-proposal.md)、[`requirements-decisions/batch-03-options.md`](requirements-decisions/batch-03-options.md)、[`requirements-analysis/`](requirements-analysis/) の `section-1.2*.md` 各文書 |
| REF-02 | [`requirements-analysis/simclr-handson-deck.md`](requirements-analysis/simclr-handson-deck.md) |
| REF-03 | [`requirements-analysis/simclr-handson-deck.md`](requirements-analysis/simclr-handson-deck.md)（REF-02 が解説する原典） |
| REF-04〜REF-06 | [`requirements-analysis/academic-research-skills.md`](requirements-analysis/academic-research-skills.md) |
| REF-07〜REF-14 | [`requirements-analysis/academic-research-skills-frameworks.md`](requirements-analysis/academic-research-skills-frameworks.md) |

---

## 採用しなかった資料

一次資料として検討したが、書誌一覧へ載せなかったもの。同じ資料を再検討する手間を省くために記録する。

| 資料 | 不採用の理由 |
|---|---|
| `dl.icdst.org` 上の「Academic and Research Skills Handbook」PDF | 出所不明のファイルホストにあり、発行主体と権利関係を確認できない |
| 生成AIによる「Academic and Research Skills」の解説回答 | 二次資料。一次資料の所在を知る手がかりとしてのみ用い、記述そのものは引用しない |

---

## 文献を追加するときの手順

1. 本ファイルの書誌一覧へ、略号・短縮形・書誌の3列を追記する。
2. 発行元の公式ページなど、**一次情報の URL** を書誌に含める。二次的な紹介記事は使わない。
3. 分析文書側は短縮形だけで引用し、書誌の詳細は本ファイルへ参照させる。
4. 「略号ごとの利用箇所」へ、その文献を使う文書を追記する。

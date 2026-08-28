# 論文英語の定型表現デコーダ（実装者向け）

Phase 1（仕様抽出リーディング）で使う。論文の英語は文学ではなく**符牒**である。
実装者にとって意味を持つ表現を、「それを読んだら何をすべきか」に翻訳したもの。

---

## 1. 工数が激減するシグナル（見つけたら喜ぶ）

| 表現 | 実装上の意味 | やること |
|---|---|---|
| `Following [Doe et al., 2023], we ...` | その論文の実装をそのままコピーせよという指示 | 引用先のコードを探す。**最強の手抜きポイント** |
| `We use the same architecture as X, except ...` | `except` 以降が唯一の差分 | Xの実装を土台にし、except節だけがΔ |
| `We build upon the official implementation of X` | 公式実装が存在する | 即座に探す。Phase 0に戻る |
| `is a standard <...>` / `we adopt the standard ...` | 車輪の再発明をするなという合図 | 既存ライブラリを使う |
| `We follow the standard protocol of X` | 評価コードも既存のものがある | 評価スクリプトを流用 |

---

## 2. 危険なシグナル（バグと再現失敗の温床）

| 表現 | 実装上の意味 | やること |
|---|---|---|
| `For simplicity, we ...` | **論文の数式と実際のコードが乖離している箇所** | 数式ではなく、この文の記述に従う |
| `In practice, we find that ...` | 理論と実装が違う。著者が試行錯誤で見つけた調整 | 必ず実装に反映。省略すると再現しない |
| `We empirically set ...` | 根拠のないマジックナンバー | 仮定台帳（Phase 3）に「疑わしさ:高」で記録 |
| `appropriately` / `suitably` / `carefully tuned` | **値が書かれていない。** 最悪の表現 | 仮定台帳に「疑わしさ:高」。OpenReviewを漁る |
| `slightly modified` | 「slightly」は信用しない。重要な差分のことが多い | 何がどう modified なのか特定するまで進まない |
| `omitted for brevity` / `see Appendix X` | 本文から情報が抜かれている | **必ず追う。** Appendixが実装の本体 |
| `with minor implementation details` | 「minor」も信用しない | 同上 |

---

## 3. 評価まわりの罠

| 表現 | 実装上の意味 |
|---|---|
| `We report the best result over N runs` | 再現時に1回で同じ数字が出なくても正常。分散が大きい |
| `averaged over 3 seeds` | seedを変えて3回回す必要がある。1回の結果と比較してはいけない |
| `after hyperparameter search on the validation set` | 論文の数字は探索後のもの。素で回しても届かない |
| `we use the checkpoint with the best validation score` | early stopping相当の処理が必要 |
| `Results are not directly comparable` | ベースラインの数字を論文から転記してはいけない |

---

## 4. 数式節を読むときの姿勢

**理解しようとする前に、shapeを書く。**

論文の数式は添字が省略されがちで、そのままでは実装できない。次を必ず特定する。

- バッチ次元はどこか（数式では省略されていることが多い）
- 総和 `∑` はどの軸に対してか
- 正規化はどの軸で行うか
- 行列の積が「バッチ内の各サンプルごと」なのか「全体」なのか

例：`L = -log( exp(sim(z_i, z_j)/τ) / Σ_k exp(sim(z_i, z_k)/τ) )`
→ `z: [B, D]`、`sim`はcosine類似度で結果は `[B, B]`、`Σ_k` はdim=1、対角成分の扱いを確認 → 分母から自分自身を除くか否かが実装差になる（**仮定台帳行き**）。

---

## 5. 読まなくてよいもの

- **Related Work** — 実装には寄与しない。Phase 0で必要な引用は既に拾っている
- **Introduction の後半（貢献の箇条書き以外）** — マーケティング
- **Broader Impact / Limitations** — 実装には不要（ただし研究目的なら読む価値はある）
- **証明・定理の詳細** — 実装に必要なのは結論の式だけ。証明を追うのは実装が動いた後でよい

# ルート README への「設計工程の進捗」表の追加

- 作成日: 2026年8月28日
- 対象: リポジトリルートの `README.md`
- 状態: **反映済み・凍結**（2026年9月1日）
- 本書は提案時点の記録であり、以後更新しない。**設計工程の進捗の正本はルート `README.md` の該当表である。**
- 本書末尾の表は提案時の下書きで、現在の README とは一致しない。参照しないこと。
- 「なぜ必要か」で前提としたルート README のドキュメントリンク一覧は、2026年9月1日に削除した。
  文書の探索は [`../README.md`](../README.md)（ドキュメント索引）が担う。

---

## なぜ必要か

**現状、ルート README のドキュメントリンク一覧は既に漏れが出ている。**

| ファイル | README への掲載 |
| --- | --- |
| `arc-screen.md` | ✅ ある |
| `arc-behavior.md` | ❌ **漏れ** |
| `arc-artifact-order.md` | ❌ **漏れ** |

さらに根本的な問題として、**リンク一覧は「存在する」ことしか示さない。**
どこまで進んだかが分からないため、「常時、進捗状況を確認できる」状態になっていない。

## 方針

| 記述 | 扱い |
| --- | --- |
| **進捗表** | **ルート README に置き、md を作るたびに更新する** |
| ドキュメントのリンク一覧 | **`docs/README.md`（索引）に一本化する** |

ルート README のリンク一覧（約35行）は、索引と重複している。
**一覧を維持するのをやめ、進捗表に置き換える。**

---

## 追加する表

「### 進行中のフェーズ0の中身」の表と、その下の引用（`> **進捗の正本は…**`）の**間**に、
次の節を挿入する。

```markdown
### 📐 設計工程の進捗（IPA 6編）

**現在地: 現行確定要求について、データモデル編の4成果物と共通ルールを作成／ 全6編中 3 編**

詳細は **[`docs/arch-guide/arc-artifact-order.md`](docs/arch-guide/arc-artifact-order.md)**（作成順序の原則）を参照。

| 編 | 枠組み | 一覧 | 共通ルール | フロー・遷移 | 説明・レイアウト |
| --- | --- | --- | --- | --- | --- |
| 画面 | ✅ [v0.2.2](docs/arch-guide/arc-screen.md) | ✅ | ✅ | ✅ | ✅ 7画面 |
| **システム振舞い** | ✅ [v0.3](docs/arch-guide/arc-behavior.md) | ✅ [v0.2](docs/arch-guide/arc-behavior-list.md) | ✅ [v0.1](docs/arch-guide/arc-behavior-rules.md) | ✅ フロー・状態 v0.1 | ✅ 47業務 v0.1 |
| **データモデル** | ✅ [v0.2](docs/arch-guide/arc-datamodel-framework.md) | ✅ [17件・要求23/23](docs/arch-guide/arc-datamodel-list.md) | ✅ [v0.2](docs/arch-guide/arc-datamodel-rules.md) | ✅ ER v0.1・CRUD v0.2 | ✅ 定義v0.2・物理仕様v1.0 |
| 外部インタフェース | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| バッチ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 帳票 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

> **一覧が先である。** 詳細から書き始めると、完了を判定できず、粒度も揃わない。
> 根拠は [`docs/arch-guide/arc-artifact-order.md`](docs/arch-guide/arc-artifact-order.md) を参照。
```

## 削除を検討する箇所

「## ドキュメント」節のリンク一覧（約35行）のうち、**要求分析の各小節へのリンク19行**は、
`docs/README.md` と完全に重複している。

**次のように置き換えることを提案する。**

```markdown
- 要求分析資料（一次資料の小節別分析・19件）: [`docs/requirements-analysis/README.md`](docs/requirements-analysis/README.md)
```

19行が1行になり、**索引の二重管理が解消される。**

⚠️ **この削除は影響が大きいため、別コミットで行うこと。** 進捗表の追加を先に済ませ、
リンク一覧の整理はその後で判断する。

## 更新の運用

以後、md を作成・修正したら次を守る。

1. **進捗表の該当行を更新する**（`arch-guide/` の文書なら「設計工程の進捗」）
2. **`docs/README.md` の索引に1行追加する**
3. **ルート README のリンク一覧には追加しない**
4. フェーズの状態が変わるときは、**先に `docs/roadmap.md` を更新する**

今回の更新は設計成果物の進捗であり、ソフトウェア実装フェーズは変わらないため、
`docs/roadmap.md`は変更していない。

規約は `.agents/skills/paper-repro-commit-output/SKILL.md` 3.7章に記録した。

// ダッシュボード画面（最小）。
// docs/mvp-design.md 第2章の画面遷移の入口。
// ここから「インテーク → 作業台 → 検証台 → レポート」へ広げていく。
import { useEffect, useState } from "react";
import { createProject, listProjects, type Project } from "@/lib/api";

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listProjects().then(setProjects).catch((e) => setError(String(e)));
  }, []);

  async function handleCreate() {
    setError(null);
    try {
      const p = await createProject(url);
      setProjects((prev) => [...prev, p]);
      setUrl("");
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1>論文 再現実装ツール（MVP）</h1>
      <p>arXiv の URL を入れてプロジェクトを作成します。</p>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://arxiv.org/abs/2505.20139"
          style={{ flex: 1, padding: 8 }}
        />
        <button onClick={handleCreate} disabled={!url}>
          作成
        </button>
      </div>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <h2>プロジェクト一覧</h2>
      <ul>
        {projects.map((p) => (
          <li key={p.project_id}>
            <code>{p.state}</code> — {p.arxiv_url}
          </li>
        ))}
      </ul>
    </main>
  );
}

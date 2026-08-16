// ダッシュボード画面（最小）。
// docs/product-design.md 第2章の画面遷移の入口。
// ここから「インテーク → 作業台 → 検証台 → レポート」へ広げていく。
import { useEffect, useState } from "react";
import { createProject, listProjects, type Project } from "@/lib/api";
import { PaperInput } from "@/components/PaperInput";

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    listProjects().then(setProjects).catch((e) => setError(String(e)));
  }, []);

  async function handleCreate(url: string) {
    setError(null);
    setIsSubmitting(true);
    try {
      const p = await createProject(url);
      setProjects((prev) => [...prev, p]);
    } catch (e) {
      setError(String(e));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-background font-sans text-foreground pb-12">
      <main className="container max-w-4xl py-16 mx-auto space-y-12 px-4 md:px-0">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl text-primary">paper-repro</h1>
          <p className="text-xl text-muted-foreground">論文読解から再現実装までの伴走パイプライン</p>
        </div>

        <PaperInput onSubmit={handleCreate} isLoading={isSubmitting} />

        {error && (
          <div className="p-4 rounded-md bg-destructive/15 text-destructive text-sm font-medium text-center">
            {error}
          </div>
        )}

        <div className="space-y-6 pt-8">
          <h2 className="text-2xl font-semibold tracking-tight border-b pb-2">プロジェクト一覧</h2>
          {projects.length === 0 ? (
            <div className="p-12 text-center border rounded-lg bg-muted/20 text-muted-foreground border-dashed">
              プロジェクトはまだありません
            </div>
          ) : (
            <ul className="grid gap-3">
              {projects.map((p) => (
                <li key={p.project_id} className="p-4 border rounded-lg bg-card flex flex-col sm:flex-row sm:items-center justify-between shadow-sm gap-4 transition-colors hover:bg-muted/30">
                  <div className="font-mono text-sm text-muted-foreground truncate flex-1">
                    <a href={p.arxiv_url} target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-primary transition-colors">
                      {p.arxiv_url}
                    </a>
                  </div>
                  <div className="px-3 py-1 text-xs font-semibold rounded-full bg-secondary text-secondary-foreground w-fit">
                    {p.state}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}

import { useEffect, useState } from "react";
import { createProject, listProjects, type Project } from "@/lib/api";
import { PaperInput } from "@/components/PaperInput";
import { LocaleSwitcher } from "@/components/LocaleSwitcher";
import { useTranslations } from "next-intl";

export async function getStaticProps({ locale }: { locale: string }) {
  return {
    props: {
      messages: (await import(`../../messages/${locale}.json`)).default
    }
  };
}

export default function Dashboard() {
  const t = useTranslations("dashboard");
  const tApi = useTranslations("paper_input");
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // 初期読み込み時のエラーハンドリング
    listProjects().then(setProjects).catch((e) => {
      const errStr = String(e);
      if (errStr.includes("Failed to fetch") || errStr.includes("NetworkError")) {
        setError(tApi("error_network"));
      } else {
        setError(errStr);
      }
    });
  }, [tApi]);

  async function handleCreate(url: string) {
    setError(null);
    setIsSubmitting(true);
    try {
      // ----------------------------------------------------
      // モック処理: バックエンド未実装/未起動時のためのダミーロジック
      // ----------------------------------------------------
      await new Promise(resolve => setTimeout(resolve, 2000));
      const mockProject: Project = {
        project_id: `mock-${Date.now()}`,
        arxiv_url: url,
        state: "intake_review"
      };
      setProjects((prev) => [mockProject, ...prev]); // 新しいものを先頭に追加
      
      // 実際の実装（バックエンド稼働時）は以下を利用します:
      // const p = await createProject(url);
      // setProjects((prev) => [p, ...prev]);
    } catch (e) {
      const errStr = String(e);
      if (errStr.includes("Failed to fetch") || errStr.includes("NetworkError")) {
        setError(tApi("error_network"));
      } else {
        setError(errStr);
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-background font-sans text-foreground pb-12">
      <header className="container max-w-4xl mx-auto py-4 px-4 md:px-0 flex justify-end">
        <LocaleSwitcher />
      </header>
      <main className="container max-w-4xl py-8 mx-auto space-y-12 px-4 md:px-0">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl text-primary">{t("title")}</h1>
          <p className="text-xl text-muted-foreground">{t("subtitle")}</p>
        </div>

        <PaperInput onSubmit={handleCreate} isLoading={isSubmitting} />

        {error && (
          <div className="p-4 rounded-md bg-destructive/15 text-destructive text-sm font-medium text-center">
            {error}
          </div>
        )}

        <div className="space-y-6 pt-8">
          <h2 className="text-2xl font-semibold tracking-tight border-b pb-2">{t("project_list_title")}</h2>
          {projects.length === 0 ? (
            <div className="p-12 text-center border rounded-lg bg-muted/20 text-muted-foreground border-dashed">
              {t("project_list_empty")}
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

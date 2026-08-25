// バックエンド API クライアント。
// docs/product-design.md の第3章のエンドポイントに対応させていく。
// 型は backend/app/core/states.py の Course / Phase / Status と一致させる。

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1";

export type Course = "reading" | "reproduction";

export type Phase =
  | "created"
  | "intake_review"
  | "reading"
  | "implementing"
  | "scoring"
  | "done"
  | "skipped";

export type Status = "idle" | "running" | "waiting_approval" | "failed";

export interface Project {
  project_id: string;
  arxiv_url: string;
  course: Course;
  phase: Phase;
  status: Status;
}

export async function listProjects(): Promise<Project[]> {
  const res = await fetch(`${API_BASE}/projects`);
  if (!res.ok) throw new Error("failed to list projects");
  return res.json();
}

export async function createProject(arxivUrl: string, course: Course): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ arxiv_url: arxivUrl, course }),
  });
  if (!res.ok) throw new Error("failed to create project");
  return res.json();
}

// TODO(Claude Code): setPolicy / getSpec / updateAssumptions / runSanity / compareScores /
//   downloadZip、そして WebSocket 進捗購読（/ws/jobs/{jobId}）を追加する。

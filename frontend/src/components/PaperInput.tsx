import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, Loader2, Link as LinkIcon } from "lucide-react";

interface PaperInputProps {
  onSubmit: (url: string) => void;
  isLoading?: boolean;
}

export function PaperInput({ onSubmit, isLoading }: PaperInputProps) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    
    // 一般的なURLのバリデーション（arXiv以外も許可）
    const urlRegex = /^https?:\/\/\S+$/;
    if (!urlRegex.test(url)) {
      setError("有効なURLを入力してください（例: https://arxiv.org/abs/2505.20139）");
      return;
    }
    
    setError(null);
    onSubmit(url);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-sm transition-all hover:shadow-md border-muted/60">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold">新規プロジェクト</CardTitle>
        <CardDescription>
          再現実装を行いたいAI論文のURL（arXivやオープンアクセスリンク等）を入力してください。
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <div className="flex flex-col space-y-2">
            <div className="relative">
              <LinkIcon className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                type="url"
                placeholder="https://arxiv.org/abs/... または その他のURL"
                value={url}
                onChange={(e) => {
                  setUrl(e.target.value);
                  if (error) setError(null);
                }}
                disabled={isLoading}
                className={`pl-9 py-6 text-base ${error ? "border-destructive focus-visible:ring-destructive" : ""}`}
              />
            </div>
            {error && <p className="text-sm text-destructive font-medium px-1">{error}</p>}
          </div>
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button type="submit" disabled={!url || isLoading} size="lg" className="w-full sm:w-auto font-semibold">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                処理中...
              </>
            ) : (
              <>
                取り込み開始
                <ArrowRight className="ml-2 h-4 w-4" />
              </>
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}

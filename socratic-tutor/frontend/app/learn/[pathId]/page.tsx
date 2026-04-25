"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { api, LearningPathResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Circle, PlayCircle, FileText, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function PathPage() {
  const router = useRouter();
  const params = useParams();
  const pathId = params.pathId as string;
  const [path, setPath] = useState<LearningPathResponse | null>(null);
  const [progress, setProgress] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }

    Promise.all([
      api.learningPaths.get(pathId, token),
      api.progress.getAll(token),
    ])
      .then(([p, prog]) => {
        setPath(p);
        const map: Record<string, boolean> = {};
        prog.forEach((r) => { map[r.lesson_id] = r.completed; });
        setProgress(map);
      })
      .catch(() => router.push("/learn"))
      .finally(() => setLoading(false));
  }, [pathId, router]);

  if (loading || !path) {
    return <div className="flex items-center justify-center h-full text-muted-foreground">Loading...</div>;
  }

  const totalLessons = path.modules.reduce((s, m) => s + m.lessons.length, 0);
  const completedCount = path.modules.reduce(
    (s, m) => s + m.lessons.filter((l) => progress[l.id]).length,
    0
  );

  return (
    <ScrollArea className="h-full"><div className="p-8 max-w-3xl mx-auto">
      <div className="mb-6">
        <Button variant="ghost" size="sm" className="mb-3 -ml-2 gap-1.5 text-muted-foreground hover:text-foreground" asChild>
          <Link href="/learn">
            <ArrowLeft className="h-3.5 w-3.5" />
            All Courses
          </Link>
        </Button>
        <Badge variant="secondary">{path.level}</Badge>
        <h1 className="text-3xl font-bold mt-2 mb-2">{path.title}</h1>
        <p className="text-muted-foreground mb-4">{path.description}</p>
        <div className="text-sm text-muted-foreground">
          {completedCount} / {totalLessons} lessons completed
        </div>
        <div className="mt-2 h-2 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary rounded-full transition-all"
            style={{ width: `${totalLessons ? (completedCount / totalLessons) * 100 : 0}%` }}
          />
        </div>
      </div>

      <div className="space-y-6">
        {path.modules.map((mod, i) => (
          <div key={mod.id}>
            <h2 className="text-lg font-semibold mb-3 text-muted-foreground uppercase text-xs tracking-wider">
              Module {i + 1}: {mod.title}
            </h2>
            <div className="space-y-2">
              {mod.lessons.map((lesson) => {
                const done = progress[lesson.id];
                return (
                  <Link key={lesson.id} href={`/learn/${pathId}/${lesson.id}`}>
                    <Card className="hover:border-primary/50 transition-colors cursor-pointer group">
                      <CardContent className="flex items-center gap-4 py-3">
                        {done ? (
                          <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
                        ) : (
                          <Circle className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                        )}
                        <div className="flex-1 min-w-0">
                          <p className="font-medium group-hover:text-primary transition-colors">
                            {lesson.title}
                          </p>
                          <p className="text-xs text-muted-foreground mt-0.5 truncate">
                            {lesson.concepts.slice(0, 3).join(" · ")}
                          </p>
                        </div>
                        <div className="flex items-center gap-2 flex-shrink-0">
                          {lesson.youtube_id && (
                            <PlayCircle className="h-4 w-4 text-muted-foreground" />
                          )}
                          <FileText className="h-4 w-4 text-muted-foreground" />
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div></ScrollArea>
  );
}

"use client";
import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  CheckCircle2,
  AlertTriangle,
  Rocket,
  Loader2,
  FileText,
  BarChart3,
  RefreshCw,
} from "lucide-react";
import Link from "next/link";
import type { useCreatorState } from "@/lib/useCreatorState";

interface QualityViewProps {
  state: ReturnType<typeof useCreatorState>;
}

interface LessonQuality {
  title: string;
  slug: string;
  passes: boolean;
  word_count: number;
  content_ok: boolean;
  content_target: boolean;
  has_concepts: boolean;
  concept_count: number;
  has_summary: boolean;
}

interface QualityData {
  lessons: LessonQuality[];
  all_pass: boolean;
  total: number;
}

export function QualityView({ state }: QualityViewProps) {
  const { phase, quality, outline, publishedSlug } = state;
  const [publishing, setPublishing] = useState(false);
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    if (phase === "reviewing" || phase === "published") {
      runCheck();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase]);

  async function runCheck() {
    setChecking(true);
    try {
      await state.loadQuality();
    } finally {
      setChecking(false);
    }
  }

  if (phase === "shaping" || phase === "building") {
    return (
      <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
        Quality metrics will appear after content is generated.
      </div>
    );
  }

  async function handlePublish() {
    setPublishing(true);
    try {
      await state.publish();
    } catch {
      // Error handled in state
    } finally {
      setPublishing(false);
    }
  }

  const qd = quality as QualityData | null;
  const lessonCount = outline?.modules.reduce((acc, m) => acc + m.lessons.length, 0) || 0;
  const passCount = qd?.lessons.filter((l) => l.passes).length ?? 0;
  const failCount = qd ? qd.total - passCount : 0;

  return (
    <div className="flex flex-col flex-1 min-h-0">
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-6 space-y-5 max-w-2xl mx-auto">

          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="space-y-0.5">
              <h2 className="text-lg font-semibold">Course Quality</h2>
              <p className="text-sm text-muted-foreground">
                Review before publishing.
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="gap-1.5 text-xs h-7"
              onClick={runCheck}
              disabled={checking}
            >
              {checking
                ? <Loader2 className="h-3 w-3 animate-spin" />
                : <RefreshCw className="h-3 w-3" />}
              {checking ? "Checking..." : "Refresh"}
            </Button>
          </div>

          {/* Summary strip */}
          <div className="grid grid-cols-2 gap-3">
            <MetricCard icon={FileText} label="Lessons" value={String(lessonCount)} />
            <MetricCard icon={BarChart3} label="Modules" value={String(outline?.modules.length || 0)} />
            {qd && (
              <>
                <MetricCard
                  icon={CheckCircle2}
                  label="Passing"
                  value={`${passCount} / ${qd.total}`}
                  highlight={qd.all_pass ? "green" : undefined}
                />
                <MetricCard
                  icon={AlertTriangle}
                  label="Issues"
                  value={String(failCount)}
                  highlight={failCount > 0 ? "amber" : undefined}
                />
              </>
            )}
          </div>

          {/* Per-lesson results */}
          {checking && !qd && (
            <Card className="p-4">
              <div className="flex items-center gap-3 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                Running quality checks...
              </div>
            </Card>
          )}

          {qd && qd.lessons.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider text-[10px]">
                Per-lesson results
              </h3>
              {qd.lessons.map((lesson) => (
                <Card key={lesson.slug} className={`px-4 py-3 ${!lesson.passes ? "border-amber-200 bg-amber-50/50" : ""}`}>
                  <div className="flex items-start gap-2.5">
                    {lesson.passes
                      ? <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 shrink-0" />
                      : <AlertTriangle className="h-4 w-4 text-amber-500 mt-0.5 shrink-0" />}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{lesson.title}</p>
                      <div className="flex flex-wrap gap-x-3 gap-y-0.5 mt-1">
                        <span className={`text-xs ${lesson.content_ok ? "text-muted-foreground" : "text-amber-600 font-medium"}`}>
                          {lesson.word_count} words {!lesson.content_ok && "(too short)"}
                          {lesson.content_ok && !lesson.content_target && lesson.word_count > 1200 && "(long)"}
                        </span>
                        <span className={`text-xs ${lesson.has_concepts ? "text-muted-foreground" : "text-amber-600 font-medium"}`}>
                          {lesson.concept_count} concepts {!lesson.has_concepts && "(missing)"}
                        </span>
                        <span className={`text-xs ${lesson.has_summary ? "text-muted-foreground" : "text-amber-600 font-medium"}`}>
                          {lesson.has_summary ? "summary ✓" : "no summary"}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}

          {qd && qd.lessons.length === 0 && (
            <div className="text-center text-sm text-muted-foreground py-8">
              No lesson content found. Generate content first.
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Publish footer */}
      <div className="p-4 border-t border-border shrink-0">
        {phase === "published" ? (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-green-600 text-sm">
              <CheckCircle2 className="h-4 w-4" />
              Course published successfully!
            </div>
            {publishedSlug && (
              <Button asChild className="w-full gap-2">
                <Link href={`/learn/${publishedSlug}`}>
                  <Rocket className="h-4 w-4" />
                  Start Learning
                </Link>
              </Button>
            )}
          </div>
        ) : (
          <Button
            onClick={handlePublish}
            disabled={publishing || checking}
            className="w-full gap-2"
          >
            {publishing ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Publishing...
              </>
            ) : (
              <>
                <Rocket className="h-4 w-4" />
                Publish Course
              </>
            )}
          </Button>
        )}
      </div>
    </div>
  );
}

function MetricCard({
  icon: Icon,
  label,
  value,
  highlight,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  highlight?: "green" | "amber";
}) {
  return (
    <Card className="flex items-center gap-3 px-4 py-3">
      <Icon className={`h-4 w-4 shrink-0 ${
        highlight === "green" ? "text-green-500"
        : highlight === "amber" ? "text-amber-500"
        : "text-muted-foreground"
      }`} />
      <div>
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className={`text-sm font-medium ${
          highlight === "green" ? "text-green-600"
          : highlight === "amber" ? "text-amber-600"
          : ""
        }`}>{value}</p>
      </div>
    </Card>
  );
}

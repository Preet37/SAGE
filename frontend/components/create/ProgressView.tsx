"use client";
import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Loader2,
  CheckCircle2,
  AlertCircle,
  Clock,
  FileText,
  Link2,
  Hash,
  ExternalLink,
  RotateCcw,
  Square,
  BookOpen,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { LessonProgress, LessonGenStatus } from "@/lib/useCreatorState";

interface ProgressViewProps {
  state: ReturnType<typeof useCreatorState>;
}

export function ProgressView({ state }: ProgressViewProps) {
  const { lessonProgress, generating, phase } = state;

  if (lessonProgress.length === 0 && phase === "shaping") {
    return (
      <EmptyState message="Use 'Build All' or 'Build Select' from the Outline, Research, or Enrich tab to generate content." />
    );
  }

  if (lessonProgress.length === 0) {
    return <EmptyState message="No build progress yet." />;
  }

  const done = lessonProgress.filter((l) => l.status === "done").length;
  const total = lessonProgress.length;
  const errors = lessonProgress.filter((l) => l.status === "error").length;
  const queued = lessonProgress.filter((l) => l.status === "queued").length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const needsResume = !generating && (queued > 0 || errors > 0) && done > 0;

  const modules = groupByModule(lessonProgress);

  return (
    <div className="flex flex-col flex-1 min-h-0">
      {/* Progress header */}
      <div className="p-6 pb-4 space-y-3 shrink-0 border-b border-border">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Build</h2>
          <div className="flex items-center gap-2">
            {generating && (
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5 text-xs h-7 text-destructive hover:text-destructive"
                onClick={state.cancelGeneration}
              >
                <Square className="h-3 w-3 fill-current" />
                Stop
              </Button>
            )}
            <span className="text-sm text-muted-foreground">
              {done}/{total} lessons
            </span>
          </div>
        </div>
        <Progress value={pct} className="h-2" />

        {needsResume && (
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">
              {queued > 0 && `${queued} lesson${queued !== 1 ? "s" : ""} pending`}
              {queued > 0 && errors > 0 && " · "}
              {errors > 0 && (
                <span className="text-destructive">
                  {errors} failed
                </span>
              )}
            </span>
            <Button
              variant="default"
              size="sm"
              className="gap-1.5 text-xs h-7"
              onClick={() => state.generateContent(true)}
              disabled={generating}
            >
              <RotateCcw className="h-3 w-3" />
              Continue Building ({queued + errors})
            </Button>
          </div>
        )}
      </div>

      {/* Lesson cards grouped by module */}
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-6 space-y-5">
          {modules.map(({ module, lessons }) => (
            <div key={module} className="space-y-2">
              {modules.length > 1 && (
                <div className="flex items-center gap-2 text-xs text-muted-foreground font-medium uppercase tracking-wide">
                  <BookOpen className="h-3 w-3" />
                  {module}
                </div>
              )}
              <div className="space-y-1.5">
                {lessons.map((lesson) => (
                  <LessonProgressCard key={lesson.slug} lesson={lesson} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}

function groupByModule(progress: LessonProgress[]) {
  const groups: { module: string; lessons: LessonProgress[] }[] = [];
  const map = new Map<string, LessonProgress[]>();
  for (const l of progress) {
    const mod = l.module || "Lessons";
    if (!map.has(mod)) {
      const arr: LessonProgress[] = [];
      map.set(mod, arr);
      groups.push({ module: mod, lessons: arr });
    }
    map.get(mod)!.push(l);
  }
  return groups;
}

function LessonProgressCard({ lesson }: { lesson: LessonProgress }) {
  const [expanded, setExpanded] = useState(false);
  const isActive = lesson.status === "generating";
  const isDone = lesson.status === "done";
  const isError = lesson.status === "error";
  const isQueued = lesson.status === "queued";
  const hasSources = isDone && lesson.sourceUrls && lesson.sourceUrls.length > 0;
  const canExpand = hasSources;

  const statusConfig: Record<
    LessonGenStatus,
    { icon: React.ComponentType<React.SVGProps<SVGSVGElement>>; color: string; label: string; badgeClass: string }
  > = {
    queued: { icon: Clock, color: "text-muted-foreground", label: "Queued", badgeClass: "" },
    generating: { icon: Loader2, color: "text-primary", label: "Generating...", badgeClass: "bg-primary/10 text-primary" },
    done: { icon: CheckCircle2, color: "text-green-500", label: "Done", badgeClass: "bg-green-500/15 text-green-500" },
    error: { icon: AlertCircle, color: "text-destructive", label: "Error", badgeClass: "bg-destructive/15 text-destructive" },
  };

  const config = statusConfig[lesson.status];
  const StatusIcon = config.icon;

  const cardClass = isActive
    ? "border-primary/40 bg-primary/[0.03]"
    : isError
      ? "border-destructive/30 bg-destructive/[0.02]"
      : isQueued
        ? "opacity-50"
        : "";

  return (
    <Card className={`overflow-hidden ${cardClass}`}>
      {isActive && (
        <div className="h-0.5 bg-primary/30 overflow-hidden">
          <div className="h-full w-1/3 bg-primary rounded-full animate-[shimmer_1.5s_ease-in-out_infinite]" />
        </div>
      )}

      {/* Header row — same pattern as enrichment cards */}
      <button
        onClick={canExpand ? () => setExpanded(!expanded) : undefined}
        className={`flex items-center gap-3 w-full px-4 py-3 text-left transition-colors ${
          canExpand ? "hover:bg-accent/20 cursor-pointer" : ""
        }`}
      >
        {canExpand ? (
          expanded
            ? <ChevronDown className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            : <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        ) : null}
        <StatusIcon className={`h-4 w-4 shrink-0 ${config.color} ${isActive ? "animate-spin" : ""}`} />
        <span className="text-sm font-medium flex-1 truncate">{lesson.title}</span>

        {/* Stats for done lessons */}
        {isDone && (
          <div className="flex items-center gap-2 shrink-0">
            {lesson.words != null && (
              <span className="flex items-center gap-1 text-xs text-muted-foreground">
                <FileText className="h-3 w-3" />
                {lesson.words.toLocaleString()}w
              </span>
            )}
            {lesson.concepts && lesson.concepts.length > 0 && (
              <span className="flex items-center gap-1 text-xs text-muted-foreground">
                <Hash className="h-3 w-3" />
                {lesson.concepts.length}
              </span>
            )}
            {hasSources && (
              <span className="flex items-center gap-1 text-xs text-muted-foreground">
                <Link2 className="h-3 w-3" />
                {lesson.sourceUrls!.length}
              </span>
            )}
            {lesson.hasKb && (
              <Badge variant="secondary" className="text-[10px] bg-primary/10 text-primary px-1.5 py-0">
                KB
              </Badge>
            )}
          </div>
        )}

        <Badge variant="secondary" className={`text-[10px] shrink-0 ${config.badgeClass}`}>
          {config.label}
        </Badge>
      </button>

      {/* Concepts row for generating lessons */}
      {isActive && lesson.concepts && lesson.concepts.length > 0 && (
        <div className="px-4 pb-3 flex flex-wrap gap-1 pl-12">
          {lesson.concepts.slice(0, 6).map((c) => (
            <span key={c} className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
              {c}
            </span>
          ))}
          {lesson.concepts.length > 6 && (
            <span className="text-[10px] text-muted-foreground">+{lesson.concepts.length - 6}</span>
          )}
        </div>
      )}

      {/* Error message */}
      {isError && lesson.error && (
        <div className="px-4 pb-3">
          <p className="text-xs text-destructive pl-7 truncate">{lesson.error}</p>
        </div>
      )}

      {/* Dropdown: sources list */}
      {expanded && hasSources && (
        <div className="px-4 pb-4 pt-1 border-t border-border/50 space-y-1.5">
          <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider pt-2">
            Sources ({lesson.sourceUrls!.length})
          </p>
          {lesson.sourceUrls!.map((url, i) => {
            let label = url;
            try {
              const p = new URL(url);
              label = `${p.hostname}${p.pathname}`.replace(/\/$/, "");
            } catch { /* use raw */ }
            return (
              <a
                key={i}
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-xs text-muted-foreground hover:text-primary transition-colors group"
              >
                <ExternalLink className="h-3 w-3 shrink-0 opacity-50 group-hover:opacity-100" />
                <span className="truncate">{label}</span>
              </a>
            );
          })}
        </div>
      )}
    </Card>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex items-center justify-center h-full text-sm text-muted-foreground px-8 text-center">
      {message}
    </div>
  );
}

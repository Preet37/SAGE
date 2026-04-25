"use client";
import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  CheckCircle2,
  AlertTriangle,
  Rocket,
  Loader2,
  FileText,
  BookOpen,
  Hash,
  ChevronDown,
  ChevronRight,
  Library,
  Pencil,
  Check,
  X,
  RefreshCw,
} from "lucide-react";
import Link from "next/link";
import type { useCreatorState } from "@/lib/useCreatorState";

interface PublishViewProps {
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

interface DashboardData {
  content: {
    lesson_count: number;
    avg_word_count: number;
    min_word_count: number;
    max_word_count: number;
  };
  knowledge: {
    format: string;
    lesson_count?: number;
    total_words?: number;
    avg_word_count?: number;
    total_sections?: number;
    count?: number;
  };
  qa: {
    approved_count: number;
    rejected_count: number;
    reasoning_types: string[];
    avg_score: number;
    synthesis_count: number;
  };
}

export function PublishView({ state }: PublishViewProps) {
  const { phase, quality, outline, publishedSlug, lessonProgress, dashboard } = state;
  const [publishing, setPublishing] = useState(false);
  const [checking, setChecking] = useState(false);
  const [editingIdentity, setEditingIdentity] = useState(false);
  const [titleDraft, setTitleDraft] = useState("");
  const [descDraft, setDescDraft] = useState("");

  const doneCount = lessonProgress.filter((l) => l.status === "done").length;
  const hasContent = doneCount > 0;

  useEffect(() => {
    if (hasContent) {
      setChecking(true);
      Promise.all([state.loadQuality(), state.loadDashboard()]).finally(() =>
        setChecking(false),
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasContent, phase]);

  if (!hasContent) {
    return (
      <div className="flex items-center justify-center h-full text-sm text-muted-foreground px-8 text-center">
        Course stats and publishing will be available after content is generated.
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
  const dd = dashboard as DashboardData | null;
  const lessonCount = outline?.modules.reduce((acc, m) => acc + m.lessons.length, 0) || 0;
  const moduleCount = outline?.modules.length || 0;
  const passCount = qd?.lessons.filter((l) => l.passes).length ?? 0;
  const failCount = qd ? qd.total - passCount : 0;
  const totalWords = qd?.lessons.reduce((acc, l) => acc + l.word_count, 0) ?? 0;
  const totalConcepts = qd?.lessons.reduce((acc, l) => acc + l.concept_count, 0) ?? 0;
  const withContent = qd?.lessons.filter((l) => l.content_ok).length ?? 0;
  const withConcepts = qd?.lessons.filter((l) => l.has_concepts).length ?? 0;
  const withSummary = qd?.lessons.filter((l) => l.has_summary).length ?? 0;
  const kbCount = dd?.knowledge?.lesson_count ?? 0;

  return (
    <div className="flex flex-col flex-1 min-h-0">
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-6 space-y-5 max-w-2xl mx-auto">

          {/* Header */}
          <div className="space-y-0.5">
            <h2 className="text-lg font-semibold">Publish</h2>
            <p className="text-sm text-muted-foreground">
              Review your course and publish when ready.
            </p>
          </div>

          {/* Course identity — title & description */}
          {outline && (
            <Card className="p-4">
              {editingIdentity ? (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <label className="text-xs font-medium text-muted-foreground">Title</label>
                    <input
                      value={titleDraft}
                      onChange={(e) => setTitleDraft(e.target.value)}
                      className="w-full text-sm font-semibold bg-transparent border border-border rounded-md px-2.5 py-1.5 focus:outline-none focus:border-primary/40"
                      autoFocus
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-medium text-muted-foreground">Description</label>
                    <textarea
                      value={descDraft}
                      onChange={(e) => setDescDraft(e.target.value)}
                      rows={3}
                      className="w-full text-sm bg-transparent border border-border rounded-md px-2.5 py-1.5 focus:outline-none focus:border-primary/40 resize-none"
                    />
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Button
                      variant="secondary"
                      size="sm"
                      className="h-7 px-3 text-xs gap-1"
                      onClick={() => {
                        state.updateOutline({
                          ...outline,
                          title: titleDraft.trim() || outline.title,
                          description: descDraft.trim(),
                        });
                        setEditingIdentity(false);
                      }}
                    >
                      <Check className="h-3 w-3" /> Save
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-7 px-3 text-xs gap-1"
                      onClick={() => setEditingIdentity(false)}
                    >
                      <X className="h-3 w-3" /> Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <div
                  className="group/id cursor-pointer"
                  onClick={() => {
                    setTitleDraft(outline.title);
                    setDescDraft(outline.description || "");
                    setEditingIdentity(true);
                  }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold">{outline.title}</p>
                      {outline.description && (
                        <p className="text-xs text-muted-foreground mt-1 line-clamp-3">
                          {outline.description}
                        </p>
                      )}
                      {!outline.description && (
                        <p className="text-xs text-muted-foreground/50 mt-1 italic">
                          No description — click to add one
                        </p>
                      )}
                    </div>
                    <Pencil className="h-3.5 w-3.5 text-muted-foreground/40 group-hover/id:text-muted-foreground transition-colors shrink-0 ml-3 mt-0.5" />
                  </div>
                </div>
              )}
            </Card>
          )}

          {/* Course stats */}
          {checking && !qd && (
            <Card className="p-4">
              <div className="flex items-center gap-3 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                Checking course quality...
              </div>
            </Card>
          )}

          {qd && (
            <Card className="p-4 space-y-3">
              <div className="grid grid-cols-3 gap-4">
                <StatItem icon={BookOpen} label="Lessons" value={`${doneCount} / ${lessonCount}`} sub={`${moduleCount} module${moduleCount !== 1 ? "s" : ""}`} />
                <StatItem icon={FileText} label="Words" value={totalWords.toLocaleString()} sub={dd ? `avg ${dd.content.avg_word_count}/lesson` : undefined} />
                <StatItem icon={Hash} label="Concepts" value={String(totalConcepts)} sub={dd ? `range ${dd.content.min_word_count}–${dd.content.max_word_count}w` : undefined} />
              </div>
              {dd && kbCount > 0 && (
                <div className="flex items-center gap-2 text-xs text-muted-foreground pt-1 border-t border-border">
                  <Library className="h-3 w-3 mt-2" />
                  <span className="mt-2">{kbCount} lesson{kbCount !== 1 ? "s" : ""} with reference KB ({dd.knowledge.total_words?.toLocaleString()} words, {dd.knowledge.total_sections} sections)</span>
                </div>
              )}
            </Card>
          )}

          {/* Readiness summary */}
          {qd && (
            <Card className="p-4 space-y-2.5">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Readiness</p>
              <div className="space-y-1.5">
                <ReadinessRow pass={withContent === qd.total} label={`${withContent} of ${qd.total} lessons have content`} detail={withContent < qd.total ? `${qd.total - withContent} too short` : undefined} />
                <ReadinessRow pass={withConcepts === qd.total} label={`${withConcepts} of ${qd.total} lessons have concepts`} detail={withConcepts < qd.total ? `${qd.total - withConcepts} missing` : undefined} />
                <ReadinessRow pass={withSummary === qd.total} label={`${withSummary} of ${qd.total} lessons have summaries`} detail={withSummary < qd.total ? `${qd.total - withSummary} missing` : undefined} />
                {kbCount > 0 && (
                  <ReadinessRow pass={kbCount >= qd.total} label={`${kbCount} of ${qd.total} lessons have reference KB`} />
                )}
              </div>
              <div className="flex items-center gap-2 pt-1 border-t border-border">
                {qd.all_pass ? (
                  <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0 mt-1" />
                ) : (
                  <AlertTriangle className="h-4 w-4 text-amber-500 shrink-0 mt-1" />
                )}
                <span className="text-sm font-medium mt-1">
                  {qd.all_pass
                    ? "All structural checks pass"
                    : `${passCount} of ${qd.total} lessons pass — ${failCount} need attention`}
                </span>
              </div>
            </Card>
          )}

          {/* Per-lesson breakdown */}
          {qd && qd.lessons.length > 0 && (
            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Per-Lesson Detail</p>
              {qd.lessons.map((lesson) => (
                <LessonQualityCard key={lesson.slug} lesson={lesson} />
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
      <div className="p-4 border-t border-border shrink-0 space-y-2">
        {phase === "published" && (
          <div className="flex items-center gap-2 text-green-600 text-sm">
            <CheckCircle2 className="h-4 w-4" />
            Course is live
          </div>
        )}

        <div className="flex items-center gap-2">
          {phase === "published" && publishedSlug && (
            <Button asChild variant="outline" className="flex-1 gap-2">
              <Link href={`/learn/${publishedSlug}`}>
                <BookOpen className="h-4 w-4" />
                View Course
              </Link>
            </Button>
          )}
          <Button
            onClick={handlePublish}
            disabled={publishing || checking}
            className={`gap-2 ${phase === "published" && publishedSlug ? "flex-1" : "w-full"}`}
          >
            {publishing ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                {phase === "published" ? "Republishing..." : "Publishing..."}
              </>
            ) : phase === "published" ? (
              <>
                <RefreshCw className="h-4 w-4" />
                Republish
              </>
            ) : (
              <>
                <Rocket className="h-4 w-4" />
                Publish Course
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}

/* ── Stat item ─────────────────────────────────────── */

function StatItem({
  icon: Icon,
  label,
  value,
  sub,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <div className="flex items-start gap-2.5">
      <Icon className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
      <div>
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="text-sm font-semibold">{value}</p>
        {sub && <p className="text-[10px] text-muted-foreground">{sub}</p>}
      </div>
    </div>
  );
}

/* ── Readiness row ─────────────────────────────────── */

function ReadinessRow({
  pass,
  label,
  detail,
}: {
  pass: boolean;
  label: string;
  detail?: string;
}) {
  return (
    <div className="flex items-center gap-2 text-sm">
      {pass ? (
        <CheckCircle2 className="h-3.5 w-3.5 text-green-500 shrink-0" />
      ) : (
        <AlertTriangle className="h-3.5 w-3.5 text-amber-500 shrink-0" />
      )}
      <span className="flex-1">{label}</span>
      {detail && (
        <span className="text-xs text-amber-600 shrink-0">{detail}</span>
      )}
    </div>
  );
}

/* ── Per-lesson quality card ───────────────────────── */

function LessonQualityCard({ lesson }: { lesson: LessonQuality }) {
  const [expanded, setExpanded] = useState(false);

  const issues: string[] = [];
  if (!lesson.content_ok) issues.push(`${lesson.word_count} words (too short)`);
  if (!lesson.has_concepts) issues.push("No concepts");
  if (!lesson.has_summary) issues.push("No summary");

  return (
    <Card className="overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-3 w-full px-4 py-3 text-left hover:bg-accent/20 transition-colors"
      >
        {expanded
          ? <ChevronDown className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
          : <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        }
        {lesson.passes ? (
          <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
        ) : (
          <AlertTriangle className="h-4 w-4 text-amber-500 shrink-0" />
        )}
        <span className="text-sm font-medium flex-1 truncate">{lesson.title}</span>
        <div className="flex items-center gap-2 shrink-0">
          <span className="text-xs text-muted-foreground flex items-center gap-1">
            <FileText className="h-3 w-3" />
            {lesson.word_count.toLocaleString()}w
          </span>
          <span className="text-xs text-muted-foreground flex items-center gap-1">
            <Hash className="h-3 w-3" />
            {lesson.concept_count}
          </span>
          <Badge
            variant="secondary"
            className={`text-[10px] ${
              lesson.passes ? "bg-green-500/15 text-green-500" : "bg-amber-500/15 text-amber-500"
            }`}
          >
            {lesson.passes ? "Pass" : "Needs work"}
          </Badge>
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-1 border-t border-border/50 space-y-2">
          {/* Word count bar */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-[10px] text-muted-foreground">
              <span>Word count</span>
              <span>{lesson.word_count.toLocaleString()} words</span>
            </div>
            <div className="flex h-1.5 rounded-full overflow-hidden bg-muted">
              <div
                className={`rounded-full transition-all ${
                  lesson.content_target ? "bg-green-500" : lesson.content_ok ? "bg-amber-400" : "bg-destructive"
                }`}
                style={{ width: `${Math.min(100, (lesson.word_count / 1200) * 100)}%` }}
              />
            </div>
            <div className="flex justify-between text-[9px] text-muted-foreground/60">
              <span>0</span>
              <span>100 min</span>
              <span>400</span>
              <span>1200 target</span>
            </div>
          </div>

          {/* Checks */}
          <div className="space-y-1 pt-1">
            <CheckRow pass={lesson.content_ok} label={`Content: ${lesson.word_count} words`} />
            <CheckRow pass={lesson.has_concepts} label={`Concepts: ${lesson.concept_count}`} />
            <CheckRow pass={lesson.has_summary} label="Summary present" />
          </div>

          {/* Issues */}
          {issues.length > 0 && (
            <div className="flex flex-wrap gap-1.5 pt-1">
              {issues.map((issue) => (
                <Badge key={issue} variant="outline" className="text-[10px] text-amber-600 border-amber-300">
                  {issue}
                </Badge>
              ))}
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

function CheckRow({ pass, label }: { pass: boolean; label: string }) {
  return (
    <div className="flex items-center gap-2 text-xs">
      {pass ? (
        <CheckCircle2 className="h-3 w-3 text-green-500 shrink-0" />
      ) : (
        <AlertTriangle className="h-3 w-3 text-amber-500 shrink-0" />
      )}
      <span className={pass ? "text-muted-foreground" : "text-amber-600"}>{label}</span>
    </div>
  );
}

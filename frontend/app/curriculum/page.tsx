"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import {
  api,
  CurriculumResponse,
  CurriculumPhaseResponse,
  AssessmentResponse,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  Loader2,
  Sparkles,
  RotateCcw,
  ChevronDown,
  CheckCircle2,
  Circle,
  Award,
  BookOpen,
  Clock,
  Layers,
  ArrowRight,
  ClipboardCheck,
  Info,
  Search,
  Lightbulb,
} from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

const LEVEL_CONFIG: Record<string, { label: string; color: string }> = {
  beginner: { label: "Beginner", color: "bg-green-500/20 text-green-400 border-green-500/30" },
  intermediate: { label: "Intermediate", color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30" },
  advanced: { label: "Advanced", color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
  expert: { label: "Expert", color: "bg-purple-500/20 text-purple-400 border-purple-500/30" },
};

function LevelBadge({ level }: { level: string }) {
  const config = LEVEL_CONFIG[level] ?? LEVEL_CONFIG.intermediate;
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", config.color)}>
      {config.label}
    </span>
  );
}

function PhaseCard({
  phase,
  expanded,
  onToggle,
  onLessonClick,
}: {
  phase: CurriculumPhaseResponse;
  expanded: boolean;
  onToggle: () => void;
  onLessonClick: (lessonId: string, pathSlug: string) => void;
}) {
  return (
    <div className="relative">
      {/* Timeline connector */}
      <div className="absolute left-5 top-0 bottom-0 w-px bg-border" />

      {/* Phase number circle */}
      <div className="flex items-start gap-4">
        <div className="relative z-10 flex items-center justify-center w-10 h-10 rounded-full bg-primary/20 border-2 border-primary text-primary text-sm font-bold flex-shrink-0">
          {phase.order}
        </div>

        <div className="flex-1 min-w-0 pb-6">
          <button
            onClick={onToggle}
            className="w-full text-left rounded-xl border border-border bg-card p-4 hover:border-primary/30 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <h3 className="font-semibold text-foreground">{phase.title}</h3>
                <div className="flex items-center gap-2">
                  <LevelBadge level={phase.level} />
                  <span className="text-xs text-muted-foreground flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {phase.estimated_hours}h
                  </span>
                </div>
              </div>
              <ChevronDown className={cn(
                "h-5 w-5 text-muted-foreground transition-transform",
                expanded && "rotate-180"
              )} />
            </div>
            <p className="text-sm text-muted-foreground mt-2">{phase.description}</p>
          </button>

          {expanded && (
            <div className="mt-3 space-y-1.5 pl-1">
              {phase.lessons.map((lesson) => (
                <button
                  key={lesson.id}
                  onClick={() => onLessonClick(lesson.id, lesson.path_slug)}
                  className="w-full flex items-start gap-2 px-3 py-2 rounded-lg text-left hover:bg-accent transition-colors group"
                >
                  {lesson.completed ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  ) : (
                    <Circle className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0 group-hover:text-primary" />
                  )}
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{lesson.title}</p>
                    <p className="text-xs text-muted-foreground truncate">{lesson.course_title}</p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Milestone */}
      {phase.milestone_title && (
        <div className="flex items-start gap-4 mt-1 mb-4">
          <div className="relative z-10 flex items-center justify-center w-10 h-10 rounded-full bg-amber-500/20 border-2 border-amber-500 flex-shrink-0">
            <Award className="h-5 w-5 text-amber-500" />
          </div>
          <div className="flex-1 rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
            <p className="text-xs font-bold text-amber-500 uppercase tracking-wider">Milestone</p>
            <p className="font-semibold text-foreground text-sm mt-0.5">{phase.milestone_title}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {phase.milestone_skills.join(", ")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default function CurriculumPage() {
  const router = useRouter();
  const [learningGoals, setLearningGoals] = useState("");
  const [curriculum, setCurriculum] = useState<CurriculumResponse | null>(null);
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingLatest, setLoadingLatest] = useState(true);
  const [hasExisting, setHasExisting] = useState(false);
  const [view, setView] = useState<"input" | "result">("input");
  const [expandedPhases, setExpandedPhases] = useState<Set<number>>(new Set());

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    async function load() {
      try {
        const [latestCurriculum, latestAssessment] = await Promise.allSettled([
          api.curriculum.getLatest(token!),
          api.assessment.getLatest(token!),
        ]);
        if (latestCurriculum.status === "fulfilled") {
          setCurriculum(latestCurriculum.value);
          setHasExisting(true);
          setView("result");
          setExpandedPhases(new Set([1]));
        }
        if (latestAssessment.status === "fulfilled") {
          setAssessment(latestAssessment.value);
        }
      } catch { /* ignore */ }
      finally { setLoadingLatest(false); }
    }
    load();
  }, [router]);

  async function handleGenerate() {
    if (!learningGoals.trim() || loading) return;
    const token = getToken();
    if (!token) return;

    setLoading(true);
    try {
      const result = await api.curriculum.generate(learningGoals.trim(), token);
      setCurriculum(result);
      setHasExisting(true);
      setView("result");
      setExpandedPhases(new Set([1]));
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Curriculum generation failed";
      alert(msg);
    } finally {
      setLoading(false);
    }
  }

  function handleRegenerate() {
    setView("input");
    setLearningGoals("");
  }

  function togglePhase(order: number) {
    setExpandedPhases((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  }

  function handleLessonClick(lessonId: string, pathSlug: string) {
    router.push(`/learn/${pathSlug}/${lessonId}`);
  }

  if (loadingLatest) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <AppHeader
        leftSlot={
          <>
            <Layers className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm">Curriculum</span>
          </>
        }
      />

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {view === "input" ? (
          /* ─── Input Form ─── */
          <div className="max-w-2xl mx-auto px-4 py-12">
            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Layers className="h-6 w-6 text-primary" />
                  <h1 className="text-2xl font-bold text-foreground">Curriculum Generator</h1>
                </div>
                <p className="text-muted-foreground">
                  Describe your learning goals and we will create a personalized curriculum tailored to your level.
                </p>
              </div>

              <textarea
                value={learningGoals}
                onChange={(e) => setLearningGoals(e.target.value)}
                placeholder="I want to master building agentic AI systems, from single-agent tools to multi-agent orchestration"
                rows={4}
                className="w-full rounded-lg border border-border bg-card px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 resize-y"
              />

              {/* Assessment indicator */}
              {assessment ? (
                <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-green-500/20 bg-green-500/5">
                  <CheckCircle2 className="h-4 w-4 text-green-500 flex-shrink-0" />
                  <span className="text-xs text-muted-foreground">
                    Skill assessment loaded — your curriculum will be personalized based on your{" "}
                    <span className="font-medium text-foreground capitalize">{assessment.overall_level}</span> profile
                  </span>
                </div>
              ) : (
                <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border bg-card">
                  <Info className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <span className="text-xs text-muted-foreground">
                    No skill assessment found. Describe your background below for a more personalized curriculum.
                  </span>
                </div>
              )}

              <Button
                onClick={handleGenerate}
                disabled={!learningGoals.trim() || loading}
                className="w-full gap-2"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Generating your curriculum...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Generate Curriculum
                  </>
                )}
              </Button>

              {hasExisting && (
                <button
                  onClick={() => setView("result")}
                  className="w-full text-center text-sm text-primary hover:underline"
                >
                  View latest curriculum
                </button>
              )}
            </div>
          </div>
        ) : curriculum ? (
          /* ─── Results View ─── */
          <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
            {/* Title card */}
            <div className="rounded-xl border border-primary/30 bg-card p-6 space-y-3">
              <h2 className="text-xl font-bold text-foreground">{curriculum.title}</h2>
              <div className="flex flex-wrap items-center gap-2">
                <span className={cn(
                  "text-xs px-2.5 py-0.5 rounded-full font-medium border",
                  "bg-primary/20 text-primary border-primary/30"
                )}>
                  {curriculum.level_range}
                </span>
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {curriculum.estimated_hours} hours total
                </span>
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <Layers className="h-3 w-3" />
                  {curriculum.phases.length} phases
                </span>
              </div>
            </div>

            {/* Personalization note */}
            {curriculum.personalization_note && (
              <div className="flex gap-3 px-4 py-3 rounded-xl border border-primary/20 bg-primary/5">
                <Info className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                <p className="text-sm text-muted-foreground">{curriculum.personalization_note}</p>
              </div>
            )}

            {/* Learning Path timeline */}
            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider flex items-center gap-2 mb-4">
                <BookOpen className="h-4 w-4" />
                Learning Path
              </p>
              <div className="space-y-2">
                {curriculum.phases.map((phase) => (
                  <PhaseCard
                    key={phase.order}
                    phase={phase}
                    expanded={expandedPhases.has(phase.order)}
                    onToggle={() => togglePhase(phase.order)}
                    onLessonClick={handleLessonClick}
                  />
                ))}
              </div>
            </div>

            {/* Gap Notes */}
            {curriculum.gaps.length > 0 && (
              <div className="rounded-xl border border-border bg-card p-6 space-y-4">
                <p className="text-xs font-medium text-orange-400 uppercase tracking-wider flex items-center gap-2">
                  <Search className="h-4 w-4" />
                  Topics Not Covered by Existing Content
                </p>
                <div className="space-y-3">
                  {curriculum.gaps.map((gap) => (
                    <div key={gap.topic} className="flex items-start justify-between gap-3 p-3 rounded-lg bg-muted/30">
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-foreground">{gap.topic}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">{gap.description}</p>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => router.push(`/concepts?topic=${encodeURIComponent(gap.explore_query)}`)}
                        className="flex-shrink-0 gap-1"
                      >
                        <Lightbulb className="h-3 w-3" />
                        Explore
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Regenerate */}
            <div className="flex justify-center pt-2">
              <Button variant="outline" onClick={handleRegenerate} className="gap-2">
                <RotateCcw className="h-4 w-4" />
                Generate New Curriculum
              </Button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
